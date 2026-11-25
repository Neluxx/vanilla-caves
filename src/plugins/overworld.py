import json
from typing import Any

from beet import Context
from beet.contrib.worldgen import WorldgenDensityFunction, WorldgenNoiseSettings

from beet_datapack_utils import versioned_packs

SLOPED_CHEESE = "minecraft:overworld/sloped_cheese"
NOODLE_CAVES = "minecraft:overworld/caves/noodle"
CAVE_FUNCTIONS = "minecraft:overworld/caves/"


def beet_default(ctx: Context):
    for pack in versioned_packs(ctx):
        # Written for every pack, so each overlay replaces the base pack's older-format file.
        with pack.edit(WorldgenNoiseSettings, "minecraft:overworld") as settings:
            final_density = settings["noise_router"]["final_density"]
            if isinstance(final_density, str):
                # From 26.3 on the router references a file that only the default overworld uses.
                with pack.edit(WorldgenDensityFunction, final_density) as function:
                    remove_noise_caves(function)
            else:
                remove_noise_caves(final_density)


def remove_noise_caves(final_density: dict[str, Any]) -> None:
    """Remove cheese, spaghetti and noodle caves and cave entrances from `final_density`."""
    replace_cave_nodes(final_density)
    # Fails the build if vanilla changed and a cave function is still referenced.
    if CAVE_FUNCTIONS in json.dumps(final_density):
        raise ValueError("final_density still references a cave density function")


def replace_cave_nodes(node: dict[str, Any]) -> None:
    for key, child in node.items():
        if child == NOODLE_CAVES:
            # Noodle caves are combined with `min`, so 1 keeps the terrain.
            node[key] = 1
        elif not isinstance(child, dict):
            continue
        elif child.get("type") == "minecraft:range_choice" and child.get("input") == SLOPED_CHEESE:
            # Chooses between sloped_cheese with cave entrances and cheese/spaghetti caves.
            node[key] = SLOPED_CHEESE
        else:
            replace_cave_nodes(child)