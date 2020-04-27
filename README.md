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
                "entities/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/bp.entity.schema.json"
        },
        {
            "fileMatch": [
                "items/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/bp.item.schema.json"
        },
        {
            "fileMatch": [
                "animation_controllers/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/bp.animation_controller.schema.json"
        },
        {
            "fileMatch": [
                "animations/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/bp.animation.schema.json"
        },
        {
            "fileMatch": [
                "loot_tables/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/bp.loot_table.schema.json"
        },
        {
            "fileMatch": [
                "recipes/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/bp.recipe.schema.json"
        },
        {
            "fileMatch": [
                "spawn_rules/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/bp.spawn_rules.schema.json"
        },
        {
            "fileMatch": [
                "trading/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/bp.trading.schema.json"
        },

        // RESOURCEPACK
        // {
        //     "fileMatch": [  //PATTERN COLISION
        //         "animation_controllers/**.json"
        //     ],
        //     "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/rp.animation_controller.schema.json"
        // },
        // {
        //     "fileMatch": [  //PATTERN COLISION
        //         "animations/**.json"
        //     ],
        //     "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/rp.animation.schema.json"
        // },
        {
            "fileMatch": [
                "attachables/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/rp.attachable.schema.json"
        },
        {
            "fileMatch": [
                "entity/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/rp.entity.schema.json"
        },
        {
            "fileMatch": [
                "particles/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/rp.particle.schema.json"
        },
        {
            "fileMatch": [
                "render_controllers/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/schemas/rp.render_controller.schema.json"
        },
    ],
```

