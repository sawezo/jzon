"""
Defines mock data structures for usage in tests. Kept here due to length.

Note 'self.expected' represents the expected output of the resulting dataframe.to_dict(oriented='records').

To generate new cases in this format use 'mcreate_tests.ipynb'.
"""


# test classes
class NestedObject:
    def __init__(self):
        """
        dicts within dicts
        """
        self.json = [
            {
                'FEATURE_I': {
                    'a': 10, 'b': 1, 'c': 2, 'd': 3}, 'FEATURE_II': {
                    'a': 4, 'b': 5, 'c': 6, 'd': 7}}, {
                'FEATURE_I': {
                    'a': 100, 'b': {
                        'nested': 10}, 'c': 20, 'd': 30}, 'FEATURE_II': {
                    'a': 40, 'b': 50, 'c': 60, 'd': 70}}]

        self.expected = {
            'root_0': {
                'PK': {
                    0: 0, 1: 1}, 'root.FEATURE_I_a': {
                    0: 10, 1: 100}, 'root.FEATURE_I_b': {
                    0: 1.0, 1: ''}, 'root.FEATURE_I_c': {
                        0: 2, 1: 20}, 'root.FEATURE_I_d': {
                            0: 3, 1: 30}, 'root.FEATURE_I_b_nested': {
                                0: '', 1: 10.0}, 'root.FEATURE_II_a': {
                                    0: 4, 1: 40}, 'root.FEATURE_II_b': {
                                        0: 5, 1: 50}, 'root.FEATURE_II_c': {
                                            0: 6, 1: 60}, 'root.FEATURE_II_d': {
                                                0: 7, 1: 70}}}


class NestedObjectMultipleTypes:
    """
    multiple types within object
    """

    def __init__(self):
        """
        objects containing multiple (valid) types
        """
        self.json = [{'FEATURE_I': {'a': 0, 'b': 'string', 'c': True},
                      'FEATURE_II': {'a': 0.0, 'b': 'gnirts', 'c': False},
                      'FEATURE_III': 'ahhh!'},
                     {'FEATURE_I': {'a': 0, 'b': 'string', 'c': True}}]

        self.expected = {
            'root_0': {
                'PK': {
                    0: 0, 1: 1}, 'root.FEATURE_III': {
                    0: 'ahhh!', 1: ''}, 'root.FEATURE_I_a': {
                    0: 0, 1: 0}, 'root.FEATURE_I_b': {
                        0: 'string', 1: 'string'}, 'root.FEATURE_I_c': {
                            0: True, 1: True}, 'root.FEATURE_II_a': {
                                0: 0.0, 1: ''}, 'root.FEATURE_II_b': {
                                    0: 'gnirts', 1: ''}, 'root.FEATURE_II_c': {
                                        0: False, 1: ''}}}


class SimpleArray:
    def __init__(self):
        """
        simple array
        """
        self.json = [{'FEATURE_I': ['a', 'b', 'c'], 'FEATURE_II': [1, 2, 3]}]

        self.expected = {
            'root_0': {
                'PK': {
                    0: 0}}, 'root_0<FEATURE_II_1': {
                'FEATURE_II.FEATURE_II': {
                    0: 1, 1: 2, 2: 3}, 'FEATURE_II.subarray_IDX': {
                        0: 0, 1: 1, 2: 2}, 'FK': {
                            0: 0, 1: 0, 2: 0}, 'PK': {
                                0: 0, 1: 1, 2: 2}}, 'root_0<FEATURE_I_1': {
                                    'FEATURE_I.FEATURE_I': {
                                        0: 'a', 1: 'b', 2: 'c'}, 'FEATURE_I.subarray_IDX': {
                                            0: 0, 1: 1, 2: 2}, 'FK': {
                                                0: 0, 1: 0, 2: 0}, 'PK': {
                                                    0: 0, 1: 1, 2: 2}}}


