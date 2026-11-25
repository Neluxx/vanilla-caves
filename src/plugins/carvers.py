from dataclasses import dataclass

from beet import Context

from beet_datapack_utils import CARVER, first_existing_key, get_config, set_range, versioned_packs


@dataclass(frozen=True)
class CaveCarver:
    # The probability that each chunk attempts to generate carvers.
    probability: float
    # Horizontally scales cave tunnels. Doesn't affect the length of tunnels.
    horizontal_radius_multiplier: tuple[float, float]
    # Vertically scales cave tunnels. Doesn't affect the length of tunnels.
    vertical_radius_multiplier: tuple[float, float]
    # Vertically scales circular voids.
    room_vertical_radius_multiplier: tuple[float, float]
    # The highest y level at which this carver attempts to generate.
    max_y: int


CAVE_CARVERS: dict[str, CaveCarver] = {
    "minecraft:cave": CaveCarver(
        probability=0.15,                            # defaults to 0.15
        horizontal_radius_multiplier=(0.8, 1.5),     # defaults to 0.7..1.4
        vertical_radius_multiplier=(0.9, 1.4),       # defaults to 0.8..1.3
        room_vertical_radius_multiplier=(0.1, 0.9),  # defaults to 0.1..0.9
        max_y=180,                                   # defaults to 180
    ),
    "minecraft:cave_extra_underground": CaveCarver(
        probability=0.2,                             # defaults to 0.07
        horizontal_radius_multiplier=(0.9, 1.6),     # defaults to 0.7..1.4
        vertical_radius_multiplier=(1.0, 1.5),       # defaults to 0.8..1.3
        room_vertical_radius_multiplier=(0.2, 1.0),  # defaults to 0.1..0.9
        max_y=42,                                    # defaults to 47
    ),
}


def beet_default(ctx: Context):
    for pack in versioned_packs(ctx):
        for name, carver in CAVE_CARVERS.items():
            with pack.edit(CARVER, name) as data:
                config = get_config(data)
                config["probability"] = carver.probability
                set_range(config, "horizontal_radius_multiplier", *carver.horizontal_radius_multiplier)
                set_range(config, "vertical_radius_multiplier", *carver.vertical_radius_multiplier)
                # Renamed from `yScale` in 26.3.
                room = first_existing_key(config, "room_vertical_radius_multiplier", "yScale")
                set_range(config, room, *carver.room_vertical_radius_multiplier)
                config["y"]["max_inclusive"]["absolute"] = carver.max_y