'''
Functions related to generating json schemas
'''
import json_paths
import typing as tp
from collections import namedtuple


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
    # The definitions dictionary always must have root
    define_objects['root'] = [[]]

    # Make sure that there is definitions property
    if 'definitions' not in target:
        target['definitions'] = {}
    definitions = target['definitions']

    class DefinitionMatch(tp.NamedTuple):
        name: str
        i: int
        match_pattern: json_paths.JsonPathPattern

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

    def add_to_definition(
        curr_def: tp.Dict, relative_path: json_paths.JsonPath, value: tp.Any
    ):
        '''
        Takes curr_def (one of the definitions in "definitions"), relative_path
        to a child of the defined object and the value and adds new child to
        the definition.
        '''
        path = relative_path.copy()
        if len(path) > 0:
            while len(path) > 1:  # Go through path until the last item
                key = path.pop(0)
                if isinstance(key, str):  # return object with current key
                    curr_def = curr_def['properties'][key]
                elif isinstance(key, int):  # index value doesn't matter in array
                    curr_def = curr_def['items']
            # Last object reached add properties/items to it if necessary
            key = path.pop(0)
            if isinstance(key, str):
                if 'properties' not in curr_def:
                    curr_def['properties'] = {
                        key: {}
                    }
                elif key not in curr_def['properties']:
                    curr_def['properties'][key] = {}
                curr_def = curr_def['properties'][key]
            elif isinstance(key, int):
                if 'items' not in curr_def:
                    curr_def['items'] = {}
                curr_def = curr_def['items']
        # Define the newly added object
        if 'type' not in curr_def:
            curr_def['type'] = []

        def _add_type(type_str: str):  # less boilerplate code...
            if type_str not in curr_def['type']:
                curr_def['type'].append(type_str)

        if isinstance(value, type(None)):
            _add_type('null')
        elif isinstance(value, bool):
            _add_type('boolean')
        elif isinstance(value, int):
            _add_type('integer')
        elif isinstance(value, float):
            _add_type('number')
        elif isinstance(value, str):
            _add_type('string')
        elif isinstance(value, list):
            _add_type('array')
        elif isinstance(value, dict):
            _add_type('object')
        else:
            raise ValueError(f'Invalid object type: {type(value)}')

    match_stack: tp.List[DefinitionMatch] = []
    for obj, path in json_paths.walk(source):
        # Add to stack if new match is detected
        definition_match = get_definition_match(path)
        if definition_match is not None:
            # Set new curr_pattern and append it to the stack
            curr_pattern = definition_match.match_pattern
            match_stack.append(definition_match)
            # Add item to the target definitions
            if definition_match.name not in definitions:
                definitions[definition_match.name] = {}

        # Remove from stack if current match isn't valid anymore
        while not json_paths.match(path, curr_pattern, full_match=False):
            match_stack.pop()
            curr_pattern = match_stack[-1].match_pattern

        # Set path to current definition in target file
        curr_def = definitions[match_stack[-1].name]
        add_to_definition(
            curr_def=curr_def,
            relative_path=path[len(curr_pattern):],
            value=obj
        )