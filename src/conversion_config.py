import json_paths as jp
from schema_builder import MetaSchema

BEHAVIOR_CONFIG = MetaSchema(
    meta_schema={
        "root": {
            "minecraft:entity": {
                "description": "description",
                "components": "component_group",
                "component_groups": {
                    jp.Wildcard.ANY_PARAMETER: "component_group",
                },
                "events": {
                    jp.Wildcard.ANY_PARAMETER: "event",
                },
            },
        },
        "component_group": {
            jp.Wildcard.ANYTHING_UNTIL_NEXT_MATCH: {
                "filters": "filter",
            },
        },
        "event": {
            jp.Wildcard.ANYTHING_UNTIL_NEXT_MATCH: {
                "filters": "filter"
            }
        },
        "filter": {
            "all_of": {
                jp.Wildcard.ANY_ITEM: "filter"
            },
            "any_of": {
                jp.Wildcard.ANY_ITEM: "filter"
            },
        },
        "description": {},
    },
    blacklist=[
        ["minecraft:entity", "minecraft:physics"],
        ["minecraft:entity", "minecraft:pushable"]
    ]
)