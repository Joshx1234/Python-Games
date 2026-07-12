# Vendored Source

This directory is a vendored copy of the Dev Container feature:
- Feature: `desktop-lite`
- Upstream repo: `https://github.com/devcontainers/features`
- Upstream path: `src/desktop-lite`
- Upstream commit: `6c375f1d65510836760bef052f4614a0df974946`

## Update Procedure

1. Clone or fetch `https://github.com/devcontainers/features`.
2. Copy `src/desktop-lite/*` into this directory.
3. Review `install.sh` for apt repository key changes.
4. Rebuild the dev container and verify desktop startup.

This copy is intentionally pinned to avoid unexpected upstream behavior changes.
