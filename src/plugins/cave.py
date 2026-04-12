from beet import Context, DataPack
from beet.contrib.vanilla import Vanilla
from beet.contrib.worldgen import WorldgenConfiguredCarver


def beet_default(ctx: Context):
    source = get_source(ctx.inject(Vanilla), ctx.meta["base_version"])
    apply_patch(ctx.data, source, nested=True)

    for directory, version in ctx.meta["overlay_versions"].items():
        overlay = ctx.data.overlays[directory]
        source = get_source(ctx.inject(Vanilla), version)
        apply_patch(overlay, source, nested=False)


def get_source(vanilla: Vanilla, version: str):
    return vanilla.releases[version].mount("data").data[WorldgenConfiguredCarver]


def apply_patch(pack: DataPack, source, nested: bool):
    patched = source["minecraft:cave"].copy()

    # The probability that each chunk attempts to generate carvers.
    config = patched.data["config"]
    config["probability"] = 0.125  # defaults to 0.15

    # Horizontally scales cave tunnels. Doesn't affect the length of tunnels.
    x_radius = config["horizontal_radius_multiplier"]["value"] if nested else config["horizontal_radius_multiplier"]
    x_radius["max_exclusive"] = 1.5  # defaults to 1.4
    x_radius["min_inclusive"] = 0.9  # defaults to 0.7

    # Vertically scales cave tunnels. Doesn't affect the length of tunnels.
    y_radius = config["vertical_radius_multiplier"]["value"] if nested else config["vertical_radius_multiplier"]
    y_radius["max_exclusive"] = 1.4  # defaults to 1.3
    y_radius["min_inclusive"] = 1  # defaults to 0.8

    # The height at which this carver attempts to generate.
    config["y"]["max_inclusive"]["absolute"] = 72  # defaults to 180

    pack[WorldgenConfiguredCarver]["minecraft:cave"] = patched
