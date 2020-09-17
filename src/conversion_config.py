import json_paths as jp
from schema_builder import MetaSchema, Policy, MetaSchemaReference
import typing as tp

Msr = MetaSchemaReference


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
            "format_version": Msr(None, Policy.STRICT),
            "minecraft:entity": {
                "description": Msr("description"),
                "components": Msr("component_group_8_10_12"),
                "component_groups": {
                    jp.Wildcard.ANY_PARAMETER: Msr("component_group_8_10_12"),
                },
                "events": {
                    jp.Wildcard.ANY_PARAMETER: Msr("event"),
                },
            },
        },
        "component_group_8_10_12": {
            jp.Wildcard.ANYTHING_UNTIL_NEXT_MATCH: {
                "filters": Msr("filter", Policy.STRICT),
            },
        },
        # 1.13.0 and 1.14.0
        "13_14": {
            "format_version": Msr(None, Policy.STRICT),
            "minecraft:entity": {
                "description": Msr("description"),
                "components": Msr("component_group_13_14"),
                "component_groups": {
                    jp.Wildcard.ANY_PARAMETER: Msr("component_group_13_14"),
                },
                "events": {
                    jp.Wildcard.ANY_PARAMETER: Msr("event"),
                },
            },
        },
        "component_group_13_14": {
            jp.Wildcard.ANYTHING_UNTIL_NEXT_MATCH: {
                "filters": Msr("filter", Policy.STRICT),
            },
        },
        # Common for all version
        "event": {
            "sequence": {
                jp.Wildcard.ANY_ITEM: Msr("event")
            },
            "randomize": {
                jp.Wildcard.ANY_ITEM: Msr("event")
            },
            jp.Wildcard.ANYTHING_UNTIL_NEXT_MATCH: {
                "filters": Msr("filter", Policy.STRICT)
            }
        },
        "filter": {
            "all_of": {
                jp.Wildcard.ANY_ITEM: Msr("filter", Policy.STRICT)
            },
            "any_of": {
                jp.Wildcard.ANY_ITEM: Msr("filter", Policy.STRICT)
            },
            "test": Msr(None, Policy.STRICT),
            "operator": Msr(None, Policy.STRICT),
            "subject": Msr(None, Policy.STRICT),
            "domain": Msr(None, Policy.EXAMPLE)
        },
        "description": {
            "animations": {
                jp.Wildcard.ANY_PARAMETER: Msr("description_config")
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
    }
)
BP_ITEM_MS = MetaSchema(
    meta_schema={
        "10_14_16": {
            "format_version": Msr(None, Policy.STRICT)
        }
    },
    blacklist=[],
    root_filters={
        '10_14_16': format_version_filter_creator(['1.10', '1.14', '1.16']),
    }
)
BP_ANIMATION_CONTROLLER_MS=MetaSchema(
    meta_schema={
        # 1.10.0
        "10": {
            "format_version": Msr(None, Policy.STRICT),
            "animation_controllers": {
                jp.Wildcard.ANY_PARAMETER: Msr("controller")
            }
        },
        "controller": {
            "states": {
                jp.Wildcard.ANY_PARAMETER: Msr("state")
            }
        },
        "state": {
            "transitions": {
                jp.Wildcard.ANY_ITEM: {
                    jp.Wildcard.ANY_PARAMETER: Msr("transition")
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
    }
)
BP_ANIMATION_MS=MetaSchema(
    meta_schema={
        # 1.10.0
        "10": {
            "format_version": Msr(None, Policy.STRICT),
            "animations": {
                jp.Wildcard.ANY_PARAMETER: Msr("animation")
            }
        },
        "animation": {
            "timeline": {
                jp.Wildcard.ANY_PARAMETER: Msr("timestamp")
            }
        },
        "timestamp": {
            jp.Wildcard.ANY_ITEM: Msr("command")
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
    }
)
BP_LOOT_TABLE_MS=MetaSchema(
    meta_schema={
        "root": {
            "pools": {
                jp.Wildcard.ANY_ITEM: Msr("pool")
            }
        },
        "pool": {
            "entries": {
                jp.Wildcard.ANY_ITEM: Msr("entry")
            }
        },
        "entry": {
            "pools": {
                jp.Wildcard.ANY_ITEM: Msr("pool")
            }
        }
    },
    blacklist=[],
    root_filters={
        'root': lambda data: True
    }
)
BP_RECIPE_MS=MetaSchema(
    meta_schema={
        "12_14": {
            "format_version": Msr(None, Policy.STRICT),
            "minecraft:recipe_shaped": {
                "key": {
                    jp.Wildcard.ANY_PARAMETER: Msr("key_parameter")
                }
            }
        },
        "key_parameter": {}
    },
    blacklist=[],
    root_filters={
        '12_14': format_version_filter_creator(['1.12', '1.14']),
    }
)
BP_SPAWN_RULE_MS=MetaSchema(
    meta_schema={
        "8_11":{
            "format_version": Msr(None, Policy.STRICT),
            "minecraft:spawn_rules": {
                "conditions": {
                    jp.Wildcard.ANY_ITEM: {
                        "minecraft:biome_filter": Msr("filter", Policy.STRICT)
                    }
                }
            }
        },
        "filter": {
            "all_of": {
                jp.Wildcard.ANY_ITEM: Msr("filter", Policy.STRICT)
            },
            "any_of": {
                jp.Wildcard.ANY_ITEM: Msr("filter", Policy.STRICT)
            }
        }
    },
    blacklist=[],
    root_filters={
        '8_11': format_version_filter_creator(['1.8.0', '1.11.0'])
    }
)
BP_TRADING_MS=MetaSchema(
    meta_schema={
        "root": {
            "tiers": {
                jp.Wildcard.ANY_ITEM: {
                    "groups": {
                        jp.Wildcard.ANY_ITEM: {
                            "trades": Msr("trade")
                        }
                    },
                    "trades": Msr("trade")
                }
            }
        },
        "trade": {}
    },
    blacklist=[],
    root_filters={
        'root': lambda data: True
    }
)
RP_ANIMATION_CONTROLLER_MS=MetaSchema(
    meta_schema={
        "10": {
            "format_version": Msr(None, Policy.STRICT),
            "animation_controllers": {
                jp.Wildcard.ANY_PARAMETER: Msr("controller")
            }
        },
        "controller": {
            "states": {
                jp.Wildcard.ANY_PARAMETER: Msr("state")
            }
        },
        "state": {
            "transitions": {
                jp.Wildcard.ANY_ITEM: {
                    jp.Wildcard.ANY_PARAMETER: Msr("transition")
                }
            },
            "animations": {
                jp.Wildcard.ANY_ITEM: {
                    jp.Wildcard.ANY_PARAMETER: Msr("animation")
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
    }
)
RP_ANIMATION_MS=MetaSchema(
    meta_schema={
        "8": {
            "format_version": Msr(None, Policy.STRICT),
            "animations": {
                jp.Wildcard.ANY_PARAMETER: Msr("animation")
            }
        },
        "animation": {
            "bones": {
                jp.Wildcard.ANY_PARAMETER: Msr("bone")
            }
        },
        "bone": {
            "rotation": {
                jp.Wildcard.ANY_PARAMETER: Msr("timestamp")
            },
            "scale": {
                jp.Wildcard.ANY_PARAMETER: Msr("timestamp")
            },
            "position": {
                jp.Wildcard.ANY_PARAMETER: Msr("timestamp")
            }
        },
        "timestamp": {},
    },
    blacklist=[],
    root_filters={
        '8': format_version_filter_creator(['1.8.0']),
    }
)
RP_ATTACHABLE_MS=MetaSchema(
    meta_schema={
        "8_10": {
            "format_version": Msr(None, Policy.STRICT),
            "minecraft:attachable": {
                "description": {
                    "materials": {
                        jp.Wildcard.ANY_PARAMETER: Msr("material")
                    },
                    "textures": {
                        jp.Wildcard.ANY_PARAMETER: Msr("texture")
                    },
                    "geometry": {
                        jp.Wildcard.ANY_PARAMETER: {}
                    },
                    "item": {
                        jp.Wildcard.ANY_PARAMETER: Msr("item_item")
                    },
                    "scripts": {
                        jp.Wildcard.ANY_PARAMETER: Msr("script")
                    },
                    "animations": {
                        jp.Wildcard.ANY_PARAMETER: Msr("animation")
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
    }
)
RP_ENTITY_MS=MetaSchema(
    meta_schema={
        # 1.8.0
        "8": {
            "format_version": Msr(None, Policy.STRICT),
            "minecraft:client_entity": {
                "description": {
                    "materials": {
                        jp.Wildcard.ANY_PARAMETER: Msr("material")
                    },
                    "textures": {
                        jp.Wildcard.ANY_PARAMETER: Msr("texture")
                    },
                    "geometry": {
                        jp.Wildcard.ANY_PARAMETER: Msr("geometry_item")
                    },
                    "animations": {
                        jp.Wildcard.ANY_PARAMETER: Msr("animation")
                    },
                    "animation_controllers": {
                        jp.Wildcard.ANY_ITEM: {
                            jp.Wildcard.ANY_PARAMETER: Msr("animation_controller")
                        }
                    },
                    "render_controllers": {
                        jp.Wildcard.ANY_ITEM: {
                            jp.Wildcard.ANY_PARAMETER: Msr("render_controller")
                        }
                    }
                },
                "scripts": {
                    "animate": {
                        jp.Wildcard.ANY_ITEM: {
                            jp.Wildcard.ANY_PARAMETER: Msr("condition")
                        }
                    }
                }
            }
        },
        # 1.10.0
        "10": {
            "format_version": Msr(None, Policy.STRICT),
            "minecraft:client_entity": {
                "description": {
                    "materials": {
                        jp.Wildcard.ANY_PARAMETER: Msr("material")
                    },
                    "textures": {
                        jp.Wildcard.ANY_PARAMETER: Msr("texture")
                    },
                    "geometry": {
                        jp.Wildcard.ANY_PARAMETER: Msr("geometry_item")
                    },
                    "animations": {
                        jp.Wildcard.ANY_PARAMETER: Msr("animation")
                    },
                    "render_controllers": {
                        jp.Wildcard.ANY_ITEM: {
                            jp.Wildcard.ANY_PARAMETER: Msr("render_controller")
                        }
                    }
                },
                "scripts": {
                    "animate": {
                        jp.Wildcard.ANY_ITEM: {
                            jp.Wildcard.ANY_PARAMETER: Msr("condition")
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
    }
)
RP_PARTICLE_MS=MetaSchema(
    meta_schema={
        # 1.10.0
        "10": {
            "format_version": Msr(None, Policy.STRICT),
            "particle_effect": {
                "events": {
                    jp.Wildcard.ANY_PARAMETER: Msr("event")
                },
                "components": {
                    "minecraft:particle_lifetime_events": {
                        "timeline": {
                            jp.Wildcard.ANY_PARAMETER: Msr("timestamp")
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
    }
)
RP_RENDER_CONTROLLER_MS=MetaSchema(
    meta_schema={
        "8_10": {
            "format_version": Msr(None, Policy.STRICT),
            "render_controllers": {
                jp.Wildcard.ANY_PARAMETER: Msr("render_controller")
            }
        },
        "render_controller": {
            "arrays": {
                "materials": {
                    jp.Wildcard.ANY_PARAMETER: Msr("array_material")
                },
                "textures": {
                    jp.Wildcard.ANY_PARAMETER: Msr("array_texture")
                },
                "geometries": {
                    jp.Wildcard.ANY_PARAMETER: Msr("array_geometry")
                },
            },
            "part_visibility": {
                jp.Wildcard.ANY_PARAMETER: Msr("part_visibility_item")
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
    }
)
RP_MODEL_MS=MetaSchema(
    meta_schema={
        # 1.8.0 and 1.10.0
        "8_10": {
            "format_version": Msr(None, Policy.STRICT),
            "format_version": Msr("format_version_8_10"),
            jp.Wildcard.ANY_PARAMETER: Msr("entity_8_10")
        },
        "format_version_8_10": {},
        "entity_8_10": {
            "bones": {
                jp.Wildcard.ANY_ITEM: {
                    "locators": {
                        jp.Wildcard.ANY_PARAMETER: Msr("locator_8_10")
                    }
                }
            }
        },
        "locator_8_10": {},
        # 1.12.0
        "12": {
            "format_version": Msr(None, Policy.STRICT),
            "minecraft:geometry": {
                jp.Wildcard.ANY_ITEM: Msr("entity_12")
            }
        },
        "entity_12": {
            "bones": {
                jp.Wildcard.ANY_ITEM: {
                    "locators": {
                        jp.Wildcard.ANY_PARAMETER: Msr("locator_12")
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
    }
)