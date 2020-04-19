'''
Functions related to generating json schemas
'''
import json_paths as jp
import typing as tp
from collections import namedtuple
from enum import Enum



class MetaSchema(object):
    '''
    A dictionary that describes the structure of the schema to create.
    '''
    def __init__(
        self,
        meta_schema: tp.Dict[str, tp.Dict],
        blacklist: tp.List[tp.List[jp.JsonPathPattern]]
    ):
        self.meta_schema = meta_schema
        self.blacklist = blacklist

    def is_blacklisted(self, path: jp.JsonPath) -> bool:
        '''
        Checks if path is on the blacklist.
        '''
        for pattern in self.blacklist:
            if jp.match(path, pattern, full_match=False).result:
                return True
        return False

    def get_reference_name(
        self,
        definition_name: str,
        pattern: tp.List[jp.JsonPathPattern]
    ) -> str:
        '''
        Returns the reference name from given pattern from definition name.
        You can get correct patterns from list_patterns() methiod
        '''
        curr_item = self.meta_schema[definition_name]
        for p in pattern:
            curr_item = curr_item[p]
        if isinstance(curr_item, str):
            return curr_item
        else:
            raise ValueError('Invalid reference path')

    def list_patterns(
        self,
        definition_name: str
    ) -> tp.List[jp.JsonPathPattern]:
        '''
        Lists paths from given definition.
        '''
        def iterate_def(definition, curr_path):
            if isinstance(definition, dict):
                for k, v in definition.items():
                    next_path = curr_path.copy()
                    next_path.append(k)
                    for result in iterate_def(v, next_path):
                        yield result
            elif isinstance(definition, list):
                for i, v in enumerate(definition):
                    next_path = curr_path.copy()
                    next_path.append(i)
                    for result in iterate_def(v, next_path):
                        yield result
            elif isinstance(definition, str):
                yield curr_path.copy()

        result = list(iterate_def(self.meta_schema[definition_name], []))
        return result

    def create_schema_paths(
        self, path: jp.JsonPath
    ) -> tp.Tuple['SchemaPath', tp.Optional['SchemaPath']]:
        '''
        Creates pair of SchemaPaths based on JsonPath. The first path is a
        path to an object and the second one is a path to reference to that
        object.
        '''
        def match_pattern(
            path: jp.JsonPath,
            patterns: tp.List[jp.JsonPathPattern]
        ) -> tp.Optional[jp.MatchMap]:
            '''
            Try to match path against patterns from the list.
            Returns the pattern which matches the path or None if none of them
            match it.
            '''
            for pattern in patterns:
                jpmatch = jp.match(path, pattern, full_match=False)
                if jpmatch.result:
                    return jpmatch
            return None

        curr_def = 'root'
        curr_path = path

        while True:
            patterns = self.list_patterns(curr_def)

            mp = match_pattern(curr_path, patterns)
            if mp is None:  # No match
                return (
                    SchemaPath(definition=curr_def, json_path=curr_path),
                    None
                )
            elif (len(mp.matches) == len(mp.value)):  # Full match
                reference_path = SchemaPath(
                    definition=curr_def,
                    map_match=mp
                )
                curr_def = self.get_reference_name(curr_def, mp.pattern)
                obj_path = SchemaPath(definition=curr_def, json_path=[])
                curr_path = curr_path[len(mp.matches):]
                return (obj_path, reference_path)
            else:  # Partial match path not exhausted (continue the loop)
                curr_def = self.get_reference_name(
                    curr_def, mp.pattern
                )
                curr_path = curr_path[len(mp.matches):]


class SchemaPathWildcard(Enum):
    '''
    Special characters for SchemaPath
    '''
    ANY_ITEM = 0
    ADDITIONAL_PROPERTY = 1

SchemaPathItem = tp.Union[str, int, SchemaPathWildcard]

