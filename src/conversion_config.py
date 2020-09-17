import json_paths as jp
from schema_builder import MetaSchema, Policy
import typing as tp


class ExportConfig(tp.NamedTuple):
    export_path: str
    pattern: str


# EXPORT CONFIG
BP_ENTITY_CFG=ExportConfig(
    export_path='../schemas/bp.entity.schema.json',
    pattern='entities/**.json',
)
BP_ITEM_CFG=ExportConfig(
    export_path='../schemas/bp.item.schema.json',
    pattern='items/**.json',
)
BP_ANIMATION_CONTROLLER_CFG=ExportConfig(
    export_path='../schemas/bp.animation_controller.schema.json',
    pattern='animation_controllers/**.json',
)
BP_ANIMATION_CFG=ExportConfig(
    export_path='../schemas/bp.animation.schema.json',
    pattern='animations/**.json',
)
BP_LOOT_TABLE_CFG=ExportConfig(
    export_path='../schemas/bp.loot_table.schema.json',
    pattern='loot_tables/**.json',
)
BP_RECIPE_CFG=ExportConfig(
    export_path='../schemas/bp.recipe.schema.json',
    pattern='recipes/**.json',
)
BP_SPAWN_RULE_CFG=ExportConfig(
    export_path='../schemas/bp.spawn_rules.schema.json',
    pattern='spawn_rules/**.json',
)
BP_TRADING_CFG=ExportConfig(
    export_path='../schemas/bp.trading.schema.json',
    pattern='trading/**.json',
)


RP_ANIMATION_CONTROLLER_CFG=ExportConfig(
    export_path='../schemas/rp.animation_controller.schema.json',
    pattern='animation_controllers/**.json',
)
RP_ANIMATION_CFG=ExportConfig(
    export_path='../schemas/rp.animation.schema.json',
    pattern='animations/**.json',
)
RP_ATTACHABLE_CFG=ExportConfig(
    export_path='../schemas/rp.attachable.schema.json',
    pattern='attachables/**.json',
)
RP_ENTITY_CFG=ExportConfig(
    export_path='../schemas/rp.entity.schema.json',
    pattern='entity/**.json',
)
RP_PARTICLE_CFG=ExportConfig(
    export_path='../schemas/rp.particle.schema.json',
    pattern='particles/**.json',
)
RP_RENDER_CONTROLLER_CFG=ExportConfig(
    export_path='../schemas/rp.render_controller.schema.json',
    pattern='render_controllers/**.json',
)
RP_MODEL_CFG=ExportConfig(
    export_path='../schemas/rp.model.schema.json',
    pattern='models/**.json',
)

def format_version_filter_creator(
    versions: tp.List[str]
) -> tp.Callable[[tp.Dict], bool]:
    '''
    Creates filter that returns true if format_version of passed dictionary is
    in versions list.
    '''
    def format_version_filter(data: tp.Dict) -> bool:
        return (
            'format_version' in data and data['format_version'] in versions
        )
    return format_version_filter

