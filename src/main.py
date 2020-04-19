import os
from zipfile import ZipFile

BP_PATH = '../packs/behavior-packs'
RP_PATH = '../packs/resource-packs'
import typing as tp
import shutil
import fnmatch
import json
import json_paths as jp
from schema_builder import create_schema_definitions

from conversion_config import (
    BEHAVIOR_CONFIG,
    BEHAVIOR_CONTROLLER_CONFIG,
    BEHAVIOR_ANIMATION_CONFIG,
    BEHAVIOR_LOOT_TABLE,
    BEHAVIOR_RECIPE,
    BEHAVIOR_SPAWN_RULE,
    BEHAVIOR_TRADING,
    RESOURCE_CONTROLLER_CONFIG,
    RESOURCE_ENTITY_CONFIG,
    RESOURCE_PARTICLE_CONFIG,
    RESOURCE_RENDER_CONTROLLER_CONFIG,
)


def jsonc_read(f: tp.IO[tp.Any]) -> tp.Any:
    '''
    Reads json with comments
    '''
    lines_list: tp.List[str] = []
    for line in f.readlines():
        line = line.strip('\n').split('//')[0]
        lines_list.append(line)
    try:
        return json.loads('\n'.join(lines_list))
    except json.decoder.JSONDecodeError as e:
        print(f'ERROR: UNABLE TO READ FILE (returning placeholder result)')
        return {}


def create_bp_schemas_from_examples(
    bp_path: str,
    behavior_schema: tp.Dict,
    controller_schema: tp.Dict,
    animation_schema: tp.Dict,
    loot_table_schema: tp.Dict,
    recipies_schema: tp.Dict,
    spawn_rules_schema: tp.Dict,
    trading_schema: tp.Dict,
    tmp_path: str='./.tmp'
):
    '''
    Tries to create behaviorpack schemas based on examples from behavior-pack.
    Uses tmp_path to create temporary files.

    - bp_path - a path to a behavior-pack (the pack can be in a zip file)

    Returns a dictionary with schemas.
    '''
    tmp_created = False  # True if temporary files were created

    # Try to read the ZIP file
    if os.path.isfile:
        with ZipFile(bp_path, 'r') as zipf:
            is_valid = zipf.testzip() is None
            if not is_valid:
                raise ValueError('Input file is not a ziped behavior-pack')
            zipf.extractall(tmp_path)
            bp_path = tmp_path
            tmp_created = True
    # Read the data from bp_path
    try:
        for root, dirs, files in os.walk(bp_path):
            for file in files:
                fp = os.path.join(root, file)
                behavior_pattern = os.path.join(bp_path, 'entities/**.json')
                controller_pattern = os.path.join(bp_path, 'animation_controllers/**.json')
                animation_pattern = os.path.join(bp_path, 'animations/**.json')
                loot_table_pattern = os.path.join(bp_path, 'loot_tables/**.json')
                recipies_pattern = os.path.join(bp_path, 'recipes/**.json')
                spawn_rules_pattern = os.path.join(bp_path, 'spawn_rules/**.json')
                trading_pattern = os.path.join(bp_path, 'trading/**.json')
                if fnmatch.fnmatch(fp, behavior_pattern):
                    with open(fp, 'r') as f:
                        entity_dict = jsonc_read(f)
                    format_version = entity_dict['format_version']
                    if format_version not in ['1.14.0', '1.13.0']:
                        print(f'Skipped file {file} - reason format_version=={format_version}')
                        continue
                    create_schema_definitions(
                        source=entity_dict, target=behavior_schema,
                        meta_schema=BEHAVIOR_CONFIG
                    )
                elif fnmatch.fnmatch(fp, controller_pattern):
                    with open(fp, 'r') as f:
                        entity_dict = jsonc_read(f)
                    format_version = entity_dict['format_version']
                    if format_version not in ['1.10.0']:
                        print(f'Skipped file {file} - reason format_version=={format_version}')
                        continue
                    create_schema_definitions(
                        source=entity_dict, target=controller_schema,
                        meta_schema=BEHAVIOR_CONTROLLER_CONFIG
                    )
                elif fnmatch.fnmatch(fp, animation_pattern):
                    with open(fp, 'r') as f:
                        entity_dict = jsonc_read(f)
                    format_version = entity_dict['format_version']
                    if format_version not in ['1.10.0']:
                        print(f'Skipped file {file} - reason format_version=={format_version}')
                        continue
                    create_schema_definitions(
                        source=entity_dict, target=animation_schema,
                        meta_schema=BEHAVIOR_ANIMATION_CONFIG
                    )
                elif fnmatch.fnmatch(fp, loot_table_pattern):
                    with open(fp, 'r') as f:
                        entity_dict = jsonc_read(f)
                    # THERE IS NO VERSIONING FOR LOOT TABLES
                    create_schema_definitions(
                        source=entity_dict, target=loot_table_schema,
                        meta_schema=BEHAVIOR_LOOT_TABLE
                    )
                elif fnmatch.fnmatch(fp, recipies_pattern):
                    with open(fp, 'r') as f:
                        entity_dict = jsonc_read(f)
                    try:
                        format_version = entity_dict['format_version']
                    except KeyError as e:
                        print(f'ERROR: Unable to read format version of recipe {fp}')
                        continue
                    if format_version not in ['1.12']:
                        print(f'Skipped file {file} - reason format_version=={format_version}')
                        continue
                    create_schema_definitions(
                        source=entity_dict, target=recipies_schema,
                        meta_schema=BEHAVIOR_RECIPE
                    )
                elif fnmatch.fnmatch(fp, spawn_rules_pattern):
                    with open(fp, 'r') as f:
                        entity_dict = jsonc_read(f)
                    format_version = entity_dict['format_version']
                    if format_version not in ['1.8.0']:
                        print(f'Skipped file {file} - reason format_version=={format_version}')
                        continue
                    create_schema_definitions(
                        source=entity_dict, target=spawn_rules_schema,
                        meta_schema=BEHAVIOR_SPAWN_RULE
                    )
                elif fnmatch.fnmatch(fp, trading_pattern):
                    with open(fp, 'r') as f:
                        entity_dict = jsonc_read(f)
                    # THERE IS NO VERSIONING FOR TRADING
                    create_schema_definitions(
                        source=entity_dict, target=trading_schema,
                        meta_schema=BEHAVIOR_TRADING
                    )



    finally:  # Remove temporary files if something went wrong
        if tmp_created:
            shutil.rmtree(tmp_path)


