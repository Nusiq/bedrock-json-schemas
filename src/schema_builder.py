'''
Functions related to generating json schemas
'''
import json_paths
import typing as tp
from collections import namedtuple
from enum import Enum


class DefItemPathWildcard(Enum):
    ANY_ITEM = 0
    ADDITIONAL_PROPERTY = 1


DefinitionItemPath = tp.List[tp.Union[str, int, DefItemPathWildcard]]


class ReferenceItem(object):
    '''
    Represents a reference in schema
    '''
    def __init__(self, target: str):
        self.target = f'#/definitions/{target}'


class DefinitionItem(object):
    '''
    Wrapper class for dictionaries derived from the properties in the schema
    dictionary.
    '''
    def __init__(self, definition_item: tp.Dict):
        self.definition_item = definition_item

    def set_definition(self, value: tp.Any):
        # Define the newly added object
        if (
            'type' not in self.definition_item and
            not isinstance(value, ReferenceItem)
        ):
            self.definition_item['type'] = []

        if isinstance(value, type(None)):
            if 'null' not in self.definition_item['type']:
                self.definition_item['type'].append('null')
        elif isinstance(value, bool):
            if 'boolean' not in self.definition_item['type']:
                self.definition_item['type'].append('boolean')
        elif isinstance(value, int):
            if 'integer' not in self.definition_item['type']:
                self.definition_item['type'].append('integer')
        elif isinstance(value, float):
            if 'number' not in self.definition_item['type']:
                self.definition_item['type'].append('number')
        elif isinstance(value, str):
            if 'string' not in self.definition_item['type']:
                self.definition_item['type'].append('string')
        elif isinstance(value, list):
            if 'array' not in self.definition_item['type']:
                self.definition_item['type'].append('array')
        elif isinstance(value, dict):
            if 'object' not in self.definition_item['type']:
                self.definition_item['type'].append('object')
        elif isinstance(value, ReferenceItem):
            self.definition_item['$ref'] = value.target
            # TODO - check if there are other properties? References shouldn't
            # have any (like 'type' or 'additionalProperties' etc.)
        else:
            raise ValueError(f'Invalid object type: {type(value)}')


class SchemaDict(object):
    '''
    Wraper class around a dictionary with schema data. Provide easy access
    to schema properties.
    '''
    def __init__(self, schema_dict: tp.Dict):
        self.schema_dict = schema_dict

        if 'definitions' not in self.schema_dict:
            self.schema_dict['definitions'] = {}

    def get_definition(self, definition: str):
        return self.schema_dict['definitions'][definition]

    def add_definition(self, name: str):
        '''
        Adds a diefinition to schema if it doesn't already exist
        '''
        if name not in self.schema_dict['definitions']:
            self.schema_dict['definitions'][name] = {}

    def get_definition_item(
        self, definition_name: str,
        relative_path: DefinitionItemPath
    ) -> DefinitionItem:
        '''
        Serches through schemas_dict (the dictionary with schema data). Starts
        in the root_name definition and goes through the relative_path. Returns
        the object reached after going through the path.
        '''
        def_item =  self.schema_dict['definitions'][definition_name]
        path = relative_path.copy()
        while len(path) > 0:  # Go through path until the last item
            key = path.pop(0)
            if isinstance(key, str):
                if 'properties' not in def_item:
                    def_item['properties'] = {}
                if key not in def_item['properties']:
                    def_item['properties'][key] = {}
                def_item = def_item['properties'][key]  # object
            elif isinstance(key, int):
                if 'items' not in def_item:
                    def_item['items'] = []
                if (
                    not isinstance(def_item['items'], list) or
                    len(def_item['items']) != key+1
                ):
                    raise ValueError('Invalid list index for the item')
                def_item.append(def_item['items'])
            elif key == DefItemPathWildcard.ANY_ITEM:
                if 'items' not in def_item:
                    def_item['items'] = {}
                def_item = def_item['items']  # array
            elif key == DefItemPathWildcard.ADDITIONAL_PROPERTY:
                if 'additionalProperties' not in def_item:
                    def_item['additionalProperties'] = {}
                def_item = def_item['additionalProperties']

        return DefinitionItem(def_item)


def create_schema_definitions(
    source: tp.Any, target: tp.Dict,
    define_objects: tp.Dict[str, tp.List[json_paths.JsonPathPattern]]
):
    '''
    Creates JSON schema for given source. The schema is saved in target
    dictionary. If target dictionary already has some definitions this
    function will expand it.

    The define_objects argument is a dictionary with names of the objects to
    define and their maching paths. Every path that matches one of the
    JsonPathPatterns in the define_objects dictionary will be defined as
    separate object in the pattern. The object name is defined by the
    key value of the define_objects dictionary.
    '''
    schema = SchemaDict(target)

    # The definitions dictionary always must have root
    define_objects['root'] = [[]]

    class DefinitionMatch(tp.NamedTuple):
        name: str
        i: int
        pattern: json_paths.JsonPathPattern

    def get_definition_match(
        path: json_paths.JsonPath
    ) -> tp.Optional[DefinitionMatch]:
        '''
        Tries to find a match in define_objects dict. Returns the name and
        index of the match on success or None on failore.
        '''
        for k, v in define_objects.items():
            for i, pattern in enumerate(v):
                if json_paths.match(path, pattern):
                    return DefinitionMatch(k, i, pattern)
        return None

    match_stack: tp.List[DefinitionMatch] = []
    first_loop = False
    for obj, path in json_paths.walk(source):
        if not first_loop:
            definition_match = get_definition_match(path)
            assert definition_match is not None
            match_stack.append(definition_match)
            schema.add_definition(definition_match.name)
            first_loop = True
        else:
            # Remove from stack if current match isn't valid anymore
            while not json_paths.match(
                path, match_stack[-1].pattern, full_match=False
            ):
                match_stack.pop()
            
            # Add to stack
            definition_match = get_definition_match(path)
            if definition_match is not None:
                # Add reference
                def_item_path: DefinitionItemPath=[]
                for i in definition_match.pattern:
                    if isinstance(i, int):
                        def_item_path.append(DefItemPathWildcard.ANY_ITEM)
                    elif i == json_paths.Wildcard.ANY_PARAMETER:
                        def_item_path.append(
                            DefItemPathWildcard.ADDITIONAL_PROPERTY
                        )
                    else:
                        def_item_path.append(i)
                schema.get_definition_item(
                    definition_name=match_stack[-1].name,
                    relative_path=def_item_path
                ).set_definition(ReferenceItem(definition_match.name))
                # Setn new value in match_stack
                match_stack.append(definition_match)
                schema.add_definition(definition_match.name)

        # Create def_item_path
        def_item_path=[]
        for i in path[len(match_stack[-1].pattern):]:
            if isinstance(i, int):
                def_item_path.append(DefItemPathWildcard.ANY_ITEM)
            else:
                def_item_path.append(i)
        # Add new item definition
        schema.get_definition_item(
            definition_name=match_stack[-1].name,
            relative_path=def_item_path
        ).set_definition(obj)
