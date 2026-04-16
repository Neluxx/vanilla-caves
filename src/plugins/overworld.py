from beet import Context
from beet.contrib.vanilla import Vanilla
from beet.contrib.worldgen import WorldgenNoiseSettings

from src.plugins.utils import iterate_versions, field_accessor


def beet_default(ctx: Context):
    vanilla = ctx.inject(Vanilla)

    for pack, version in iterate_versions(ctx):
        source = vanilla.releases[version].mount("data").data[WorldgenNoiseSettings]
        patched = source["minecraft:overworld"].copy()
        noise_router = patched.data["noise_router"]
        final_density = noise_router["final_density"]

        # Disable noise caves by short-circuiting the final density function.
        # The vanilla final_density multiplies sloped_cheese by a cave-carving
        # density; setting argument2 to 1 removes the cave contribution, and
        # replacing the deeply nested argument with a direct reference to
        # sloped_cheese bypasses the noise cave computation entirely.
        final_density["argument2"] = 1
        final_density["argument1"]["argument"]["argument2"]["argument"]["argument"]["argument2"]["argument2"]["argument2"]["argument2"]["argument2"]["argument2"] = "minecraft:overworld/sloped_cheese"

        pack[WorldgenNoiseSettings]["minecraft:overworld"] = patched
