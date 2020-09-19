# Bedrock-Schemas
A tool for generating schemas for json files for behavior-pack and
resource-pack for Minecraft Bedrock edition.

Put source packs into `/packs` directory.

# How to use it?

Just add this to your configuration in the `settings.json` for VS Code.
```
    "json.schemas": [
        // BEHAVIORPACK
        {
            "fileMatch": [
                "behavior_packs/*/entities/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/bp.entity.schema.json"
        },
        {
            "fileMatch": [
                "behavior_packs/*/items/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/bp.item.schema.json"
        },
        {
            "fileMatch": [
                "behavior_packs/*/animation_controllers/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/bp.animation_controller.schema.json"
        },
        {
            "fileMatch": [
                "behavior_packs/*/animations/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/bp.animation.schema.json"
        },
        {
            "fileMatch": [
                "behavior_packs/*/loot_tables/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/bp.loot_table.schema.json"
        },
        {
            "fileMatch": [
                "behavior_packs/*/recipes/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/bp.recipe.schema.json"
        },
        {
            "fileMatch": [
                "behavior_packs/*/spawn_rules/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/bp.spawn_rules.schema.json"
        },
        {
            "fileMatch": [
                "behavior_packs/*/trading/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/bp.trading.schema.json"
        },

        // RESOURCEPACK
        {
            "fileMatch": [
                "resource_packs/*/animation_controllers/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/rp.animation_controller.schema.json"
        },
        {
            "fileMatch": [
                "resource_packs/*/animations/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/rp.animation.schema.json"
        },
        {
            "fileMatch": [
                "resource_packs/*/models/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/rp.model.schema.json"
        },
        {
            "fileMatch": [
                "resource_packs/*/attachables/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/rp.attachable.schema.json"
        },
        {
            "fileMatch": [
                "resource_packs/*/entity/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/rp.entity.schema.json"
        },
        {
            "fileMatch": [
                "resource_packs/*/particles/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/rp.particle.schema.json"
        },
        {
            "fileMatch": [
                "resource_packs/*/render_controllers/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/rp.render_controller.schema.json"
        },
        {
            "fileMatch": [
                "resource_packs/*/blocks.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/rp.blocks.json.schema.json"
        },
        {
            "fileMatch": [
                "resource_packs/*/sounds.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/rp.sounds.json.schema.json"
        },
    ],
```


Everything is generated from examples (not from documentation which
unfortunately has some errors) so some things may be missing.


# Experimental - strict schemas

This configuration uses experimental strict schemas. The difference between
the strict and basic schemas is that the strict schemas don't accept unknown
properties for the object. Using that will probably result in a large number
of false errors.
```
    "json.schemas": [
        // BEHAVIORPACK
        {
            "fileMatch": [
                "behavior_packs/*/entities/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas_strict/bp.entity.schema.json"
        },
        {
            "fileMatch": [
                "behavior_packs/*/items/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas_strict/bp.item.schema.json"
        },
        {
            "fileMatch": [
                "behavior_packs/*/animation_controllers/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas_strict/bp.animation_controller.schema.json"
        },
        {
            "fileMatch": [
                "behavior_packs/*/animations/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas_strict/bp.animation.schema.json"
        },
        {
            "fileMatch": [
                "behavior_packs/*/loot_tables/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas_strict/bp.loot_table.schema.json"
        },
        {
            "fileMatch": [
                "behavior_packs/*/recipes/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas_strict/bp.recipe.schema.json"
        },
        {
            "fileMatch": [
                "behavior_packs/*/spawn_rules/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas_strict/bp.spawn_rules.schema.json"
        },
        {
            "fileMatch": [
                "behavior_packs/*/trading/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas_strict/bp.trading.schema.json"
        },

        // RESOURCEPACK
        {
            "fileMatch": [
                "resource_packs/*/animation_controllers/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas_strict/rp.animation_controller.schema.json"
        },
        {
            "fileMatch": [
                "resource_packs/*/animations/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas_strict/rp.animation.schema.json"
        },
        {
            "fileMatch": [
                "resource_packs/*/models/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas_strict/rp.model.schema.json"
        },
        {
            "fileMatch": [
                "resource_packs/*/attachables/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas_strict/rp.attachable.schema.json"
        },
        {
            "fileMatch": [
                "resource_packs/*/entity/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas_strict/rp.entity.schema.json"
        },
        {
            "fileMatch": [
                "resource_packs/*/particles/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas_strict/rp.particle.schema.json"
        },
        {
            "fileMatch": [
                "resource_packs/*/render_controllers/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas_strict/rp.render_controller.schema.json"
        },
        {
            "fileMatch": [
                "resource_packs/*/blocks.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas_strict/rp.blocks.json.schema.json"
        },
        {
            "fileMatch": [
                "resource_packs/*/sounds.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas_strict/rp.sounds.json.schema.json"
        },
    ],
```