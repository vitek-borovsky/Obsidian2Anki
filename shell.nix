{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    pyright
    (python311.withPackages (ps: with ps; [
        requests
        pytest
    ]))


  ];

  shellHook = ''
  '';
}