# META SCHEMAS
BP_ENTITY_MS = MetaSchema(
    meta_schema={
        # 1.8.0 and 1.10.0 and 1.12.0
        "8_10_12": {
            "minecraft:entity": {
                "description": "description",
                "components": "component_group_8_10_12",
                "component_groups": {
                    jp.Wildcard.ANY_PARAMETER: "component_group_8_10_12",
                },
                "events": {
                    jp.Wildcard.ANY_PARAMETER: "event",
                },
            },
        },
        "component_group_8_10_12": {
            jp.Wildcard.ANYTHING_UNTIL_NEXT_MATCH: {
                "filters": "filter",
            },
        },
        # 1.13.0 and 1.14.0
        "13_14": {
            "minecraft:entity": {
                "description": "description",
                "components": "component_group_13_14",
                "component_groups": {
                    jp.Wildcard.ANY_PARAMETER: "component_group_13_14",
                },
                "events": {
                    jp.Wildcard.ANY_PARAMETER: "event",
                },
            },
        },
        "component_group_13_14": {
            jp.Wildcard.ANYTHING_UNTIL_NEXT_MATCH: {
                "filters": "filter",
            },
        },
        # Common for all version
        "event": {
            "sequence": {
                jp.Wildcard.ANY_ITEM: "event"
            },
            "randomize": {
                jp.Wildcard.ANY_ITEM: "event"
            },
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
            jp.Wildcard.ANY_ITEM: "filter"
        },
        "description": {
            "animations": {
                jp.Wildcard.ANY_PARAMETER: "description_config"
            }
        },
        "description_config": {}
    },
    blacklist=[
        ["minecraft:entity", "minecraft:physics"],
        ["minecraft:entity", "minecraft:pushable"],
        ["minecraft:entity", "events", "minecraft:become_angry", "remove", "minecraft:silverfish_calm"],
        ["minecraft:entity", "events", "minecraft:on_calm", "remove", "minecraft:silverfish_angry"],
    ],
    root_filters={
        '8_10_12': format_version_filter_creator(['1.8.0', '1.10.0', '1.12.0']),
        '13_14': format_version_filter_creator(['1.13.0', '1.14.0']),
    },
    path_policies=[
        (['format_version'], Policy.STRICT)
    ]
)
BP_ITEM_MS = MetaSchema(
    meta_schema={
        "10_14_16": {}  # 1.10, 1.14, 1.16
    },
    blacklist=[],
    root_filters={
        '10_14_16': format_version_filter_creator(['1.10', '1.14', '1.16']),
    },
    path_policies=[
        (['format_version'], Policy.STRICT)
    ]
)
BP_ANIMATION_CONTROLLER_MS=MetaSchema(
    meta_schema={
        # 1.10.0
        "10": {
            "animation_controllers": {
                jp.Wildcard.ANY_PARAMETER: "controller"
            }
        },
        "controller": {
            "states": {
                jp.Wildcard.ANY_PARAMETER: "state"
            }
        },
        "state": {
            "transitions": {
                jp.Wildcard.ANY_ITEM: {
                    jp.Wildcard.ANY_PARAMETER: "transition"
                }
            }
        },
        "transition": {}
    },
    blacklist=[
        [
            "animation_controllers", "states", jp.Wildcard.ANY_PARAMETER,
            "transitions", jp.Wildcard.ANY_ITEM, jp.Wildcard.ANY_PARAMETER
        ]
    ],
    root_filters={
        '10': format_version_filter_creator(['1.10.0'])
    },
    path_policies=[
        (['format_version'], Policy.STRICT)
    ]
)
BP_ANIMATION_MS=MetaSchema(
    meta_schema={
        # 1.10.0
        "10": {
            "animations": {
                jp.Wildcard.ANY_PARAMETER: "animation"
            }
        },
        "animation": {
            "timeline": {
                jp.Wildcard.ANY_PARAMETER: "timestamp"
            }
        },
        "timestamp": {
            jp.Wildcard.ANY_ITEM: "command"
        },
        "command": {},
    },
    blacklist=[
        [
            "animations", jp.Wildcard.ANY_PARAMETER, "timeline",
            jp.Wildcard.ANY_PARAMETER, jp.Wildcard.ANY_ITEM
        ]
    ],
    root_filters={
        '10': format_version_filter_creator(['1.10.0'])
    },
    path_policies=[
        (['format_version'], Policy.STRICT)
    ]
)
BP_LOOT_TABLE_MS=MetaSchema(
    meta_schema={
        "root": {
            "pools": {
                jp.Wildcard.ANY_ITEM: "pool"
            }
        },
        "pool": {
            "entries": {
                jp.Wildcard.ANY_ITEM: "entry"
            }
        },
        "entry": {
            "pools": {
                jp.Wildcard.ANY_ITEM: "pool"
            }
        }
    },
    blacklist=[],
    root_filters={
        'root': lambda data: True
    },
    path_policies=[]
)
BP_RECIPE_MS=MetaSchema(
    meta_schema={
        "12_14": {
            "minecraft:recipe_shaped": {
                "key": {
                    jp.Wildcard.ANY_PARAMETER: "key_parameter"
                }
            }
        },
        "key_parameter": {}
    },
    blacklist=[],
    root_filters={
        '12_14': format_version_filter_creator(['1.12', '1.14']),
    },
    path_policies=[
        (['format_version'], Policy.STRICT)
    ]
)
BP_SPAWN_RULE_MS=MetaSchema(
    meta_schema={
        "8_11":{
            "minecraft:spawn_rules": {
                "conditions": {
                    jp.Wildcard.ANY_ITEM: {
                        "minecraft:biome_filter": "filter"
                    }
                }
            }
        },
        "filter": {
            "all_of": {
                jp.Wildcard.ANY_ITEM: "filter"
            },
            "any_of": {
                jp.Wildcard.ANY_ITEM: "filter"
            },
        }
    },
    blacklist=[],
    root_filters={
        '8_11': format_version_filter_creator(['1.8.0', '1.11.0'])
    },
    path_policies=[
        (['format_version'], Policy.STRICT)
    ]
)
BP_TRADING_MS=MetaSchema(
    meta_schema={
        "root": {
            "tiers": {
                jp.Wildcard.ANY_ITEM: {
                    "groups": {
                        jp.Wildcard.ANY_ITEM: {
                            "trades": "trade"
                        }
                    },
                    "trades": "trade"
                }
            }
        },
        "trade": {}
    },
    blacklist=[],
    root_filters={
        'root': lambda data: True
    },
    path_policies=[]
)
RP_ANIMATION_CONTROLLER_MS=MetaSchema(
    meta_schema={
        "10": {
            "animation_controllers": {
                jp.Wildcard.ANY_PARAMETER: "controller"
            }
        },
        "controller": {
            "states": {
                jp.Wildcard.ANY_PARAMETER: "state"
            }
        },
        "state": {
            "transitions": {
                jp.Wildcard.ANY_ITEM: {
                    jp.Wildcard.ANY_PARAMETER: "transition"
                }
            },
            "animations": {
                jp.Wildcard.ANY_ITEM: {
                    jp.Wildcard.ANY_PARAMETER: "animation"
                }
            }
        },
        "transition": {},
        "animation": {}
    },
    blacklist=[
        [
            "animation_controllers", "states", jp.Wildcard.ANY_PARAMETER,
            "transitions", jp.Wildcard.ANY_ITEM, jp.Wildcard.ANY_PARAMETER
        ]
    ],
    root_filters={
        '10': format_version_filter_creator(['1.10.0']),
    },
    path_policies=[
        (['format_version'], Policy.STRICT)
    ]
)
RP_ANIMATION_MS=MetaSchema(
    meta_schema={
        "8": {
            "animations": {
                jp.Wildcard.ANY_PARAMETER: "animation"
            }
        },
        "animation": {
            "bones": {
                jp.Wildcard.ANY_PARAMETER: "bone"
            }
        },
        "bone": {
            "rotation": {
                jp.Wildcard.ANY_PARAMETER: "timestamp"
            },
            "scale": {
                jp.Wildcard.ANY_PARAMETER: "timestamp"
            },
            "position": {
                jp.Wildcard.ANY_PARAMETER: "timestamp"
            }
        },
        "timestamp": {},
    },
    blacklist=[],
    root_filters={
        '8': format_version_filter_creator(['1.8.0']),
    },
    path_policies=[
        (['format_version'], Policy.STRICT)
    ]
)
RP_ATTACHABLE_MS=MetaSchema(
    meta_schema={
        "8_10": {
            "minecraft:attachable": {
                "description": {
                    "materials": {
                        jp.Wildcard.ANY_PARAMETER: "material"
                    },
                    "textures": {
                        jp.Wildcard.ANY_PARAMETER: "texture"
                    },
                    "geometry": {
                        jp.Wildcard.ANY_PARAMETER: {}
                    },
                    "item": {
                        jp.Wildcard.ANY_PARAMETER: "item_item"
                    },
                    "scripts": {
                        jp.Wildcard.ANY_PARAMETER: "script"
                    },
                    "animations": {
                        jp.Wildcard.ANY_PARAMETER: "animation"
                    },
                }
            }
        },
        "material": {},
        "texture": {},
        "geometry_item": {},
        "item_item": {},
        "script": {},
        "animation": {},
    },
    blacklist=[],
    root_filters={
        '8_10': format_version_filter_creator(['1.8.0', '1.10.0', '1.10'])
    },
    path_policies=[
        (['format_version'], Policy.STRICT)
    ]
)
RP_ENTITY_MS=MetaSchema(
    meta_schema={
        # 1.8.0
        "8": {
            "minecraft:client_entity": {
                "description": {
                    "materials": {
                        jp.Wildcard.ANY_PARAMETER: "material"
                    },
                    "textures": {
                        jp.Wildcard.ANY_PARAMETER: "texture"
                    },
                    "geometry": {
                        jp.Wildcard.ANY_PARAMETER: "geometry_item"
                    },
                    "animations": {
                        jp.Wildcard.ANY_PARAMETER: "animation"
                    },
                    "animation_controllers": {
                        jp.Wildcard.ANY_ITEM: {
                            jp.Wildcard.ANY_PARAMETER: "animation_controller"
                        }
                    },
                    "render_controllers": {
                        jp.Wildcard.ANY_ITEM: {
                            jp.Wildcard.ANY_PARAMETER: "render_controller"
                        }
                    }
                },
                "scripts": {
                    "animate": {
                        jp.Wildcard.ANY_ITEM: {
                            jp.Wildcard.ANY_PARAMETER: "condition"
                        }
                    }
                }
            }
        },
        # 1.10.0
        "10": {
            "minecraft:client_entity": {
                "description": {
                    "materials": {
                        jp.Wildcard.ANY_PARAMETER: "material"
                    },
                    "textures": {
                        jp.Wildcard.ANY_PARAMETER: "texture"
                    },
                    "geometry": {
                        jp.Wildcard.ANY_PARAMETER: "geometry_item"
                    },
                    "animations": {
                        jp.Wildcard.ANY_PARAMETER: "animation"
                    },
                    "render_controllers": {
                        jp.Wildcard.ANY_ITEM: {
                            jp.Wildcard.ANY_PARAMETER: "render_controller"
                        }
                    }
                },
                "scripts": {
                    "animate": {
                        jp.Wildcard.ANY_ITEM: {
                            jp.Wildcard.ANY_PARAMETER: "condition"
                        }
                    }
                }
            }
        },
        # Common for all versions
        "material": {},
        "texture": {},
        "geometry_item": {},
        "animation": {},
        "animation_controller": {},
        "render_controller": {},
        "condition": {},
    },
    blacklist=[],
    root_filters={
        '8': format_version_filter_creator(['1.8.0']),
        '10': format_version_filter_creator(['1.10.0']),
    },
    path_policies=[
        (['format_version'], Policy.STRICT)
    ]
)
RP_PARTICLE_MS=MetaSchema(
    meta_schema={
        # 1.10.0
        "10": {
            "particle_effect": {
                "events": {
                    jp.Wildcard.ANY_PARAMETER: "event"
                },
                "components": {
                    "minecraft:particle_lifetime_events": {
                        "timeline": {
                            jp.Wildcard.ANY_PARAMETER: "timestamp"
                        }
                    }
                }
            }
        },
        "event": {},
        "timestamp": {},
    },
    blacklist=[
        [
            "particle_effect", "components", "minecraft:particle_lifetime_expression",
            "activation_expression"
        ]
    ],
    root_filters={
        '10': format_version_filter_creator(['1.10.0']),
    },
    path_policies=[
        (['format_version'], Policy.STRICT)
    ]
)
RP_RENDER_CONTROLLER_MS=MetaSchema(
    meta_schema={
        "8_10": {
            "render_controllers": {
                jp.Wildcard.ANY_PARAMETER: "render_controller"
            }
        },
        "render_controller": {
            "arrays": {
                "materials": {
                    jp.Wildcard.ANY_PARAMETER: "array_material"
                },
                "textures": {
                    jp.Wildcard.ANY_PARAMETER: "array_texture"
                },
                "geometries": {
                    jp.Wildcard.ANY_PARAMETER: "array_geometry"
                },
            },
            "part_visibility": {
                jp.Wildcard.ANY_PARAMETER: "part_visibility_item"
            },
        },
        "array_material": {},
        "array_texture": {},
        "array_geometry": {},
        "part_visibility_item": {}
    },
    blacklist=[],
    root_filters={
        '8_10': format_version_filter_creator(['1.8.0', '1.10.0', '1.10']),
    },
    path_policies=[
        (['format_version'], Policy.STRICT)
    ]
)
RP_MODEL_MS=MetaSchema(
    meta_schema={
        # 1.8.0 and 1.10.0
        "8_10": {
            "format_version": "format_version_8_10",
            jp.Wildcard.ANY_PARAMETER: "entity_8_10"
        },
        "format_version_8_10": {},
        "entity_8_10": {
            "bones": {
                jp.Wildcard.ANY_ITEM: {
                    "locators": {
                        jp.Wildcard.ANY_PARAMETER: "locator_8_10"
                    }
                }
            }
        },
        "locator_8_10": {},
        # 1.12.0
        "12": {
            "minecraft:geometry": {
                jp.Wildcard.ANY_ITEM: "entity_12"
            }
        },
        "entity_12": {
            "bones": {
                jp.Wildcard.ANY_ITEM: {
                    "locators": {
                        jp.Wildcard.ANY_PARAMETER: "locator_12"
                    }
                }
            }
        },
        "locator_12": {}
    },
    blacklist=[],
    root_filters={
        '8_10': format_version_filter_creator(['1.8.0', '1.10.0']),
        '12': format_version_filter_creator(['1.12.0']),
    },
    path_policies=[
        (['format_version'], Policy.STRICT)
    ]
)