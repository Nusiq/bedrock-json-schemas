from __future__ import annotations
'''
Functions related to generating json schemas
'''
import json_paths as jp
from collections import namedtuple
from enum import Enum
from typing import (
    NamedTuple, Optional, Any, Tuple, List, Callable, Union, Generator, Dict)

class Policy(Enum):
    '''
    Defines how to handle encounters of primitive values in the creation of
    schema. There are 3 options:
    - STRICT - add the value to enum that defines acceptablem values.
    - EXAMPLE - add the value to list of examples.
    - NONE - don't do anythoing.
    '''
    STRICT = 0
    EXAMPLE = 1
    NONE = 2

class MetaSchemaReference(NamedTuple):
    '''
    Used in MetaSchema.meta_schema dictionary to define a reference object and
    the policy for josn path.
    '''
    reference: Optional[str]
    policy: Policy = Policy.NONE

class MetaSchema(object):
    '''
    A dictionary that describes the structure of the schema to create.
    '''
    def __init__(
        self,
        meta_schema: Dict[str, Dict],
        blacklist: List[List[jp.JsonPathPattern]],
        root_filters: Dict[str, Callable[[Dict], str]]
    ):
        self.meta_schema = meta_schema
        self.blacklist = blacklist
        self.root_filters = root_filters

    def get_root_name(self, data: Any) -> Optional[str]:
        '''
        Returns the root name of schema for given data.
        '''
        for name, rf in self.root_filters.items():
            if rf(data):
                return name
        return None

    def is_blacklisted(self, path: jp.JsonPath) -> bool:
        '''
        Checks if path is on the blacklist.
        '''
        for pattern in self.blacklist:
            if jp.match(path, pattern, full_match=False).result:
                return True
        return False

    # This one uses only self.meta_schema from object properties
    # (in sub-methods)
    def create_schema_paths(
        self, path: jp.JsonPath, root_name: str = 'root'
    ) -> Tuple[SchemaPath, Optional[SchemaPath]]:
        '''
        Creates pair of SchemaPaths based on JsonPath. The first path is a
        path to an object and the second one is a path to reference to that
        object.
        '''
        def match_pattern(
            path: jp.JsonPath,
            patterns: List[Tuple[jp.JsonPathPattern, Policy]]
        ) -> Tuple[Optional[jp.MatchMap], Policy]:
            '''
            Try to match path against patterns from the list.
            Returns the pattern which matches the path or None if none of them
            match it.
            '''
            for pattern, policy in patterns:
                jpmatch = jp.match(path, pattern, full_match=False)
                if jpmatch.result:
                    return jpmatch, policy
            return None, Policy.NONE

        def get_reference_name(
            definition_name: str, pattern: List[jp.JsonPathPattern]
        ) -> MetaSchemaReference:
            '''
            Returns the reference name from given pattern from definition name.
            You can get correct patterns from list_patterns() methiod
            '''
            curr_item = self.meta_schema[definition_name]
            for p in pattern:
                curr_item = curr_item[p]
            if isinstance(curr_item, MetaSchemaReference):
                return curr_item
            else:
                raise ValueError('Invalid reference path')

        def list_patterns(
            definition_name: str
        ) -> List[Tuple[jp.JsonPathPattern, Policy]]:
            '''
            Lists paths from given definition.
            '''
            def iterate_def(
                definition, curr_path
            ) -> Generator[Tuple[jp.JsonPathPattern, Policy], None, None]:
                if isinstance(definition, dict):
                    for k, v in definition.items():
                        next_path = curr_path.copy()
                        next_path.append(k)
                        for result, policy in iterate_def(v, next_path):
                            yield result, policy
                elif isinstance(definition, list):
                    for i, v in enumerate(definition):
                        next_path = curr_path.copy()
                        next_path.append(i)
                        for result, policy in iterate_def(v, next_path):
                            yield result, policy
                elif isinstance(definition, MetaSchemaReference):
                    yield curr_path.copy(), definition.policy
                else:
                    raise Exception('Invalid meta_schema definition!')

            result: List[Tuple[jp.JsonPathPattern, Policy]] = list(
                iterate_def(self.meta_schema[definition_name], []))
            return result

        curr_def = root_name
        curr_path = path

        while True:
            patterns = list_patterns(curr_def)
            mp, policy = match_pattern(curr_path, patterns)
            if mp is None:  # No match
                return (
                    SchemaPath(
                        definition=curr_def, policy=policy, json_path=curr_path),
                    None
                )
            else:
                new_def, policy = get_reference_name(curr_def, mp.pattern)
                if new_def is None:  # This is not reference. It's just a policy definition
                    return (
                        SchemaPath(
                            definition=curr_def, policy=policy, json_path=curr_path),
                        None
                    )
                if (len(mp.matches) == len(mp.value)):  # Full match
                    reference_path = SchemaPath(
                        definition=curr_def, policy=policy, map_match=mp)  # TODO - Im not sure if this 'policy' is correct.
                    curr_def = new_def
                    obj_path = SchemaPath(
                        definition=curr_def, policy=policy, json_path=[])  # TODO - Im not sure if this 'policy' is correct.
                    curr_path = curr_path[len(mp.matches):]
                    return (obj_path, reference_path)
                else:  # Partial match path not exhausted (continue the loop)
                    curr_def = new_def
                    curr_path = curr_path[len(mp.matches):]


