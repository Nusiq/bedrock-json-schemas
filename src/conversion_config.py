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

BEHAVIOR_CONTROLLER_CONFIG=MetaSchema(
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

BEHAVIOR_ANIMATION_CONFIG=MetaSchema(
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

BEHAVIOR_LOOT_TABLE=MetaSchema(
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

BEHAVIOR_RECIPE=MetaSchema(
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

BEHAVIOR_SPAWN_RULE=MetaSchema(
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

BEHAVIOR_TRADING=MetaSchema(
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

RESOURCE_CONTROLLER_CONFIG=MetaSchema(
    meta_schema={
        "root": {
            "animation_controllers": {
                "states": {
                    jp.Wildcard.ANY_PARAMETER: "state"
                }
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

RESOURCE_ENTITY_CONFIG=MetaSchema(
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
        "condition": {}
    },
    blacklist=[]
)

RESOURCE_PARTICLE_CONFIG=MetaSchema(
    meta_schema={
        "root": {}
    },
    blacklist=[]
)

RESOURCE_RENDER_CONTROLLER_CONFIG=MetaSchema(
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