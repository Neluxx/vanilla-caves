from beet import Context
from beet.contrib.vanilla import Vanilla
from beet.contrib.worldgen import WorldgenConfiguredCarver

from src.plugins.utils import iterate_versions, parse_version


def beet_default(ctx: Context):
    vanilla = ctx.inject(Vanilla)

    for pack, version in iterate_versions(ctx):
        source = vanilla.releases[version].mount("data").data[WorldgenConfiguredCarver]
        patched = source["minecraft:cave"].copy()
        config = patched.data["config"]
        nested = parse_version(version) < (1, 20, 5)

        def field(name):
            return config[name]["value"] if nested else config[name]

        # The probability that each chunk attempts to generate carvers.
        config["probability"] = 0.2  # defaults to 0.15

        # Horizontally scales cave tunnels. Doesn't affect the length of tunnels.
        x_radius = field("horizontal_radius_multiplier")
        x_radius["max_exclusive"] = 1.4  # defaults to 1.4
        x_radius["min_inclusive"] = 0.7  # defaults to 0.7

        # Vertically scales cave tunnels. Doesn't affect the length of tunnels.
        y_radius = field("vertical_radius_multiplier")
        y_radius["max_exclusive"] = 1.3  # defaults to 1.3
        y_radius["min_inclusive"] = 0.8  # defaults to 0.8

        # The height at which this carver attempts to generate.
        config["y"]["max_inclusive"]["absolute"] = 96  # defaults to 180

        pack[WorldgenConfiguredCarver]["minecraft:cave"] = patched