class SchemaPathWildcard(Enum):
    '''
    Special characters for SchemaPath
    '''
    ANY_ITEM = 0
    ADDITIONAL_PROPERTY = 1


SchemaPathItem = Union[str, int, SchemaPathWildcard]


class SchemaPath(object):
    '''
    Path to an item in SchemaDict
    '''
    def __init__(
        self, definition: str,
        policy: Policy,
        map_match: jp.MatchMap=None,
        json_path: jp.JsonPath=None
    ):
        '''
        Creates SchemaPath from MatchMap or JsonPath. One or the other must
        be specified. You cannot specify both.
        '''
        self.policy = policy
        if map_match is None and json_path is None:
            raise ValueError('You must specify map_match or json_path')
        elif map_match is not None and json_path is not None:
            raise ValueError("You can't specify both map_match and json_path")
        elif map_match is not None:
            path = self._path_list_from_map_match(map_match)
        else:  # json_path is not None
            path = self._path_list_from_json_path(json_path)
        self.definition: str = definition
        self.path: List[SchemaPathItem] = path

    def _path_list_from_map_match(
        self, map_match: jp.MatchMap
    ) -> List[SchemaPathItem]:
        '''Used in init to create path_list from map_match'''
        sp_path: List[SchemaPathItem] = []
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
    ) -> List[SchemaPathItem]:
        '''Used in init to create path_list from json_path'''
        sp_path: List[SchemaPathItem] = []
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
    def __init__(self, schema_dict: Dict):
        self.schema_dict = schema_dict

        if 'definitions' not in self.schema_dict:
            self.schema_dict['definitions'] = {}

    def append(
        self, obj: Any, path: SchemaPath
    ):
        '''
        Adds object to schema_dict using the SchemaPath object. The policy
        argument is when primitive type is added.
        - NONE - just marks the type of the object in certain path
        - STRICT - adds the object to list of acceptable values
        - EXAMPLE - marks the type and adds an example to list.

        Objects, arrays and reference types always take NONE polic even if you\
        specify other.
        '''
        policy = path.policy
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
                curr_def['type'].sort()
        elif isinstance(obj, bool):
            if 'boolean' not in curr_def['type']:
                curr_def['type'].append('boolean')
                curr_def['type'].sort()
        elif isinstance(obj, int):
            if 'integer' not in curr_def['type']:
                curr_def['type'].append('integer')
                curr_def['type'].sort()
        elif isinstance(obj, float):
            if 'number' not in curr_def['type']:
                curr_def['type'].append('number')
                curr_def['type'].sort()
        elif isinstance(obj, str):
            if 'string' not in curr_def['type']:
                curr_def['type'].append('string')
                curr_def['type'].sort()
        elif isinstance(obj, list):
            if 'array' not in curr_def['type']:
                curr_def['type'].append('array')
                curr_def['type'].sort()
        elif isinstance(obj, dict):
            if 'object' not in curr_def['type']:
                curr_def['type'].append('object')
                curr_def['type'].sort()
        elif isinstance(obj, SchemaReference):
            curr_def['$ref'] = obj.target
        else:
            raise ValueError(f'Invalid object type: {type(obj)}')

        # Reset policy for complex objects
        if (
            isinstance(obj, list) or isinstance(obj, dict) or
            isinstance(obj, SchemaReference)
        ):
            policy = Policy.NONE

        # Add example or item to enum
        if policy is Policy.EXAMPLE:
            if 'examples' not in curr_def:
                curr_def['examples'] = []
            if obj not in curr_def['examples']:
                curr_def['examples'].append(obj)
        elif policy is Policy.STRICT:
            if 'enum' not in curr_def:
                curr_def['enum'] = []
            if obj not in curr_def['enum']:
                curr_def['enum'].append(obj)


def create_schema_definitions(
    source: Any, target: Dict, meta_schema: MetaSchema
) -> bool:
    '''Creates schema definition. Returns succes value'''
    schema_dict = SchemaDict(target)
    root_name: Optional[str] = meta_schema.get_root_name(source)
    if root_name is None:
        print('Unable to select root name')
        return False


    for obj, path in jp.walk(source):
        if meta_schema.is_blacklisted(path):
            continue
        schema_path, reference_path = meta_schema.create_schema_paths(
            path, root_name
        )

        # policy = meta_schema.get_policy(obj, path)
        schema_dict.append(obj, schema_path)
        if reference_path is not None:
            schema_dict.append(
                SchemaReference(schema_path.definition),
                reference_path
            )
    return True
