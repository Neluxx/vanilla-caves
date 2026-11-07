from typing import Any

from beet import Context
from beet.contrib.worldgen import WorldgenNoiseSettings

from datapack_utils import Targets, is_reference, replace_nodes

SLOPED_CHEESE = "minecraft:overworld/sloped_cheese"
NOODLE_CAVES = "minecraft:overworld/caves/noodle"


def is_cave_choice(node: Any) -> bool:
    """Match the range_choice that mixes noise caves into sloped_cheese."""
    return (
        isinstance(node, dict)
        and node.get("type") == "minecraft:range_choice"
        and is_reference(node.get("input"), SLOPED_CHEESE)
    )


def beet_default(ctx: Context):
    for target in ctx.inject(Targets):
        with target.patch(WorldgenNoiseSettings, "minecraft:overworld") as settings:
            noise_router = settings["noise_router"]

            # Since 26.3 the router only references `minecraft:overworld/final_density`.
            # Inline a copy of it, so only the default overworld noise settings change
            # and this file replaces the base pack's older-format overworld.json.
            noise_router["final_density"] = target.inline_density_function(
                noise_router["final_density"]
            )
            final_density = noise_router["final_density"]

            # Replace the range_choice on sloped_cheese with sloped_cheese itself to
            # remove cheese, spaghetti and cave entrances, then replace the noodle
            # reference with 1 to remove noodle caves. Both are found by content, so
            # this works before and after 26.3 and fails the build if vanilla changes.
            replace_nodes(final_density, is_cave_choice, SLOPED_CHEESE, expected=1)
            replace_nodes(final_density, lambda node: node == NOODLE_CAVES, 1, expected=1)