"""
Breakdown a JSON file into a set of atomic tables.

Assumes the four JSON rules:
    1. Data is in name/value pairs.
    2. Data is separated by commas.
    3. Curly braces hold objects.
    4. Square brackets hold arrays.

@author Samuel Zonay
"""


# standard
import json
from IPython.display import display
from typing import Union, List, Dict, Any, TypeVar, Tuple

# data science
import numpy as np
import pandas as pd


# configurations
pd.options.mode.chained_assignment = None


# variables
PandasDataFrame = TypeVar("pd.DataFrame")
DEBUG = False  # set to True for steps taken to break down data


# breaking down json into atomic tables
def initial_data_setup(data: Union[List[Dict[str,
                                             Any]],
                                   Dict[str,
                                        Any]],
                       endpoint_name: str) -> Tuple[PandasDataFrame,
                                                    Dict[str,
                                                         PandasDataFrame],
                                                    Dict[str,
                                                         PandasDataFrame]]:
    """
    Setup initial data structures for main loop.
    """
    if isinstance(data, dict):  # ensure consistency in usage/testing
        data = [data]
    df = pd.DataFrame(data)

    return df, {f"{endpoint_name}_0": df}, dict()


def get_next_item_to_breakdown(df: PandasDataFrame,
                               table_tag2df: Dict[str,
                                                  PandasDataFrame]) -> Tuple[str,
                                                                             PandasDataFrame,
                                                                             str,
                                                                             str]:
    """
    Setup next dataframe to breakdown. This is the new'parent' dataframe.
    """
    current_df_tag, df = next(iter(table_tag2df.items()))
    current_level = int(current_df_tag.split("_")[-1])
    current_pk_col = current_df_tag + "_PK"

    return current_df_tag, df, current_level, current_pk_col


def reorder_cell_array_values(values: List[Any]) -> List[Any]:
    """
    Reorder array items to avoid json_normalize() errors.
    """
    cells_with_reordered_vals = list()
    for cell_value in values:
        if isinstance(cell_value, list):

            # order any type, then dictionaries then finally arrays
            reordered_subitems = [
                val for val in cell_value if not isinstance(
                    val, dict) and not isinstance(
                    val, list)] + [
                val for val in cell_value if isinstance(
                    val, dict)] + [
                        val for val in cell_value if isinstance(
                            val, list)]
            cells_with_reordered_vals.append(reordered_subitems)
        else:
            cells_with_reordered_vals.append(cell_value)

    return cells_with_reordered_vals


def rename_expanded_array_cols(
        df: PandasDataFrame,
        col_to_break: str) -> PandasDataFrame:
    """
    Renaming new expanded cols (default is parent array index).
    """
    # catching when expanded column is named '0' (if full of
    # lists)
    integer_columns = [
        col for col in df.columns if isinstance(
            col, int)]

    # if there was an array in the array, cols
    # renamed with the index to avoid integer column names
    if len(integer_columns) > 1:
        new_names = [
            col_to_break +
            f"_idx_{num}" for num in integer_columns]
    else:
        # no need for additional idx tracking
        new_names = [col_to_break]

    col2rename = dict(zip(integer_columns, new_names))
    df.rename(col2rename, axis=1, inplace=True)

    return df


def get_cols_with_vals_of_types(
        df: PandasDataFrame,
        types: List[str]) -> List[str]:
    """
    Figure out what columns contain values of certain types (will be broken up).

    Columns returned contained at least one value that is of at least one of the specified types.
    """
    cols_to_breakdown = list()
    for col in list(df):
        # if any values in column are of this type, need to breakdown feature
        if any([str(type_) in {str(type(v))
               for v in df[col]} for type_ in types]):
            cols_to_breakdown.append(col)

    return cols_to_breakdown


def update_breakdown_cols(type2cols_to_breakdown: Dict[str,
                                                       List[str]],
                          df: PandasDataFrame) -> Tuple[bool,
                                                        Dict[str,
                                                             List[str]]]:
    """
    Check for additional columns to breakdown after first breakdown.
    """
    for type_ in type2cols_to_breakdown:
        type2cols_to_breakdown[type_].extend(get_cols_with_vals_of_types(
            df, [type_]))  # the previously expanded column dataframe

    return type2cols_to_breakdown


