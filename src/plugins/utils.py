from typing import Callable, Iterator, Tuple

from beet import Context, DataPack


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
