from beet import Context
from beet.contrib.vanilla import Vanilla

from src.plugins.utils import carver_registry, field_accessor, iterate_versions, resolve_key, worldgen_config


def beet_default(ctx: Context):
    vanilla = ctx.inject(Vanilla)

    for pack, version in iterate_versions(ctx):
        registry = carver_registry(version)
        source = vanilla.releases[version].mount("data").data[registry]
        patched = source["minecraft:cave_extra_underground"].copy()
        config = worldgen_config(patched.data)
        field = field_accessor(config, version)

        # The probability that each chunk attempts to generate carvers.
        config["probability"] = 0.2  # defaults to 0.07

        # Horizontally scales cave tunnels. Doesn't affect the length of tunnels.
        field("horizontal_radius_multiplier")["max_exclusive"] = 1.6  # defaults to 1.4
        field("horizontal_radius_multiplier")["min_inclusive"] = 0.9  # defaults to 0.7

        # Vertically scales cave tunnels. Doesn't affect the length of tunnels.
        field("vertical_radius_multiplier")["max_exclusive"] = 1.5  # defaults to 1.3
        field("vertical_radius_multiplier")["min_inclusive"] = 1.0  # defaults to 0.8

        # Vertically scales circular voids.
        # Renamed from `yScale` to `room_vertical_radius_multiplier` in 26.3.
        room = resolve_key(config, "room_vertical_radius_multiplier", "yScale")
        field(room)["max_exclusive"] = 1.0  # defaults to 0.9
        field(room)["min_inclusive"] = 0.2  # defaults to 0.1

        # The height at which this carver attempts to generate.
        config["y"]["max_inclusive"]["absolute"] = 42  # defaults to 47

        pack[registry]["minecraft:cave_extra_underground"] = patched
