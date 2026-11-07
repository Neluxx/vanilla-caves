from beet import Context

from datapack_utils import CARVER, Targets, provider, resolve_key, set_range, worldgen_config


def beet_default(ctx: Context):
    for target in ctx.inject(Targets):
        with target.patch(CARVER, "minecraft:cave") as cave:
            config = worldgen_config(cave)

            # The probability that each chunk attempts to generate carvers.
            config["probability"] = 0.15  # defaults to 0.15

            # Horizontally scales cave tunnels. Doesn't affect the length of tunnels.
            set_range(provider(config, "horizontal_radius_multiplier"), 0.8, 1.5)  # defaults to 0.7..1.4

            # Vertically scales cave tunnels. Doesn't affect the length of tunnels.
            set_range(provider(config, "vertical_radius_multiplier"), 0.9, 1.4)  # defaults to 0.8..1.3

            # Vertically scales circular voids (renamed from `yScale` in 26.3).
            room = resolve_key(config, "room_vertical_radius_multiplier", "yScale")
            set_range(provider(config, room), 0.1, 0.9)  # defaults to 0.1..0.9

            # The height at which this carver attempts to generate.
            config["y"]["max_inclusive"]["absolute"] = 180  # defaults to 180