class NestedArray:
    def __init__(self):
        """
        objects containing multiple (valid) types
        """
        self.json = [{'FEATURE_I': [[['a', 4], ['a', 4]], [['a', 4], ['a', 4]]],
                      'FEATURE_II': [[['a', 4], ['c', 2]], [['a', 4], ['a', 4]]]}]

        self.expected = {'root_0': {'PK': {0: 0}},
                         'root_0<FEATURE_II_1': {'FEATURE_II.subarray_IDX': {0: 0, 1: 1},
                                                 'FK': {0: 0, 1: 0},
                                                 'PK': {0: 0, 1: 1}},
                         'root_0<FEATURE_II_1<FEATURE_II_idx_0_2': {'FEATURE_II_idx_0.FEATURE_II_idx_0': {0: 'a',
                                                                                                          1: 4,
                                                                                                          2: 'a',
                                                                                                          3: 4},
                                                                    'FEATURE_II_idx_0.subarray_IDX': {0: 0,
                                                                                                      1: 1,
                                                                                                      2: 0,
                                                                                                      3: 1},
                                                                    'FK': {0: 0, 1: 0, 2: 1, 3: 1},
                                                                    'PK': {0: 0, 1: 1, 2: 2, 3: 3}},
                         'root_0<FEATURE_II_1<FEATURE_II_idx_1_2': {'FEATURE_II_idx_1.FEATURE_II_idx_1': {0: 'c',
                                                                                                          1: 2,
                                                                                                          2: 'a',
                                                                                                          3: 4},
                                                                    'FEATURE_II_idx_1.subarray_IDX': {0: 0,
                                                                                                      1: 1,
                                                                                                      2: 0,
                                                                                                      3: 1},
                                                                    'FK': {0: 0, 1: 0, 2: 1, 3: 1},
                                                                    'PK': {0: 0, 1: 1, 2: 2, 3: 3}},
                         'root_0<FEATURE_I_1': {'FEATURE_I.subarray_IDX': {0: 0, 1: 1},
                                                'FK': {0: 0, 1: 0},
                                                'PK': {0: 0, 1: 1}},
                         'root_0<FEATURE_I_1<FEATURE_I_idx_0_2': {'FEATURE_I_idx_0.FEATURE_I_idx_0': {0: 'a',
                                                                                                      1: 4,
                                                                                                      2: 'a',
                                                                                                      3: 4},
                                                                  'FEATURE_I_idx_0.subarray_IDX': {0: 0,
                                                                                                   1: 1,
                                                                                                   2: 0,
                                                                                                   3: 1},
                                                                  'FK': {0: 0, 1: 0, 2: 1, 3: 1},
                                                                  'PK': {0: 0, 1: 1, 2: 2, 3: 3}},
                         'root_0<FEATURE_I_1<FEATURE_I_idx_1_2': {'FEATURE_I_idx_1.FEATURE_I_idx_1': {0: 'a',
                                                                                                      1: 4,
                                                                                                      2: 'a',
                                                                                                      3: 4},
                                                                  'FEATURE_I_idx_1.subarray_IDX': {0: 0,
                                                                                                   1: 1,
                                                                                                   2: 0,
                                                                                                   3: 1},
                                                                  'FK': {0: 0, 1: 0, 2: 1, 3: 1},
                                                                  'PK': {0: 0, 1: 1, 2: 2, 3: 3}}}


class ObjectsInArrays:
    def __init__(self):
        """
        arrays with objects
        """
        self.json = [{'TABLE_I': [{'a': 0, 'b': 1, 'c': 2, 'd': 3},
                                  {'a': 4, 'b': 5, 'c': 6, 'd': 7}],
                      'TABLE_II': [{'a': 0, 'b': 1, 'c': 2, 'd': 3},
                                   {'a': 4, 'b': 5, 'c': 6, 'd': 7}]}]

        self.expected = {'root_0': {'PK': {0: 0}},
                         'root_0<TABLE_II_1': {'FK': {0: 0, 1: 0},
                                               'PK': {0: 0, 1: 1},
                                               'TABLE_II.a': {0: 0, 1: 4},
                                               'TABLE_II.b': {0: 1, 1: 5},
                                               'TABLE_II.c': {0: 2, 1: 6},
                                               'TABLE_II.d': {0: 3, 1: 7},
                                               'TABLE_II.subarray_IDX': {0: 0, 1: 1}},
                         'root_0<TABLE_I_1': {'FK': {0: 0, 1: 0},
                                              'PK': {0: 0, 1: 1},
                                              'TABLE_I.a': {0: 0, 1: 4},
                                              'TABLE_I.b': {0: 1, 1: 5},
                                              'TABLE_I.c': {0: 2, 1: 6},
                                              'TABLE_I.d': {0: 3, 1: 7},
                                              'TABLE_I.subarray_IDX': {0: 0, 1: 1}}}


