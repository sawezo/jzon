"""
testing suite

to run tests enter `pytest run.py [--disable-pytest-warnings]` in shell
"""

# standard
import sys
import pytest

# module
from mock_structures import *
sys.path.append("../src/")
import breakdown, merge


# fixtures
@pytest.fixture
def nested_objects():
    return NestedObject()


@pytest.fixture
def nested_objects_multiple_types_deep():
    return NestedObjectMultipleTypes()


@pytest.fixture
def simple_array():
    return SimpleArray()


@pytest.fixture
def nested_array():
    return NestedArray()


@pytest.fixture
def objects_in_arrays():
    return ObjectsInArrays()


@pytest.fixture
def arrays_in_objects():
    return ArraysInObjects()


@pytest.fixture
def array_leading_differs():
    return ArrayLeadingDiffers()


@pytest.fixture
def complex_():
    return Complex()


@pytest.fixture
def complex2_():
    return Complex2()


@pytest.fixture
def duplicated():
    return Duplicated()


# functions
def assert_over_tag2df(tag2df, object_, merged=False):
    """
    run table checks over each k, v pair of the breakdown return object
    """
    if not merged: # testing flattened file
        for tag, df in tag2df.items():
            assert(df.to_dict() == object_.expected[tag])
    else: # testing merged outputs
        for tag, df in tag2df.items():
            assert(df.to_dict() == object_.merged[tag])



# tests
def test_nested_object_data(nested_objects):
    tag2df = breakdown.breakdown_json(nested_objects.json)
    assert_over_tag2df(tag2df, nested_objects)


def test_nested_objects_multiple_types_deep(
        nested_objects_multiple_types_deep):
    tag2df = breakdown.breakdown_json(nested_objects_multiple_types_deep.json)
    assert_over_tag2df(tag2df, nested_objects_multiple_types_deep)


def test_simple_array(simple_array):
    tag2df = breakdown.breakdown_json(simple_array.json)
    assert_over_tag2df(tag2df, simple_array)


def test_nested_array(nested_array):
    tag2df = breakdown.breakdown_json(nested_array.json)
    assert_over_tag2df(tag2df, nested_array)


def test_objects_in_arrays_data(objects_in_arrays):
    tag2df = breakdown.breakdown_json(objects_in_arrays.json)
    assert_over_tag2df(tag2df, objects_in_arrays)


def test_arrays_in_objects(arrays_in_objects):
    tag2df = breakdown.breakdown_json(arrays_in_objects.json)
    assert_over_tag2df(tag2df, arrays_in_objects)


def test_array_leading_differs(array_leading_differs):
    tag2df = breakdown.breakdown_json(array_leading_differs.json)
    assert_over_tag2df(tag2df, array_leading_differs)


def test_complex_(complex_):
    tag2df = breakdown.breakdown_json(complex_.json)
    assert_over_tag2df(tag2df, complex_)


def test_complex2_(complex2_):
    tag2df = breakdown.breakdown_json(complex2_.json)
    assert_over_tag2df(tag2df, complex2_)


def test_duplicated(duplicated):
    tag2df = breakdown.breakdown_json(duplicated.json)
    assert_over_tag2df(tag2df, duplicated)


def test_merge(complex2_):
    tag2df = breakdown.breakdown_json(complex2_.json)
    merged_tag2df = merge.merge_tables(tag2df)
    assert_over_tag2df(merged_tag2df, complex2_, merged=True)