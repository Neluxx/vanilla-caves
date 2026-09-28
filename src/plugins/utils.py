from typing import Any, Callable, Iterator, Tuple, Type

from beet import Context, DataPack, JsonFile
from beet.contrib.worldgen import (
    WorldgenCarver,
    WorldgenConfiguredCarver,
    WorldgenConfiguredFeature,
    WorldgenFeature,
)


def parse_version(version: str) -> Tuple[int, ...]:
    """Parse a Minecraft version string like '1.20.5' into a tuple."""
    return tuple(int(part) for part in version.split("."))


def iterate_versions(ctx: Context) -> Iterator[Tuple[DataPack, str]]:
    """Yield (pack, version) for the base pack and each configured overlay.

    Reads `base_version` and `overlay_versions` from `ctx.meta`.
    """
    yield ctx.data, ctx.meta["base_version"]

    for directory, version in ctx.meta.get("overlay_versions", {}).items():
        yield ctx.data.overlays[directory], version


def field_accessor(config: dict, version: str) -> Callable[[str], dict]:
    """Return an accessor for worldgen config fields that handles the
    pre-1.20.5 `{value: {...}}` nesting transparently.

    Usage:
        field = field_accessor(config, version)
        field("horizontal_radius_multiplier")["min_inclusive"] = 0.7
    """
    nested = parse_version(version) < (1, 20, 5)
    return lambda name: config[name]["value"] if nested else config[name]


def carver_registry(version: str) -> Type[JsonFile]:
    """26.3 moved `worldgen/configured_carver` to `worldgen/carver`."""
    if parse_version(version) >= (26, 3):
        return WorldgenCarver
    return WorldgenConfiguredCarver


def feature_registry(version: str) -> Type[JsonFile]:
    """26.3 moved `worldgen/configured_feature` to `worldgen/feature`."""
    if parse_version(version) >= (26, 3):
        return WorldgenFeature
    return WorldgenConfiguredFeature


def worldgen_config(data: dict) -> dict:
    """Return the object holding a carver's or feature's settings.

    Before 26.3 the settings are wrapped in a `config` object. Since 26.3
    they sit directly on the root object next to `type`.
    """
    return data.get("config", data)


def resolve_key(data: dict, *candidates: str) -> str:
    """Return the first key from `candidates` that exists in `data`.

    Used for fields that were renamed between versions, e.g.
    `resolve_key(config, "room_vertical_radius_multiplier", "yScale")`.
    """
    for key in candidates:
        if key in data:
            return key
    raise KeyError(f"None of {candidates} found in {sorted(data)}")


def replace_nodes(tree: Any, match: Callable[[Any], bool], replacement: Any) -> int:
    """Replace every node below `tree` for which `match` returns True.

    Walks dicts and lists recursively and does not descend into replaced
    nodes. Returns the number of replacements, so callers can verify that
    the vanilla structure still looks as expected.
    """
    if isinstance(tree, dict):
        items = list(tree.items())
    elif isinstance(tree, list):
        items = list(enumerate(tree))
    else:
        return 0

    count = 0
    for key, child in items:
        if match(child):
            tree[key] = replacement
            count += 1
        else:
            count += replace_nodes(child, match, replacement)
    return count
