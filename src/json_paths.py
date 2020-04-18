'''
Matching internal paths inside JSON files.
'''
import typing as tp
from enum import Enum


JsonPath = tp.List[tp.Union[str, int]]
JsonPathPattern = tp.List[tp.Union[str, int, 'Wildcard']]

class Wildcard(Enum):
    '''
    Special characters for JSON path
    
    - ANY_ITEM - Any item index of a list (any int)
    - ANY_PARAMETER - Any key in a dictionary (any str)
    - ANYTHING - Any index of a list or any key in a dictionary (any int or
      str)
    - ANYTHING_UNTIL_NEXT_MATCH - This wildcard can match zero, one or multiple
      items in a path. It matches anything except things that match the next
      item in the JsonPath. It cannot be the last part of th JsonPathPattern
      and its not allowed to repeat this Wildcard in a row.
    '''
    ANY_ITEM = 0
    ANY_PARAMETER = 1
    ANYTHING = 2
    ANYTHING_UNTIL_NEXT_MATCH = 3


class MatchMapItem(tp.NamedTuple):
    '''
    A class that represents single match from match function.
    '''
    item: tp.Union[str, int]
    pattern: tp.Union[str, int, 'Wildcard']

class MatchMap(tp.NamedTuple):
    '''
    Result of the match function
    '''
    result: bool
    matches: tp.List[MatchMapItem]
    value: JsonPath
    pattern: JsonPathPattern

def match(
    value: JsonPath,
    pattern: JsonPathPattern,
    full_match: bool = True
) -> MatchMap:
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

    def safe_next(iter):
        try:
            return next(iter)
        except StopIteration:
            return None

    pattern_iter = iter(pattern)
    anything_until_p = False

    match_maps: tp.List[MatchMapItem] = []
    for v in value:
        if not anything_until_p:
            p = safe_next(pattern_iter)
            if p is None:  # Its the end but not a full match
                return MatchMap(not full_match, match_maps, value, pattern)
            if p is Wildcard.ANYTHING_UNTIL_NEXT_MATCH:
                anything_until_p = True
                p = safe_next(pattern_iter)
                if p is None or p is Wildcard.ANYTHING_UNTIL_NEXT_MATCH:
                    raise ValueError('Invalid pattern')

        items_matched = match_items(v, p)
        if anything_until_p:
            if items_matched:
                anything_until_p = False
                match_maps.append(MatchMapItem(v, p))
            else:
                match_maps.append(MatchMapItem(v, Wildcard.ANYTHING_UNTIL_NEXT_MATCH))
        else:
            if not items_matched:
                return MatchMap(False, match_maps, value, pattern)
            match_maps.append(MatchMapItem(v, p))
    # Didn't find the last pattern for anything_until_p
    if anything_until_p:
        return MatchMap(False, match_maps, value, pattern)
    # There shouldn't be any leftover items in pattern_iter
    p = safe_next(pattern_iter)
    if p is None:
        return MatchMap(True, match_maps, value, pattern)
    return MatchMap(False, match_maps, value, pattern)


def walk(
    jsonable: tp.Any, _curr_path: JsonPath = None
) -> tp.Iterable[tp.Tuple[tp.Any, JsonPath]]:
    '''
    Walks recursively through a jsonable object and yields child objects
    and their json paths.

    Parent objects are always returned before their child objects.
    '''
    if _curr_path is None:
        _curr_path = []
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