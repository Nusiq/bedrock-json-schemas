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
    ],
```

# What is generated?
The schemas are generated for files that use format_versions from list below.
Everything is generated from examples (not from documentation which
unfortunately has some errors) so some things may be missing.

## BEHAVIORPACK SCHEMAS
| type                    | value                                  |
| ------------------------|--------------------------------------- |
| animation_controllers   | 1.10.0                                 |
| animations              | 1.10.0                                 |
| entities                | 1.8.0, 1.10.0, 1.12.0, 1.13.0, 1.14.0  |
| trading                 | None                                   |
| loot_tables             | None                                   |
| items                   | 1.16, 1.14, 1.10                       |
| recipes                 | 1.12, 1.14                             |
| spawn_rules             | 1.8.0, 1.11.0                          |

## RESOURCEPACK SCHEMAS
| type                   |value                                   |
| -----------------------|--------------------------------------- |
| animation_controllers  | 1.10.0                                 |
| animations             | 1.8.0                                  |
| entity                 | 1.8.0, 1.10.0                          |
| particles              | 1.10.0                                 |
| render_controllers     | 1.8.0, 1.10.0, 1.10                    |
| attachables            | 1.10.0, 1.10, 1.8.0                    |
| models                 | 1.8.0, 1.10.0, 1.12.0                  |

\* This table isn't automatically generated so it's not guaranteed its
up-to-date.