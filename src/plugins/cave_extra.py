from beet import Context, DataPack
from beet.contrib.vanilla import Vanilla
from beet.contrib.worldgen import WorldgenConfiguredCarver

CAVE = "minecraft:cave_extra_underground"
PROBABILITY = 0.2  # defaults to 0.07
X_MAX_EXCLUSIVE = 1.5  # defaults to 1.4
X_MIN_INCLUSIVE = 0.9  # defaults to 0.7
Y_MAX_EXCLUSIVE = 1.4  # defaults to 1.3
Y_MIN_INCLUSIVE = 1  # defaults to 0.8
Y_ABSOLUTE_MAX = 48  # defaults to 47


def beet_default(ctx: Context):
    base_version = ctx.meta["base_version"]
    overlay_versions = ctx.meta["overlay_versions"]
    vanilla = ctx.inject(Vanilla)

    source = get_source(vanilla, base_version)
    apply_patch(ctx.data, source, nested=True)

    for directory, version in overlay_versions.items():
        overlay = ctx.data.overlays[directory]
        source = get_source(vanilla, version)
        apply_patch(overlay, source, nested=False)


def get_source(vanilla: Vanilla, version: str):
    return vanilla.releases[version].mount("data").data[WorldgenConfiguredCarver]


def apply_patch(pack: DataPack, source, nested: bool):
    patched = source[CAVE].copy()
    config = patched.data["config"]
    config["probability"] = PROBABILITY

    x_radius = config["horizontal_radius_multiplier"]["value"] if nested else config["horizontal_radius_multiplier"]
    x_radius["max_exclusive"] = X_MAX_EXCLUSIVE
    x_radius["min_inclusive"] = X_MIN_INCLUSIVE

    y_radius = config["vertical_radius_multiplier"]["value"] if nested else config["vertical_radius_multiplier"]
    y_radius["max_exclusive"] = Y_MAX_EXCLUSIVE
    y_radius["min_inclusive"] = Y_MIN_INCLUSIVE

    config["y"]["max_inclusive"]["absolute"] = Y_ABSOLUTE_MAX

    pack[WorldgenConfiguredCarver][CAVE] = patched
