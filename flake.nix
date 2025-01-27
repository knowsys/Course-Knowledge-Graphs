{
  description = "Solutions and examples for the Knowledge Graphs course";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";

    utils.url = "github:gytis-ivaskevicius/flake-utils-plus";

    nemo = {
      url = "github:knowsys/nemo/refs/tags/v0.7.1";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        utils.follows = "utils";
      };
    };

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      utils,
      nemo,
      uv2nix,
      pyproject-nix,
      pyproject-build-systems,
      ...
    }@inputs:
    let
      inherit (utils.lib) mkFlake;
      inherit (inputs.nixpkgs) lib;

      workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };
      hacks = pkgs: pkgs.callPackage pyproject-nix.build.hacks { };
      overlay = workspace.mkPyprojectOverlay {
        sourcePreference = "wheel";
      };

      nemoOverlay = pkgs: final: prev: {
        nemo-python = (hacks final).nixpkgsPrebuilt {
          from = nemo.packages."${pkgs.system}".nemo-python;
          prev = prev.requests; # ugly hack, but we require requests anyway
        };
      };

      pyprojectOverrides = final: prev: {
        networkit = prev.networkit.overrideAttrs (old: {
          nativeBuildInputs = old.nativeBuildInputs ++ [
            (final.resolveBuildSystem {
              cmake = [ ];
              cython = [ ];
              scikit-build-core = [ ];
              setuptools = [ ];
              numpy = [ ];
            })
          ];
        });
      };

      python = pkgs: pkgs.python312;

      pythonSet =
        pkgs:
        (pkgs.callPackage pyproject-nix.build.packages {
          python = python pkgs;
        }).overrideScope
          (
            lib.composeManyExtensions [
              pyproject-build-systems.overlays.default
              overlay
              (nemoOverlay pkgs)
              pyprojectOverrides
            ]
          );

      virtualenv =
        pkgs:
        (pythonSet pkgs).mkVirtualEnv "knowledge-graphs-venv" (
          workspace.deps.all // { nemo-python = [ ]; }
        );
    in
    mkFlake {
      inherit self inputs;

      channels.nixpkgs.overlaysBuilder = channels: [
        nemo.overlays.default
      ];

      outputsBuilder = channels: {
        devShells.default =
          let
            pkgs = channels.nixpkgs;
          in
          pkgs.mkShell {
            packages = [
              (virtualenv pkgs)
              pkgs.black
              pkgs.mypy
              pkgs.nemo
              pkgs.uv
            ];
            env =
              {
                UV_NO_SYNC = "1";
                UV_PYTHON_DOWNLOADS = "never";
                UV_PYTHON = python pkgs;
              }
              // lib.optionalAttrs pkgs.stdenv.isLinux {
                LD_LIBRARY_PATH = lib.makeLibraryPath pkgs.pythonManylinuxPackages.manylinux1;
              };
            shellHook = ''
              unset PYTHONPATH
            '';
          };
      };
    };
}