class ArraysInObjects:
    def __init__(self):
        """
        objects with arrays
        """
        self.json = [
            {'TABLE_I': ['a', 3, True],
             'TABLE_II': ['b', 3.0, False]}]

        self.expected = {'root_0': {'PK': {0: 0}},
                         'root_0<TABLE_II_1': {'FK': {0: 0, 1: 0, 2: 0},
                                               'PK': {0: 0, 1: 1, 2: 2},
                                               'TABLE_II.TABLE_II': {0: 'b', 1: 3.0, 2: False},
                                               'TABLE_II.subarray_IDX': {0: 0, 1: 1, 2: 2}},
                         'root_0<TABLE_I_1': {'FK': {0: 0, 1: 0, 2: 0},
                                              'PK': {0: 0, 1: 1, 2: 2},
                                              'TABLE_I.TABLE_I': {0: 'a', 1: 3, 2: True},
                                              'TABLE_I.subarray_IDX': {0: 0, 1: 1, 2: 2}}}


class ArrayLeadingDiffers:
    def __init__(self):
        """
        arrays with different leading types (can break json_normalize())
        """
        self.json = [{'DATA': [[{'a': 1, 'b': 2}, 'string'],
                               ['another_string', {'a': 2, 'b': 3, 'c': 4}],
                               [True, 'another_string', {'a': 2, 'b': 3, 'c': 4}],
                               [49, 'yet_another_string']]}]

        self.expected = {'root_0': {'PK': {0: 0}},
                         'root_0<DATA_1': {'DATA.DATA_idx_0': {0: '',
                                                               1: 'another_string',
                                                               2: True,
                                                               3: 49},
                                           'DATA.DATA_idx_0_a': {0: 1.0, 1: '', 2: '', 3: ''},
                                           'DATA.DATA_idx_0_b': {0: 2.0, 1: '', 2: '', 3: ''},
                                           'DATA.DATA_idx_1': {0: 'string',
                                                               1: '',
                                                               2: 'another_string',
                                                               3: 'yet_another_string'},
                                           'DATA.DATA_idx_1_a': {0: '', 1: 2.0, 2: '', 3: ''},
                                           'DATA.DATA_idx_1_b': {0: '', 1: 3.0, 2: '', 3: ''},
                                           'DATA.DATA_idx_1_c': {0: '', 1: 4.0, 2: '', 3: ''},
                                           'DATA.DATA_idx_2': {0: '', 1: '', 2: '', 3: ''},
                                           'DATA.DATA_idx_2_a': {0: '', 1: '', 2: 2.0, 3: ''},
                                           'DATA.DATA_idx_2_b': {0: '', 1: '', 2: 3.0, 3: ''},
                                           'DATA.DATA_idx_2_c': {0: '', 1: '', 2: 4.0, 3: ''},
                                           'DATA.subarray_IDX': {0: 0, 1: 1, 2: 2, 3: 3},
                                           'FK': {0: 0, 1: 0, 2: 0, 3: 0},
                                           'PK': {0: 0, 1: 1, 2: 2, 3: 3}}}


