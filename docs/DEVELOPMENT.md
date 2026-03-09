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

### Build

Compiles the project and writes the output to the `build/` directory.

```powershell
beet build
```

### Watch

Rebuilds automatically whenever a source file changes. Useful during active development.

```powershell
beet watch
```

### Link

Symlinks the built pack directly into your Minecraft `datapacks/` folder so changes are immediately reflected in-game without manual copying.

```powershell
beet link
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
│   └── datapack/          # Datapack source files
│       └── v1_20_5/       # Overlay for overwrites
│       └── v1_21_7/       # Overlay for overwrites
├── build/                 # Build output (git-ignored)
├── beet.yml               # Beet project configuration
├── pyproject.toml         # Python project & dependency config
└── spyglass.json          # Datapack helper plus extension config
```

## Configuration

Pack format ranges are configured in `beet.yml`. The project currently targets:

| Pack | Min format | Max format | Versions |
|------|-----------|-----------|----------|
| Data pack | 10 | 94 | 1.19 – 1.21.11 |

Overlays are picked up automatically from subdirectories within the load path. Format ranges for overlays are set explicitly in `beet.yml`.

### Datapack Helper Plus

This template includes a `spyglass.json` for the [Datapack Helper Plus](https://marketplace.visualstudio.com/items?itemName=SPGoding.datapack-language-server) VS Code extension:

```json
{
  "env": {
    "gameVersion": "Auto"
  }
}
```

With `"gameVersion": "Auto"`, DHP detects the target Minecraft version from your `pack.mcmeta` automatically. Since DHP can only validate against one version at a time, you can temporarily set `"gameVersion"` to a specific version (e.g. `"1.20.5"`) when you need to check code inside an overlay against that particular version.
