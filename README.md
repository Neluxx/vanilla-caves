# Beet Datapack Template

A Minecraft datapack (and resourcepack) template using [beet](https://github.com/mcbeet/beet) — a powerful toolchain for building, watching, and deploying data packs and resource packs.

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
│   ├── datapack/          # Datapack source files
│   │   └── v1_21/         # Overlay for overwrites
│   └── resourcepack/      # Resourcepack source files
├── build/                 # Build output (git-ignored)
├── beet.yml               # Beet project configuration
├── pyproject.toml         # Python project & dependency config
└── spyglass.json          # Datapack helper plus extension config
```

## Configuration

Pack format ranges are configured in `beet.yml`. The project currently targets:

| Pack | Min format | Max format | Versions |
|------|-----------|-----------|----------|
| Data pack | 15 | 94 | 1.20 – 1.21.11 |
| Resource pack | 15 | 75 | 1.20 – 1.21.11 |

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

## Support the Project

If you enjoy this datapack and find it useful, please consider giving the repository a star and following me on GitHub.  
This helps the project gain visibility and motivates further development and maintenance.

## Contributing
Contributions are welcome! Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for commit conventions and guidelines.

## Syncing Datapack Repositories
If you maintain a datapack repository based on this template, see [SYNC.md](docs/SYNC.md) for instructions on how to pull in template updates.

## Resources

- [Beet GitHub](https://github.com/mcbeet/beet)
- [Beet Documentation](https://mcbeet.dev)
- [Minecraft Wiki - Data pack format](https://minecraft.wiki/w/Pack_format#Data_pack_format_history)
- [Minecraft Wiki - Resource pack format](https://minecraft.wiki/w/Pack_format#Resource_pack_format_history)