class Complex:
    def __init__(self):
        """
        mixed types, nested objects and a mixture of objects and arrays
        """
        self.json = [{'animals': [{'name': 'faith', 'type': 'cat'},
                                  {'name': 'shadow', 'type': 'doge'}],
                      'date': '2021-01-01',
                      'other': {'mood': 'happy'},
                      'people': [{'interests': ['geetar', 'kittens', 'sillyness'], 'name': 'dave'},
                                 {'interests': ['horses', 'painting', 'mma'], 'name': 'becca'}],
                      'user_id': 'FDSA1234'},
                     {'animals': [{'name': 'felix', 'type': 'ardvark'}],
                      'date': '2021-01-02',
                      'people': [{'interests': ['motorcycles', 'geetar'], 'name': 'mike'},
                                 {'interests': ['reading', 'writing'], 'name': 'tom'}],
                      'user_id': 'ASDF4321'}]

        self.expected = {'root_0': {'PK': {0: 0, 1: 1},
                                    'root.date': {0: '2021-01-01', 1: '2021-01-02'},
                                    'root.other_mood': {0: 'happy', 1: ''},
                                    'root.user_id': {0: 'FDSA1234', 1: 'ASDF4321'}},
                         'root_0<animals_1': {'FK': {0: 0, 1: 0, 2: 1},
                                              'PK': {0: 0, 1: 1, 2: 2},
                                              'animals.name': {0: 'faith', 1: 'shadow', 2: 'felix'},
                                              'animals.subarray_IDX': {0: 0, 1: 1, 2: 0},
                                              'animals.type': {0: 'cat', 1: 'doge', 2: 'ardvark'}},
                         'root_0<people_1': {'FK': {0: 0, 1: 0, 2: 1, 3: 1},
                                             'PK': {0: 0, 1: 1, 2: 2, 3: 3},
                                             'people.name': {0: 'dave',
                                                             1: 'becca',
                                                             2: 'mike',
                                                             3: 'tom'},
                                             'people.subarray_IDX': {0: 0, 1: 1, 2: 0, 3: 1}},
                         'root_0<people_1<interests_2': {'FK': {0: 0,
                                                                1: 0,
                                                                2: 0,
                                                                3: 1,
                                                                4: 1,
                                                                5: 1,
                                                                6: 2,
                                                                7: 2,
                                                                8: 3,
                                                                9: 3},
                                                         'PK': {0: 0,
                                                                1: 1,
                                                                2: 2,
                                                                3: 3,
                                                                4: 4,
                                                                5: 5,
                                                                6: 6,
                                                                7: 7,
                                                                8: 8,
                                                                9: 9},
                                                         'interests.interests': {0: 'geetar',
                                                                                 1: 'kittens',
                                                                                 2: 'sillyness',
                                                                                 3: 'horses',
                                                                                 4: 'painting',
                                                                                 5: 'mma',
                                                                                 6: 'motorcycles',
                                                                                 7: 'geetar',
                                                                                 8: 'reading',
                                                                                 9: 'writing'},
                                                         'interests.subarray_IDX': {0: 0,
                                                                                    1: 1,
                                                                                    2: 2,
                                                                                    3: 0,
                                                                                    4: 1,
                                                                                    5: 2,
                                                                                    6: 0,
                                                                                    7: 1,
                                                                                    8: 0,
                                                                                    9: 1}}}


