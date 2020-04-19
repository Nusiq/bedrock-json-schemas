# Bedrock-Schemas
A tool for generating schemas for json files for behavior-pack and
resource-pack for Minecraft Bedrock edition.

Put source packs into `/packs` directory.

# How to use it?

Just add this to your configuration in the `settings.json` for VS Code.
```
    "json.schemas": [
        {
            "fileMatch": [
                "entities/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/results/behavior_schema.json"
        },
        {
            "fileMatch": [
                "animations/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/results/animation_schema.json"
        },
        {
            "fileMatch": [
                "animation_controllers/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/results/controller_schema.json"
        },
        {
            "fileMatch": [
                "loot_tables/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/results/loot_table_schema.json"
        },
        {
            "fileMatch": [
                "spawn_rules/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/results/spawn_rules_schema.json"
        },
        {
            "fileMatch": [
                "trading/**.json"
            ],
            "url": "https://raw.githubusercontent.com/Nusiq/bedrock-json-schemas/master/results/trading_schema.json"
        }
    ]
```