def get_schema_dict() -> tp.Dict:
    return {"$ref": "#/definitions/root"}

if __name__ == "__main__":
    # GENERATE SCHEMAS FOR BEHAVIORPACK
    behavior_schema: tp.Dict = get_schema_dict()
    controller_schema: tp.Dict = get_schema_dict()
    animation_schema: tp.Dict = get_schema_dict()
    loot_table_schema: tp.Dict = get_schema_dict()
    recipies_schema: tp.Dict = get_schema_dict()
    spawn_rules_schema: tp.Dict = get_schema_dict()
    trading_schema: tp.Dict = get_schema_dict()
    
    for dir_ in os.listdir(BP_PATH):
        create_bp_schemas_from_examples(
            os.path.join(BP_PATH, dir_),
            behavior_schema,
            controller_schema,
            animation_schema,
            loot_table_schema,
            recipies_schema,
            spawn_rules_schema,
            trading_schema
        )
    with open('../results/behavior_schema.json', 'w') as f:
        json.dump(behavior_schema, f, indent='\t')
    with open('../results/controller_schema.json', 'w') as f:
        json.dump(controller_schema, f, indent='\t')
    with open('../results/animation_schema.json', 'w') as f:
        json.dump(animation_schema, f, indent='\t')
    with open('../results/loot_table_schema.json', 'w') as f:
        json.dump(loot_table_schema, f, indent='\t')
    with open('../results/recipies_schema.json', 'w') as f:
        json.dump(recipies_schema, f, indent='\t')
    with open('../results/spawn_rules_schema.json', 'w') as f:
        json.dump(spawn_rules_schema, f, indent='\t')
    with open('../results/trading_schema.json', 'w') as f:
        json.dump(trading_schema, f, indent='\t')

    # GENERATE SCHEMAS FOR RESOURCEPACK
    # TODO - implement