class Complex2:
    def __init__(self):
        """
        mixed types, nested objects and a mixture of objects and arrays

        deeper nesting than Complex()
        """
        self.json = [{'animals': [{'name': 'faith', 'type': 'cat'},
                                  {'name': 'shadow', 'type': 'doge'}],
                      'date': '2021-01-01',
                      'other': {'mood': 'happy'},
                      'people': [{'interests': [{'geetar': {'favorite': 'van halen',
                                                            'type': 'frankenstrat'}},
                                                'kittens',
                                                'sillyness'],
                                  'name': 'dave'},
                                 {'interests': ['horses', 'painting', 'mma'], 'name': 'becca'}],
                      'user_id': 'FDSA1234'},
                     {'animals': [{'name': 'felix', 'type': 'ardvark'}],
                      'date': '2021-01-02',
                      'people': [{'interests': ['motorcycles',
                                                {'geetar': {'favorite': 'hendrix',
                                                            'type': 'fender'}}],
                                  'name': 'mike'},
                                 {'interests': ['reading', 'writing'], 'name': 'tom'}],
                      'user_id': 'ASDF4321'}]

        self.expected = {'root_0': {'PK': {0: 0, 1: 1},
                                    'root.date': {0: '2021-01-01', 1: '2021-01-02'},
                                    'root.other_mood': {0: 'happy', 1: ''},
                                    'root.user_id': {0: 'FDSA1234', 1: 'ASDF4321'}},
                         'root_0<animals_1': {'FK': {0: 0, 1: 0, 2: 1},
                                              'PK': {0: 0, 1: 1, 2: 2},
                                              'animals.name': {0: 'faith', 1: 'shadow', 2: 'felix'},
                                              'animals.subarray_IDX': {0: 0, 1: 1, 2: 0},
                                              'animals.type': {0: 'cat', 1: 'doge', 2: 'ardvark'}},
                         'root_0<people_1': {'FK': {0: 0, 1: 0, 2: 1, 3: 1},
                                             'PK': {0: 0, 1: 1, 2: 2, 3: 3},
                                             'people.name': {0: 'dave',
                                                             1: 'becca',
                                                             2: 'mike',
                                                             3: 'tom'},
                                             'people.subarray_IDX': {0: 0, 1: 1, 2: 0, 3: 1}},
                         'root_0<people_1<interests_2': {'FK': {0: 0,
                                                                1: 0,
                                                                2: 0,
                                                                3: 1,
                                                                4: 1,
                                                                5: 1,
                                                                6: 2,
                                                                7: 2,
                                                                8: 3,
                                                                9: 3},
                                                         'PK': {0: 0,
                                                                1: 1,
                                                                2: 2,
                                                                3: 3,
                                                                4: 4,
                                                                5: 5,
                                                                6: 6,
                                                                7: 7,
                                                                8: 8,
                                                                9: 9},
                                                         'interests.interests': {0: 'kittens',
                                                                                 1: 'sillyness',
                                                                                 2: '',
                                                                                 3: 'horses',
                                                                                 4: 'painting',
                                                                                 5: 'mma',
                                                                                 6: 'motorcycles',
                                                                                 7: '',
                                                                                 8: 'reading',
                                                                                 9: 'writing'},
                                                         'interests.interests_geetar_favorite': {0: '',
                                                                                                 1: '',
                                                                                                 2: 'van '
                                                                                                 'halen',
                                                                                                 3: '',
                                                                                                 4: '',
                                                                                                 5: '',
                                                                                                 6: '',
                                                                                                 7: 'hendrix',
                                                                                                 8: '',
                                                                                                 9: ''},
                                                         'interests.interests_geetar_type': {0: '',
                                                                                             1: '',
                                                                                             2: 'frankenstrat',
                                                                                             3: '',
                                                                                             4: '',
                                                                                             5: '',
                                                                                             6: '',
                                                                                             7: 'fender',
                                                                                             8: '',
                                                                                             9: ''},
                                                         'interests.subarray_IDX': {0: 0,
                                                                                    1: 1,
                                                                                    2: 2,
                                                                                    3: 0,
                                                                                    4: 1,
                                                                                    5: 2,
                                                                                    6: 0,
                                                                                    7: 1,
                                                                                    8: 0,
                                                                                    9: 1}}}

        self.merged = {'root_0<animals_1': {'animals.name': {0: 'faith', 1: 'shadow', 2: 'felix'},
                                           'animals.subarray_IDX': {0: 0, 1: 1, 2: 0},
                                           'animals.type': {0: 'cat', 1: 'doge', 2: 'ardvark'},
                                           'root.date': {0: '2021-01-01',
                                                           1: '2021-01-01',
                                                           2: '2021-01-02'},
                                           'root.other_mood': {0: 'happy', 1: 'happy', 2: ''},
                                           'root.user_id': {0: 'FDSA1234',
                                                           1: 'FDSA1234',
                                                           2: 'ASDF4321'}},
                       'root_0<people_1<interests_2': {'interests.interests': {0: 'kittens',
                                                                               1: 'sillyness',
                                                                               2: '',
                                                                               3: 'horses',
                                                                               4: 'painting',
                                                                               5: 'mma',
                                                                               6: 'motorcycles',
                                                                               7: '',
                                                                               8: 'reading',
                                                                               9: 'writing'},
                                                       'interests.interests_geetar_favorite': {0: '',
                                                                                               1: '',
                                                                                               2: 'van '
                                                                                                   'halen',
                                                                                               3: '',
                                                                                               4: '',
                                                                                               5: '',
                                                                                               6: '',
                                                                                               7: 'hendrix',
                                                                                               8: '',
                                                                                               9: ''},
                                                       'interests.interests_geetar_type': {0: '',
                                                                                           1: '',
                                                                                           2: 'frankenstrat',
                                                                                           3: '',
                                                                                           4: '',
                                                                                           5: '',
                                                                                           6: '',
                                                                                           7: 'fender',
                                                                                           8: '',
                                                                                           9: ''},
                                                       'interests.subarray_IDX': {0: 0,
                                                                                   1: 1,
                                                                                   2: 2,
                                                                                   3: 0,
                                                                                   4: 1,
                                                                                   5: 2,
                                                                                   6: 0,
                                                                                   7: 1,
                                                                                   8: 0,
                                                                                   9: 1},
                                                       'people.name': {0: 'dave',
                                                                       1: 'dave',
                                                                       2: 'dave',
                                                                       3: 'becca',
                                                                       4: 'becca',
                                                                       5: 'becca',
                                                                       6: 'mike',
                                                                       7: 'mike',
                                                                       8: 'tom',
                                                                       9: 'tom'},
                                                       'people.subarray_IDX': {0: 0,
                                                                               1: 0,
                                                                               2: 0,
                                                                               3: 1,
                                                                               4: 1,
                                                                               5: 1,
                                                                               6: 0,
                                                                               7: 0,
                                                                               8: 1,
                                                                               9: 1},
                                                       'root.date': {0: '2021-01-01',
                                                                   1: '2021-01-01',
                                                                   2: '2021-01-01',
                                                                   3: '2021-01-01',
                                                                   4: '2021-01-01',
                                                                   5: '2021-01-01',
                                                                   6: '2021-01-02',
                                                                   7: '2021-01-02',
                                                                   8: '2021-01-02',
                                                                   9: '2021-01-02'},
                                                       'root.other_mood': {0: 'happy',
                                                                           1: 'happy',
                                                                           2: 'happy',
                                                                           3: 'happy',
                                                                           4: 'happy',
                                                                           5: 'happy',
                                                                           6: '',
                                                                           7: '',
                                                                           8: '',
                                                                           9: ''},
                                                       'root.user_id': {0: 'FDSA1234',
                                                                       1: 'FDSA1234',
                                                                       2: 'FDSA1234',
                                                                       3: 'FDSA1234',
                                                                       4: 'FDSA1234',
                                                                       5: 'FDSA1234',
                                                                       6: 'ASDF4321',
                                                                       7: 'ASDF4321',
                                                                       8: 'ASDF4321',
                                                                       9: 'ASDF4321'}}}


class Duplicated:
    def __init__(self):
        """
        Data object with duplicated nested key and data key that will result in duplicated column
        when broken up.
        """
        self.json = {"a": [1, True], "b": {"a": 1, "b": ["b"]}, "b_b": None}

        self.expected = {
            'root_0': {
                'PK': {
                    0: 0}, 'root.b_a': {
                    0: 1}, 'root.b_b': {
                    0: ''}}, 'root_0<a_1': {
                        'FK': {
                            0: 0, 1: 0}, 'PK': {
                                0: 0, 1: 1}, 'a.a': {
                                    0: 1, 1: True}, 'a.subarray_IDX': {
                                        0: 0, 1: 1}}, 'root_0<b.b_1': {
                                            'FK': {
                                                0: 0}, 'PK': {
                                                    0: 0}, 'b.b.b_b': {
                                                        0: 'b'}, 'b.b.subarray_IDX': {
                                                            0: 0}}}
