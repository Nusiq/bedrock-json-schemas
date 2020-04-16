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

def jsonc_read(f: tp.IO[tp.Any]) -> tp.Any:
    '''
    Reads json with comments
    '''
    lines_list: tp.List[str] = []
    for line in f.readlines():
        line = line.strip('\n').split('//')[0]
        lines_list.append(line)
    return json.loads('\n'.join(lines_list))


def create_behavior_schema_definitions(fp: str, definitions: tp.Dict):
    with open(fp, 'r') as f:
        entity_dict = jsonc_read(f)
    # for obj, path in jp.walk(entity_dict):
    #     print(f'{str(type(obj)):20} {path}')
    create_schema_definitions(
        source=entity_dict, target=definitions,
        define_objects={
            "description": [
                ["minecraft:entity", "description"]
            ],
            "component_group": [
                ["minecraft:entity", "components"],
                ["minecraft:entity", "component_groups", jp.Wildcard.ANY_PARAMETER],
            ],
            "event": [
                ["minecraft:entity", "events", jp.Wildcard.ANY_PARAMETER]
            ]
        }
    )


def create_bp_schemas_from_examples(
    bp_path: str, output: tp.Dict, tmp_path: str='./.tmp'
) -> tp.Dict:
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
                if fnmatch.fnmatch(fp, behavior_pattern):
                    create_behavior_schema_definitions(fp, output)
        return output
    finally:  # Remove temporary files if something went wrong
        if tmp_created:
            shutil.rmtree(tmp_path)


if __name__ == "__main__":
    target_dict: tp.Dict = {}
    for dir_ in os.listdir(BP_PATH):
        result = create_bp_schemas_from_examples(
            os.path.join(BP_PATH, dir_),
            output=target_dict
        )
    with open('../result/result.json', 'w') as f:
        json.dump(result, f, indent='\t')
