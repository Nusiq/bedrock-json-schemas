'''
Matching internal paths inside JSON files.
'''
import typing as tp
from enum import Enum


JsonPath = tp.List[tp.Union[str, int]]
JsonPathPattern = tp.List[tp.Union[str, int, 'Wildcard']]

class Wildcard(Enum):
    '''Special characters for JSON path'''
    ANY_ITEM = 0  # any index of a list
    ANY_PARAMETER = 1  # an dictionary parameter name
    ANYTHING = 2  # any index of a list or any dictionary parameter name


def match(
    value: JsonPath,
    pattern: JsonPathPattern,
    full_match: bool = True
) -> bool:
    '''
    Compares JSON path with a pattern and returns a match success.
    
    - value - a JSON path
    - pattern - a pattern to match
    - full_match - if True the value and the pattern must have the same length,
      if false than the pattern matches tries to match only first N items from
      the value (N is the number of items in pattern)
    '''
    def match_items(
        v: tp.Union[str, int],
        p: tp.Union[str, int, Wildcard]
    ):
        '''Single match of corresponding items'''
        if p is Wildcard.ANYTHING:
            return True
        if type(v) is int:
            if type(p) is int:
                return v == p
            elif p is Wildcard.ANY_ITEM:
                return True
        elif type(v) is str:
            if type(p) is str:
                return v == p
            elif p is Wildcard.ANY_PARAMETER:
                return True
        else:
            raise ValueError('Invalid JSON path')

    if full_match:
        if len(value) != len(pattern):
            return False
    else:
        if len(value) < len(pattern):
            return False
        else:
            value = value[:len(pattern)]
    for v, p in zip(value, pattern):
        if not match_items(v, p):
            return False
    return True

def walk(
    jsonable: tp.Any, _curr_path: JsonPath = []
) -> tp.Iterable[tp.Tuple[tp.Any, JsonPath]]:
    '''
    Walks recursively through a jsonable object and yields child objects
    and their json paths.

    Parent objects are always returned before their child objects.
    '''
    if not isinstance(
        jsonable, (int, float, bool, str, type(None), dict, list)
    ):
        raise ValueError(f'Invalid type of jsonable - {type(jsonable)}')
    yield (jsonable, _curr_path)
    if isinstance(jsonable, dict):
        for k, v in jsonable.items():
            next_path = _curr_path.copy()
            next_path.append(k)
            for result in walk(v, next_path):
                yield result
    elif isinstance(jsonable, list):
        for i, v in enumerate(jsonable):
            next_path = _curr_path.copy()
            next_path.append(i)
            for result in walk(v, next_path):
                yield result


def get(path: JsonPath, jsonable: tp.Any) -> tp.Any:
    '''
    Tries to return an item from jsonable using path. Raises KeyError on fail.
    '''
    try:
        for k in path:
            jsonable = jsonable[k]
        return jsonable
    except:
        raise KeyError(f'{k}')