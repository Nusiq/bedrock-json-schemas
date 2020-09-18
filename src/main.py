import os
from zipfile import ZipFile

BP_PATH = '../packs/behavior_packs'
RP_PATH = '../packs/resource_packs'
TMP_PATH = '../.tmp'

import typing as tp
import shutil
import fnmatch
import json
from jsonc_decoder import JSONCDecoder
from json_encoder import CompactEncoder
import json_paths as jp
from schema_builder import create_schema_definitions
from collections import defaultdict

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
    RP_MODEL_MS, RP_MODEL_CFG,
    RP_BLOCKS_JSON_FILE_MS, RP_BLOCKS_JSON_FILE_CFG,
)

class CreateSchemaInput(object):
    def __init__(self, meta_schema, export_config):
        self.meta_schema: MetaSchema = meta_schema
        self.export_config: ExportConfig = export_config
        self.schema: tp.Dict = {
            "anyOf": [
                {"$ref": f'#/definitions/{i}'}
                for i in meta_schema.root_filters.keys()
            ]
        }

def create_schemas(
    source_path: str, inputs: tp.List[CreateSchemaInput],
    tmp_path: str
):
    tmp_created = False  # True if temporary files were created

    # Try to read the ZIP file
    if os.path.isfile(source_path):
        with ZipFile(source_path, 'r') as zipf:
            is_valid = zipf.testzip() is None
            if not is_valid:
                raise ValueError('Input file is not a ziped behavior-pack')
            zipf.extractall(tmp_path)
            extracted_data_path = tmp_path
            tmp_created = True
    else:
        extracted_data_path = source_path

    try:
        for root, dirs, files in os.walk(extracted_data_path):
            for file_ in files:
                fp = os.path.join(root, file_)
                for inp in inputs:
                    pattern = os.path.join(extracted_data_path, inp.export_config.pattern)
                    if fnmatch.fnmatch(fp, pattern):
                        with open(fp, 'r') as f:
                            source = json.load(f, cls=JSONCDecoder)
                        if not create_schema_definitions(
                            source=source,
                            target=inp.schema,
                            meta_schema=inp.meta_schema
                        ):
                            raise Exception(f'Missing schema root for file: {source_path} :: {fp}')
    finally:  # Remove temporary files if something went wrong
        if tmp_created:
            shutil.rmtree(tmp_path)


# Some additional configuration...
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
rp_schema_inputs = [
    CreateSchemaInput(RP_ANIMATION_CONTROLLER_MS, RP_ANIMATION_CONTROLLER_CFG,),
    CreateSchemaInput(RP_ANIMATION_MS, RP_ANIMATION_CFG,),
    CreateSchemaInput(RP_ATTACHABLE_MS, RP_ATTACHABLE_CFG,),
    CreateSchemaInput(RP_ENTITY_MS, RP_ENTITY_CFG,),
    CreateSchemaInput(RP_PARTICLE_MS, RP_PARTICLE_CFG,),
    CreateSchemaInput(RP_RENDER_CONTROLLER_MS, RP_RENDER_CONTROLLER_CFG,),
    CreateSchemaInput(RP_MODEL_MS, RP_MODEL_CFG,),
    CreateSchemaInput(RP_BLOCKS_JSON_FILE_MS, RP_BLOCKS_JSON_FILE_CFG),
]


if __name__ == "__main__":
    # GENERATING BEHAVIORPACK SCHEMAS
    print('GENERATING BEHAVIORPACK SCHEMAS')
    for dir_ in os.listdir(BP_PATH):
        create_schemas(os.path.join(BP_PATH, dir_), bp_schema_inputs, TMP_PATH)

    for inp in bp_schema_inputs:
        with open(inp.export_config.export_path, 'w') as f:
            json.dump(inp.schema, f, cls=CompactEncoder)

    # GENERATING RESOURCEPACK SCHEMAS
    print('GENERATING RESOURCEPACK SCHEMAS')
    for dir_ in os.listdir(RP_PATH):
        create_schemas(os.path.join(RP_PATH, dir_), rp_schema_inputs, TMP_PATH)

    for inp in rp_schema_inputs:
        with open(inp.export_config.export_path, 'w') as f:
            json.dump(inp.schema, f, cls=CompactEncoder)