def get_cell_datatypes_by_index(
        df: PandasDataFrame, col_to_break: str) -> Tuple[Dict[int, str], Dict[str, List[int]]]:
    """
    Generate a mapping/reverse mapping of indices to cell value type.
    """
    idx2type = {idx: str(type(value))
                for idx, value in df[col_to_break].items()}
    type2idxs = {type_: [idx for idx in idx2type if idx2type[idx] == type_]
                 for type_ in idx2type.values()}

    return idx2type, type2idxs


def process_expanded_column_child_table(
        df: PandasDataFrame,
        current_pk_col: str,
        drop_empty: bool) -> PandasDataFrame:
    """
    Intermediate processing of table (remove empty rows/column if desired, rename features, etc.).

    Done while current name tag is in scope.
    """
    # adding subarray index feature (resets at each parent PK value  parent)
    df["subarray_IDX"] = df.groupby(current_pk_col)[current_pk_col].cumcount()

    # this child table references PK of parent table (focus in breakdown_json
    # main loop)
    df.rename({current_pk_col: "FK"}, axis=1, inplace=True)
    # this table's PK will be added later when this table is the 'current_df'
    # in breakdown_json main loop

    # drop cols without data (if desired)
    if drop_empty:
        df.replace({None: np.nan}, inplace=True)
        df.dropna(how="all", axis=1, inplace=True)

    # NaNs result if there was an object in a list that was broken out into
    # its own cols
    df.fillna("", inplace=True)

    return df


def process_expanded_column_object_only_table(
        df: PandasDataFrame,
        drop_empty: bool) -> PandasDataFrame:
    """
    for columns that only contained dictionaries before breaking down (and therefore arent child tables but
    are rather going to be remerged back with the original parent frame)
    """
    # drop cols with no actual data (only here because they had values for
    # indexing)
    if drop_empty:
        df.replace({None: np.nan}, inplace=True)
        df.dropna(how="all", axis=1, inplace=True)

    return df


def process_final_table(
        df: PandasDataFrame,
        current_pk_col: str,
        current_df_tag: str) -> PandasDataFrame:
    """
    final processing of fully expanded data table

    completely empty columns are not dropped (in case there will be data there in the future)
    """
    # renames
    df.rename({current_pk_col: "PK"}, axis=1, inplace=True)

    # sort cols (note some may not have fk/subarray idx (i.e. root table))
    idx_cols = [c for c in ["PK", "FK", "subarray_IDX"] if c in list(df)]
    df = df[idx_cols + [c for c in list(df) if c not in idx_cols]]

    df.fillna("", inplace=True)

    # add parent frame tags
    parent_df_tag = "_".join(current_df_tag.split("<")[-1].split("_")[:-1])
    df.columns = [
        parent_df_tag +
        "." +
        str(c).replace(
            ".",
            "_") if c not in [
            "PK",
            "FK"] else str(c) for c in list(df)]

    # dropping duplicates; this is done including PK/FK to avoid leaving out
    # data matches during merging
    df.drop_duplicates(inplace=True)

    # tidy
    df.reset_index(drop=True, inplace=True)

    return df


def add_frame_to_breakdown_queue(
        broken_down_col: str,
        current_level: str,
        current_df_tag: str,
        table_tag2df: Dict[str, PandasDataFrame],
        expanded_col_df: PandasDataFrame) -> Dict[str, PandasDataFrame]:
    """
    Add a dataframe to the mapping of items to be further broken down (as needed).
    """
    expanded_level = current_level + 1  # this expanded column table is a level deeper
    table_tag2df[f"{current_df_tag}<{broken_down_col}_{expanded_level}"] = expanded_col_df

    return table_tag2df


