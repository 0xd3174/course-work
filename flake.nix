{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
  in {
    devShells.${system}.default = pkgs.mkShell {
      buildInputs = with pkgs; [
        (texlive.combine {
          inherit (texlive) scheme-medium
            biblatex biblatex-gost
            extsizes
            titlesec
            tocloft
            biber
            enumitem
            pdfpages;
        })
        corefonts # Windows fonts (especially Times New Roman)
      ];

      shellHook = ''
        export FONTCONFIG_FILE=${pkgs.makeFontsConf { fontDirectories = [ pkgs.corefonts ]; }}
      '';
    };
  };
}
