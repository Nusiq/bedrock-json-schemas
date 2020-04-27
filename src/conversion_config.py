import json_paths as jp
from schema_builder import MetaSchema
import typing as tp


class ExportConfig(tp.NamedTuple):
    export_path: str
    pattern: str
    # List of functions that take the JSON file as the input and must return
    # and check its content. If everything is fine they return True
    assertions: tp.List[tp.Callable[[tp.Dict], bool]]


# EXPORT CONFIG
BP_ENTITY_CFG=ExportConfig(
    export_path='../schemas/bp.entity.schema.json',
    pattern='entities/**.json',
    assertions=[
        lambda d: d['format_version'] in ['1.14.0', '1.13.0']
    ]
)
BP_ITEM_CFG=ExportConfig(
    export_path='../schemas/bp.item.schema.json',
    pattern='items/**.json',
    assertions=[
        lambda d: d['format_version'] in ['1.10']
    ]
)
BP_ANIMATION_CONTROLLER_CFG=ExportConfig(
    export_path='../schemas/bp.animation_controller.schema.json',
    pattern='animation_controllers/**.json',
    assertions=[
        lambda d: d['format_version'] in ['1.10.0']
    ]
)
BP_ANIMATION_CFG=ExportConfig(
    export_path='../schemas/bp.animation.schema.json',
    pattern='animations/**.json',
    assertions=[
        lambda d: d['format_version'] in ['1.10.0']
    ]
)
BP_LOOT_TABLE_CFG=ExportConfig(
    export_path='../schemas/bp.loot_table.schema.json',
    pattern='loot_tables/**.json',
    assertions=[]  # No rules
)
BP_RECIPE_CFG=ExportConfig(
    export_path='../schemas/bp.recipe.schema.json',
    pattern='recipes/**.json',
    assertions=[
        lambda d: d['format_version'] in ['1.12', '1.13', '1.14']
    ]
)
BP_SPAWN_RULE_CFG=ExportConfig(
    export_path='../schemas/bp.spawn_rules.schema.json',
    pattern='spawn_rules/**.json',
    assertions=[
        lambda d: d['format_version'] in ['1.8.0']
    ]
)
BP_TRADING_CFG=ExportConfig(
    export_path='../schemas/bp.trading.schema.json',
    pattern='trading/**.json',
    assertions=[]  # No rules
)


RP_ANIMATION_CONTROLLER_CFG=ExportConfig(
    export_path='../schemas/rp.animation_controller.schema.json',
    pattern='animation_controllers/**.json',
    assertions=[
        lambda d: d['format_version'] in ['1.10.0']
    ]
)
RP_ANIMATION_CFG=ExportConfig(
    export_path='../schemas/rp.animation.schema.json',
    pattern='animations/**.json',
    assertions=[
         lambda d: d['format_version'] in ['1.8.0']
    ]
)
RP_ATTACHABLE_CFG=ExportConfig(
    export_path='../schemas/rp.attachable.schema.json',
    pattern='attachables/**.json',
    assertions=[
        lambda d: d['format_version'] in ['1.10.0']
    ]
)
RP_ENTITY_CFG=ExportConfig(
    export_path='../schemas/rp.entity.schema.json',
    pattern='entity/**.json',
    assertions=[
        lambda d: d['format_version'] in ['1.10.0']
    ]
)
RP_PARTICLE_CFG=ExportConfig(
    export_path='../schemas/rp.particle.schema.json',
    pattern='particles/**.json',
    assertions=[
        lambda d: d['format_version'] in ['1.10.0']
    ]
)
RP_RENDER_CONTROLLER_CFG=ExportConfig(
    export_path='../schemas/rp.render_controller.schema.json',
    pattern='render_controllers/**.json',
    assertions=[
        lambda d: d['format_version'] in ['1.10.0', '1.10', '1.8.0']
    ]
)


# META SCHEMAS
BP_ENTITY_MS = MetaSchema(
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
        "description": {
            "animations": {
                jp.Wildcard.ANY_PARAMETER: "description_animation"
            }
        },
        "description_animation": {}
    },
    blacklist=[
        ["minecraft:entity", "minecraft:physics"],
        ["minecraft:entity", "minecraft:pushable"]
    ]
)
BP_ITEM_MS = MetaSchema(meta_schema={"root": {}}, blacklist=[])
BP_ANIMATION_CONTROLLER_MS=MetaSchema(
    meta_schema={
        "root": {
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
    ]
)
BP_ANIMATION_MS=MetaSchema(
    meta_schema={
        "root": {
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
    blacklist=[]
)
BP_RECIPE_MS=MetaSchema(
    meta_schema={
        "root": {
            "minecraft:recipe_shaped": {
                "key": {
                    jp.Wildcard.ANY_PARAMETER: "key_parameter"
                }
            }
        },
        "key_parameter": {}
    },
    blacklist=[]
)
BP_SPAWN_RULE_MS=MetaSchema(
    meta_schema={
        "root":{
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
    blacklist=[]
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
    blacklist=[]
)
RP_ANIMATION_CONTROLLER_MS=MetaSchema(
    meta_schema={
        "root": {
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
    ]
)
RP_ANIMATION_MS=MetaSchema(
    meta_schema={
        "root": {
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
    blacklist=[]
)
RP_ATTACHABLE_MS=MetaSchema(
    meta_schema={
        "root": {
            "minecraft:attachable": {
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
                    "item": {
                        jp.Wildcard.ANY_PARAMETER: "item_item"
                    },
                    "scripts": {
                        jp.Wildcard.ANY_PARAMETER: "script"
                    },
                }
            }
        },
        "material": {},
        "texture": {},
        "geometry_item": {},
        "item_item": {},
        "script": {},
    },
    blacklist=[]
)
RP_ENTITY_MS=MetaSchema(
    meta_schema={
        "root": {
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
        "material": {},
        "texture": {},
        "geometry_item": {},
        "animation": {},
        "condition": {},
        "render_controller": {}
    },
    blacklist=[]
)
RP_PARTICLE_MS=MetaSchema(
    meta_schema={
        "root": {
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
        "timestamp": {}
    },
    blacklist=[]
)
RP_RENDER_CONTROLLER_MS=MetaSchema(
    meta_schema={
        "root": {
            "render_controllers": {
                jp.Wildcard.ANY_PARAMETER: {
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
                }
            }
        },
        "array_material": {},
        "array_texture": {},
        "array_geometry": {},
        "part_visibility_item": {}
    },
    blacklist=[]
)
