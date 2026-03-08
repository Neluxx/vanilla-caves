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
├── src/
│   ├── datapack/          # Datapack source files
│   │   └── v1_21_9/       # Overlay for overwrites
│   └── resourcepack/      # Resourcepack source files
├── build/                 # Build output (git-ignored)
├── beet.yml               # Beet project configuration
└── pyproject.toml         # Python project & dependency config
```

## Configuration

Pack format ranges are configured in `beet.yml`. The project currently targets:

| Pack | Min format | Max format | Versions |
|------|-----------|-----------|----------|
| Data pack | 81 | 94 | 1.20.5 – 1.21.9 |
| Resource pack | 69 | 75 | 1.20.5 – 1.21.9 |

Overlays are picked up automatically from subdirectories within the load path. Format ranges for overlays are set explicitly in `beet.yml`.

## Resources

- [Beet GitHub](https://github.com/mcbeet/beet)
- [Beet Documentation](https://mcbeet.dev)
- [Minecraft Wiki - Data pack format](https://minecraft.wiki/w/Pack_format#Data_pack_format_history)
- [Minecraft Wiki - Resource pack format](https://minecraft.wiki/w/Pack_format#Resource_pack_format_history)

## Contributing
Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for commit conventions and guidelines.

## Syncing Datapack Repositories
If you maintain a datapack repository based on this template, see [SYNC.md](SYNC.md) for instructions on how to pull in template updates.