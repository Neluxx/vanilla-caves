from beet import Context, DataPack, Function, FunctionTag

from src.plugins.utils import iterate_versions


def beet_default(ctx: Context):
    # Use for modifying vanilla data
    # vanilla = ctx.inject(Vanilla)

    for pack, version in iterate_versions(ctx):
        # Get the vanilla data source, e.g. worldgen/configured_carver/cave.json
        # source = vanilla.releases[version].mount("data").data[WorldgenConfiguredCarver]
        # patched = source["minecraft:cave"].copy()

        pack[Function]["beet_datapack_template:hello_world"] = Function(["say Hello World"])
        pack["minecraft:load"] = FunctionTag({"values": ["beet_datapack_template:hello_world"]})
