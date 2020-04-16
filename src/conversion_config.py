import json_paths as jp

BEHAVIOR_CONFIG = {
    "description": [
        ["minecraft:entity", "description"]
    ],
    "component_group": [
        ["minecraft:entity", "components"],
        ["minecraft:entity", "component_groups", jp.Wildcard.ANY_PARAMETER],
    ],
    "event": [
        ["minecraft:entity", "events", jp.Wildcard.ANY_PARAMETER]
    ],
    # "filter": [
    #     ['minecraft:entity', 'events', jp.Wildcard.ANY_PARAMETER, 'sequence', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'component_groups', jp.Wildcard.ANY_PARAMETER, 'minecraft:behavior.go_home', 'on_home', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:behavior.avoid_mob_type', 'entity_types', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:behavior.hurt_by_target', 'entity_types', 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:on_target_escape', 'filters'],
    #     ['minecraft:entity', 'events', jp.Wildcard.ANY_PARAMETER, 'randomize', jp.Wildcard.ANY_ITEM, 'randomize', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:scheduler', 'scheduled_events', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:interact', 'interactions', 'on_interact', 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:behavior.share_items', 'entity_types', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:hurt_on_condition', 'damage_conditions', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:healable', 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:interact', 'interactions', jp.Wildcard.ANY_ITEM, 'on_interact', 'filters'],
    #     ['minecraft:entity', 'component_groups', jp.Wildcard.ANY_PARAMETER, 'minecraft:environment_sensor', 'triggers', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'component_groups', jp.Wildcard.ANY_PARAMETER, 'minecraft:rail_sensor', 'on_activate', 'filters'],
    #     ['minecraft:entity', 'component_groups', jp.Wildcard.ANY_PARAMETER, 'minecraft:behavior.hurt_by_target', 'entity_types', 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:behavior.send_event', 'event_choices', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:environment_sensor', 'triggers', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'component_groups', jp.Wildcard.ANY_PARAMETER, 'minecraft:spawn_entity', 'filters'],
    #     ['minecraft:entity', 'component_groups', jp.Wildcard.ANY_PARAMETER, 'minecraft:environment_sensor', 'triggers', 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:behavior.look_at_entity', 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:behavior.nearest_attackable_target', 'entity_types', 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:behavior.drink_potion', 'potions', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:lookat', 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:despawn', 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:damage_sensor', 'triggers', 'on_damage', 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:behavior.follow_caravan', 'entity_types', 'filters'],
    #     ['minecraft:entity', 'events', jp.Wildcard.ANY_PARAMETER, 'sequence', jp.Wildcard.ANY_ITEM, 'sequence', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'component_groups', jp.Wildcard.ANY_PARAMETER, 'minecraft:interact', 'interactions', jp.Wildcard.ANY_ITEM, 'on_interact', 'filters'],
    #     ['minecraft:entity', 'component_groups', jp.Wildcard.ANY_PARAMETER, 'minecraft:behavior.avoid_mob_type', 'entity_types', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:on_target_acquired', 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:behavior.target_when_pushed', 'entity_types', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:behavior.nearest_attackable_target', 'entity_types', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'component_groups', jp.Wildcard.ANY_PARAMETER, 'minecraft:behavior.nearest_prioritized_attackable_target', 'entity_types', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:damage_sensor', 'triggers', jp.Wildcard.ANY_ITEM, 'on_damage', 'filters'],
    #     ['minecraft:entity', 'events', jp.Wildcard.ANY_PARAMETER, 'filters'],
    #     ['minecraft:entity', 'component_groups', jp.Wildcard.ANY_PARAMETER, 'minecraft:behavior.look_at_entity', 'filters'],
    #     ['minecraft:entity', 'component_groups', jp.Wildcard.ANY_PARAMETER, 'minecraft:behavior.drop_item_for', 'entity_types', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'component_groups', jp.Wildcard.ANY_PARAMETER, 'minecraft:damage_sensor', 'triggers', 'on_damage', 'filters'],
    #     ['minecraft:entity', 'components', 'minecraft:environment_sensor', 'triggers', 'filters'],
    #     ['minecraft:entity', 'component_groups', jp.Wildcard.ANY_PARAMETER, 'minecraft:behavior.sneeze', 'entity_types', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'component_groups', jp.Wildcard.ANY_PARAMETER, 'minecraft:scheduler', 'scheduled_events', jp.Wildcard.ANY_ITEM, 'filters'],
    #     ['minecraft:entity', 'component_groups', jp.Wildcard.ANY_PARAMETER, 'minecraft:behavior.nearest_attackable_target', 'entity_types', jp.Wildcard.ANY_ITEM, 'filters']
    # ]
}

BEHAVIOR_BLACKLIST = [
    ["minecraft:entity", "minecraft:physics"],
    ["minecraft:entity", "minecraft:pushable"]
]