def breakdown_single_column(
        df: PandasDataFrame,
        col_to_break: str,
        current_pk_col: str) -> PandasDataFrame:
    """
    Breakdown cell values in a single column.

    To do this the values in this column are sorted by value type.
    This is to avoid breaking down items that aren't meant to be broken up (e.g.
    dont want 'abc' ---> 'a' 'b' 'c') and to avoid json_normalize() errors.
    """
    df = df[[col_to_break, current_pk_col]]  # don't duplicate other columns

    # methodology differs slightly depending on datatype in cell
    idx2type, type2idxs = get_cell_datatypes_by_index(df, col_to_break)

    # reorder array items to avoid json_normalize() errors
    if "<class 'list'>" in type2idxs:
        cells_with_reordered_vals = reorder_cell_array_values(df[col_to_break])
        df[col_to_break] = cells_with_reordered_vals

    # break up each cell value (dependent on if list/object) or leave alone if
    # simple value
    non_breakdown_idxs, expanded_items = list(), list()
    for type_, idxs in type2idxs.items():

        # not a cell value to breakdown
        if type_ not in ["<class 'dict'>", "<class 'list'>"]:
            # ignore non-breakdown cells if they are all NaN (parsed as float)
            if len(df.iloc[idxs].dropna()) > 0:
                # if here col to breakdown will also be in expanded dataframe
                # with these simple values
                non_breakdown_idxs.extend(idxs)

        else:  # this is a cell to breakdown
            normed_json = json.loads(df.iloc[idxs].to_json(orient="records"))

            if type_ == "<class 'dict'>":
                # dicts to breakdown so dont provide record_path (want separate
                # cols and not rows for each key)
                expanded_type_df = pd.json_normalize(
                    data=normed_json, meta=current_pk_col)

            elif type_ == "<class 'list'>":
                expanded_type_df = pd.json_normalize(data=normed_json,

                                                     # only breakdown this
                                                     # column
                                                     record_path=str(
                                                         col_to_break),

                                                     # keep 'parent' level row
                                                     # index as FK to merge
                                                     # with parent table
                                                     meta=[current_pk_col,
                                                           "subarray_IDX"],

                                                     errors='ignore')  # ignore when subarray_IDX is not present

                # renaming new expanded cols (default is parent array index)
                expanded_type_df = rename_expanded_array_cols(
                    expanded_type_df, col_to_break)

            expanded_items.append(expanded_type_df)

    # the items that should be left unchanged (if no values to breakup in some
    # cells)
    if len(non_breakdown_idxs) > 0:
        expanded_items.append(df.iloc[non_breakdown_idxs])
    expanded_col_df = pd.concat(expanded_items, axis=0)

    return expanded_col_df


def post_object_only_expansion(col_to_break: str,
                               current_pk_col: str,
                               drop_empty: str,
                               type2cols_to_breakdown: Dict[str,
                                                            List[str]],
                               df: PandasDataFrame,
                               expanded_col_df: PandasDataFrame) -> Tuple[PandasDataFrame,
                                                                          PandasDataFrame]:
    """
    Handle the outcome of an expanded column that only had objects to breakdown.
    """
    expanded_col_df = process_expanded_column_object_only_table(
        expanded_col_df, drop_empty)

    # left merge since a None in the object cell expanded would
    # throw out data over other columns
    df = df[[c for c in df.columns if c != col_to_break]].merge(
        expanded_col_df, on=current_pk_col, how="left")
    if DEBUG:
        print("resulting in updating parent frame with following df:")
        display(expanded_col_df.head(3))

    return expanded_col_df, df


def post_array_expansion(current_pk_col: str,
                         col_to_break: str,
                         current_level: str,
                         current_df_tag: str,
                         expanded_col_df: PandasDataFrame,
                         df: PandasDataFrame,
                         drop_empty: bool,
                         table_tag2df: Dict[str,
                                            PandasDataFrame]) -> Tuple[PandasDataFrame,
                                                                       PandasDataFrame,
                                                                       Dict[str,
                                                                            PandasDataFrame]]:
    """
    Handling the outcome of an expansion of a column that contained at least one array.
    """
    expanded_col_df = process_expanded_column_child_table(
        expanded_col_df, current_pk_col, drop_empty)
    if DEBUG:
        print("resulting in child frame:")
        display(expanded_col_df.head(3))

    # new table will also need to be checked for cols to breakdown
    table_tag2df = add_frame_to_breakdown_queue(
        col_to_break,
        current_level,
        current_df_tag,
        table_tag2df,
        expanded_col_df)

    # drop the now-expanded column from the current loop-level df
    # done in merge for object-only cells
    df.drop([col_to_break], axis=1, inplace=True)

    return df, expanded_col_df, table_tag2df


