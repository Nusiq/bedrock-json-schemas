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
    MetaSchema, ExportConfig,

    # Behaviorpack
    BP_ENTITY_MS, BP_ENTITY_CFG,
    BP_ITEM_MS, BP_ITEM_CFG,
    BP_ANIMATION_CONTROLLER_MS, BP_ANIMATION_CONTROLLER_CFG,
    BP_ANIMATION_MS, BP_ANIMATION_CFG,
    BP_LOOT_TABLE_MS, BP_LOOT_TABLE_CFG,
    BP_RECIPE_MS, BP_RECIPE_CFG,
    BP_SPAWN_RULE_MS, BP_SPAWN_RULE_CFG,
    BP_TRADING_MS, BP_TRADING_CFG,

    # Resourcepack
    RP_ANIMATION_CONTROLLER_MS, RP_ANIMATION_CONTROLLER_CFG,
    RP_ANIMATION_MS, RP_ANIMATION_CFG,
    RP_ATTACHABLE_MS, RP_ATTACHABLE_CFG,
    RP_ENTITY_MS, RP_ENTITY_CFG,
    RP_PARTICLE_MS, RP_PARTICLE_CFG,
    RP_RENDER_CONTROLLER_MS, RP_RENDER_CONTROLLER_CFG,
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


def get_schema_dict() -> tp.Dict:
    return {"$ref": "#/definitions/root"}

class CreateSchemaInput(object):
    def __init__(self, meta_schema, export_config):
        self.meta_schema: MetaSchema = meta_schema
        self.export_config: ExportConfig = export_config
        self.schema: tp.Dict = get_schema_dict()

def create_schemas(
    source_path: str, inputs: tp.List[CreateSchemaInput],
    tmp_path: str='./.tmp'
):
    tmp_created = False  # True if temporary files were created

    # Try to read the ZIP file
    if os.path.isfile:
        with ZipFile(source_path, 'r') as zipf:
            is_valid = zipf.testzip() is None
            if not is_valid:
                raise ValueError('Input file is not a ziped behavior-pack')
            zipf.extractall(tmp_path)
            bp_path = tmp_path
            tmp_created = True
    try:
        for root, dirs, files in os.walk(bp_path):
            for file_ in files:
                fp = os.path.join(root, file_)
                for inp in inputs:
                    pattern = os.path.join(bp_path, inp.export_config.pattern)
                    if fnmatch.fnmatch(fp, pattern):
                        with open(fp, 'r') as f:
                            source = jsonc_read(f)
                        for assertion in inp.export_config.assertions:
                            try:
                                if not assertion(source):
                                    print(
                                        f'Skipped file: {fp} assertion '
                                        'condition not met'
                                    )
                                    break
                            except:
                                print(
                                    f'Skipped file: {fp} error during '
                                    'checking conditions'
                                )
                                break
                        else:  # All assertion conditions met
                            create_schema_definitions(
                                source=source,
                                target=inp.schema,
                                meta_schema=inp.meta_schema
                            )
    finally:  # Remove temporary files if something went wrong
        if tmp_created:
            shutil.rmtree(tmp_path)


if __name__ == "__main__":
    # GENERATING BEHAVIORPACK SCHEMAS
    print('GENERATING BEHAVIORPACK SCHEMAS')
    bp_schema_inputs = [
        CreateSchemaInput(BP_ENTITY_MS, BP_ENTITY_CFG),
        CreateSchemaInput(BP_ITEM_MS, BP_ITEM_CFG),
        CreateSchemaInput(
            BP_ANIMATION_CONTROLLER_MS, BP_ANIMATION_CONTROLLER_CFG
        ),
        CreateSchemaInput(BP_ANIMATION_MS, BP_ANIMATION_CFG),
        CreateSchemaInput(BP_LOOT_TABLE_MS, BP_LOOT_TABLE_CFG),
        CreateSchemaInput(BP_RECIPE_MS, BP_RECIPE_CFG),
        CreateSchemaInput(BP_SPAWN_RULE_MS, BP_SPAWN_RULE_CFG),
        CreateSchemaInput(BP_TRADING_MS, BP_TRADING_CFG),
    ]
    
    for dir_ in os.listdir(BP_PATH):
        create_schemas(os.path.join(BP_PATH, dir_), bp_schema_inputs)

    for inp in bp_schema_inputs:
        with open(inp.export_config.export_path, 'w') as f:
            json.dump(inp.schema, f, indent='\t')


    # GENERATING RESOURCEPACK SCHEMAS
    print('GENERATING RESOURCEPACK SCHEMAS')
    rp_schema_inputs = [
        CreateSchemaInput(RP_ANIMATION_CONTROLLER_MS, RP_ANIMATION_CONTROLLER_CFG,),
        CreateSchemaInput(RP_ANIMATION_MS, RP_ANIMATION_CFG,),
        CreateSchemaInput(RP_ATTACHABLE_MS, RP_ATTACHABLE_CFG,),
        CreateSchemaInput(RP_ENTITY_MS, RP_ENTITY_CFG,),
        CreateSchemaInput(RP_PARTICLE_MS, RP_PARTICLE_CFG,),
        CreateSchemaInput(RP_RENDER_CONTROLLER_MS, RP_RENDER_CONTROLLER_CFG,),
    ]
    
    for dir_ in os.listdir(RP_PATH):
        create_schemas(os.path.join(RP_PATH, dir_), rp_schema_inputs)

    for inp in rp_schema_inputs:
        with open(inp.export_config.export_path, 'w') as f:
            json.dump(inp.schema, f, indent='\t')