class SchemaPath(object):
    '''
    Path to an item in SchemaDict
    '''
    def __init__(
        self, definition: str,
        map_match: jp.MatchMap=None,
        json_path: jp.JsonPath=None
    ):
        '''
        Creates SchemaPath from MatchMap or JsonPath. One or the other must
        be specified. You cannot specify both.
        '''
        if map_match is None and json_path is None:
            raise ValueError('You must specify map_match or json_path')
        elif map_match is not None and json_path is not None:
            raise ValueError("You can't specify both map_match and json_path")
        elif map_match is not None:
            path = self._path_list_from_map_match(map_match)
        else:  # json_path is not None
            path = self._path_list_from_json_path(json_path)
        self.definition: str = definition
        self.path: tp.List[SchemaPathItem] = path

    def _path_list_from_map_match(
        self, map_match: jp.MatchMap
    ) -> tp.List[SchemaPathItem]:
        '''Used in init to create path_list from map_match'''
        sp_path: tp.List[SchemaPathItem] = []
        for mm in map_match.matches:
            if isinstance(mm.pattern, (int, str)):
                sp_path.append(mm.pattern)
            elif mm.pattern is jp.Wildcard.ANY_ITEM:
                sp_path.append(SchemaPathWildcard.ANY_ITEM)
            elif mm.pattern is jp.Wildcard.ANY_PARAMETER:
                sp_path.append(SchemaPathWildcard.ADDITIONAL_PROPERTY)
            elif mm.pattern is jp.Wildcard.ANYTHING_UNTIL_NEXT_MATCH:
                if isinstance(mm.item, int):
                    sp_path.append(SchemaPathWildcard.ANY_ITEM)
                elif isinstance(mm.item, str):
                    sp_path.append(mm.item)
                else:
                    raise ValueError('Unsuported MatchMapItem item')
            elif mm.pattern is jp.Wildcard.ANYTHING:
                if isinstance(mm.item, int):
                    sp_path.append(SchemaPathWildcard.ANY_ITEM)
                elif isinstance(mm.item, str):
                    sp_path.append(
                        SchemaPathWildcard.ADDITIONAL_PROPERTY
                    )
                else:
                    raise ValueError('Unsuported MatchMapItem item')
            else:
                raise ValueError('Unsuported MatchMapItem pattern')
        return sp_path

    def _path_list_from_json_path(
        self, json_path: jp.JsonPath
    ) -> tp.List[SchemaPathItem]:
        '''Used in init to create path_list from json_path'''
        sp_path: tp.List[SchemaPathItem] = []
        for p in json_path:
            if isinstance(p, int):
                sp_path.append(SchemaPathWildcard.ANY_ITEM)
            else:
                sp_path.append(p)
        return sp_path

class SchemaReference(object):
    '''
    Represents a reference in schema
    '''
    def __init__(self, target: str):
        self.target = f'#/definitions/{target}'

class SchemaDict(object):
    '''
    Wraper class around a dictionary with schema data. Provide easy access
    to schema properties.
    '''
    def __init__(self, schema_dict: tp.Dict):
        self.schema_dict = schema_dict

        if 'definitions' not in self.schema_dict:
            self.schema_dict['definitions'] = {}

    def append(self, obj: tp.Any, path: SchemaPath):
        if path.definition not in self.schema_dict['definitions']:
            self.schema_dict['definitions'][path.definition] = {}
        curr_def = self.schema_dict['definitions'][path.definition]
        
        # Create / acces the defininition item
        for key in path.path:
            if isinstance(key, str):
                if 'properties' not in curr_def:
                    curr_def['properties'] = {}
                if key not in curr_def['properties']:
                    curr_def['properties'][key] = {}
                curr_def = curr_def['properties'][key]  # object
            elif isinstance(key, int):
                if 'items' not in curr_def:
                    curr_def['items'] = []
                if (
                    not isinstance(curr_def['items'], list) or
                    len(curr_def['items']) != key+1
                ):
                    raise ValueError('Invalid list index for the item')
                curr_def.append(curr_def['items'])
            elif key == SchemaPathWildcard.ANY_ITEM:
                if 'items' not in curr_def:
                    curr_def['items'] = {}
                curr_def = curr_def['items']  # array
            elif key == SchemaPathWildcard.ADDITIONAL_PROPERTY:
                if 'additionalProperties' not in curr_def:
                    curr_def['additionalProperties'] = {}
                curr_def = curr_def['additionalProperties']
            else:
                raise ValueError(f'Unknown path key type {key}')

        # Add data to the definition item
        if 'type' not in curr_def and not isinstance(obj, SchemaReference):
            curr_def['type'] = []

        if isinstance(obj, type(None)):
            if 'null' not in curr_def['type']:
                curr_def['type'].append('null')
        elif isinstance(obj, bool):
            if 'boolean' not in curr_def['type']:
                curr_def['type'].append('boolean')
        elif isinstance(obj, int):
            if 'integer' not in curr_def['type']:
                curr_def['type'].append('integer')
        elif isinstance(obj, float):
            if 'number' not in curr_def['type']:
                curr_def['type'].append('number')
        elif isinstance(obj, str):
            if 'string' not in curr_def['type']:
                curr_def['type'].append('string')
        elif isinstance(obj, list):
            if 'array' not in curr_def['type']:
                curr_def['type'].append('array')
        elif isinstance(obj, dict):
            if 'object' not in curr_def['type']:
                curr_def['type'].append('object')
        elif isinstance(obj, SchemaReference):
            curr_def['$ref'] = obj.target
            # TODO - check if there are other properties? References shouldn't
            # have any (like 'type' or 'additionalProperties' etc.)
        else:
            raise ValueError(f'Invalid object type: {type(obj)}')


def create_schema_definitions(
    source: tp.Any, target: tp.Dict, meta_schema: MetaSchema
):
    schema_dict = SchemaDict(target)

    for obj, path in jp.walk(source):
        if meta_schema.is_blacklisted(path):
            continue
        schema_path, reference_path = meta_schema.create_schema_paths(path)
        schema_dict.append(obj, schema_path)
        if reference_path is not None:
            schema_dict.append(
                SchemaReference(schema_path.definition),
                reference_path
            )
