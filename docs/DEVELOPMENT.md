# Development

## Requirements

- [Python](https://www.python.org/) 3.14+
- [uv](https://docs.astral.sh/uv/) (package manager)

## Setup

### 1. Create virtual environment and install dependencies

```powershell
uv sync
```

### 2. Activate the virtual environment

```powershell
# Windows (PowerShell)
.\.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

> You need to activate the virtual environment once per terminal session before using `beet`.

## Usage

This project ships two beet configurations:

- `beet.yml` — targets Minecraft **1.21.9+** (pack format ≥ 82), using the modern `min_format` / `max_format` fields only.
- `beet.legacy.yml` — targets Minecraft versions **below 1.21.9** (pack format < 82), including the deprecated `pack_format`, `supported_formats`, and overlay `formats` fields required for backwards compatibility.

By default, `beet` uses `beet.yml`. To build the legacy pack, pass the config explicitly with `-p`.

### Build

Compiles the project and writes the output to the `build/` directory.

```powershell
# Modern (1.21.9+)
beet build

# Legacy (< 1.21.9)
beet -p beet.legacy.yml build
```

### Watch

Rebuilds automatically whenever a source file changes. Useful during active development.

```powershell
# Modern (1.21.9+)
beet watch

# Legacy (< 1.21.9)
beet -p beet.legacy.yml watch
```

### Link

Symlinks the built pack directly into your Minecraft `datapacks/` folder so changes are immediately reflected in-game without manual copying.

```powershell
# Modern (1.21.9+)
beet link

# Legacy (< 1.21.9)
beet -p beet.legacy.yml link
```

> Run `beet build` or `beet watch` alongside this so the linked output stays up to date.

### Clear cache

Clears beet's internal cache. Useful if you run into stale build artifacts or unexpected behavior.

```powershell
beet cache --clear
```

## Project Structure

```
.
├── docs/
├── src/
│   ├── datapack/          # Datapack source files
│   │   └── v1_21/         # Overlay for overwrites
│   └── resourcepack/      # Resourcepack source files
├── build/                 # Build output (git-ignored)
├── beet.yml               # Beet project configuration
├── beet.legacy.yml        # Beet legacy project configuration
└── pyproject.toml         # Python project & dependency config
```

## Updating dependencies

Dependencies are pinned in `uv.lock`. To pull in newer versions that still satisfy the constraints in `pyproject.toml`, use `uv lock --upgrade`.

### Upgrade all dependencies

Re-resolves every dependency to the latest compatible version and updates `uv.lock`.

```powershell
uv lock --upgrade
```

### Upgrade a single package

Useful when you only want to bump one dependency without touching the rest of the lockfile.

```powershell
uv lock --upgrade-package beet
```

After upgrading, sync the virtual environment so the new versions are actually installed:

```powershell
uv sync
```

> Commit the updated `uv.lock` so other contributors get the same resolved versions.