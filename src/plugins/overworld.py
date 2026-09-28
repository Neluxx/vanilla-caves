from typing import Any

from beet import Context
from beet.contrib.vanilla import Vanilla
from beet.contrib.worldgen import WorldgenDensityFunction, WorldgenNoiseSettings

from src.plugins.utils import iterate_versions, replace_nodes

SLOPED_CHEESE = "minecraft:overworld/sloped_cheese"
NOODLE_CAVES = "minecraft:overworld/caves/noodle"


def is_sloped_cheese(node: Any) -> bool:
    """Match a reference to sloped_cheese, plain or wrapped in `cache_once`."""
    if node == SLOPED_CHEESE:
        return True
    return (
        isinstance(node, dict)
        and node.get("type") == "minecraft:cache_once"
        and node.get("argument") == SLOPED_CHEESE
    )


def is_cave_choice(node: Any) -> bool:
    """Match the range_choice that mixes noise caves into sloped_cheese."""
    return (
        isinstance(node, dict)
        and node.get("type") == "minecraft:range_choice"
        and is_sloped_cheese(node.get("input"))
    )


def beet_default(ctx: Context):
    vanilla = ctx.inject(Vanilla)

    for pack, version in iterate_versions(ctx):
        data = vanilla.releases[version].mount("data").data
        patched = data[WorldgenNoiseSettings]["minecraft:overworld"].copy()
        noise_router = patched.data["noise_router"]

        # Since 26.3 the router only references `minecraft:overworld/final_density`.
        # Inline a copy of it, so only the default overworld noise settings are
        # changed (just like before) and this file replaces the base pack's
        # older-format overworld.json in the overlay.
        if isinstance(noise_router["final_density"], str):
            reference = noise_router["final_density"]
            noise_router["final_density"] = data[WorldgenDensityFunction][reference].copy().data

        final_density = noise_router["final_density"]

        # Disable noise caves by short-circuiting the final density function.
        # Inside the terrain, a range_choice on sloped_cheese carves cheese,
        # spaghetti and cave entrances; replacing it with sloped_cheese itself
        # bypasses the noise cave computation entirely. The final_density then
        # takes the minimum of the terrain and the noodle caves; replacing the
        # noodle reference with 1 removes them.
        # Both are located by content, so the patch works for the pre-26.3
        # (argument1/argument2) and the 26.3+ (left/right) formats.
        replaced = {
            "cave range_choice": replace_nodes(final_density, is_cave_choice, SLOPED_CHEESE),
            "noodle caves": replace_nodes(final_density, lambda node: node == NOODLE_CAVES, 1),
        }
        for what, count in replaced.items():
            if count != 1:
                raise ValueError(f"Expected 1 {what} in {version} final_density, found {count}")

        pack[WorldgenNoiseSettings]["minecraft:overworld"] = patched
