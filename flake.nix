{
  description = "Solutions and examples for the Knowledge Graphs course";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";
    utils.url = "github:gytis-ivaskevicius/flake-utils-plus";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        flake-utils.follows = "utils/flake-utils";
      };
    };
  };

  outputs = { self, nixpkgs, utils, poetry2nix, ... }@inputs:
    let inherit (utils.lib) mkFlake;
    in mkFlake {
      inherit self inputs;

      channels.nixpkgs.overlaysBuilder = channels: [ poetry2nix.overlay ];

      outputsBuilder = channels: {
        devShell = let
          pkgs = channels.nixpkgs;
          poetryEnv = pkgs.poetry2nix.mkPoetryEnv {
            projectDir = ./.;
            overrides = pkgs.poetry2nix.overrides.withDefaults (self: super: {
              networkit = super.networkit.overridePythonAttrs (old: {
                nativeBuildInputs = [ self.cython pkgs.cmake ]
                  ++ (old.nativeBuildInputs or [ ]);
                buildInputs = [ self.scikit-build ] ++ (old.buildInputs or [ ]);
                dontUseCmakeConfigure = true;
              });
            });
          };
        in poetryEnv.env.overrideAttrs
        (oldAttrs: { buildInputs = with pkgs; [ black poetry ]; });
      };
    };
}
