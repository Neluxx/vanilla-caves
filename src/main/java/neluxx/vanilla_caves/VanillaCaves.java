package neluxx.vanilla_caves;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.resource.ResourceManagerHelper;
import net.fabricmc.fabric.api.resource.ResourcePackActivationType;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.util.Identifier;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class VanillaCaves implements ModInitializer {
	public static final String MOD_ID = "vanilla-caves";

	// This logger is used to write text to the console and the log file.
	// It is considered best practice to use your mod id as the logger's name.
	// That way, it's clear which mod wrote info, warnings, and errors.
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	@Override
	public void onInitialize() {
		// This code runs as soon as Minecraft is in a mod-load-ready state.
		// However, some things (like resources) may still be uninitialized.
		// Proceed with mild caution.

		LOGGER.info("Hello Fabric world!");

        // Register the datapack
        ResourceManagerHelper.registerBuiltinResourcePack(
                Identifier.of("minecraft", "datapack"),
                FabricLoader.getInstance().getModContainer(MOD_ID).orElseThrow(),
                ResourcePackActivationType.ALWAYS_ENABLED
        );

        LOGGER.info("Vanilla Caves datapack registered!");
	}
}