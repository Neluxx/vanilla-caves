from beet import Context
from beet.contrib.vanilla import Vanilla
from beet.contrib.worldgen import WorldgenConfiguredCarver

from src.plugins.utils import iterate_versions, field_accessor


def beet_default(ctx: Context):
    vanilla = ctx.inject(Vanilla)

    for pack, version in iterate_versions(ctx):
        source = vanilla.releases[version].mount("data").data[WorldgenConfiguredCarver]
        patched = source["minecraft:cave"].copy()
        config = patched.data["config"]
        field = field_accessor(config, version)

        # The probability that each chunk attempts to generate carvers.
        config["probability"] = 0.2  # defaults to 0.07

        # Horizontally scales cave tunnels. Doesn't affect the length of tunnels.
        field("horizontal_radius_multiplier")["max_exclusive"] = 1.5  # defaults to 1.4
        field("horizontal_radius_multiplier")["min_inclusive"] = 0.9  # defaults to 0.7

        # Vertically scales cave tunnels. Doesn't affect the length of tunnels.
        field("vertical_radius_multiplier")["max_exclusive"] = 1.4  # defaults to 1.3
        field("vertical_radius_multiplier")["min_inclusive"] = 1.0  # defaults to 0.8

        # The height at which this carver attempts to generate.
        config["y"]["max_inclusive"]["absolute"] = 48  # defaults to 180

        pack[WorldgenConfiguredCarver]["minecraft:cave"] = patched