def breakdown_columns(df: PandasDataFrame,
                      current_df_tag: str,
                      current_pk_col: str,
                      drop_empty: bool,
                      current_level: int,
                      table_tag2df: Dict[str,
                                         PandasDataFrame]) -> Tuple[PandasDataFrame,
                                                                    Dict[str,
                                                                         PandasDataFrame]]:
    """
    Breaking down columns (cols that contain arrays/objects) for the current 'parent' dataframe.

    Done separately by type since different orders of types will break pandas json_normalize() in multi-type arrays.
    """
    if DEBUG:
        print(f"new parent df with tag {current_df_tag}:")
        display(df.head(3))

    type2cols_to_breakdown = {
        str(type_): get_cols_with_vals_of_types(df, [type_])
        for type_ in [dict, list]}

    idx = 0
    last_expanded_object, expanded_col_df = False, None
    while True:  # still columns to breakdown
        idx += 1
        # if last item expanded was an object, make sure no new cols of concern
        # were merged back into frame
        if last_expanded_object:  # only pass expanded col df since this will be trimmed to the new columns in the parent frame
            type2cols_to_breakdown = update_breakdown_cols(
                type2cols_to_breakdown, expanded_col_df)

        # get the next column to breakdown
        try:
            type_, col_to_break = [
                (type_, col) for type_, cols in type2cols_to_breakdown.items()
                for col in cols][0]
            if DEBUG:
                print(f"breaking down column '{col_to_break}'")
        except IndexError:
            break  # all done with this data frame

        expanded_col_df = breakdown_single_column(
            df, col_to_break, current_pk_col)

        # if col had only subdictionaries, merge broken frame back into parent
        if col_to_break not in type2cols_to_breakdown["<class 'list'>"]:
            expanded_col_df, df = post_object_only_expansion(
                col_to_break, current_pk_col, drop_empty,
                type2cols_to_breakdown, df, expanded_col_df)
            last_expanded_object = True

        else:  # if at least one cell in col had a subarray, make new child table
            df, expanded_col_df, table_tag2df = post_array_expansion(
                current_pk_col, col_to_break, current_level, current_df_tag,
                expanded_col_df, df, drop_empty, table_tag2df)
            last_expanded_object = False

        # remove col from breakdown list
        type2cols_to_breakdown[type_].remove(col_to_break)

    return df, table_tag2df


def breakdown_json(data: Union[List[Dict[str, Any]], Dict[str, Any]],
                   endpoint_name: str = "root",
                   drop_empty: bool = False) -> Dict[str, PandasDataFrame]:
    """
    Unpacks json data and converts to multiple long-form 'atomic' dataframes.

    Panda's `json_normalize()` is helpful but not too flexible, especially when dealing with nested subarrays.
    Thus this code essentially wraps this functionality while organizing the resulting unpacked data.
    """
    # prepare initial dataframe
    df, table_tag2df, table_tag2processed_df = initial_data_setup(
        data, endpoint_name)

    # main breakdown loop
    while True:  # still items to break down

        try:  # get next item in 'queue' of tables to attempt to expand
            current_df_tag, df, current_level, current_pk_col = get_next_item_to_breakdown(
                df, table_tag2df)
        except StopIteration:  # no more data in the queue
            break
        else:
            # adding a unique primary key
            df.reset_index(inplace=True, drop=True)
            df[current_pk_col] = df.index

            # breakdown the columns
            df, table_tag2df = breakdown_columns(
                df, current_df_tag, current_pk_col, drop_empty, current_level, table_tag2df)

            # process current reference-point dataframe then remove from the 'need
            # to expand' queue
            table_tag2processed_df[current_df_tag] = process_final_table(
                df, current_pk_col, current_df_tag)
            del table_tag2df[current_df_tag]

    return table_tag2processed_df


# development
def dev(data, mode=None):
    """
    wrapper for development in place of decorator
    """
    global DEBUG
    if mode == "DEBUG":
        DEBUG = True
    else:
        DEBUG = False  # set to False if running tests

    return breakdown_json(data)
