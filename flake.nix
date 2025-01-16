{
  description = "Solutions and examples for the Knowledge Graphs course";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    utils.url = "github:gytis-ivaskevicius/flake-utils-plus";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        flake-utils.follows = "utils/flake-utils";
      };
    };
    nemo = {
      url = "github:knowsys/nemo/refs/tags/v0.7.0";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        utils.follows = "utils";
      };
    };
  };

  outputs =
    {
      self,
      utils,
      poetry2nix,
      nemo,
      ...
    }@inputs:
    let
      inherit (utils.lib) mkFlake;
    in
    mkFlake {
      inherit self inputs;

      channels.nixpkgs.overlaysBuilder = channels: [
        poetry2nix.overlays.default
        nemo.overlays.default
      ];

      outputsBuilder = channels: {
        devShells.default =
          let
            pkgs = channels.nixpkgs;
            poetryEnv = pkgs.poetry2nix.mkPoetryEnv {
              projectDir = ./.;
              overrides = pkgs.poetry2nix.overrides.withDefaults (
                self: super: {
                  networkit = super.networkit.overridePythonAttrs (old: {
                    src = pkgs.fetchFromGitHub {
                      owner = "networkit";
                      repo = "networkit";
                      rev = "9b33495752e5b98f1401faea911c026279a0d478";
                      hash = "sha256-sarzPsbrXpMam16z2kKn53nAW2I99CQ67diaIYLKjCI=";
                      fetchSubmodules = true;

                    };
                    nativeBuildInputs = [
                      self.cython
                      pkgs.cmake
                    ] ++ (old.nativeBuildInputs or [ ]);

                    buildInputs = [ self.scikit-build ] ++ (old.buildInputs or [ ]);
                    dontUseCmakeConfigure = true;
                  });
                }
              );
              extraPackages = pypkgs: [ pkgs.nemo-python ];
            };
          in
          poetryEnv.env.overrideAttrs (oldAttrs: {
            buildInputs = [
              pkgs.black
              pkgs.poetry
              pkgs.mypy
              pkgs.nemo
            ];
          });
      };
    };
}
