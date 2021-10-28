# ```jzon```

## Contents:
* [Description](#description)
* [Breakdown](#breakdown)
* [Exploration](#exploration)

&#10071;: <b>Note that 'Exploration' functionality is still in development.</b>

## Setup


```python
# standard
import sys

# data science
import pandas as pd

# module
from src import breakdown, merge
```

## Description
<a class="anchor" id="description"></a>

This module was designed to help you handle JSON files. Though there exists some functionality in common packages to help handle ```.json``` files, there are many cases where existing functionality is not flexible. 

The current implementation helps you explore and break down deeply nested files into individual tables. Here 'nested' not only refers to nested objects (```{"a":{"b":"c"}}```) but also nested arrays (```{"a":{"b":["c"]}```) and complex files with different types in arrays. This is important because existing functionality (e.g. Panda's ```DataFrame.json_normalize()```) and would likely either break or improperly convert data of such forms.

Future implementation will also enable the key mapping and exploration of complex files by providing functions to generate graph diagrams of keys and their respective value types over all documents.  

## Breakdown 
<a class="anchor" id="breakdown"></a>

### Getting Atomic Tables

Say we want to break this down into flat files, with each subarray represented as a new table (to avoid extremely complex files). In this case, Panda's ```json_normalize()``` functionality won't unpack the nested subarrays. Even if we add specific commands to unpack one of them through all levels of the nested hierarchy, it wouldn't do so as desired.

This is easiest to see with mock JSON data that has a slightly confusing schema (noting there are much more complex formats in the wild!):


```python
data = \
[{'animals': [{'name': 'faith', 'type': 'cat'},
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
```


```python
pd.json_normalize(data) # people/animals still compacted
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>animals</th>
      <th>date</th>
      <th>people</th>
      <th>user_id</th>
      <th>other.mood</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>[{'name': 'faith', 'type': 'cat'}, {'name': 's...</td>
      <td>2021-01-01</td>
      <td>[{'interests': [{'geetar': {'favorite': 'van h...</td>
      <td>FDSA1234</td>
      <td>happy</td>
    </tr>
    <tr>
      <th>1</th>
      <td>[{'name': 'felix', 'type': 'ardvark'}]</td>
      <td>2021-01-02</td>
      <td>[{'interests': ['motorcycles', {'geetar': {'fa...</td>
      <td>ASDF4321</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>



This is where the current module comes in.


```python
table_tag2df = breakdown.dev(data)

print(list(table_tag2df.keys())) # the atomic tables that were created 
display(table_tag2df["root_0<animals_1"]) # an example
```

    ['root_0', 'root_0<animals_1', 'root_0<people_1', 'root_0<people_1<interests_2']



<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PK</th>
      <th>FK</th>
      <th>animals.subarray_IDX</th>
      <th>animals.name</th>
      <th>animals.type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>faith</td>
      <td>cat</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>shadow</td>
      <td>doge</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>1</td>
      <td>0</td>
      <td>felix</td>
      <td>ardvark</td>
    </tr>
  </tbody>
</table>
</div>


### Getting Merged Tables for Each Table Chain

What if we want to do some cleaning and get rid of all of the individual atomic tables? To do this, we can merge them together. This is done so that each unique 'chain' from root node 'A' to the deepest child nodes are created. Note that redundant chains are ignored. In other words, a merge of parent table A and child table B will not be created if there is also a merge of parent table A with child table B that has child table C. However, if there is another possible child of table B (call it C2), then two merges would be made: A-B-C and A-B-C2. 


```python
# merging
tag2df = merge.merge_tables(table_tag2df)
```

    
     ✅ creating table over chain 'root_0<people_1<interests_2'
    
     ✅ creating table over chain 'root_0<animals_1'
    ❌ skipping root_0<people_1 since it has subtables



```python
# the resulting tables
for merged_tag, merged_tag_df in tag2df.items():
    print(f"Merged table tag: {merged_tag}")
    display(merged_tag_df.head(3))
```

    Merged table tag: root_0<people_1<interests_2



<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>root.date</th>
      <th>root.user_id</th>
      <th>root.other_mood</th>
      <th>people.subarray_IDX</th>
      <th>people.name</th>
      <th>interests.subarray_IDX</th>
      <th>interests.interests_geetar_favorite</th>
      <th>interests.interests_geetar_type</th>
      <th>interests.interests</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2021-01-01</td>
      <td>FDSA1234</td>
      <td>happy</td>
      <td>0</td>
      <td>dave</td>
      <td>0</td>
      <td></td>
      <td></td>
      <td>kittens</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2021-01-01</td>
      <td>FDSA1234</td>
      <td>happy</td>
      <td>0</td>
      <td>dave</td>
      <td>1</td>
      <td></td>
      <td></td>
      <td>sillyness</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2021-01-01</td>
      <td>FDSA1234</td>
      <td>happy</td>
      <td>0</td>
      <td>dave</td>
      <td>2</td>
      <td>van halen</td>
      <td>frankenstrat</td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>


    Merged table tag: root_0<animals_1



<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>root.date</th>
      <th>root.user_id</th>
      <th>root.other_mood</th>
      <th>animals.subarray_IDX</th>
      <th>animals.name</th>
      <th>animals.type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2021-01-01</td>
      <td>FDSA1234</td>
      <td>happy</td>
      <td>0</td>
      <td>faith</td>
      <td>cat</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2021-01-01</td>
      <td>FDSA1234</td>
      <td>happy</td>
      <td>1</td>
      <td>shadow</td>
      <td>doge</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2021-01-02</td>
      <td>ASDF4321</td>
      <td></td>
      <td>0</td>
      <td>felix</td>
      <td>ardvark</td>
    </tr>
  </tbody>
</table>
</div>



```python
# compare with the original data
pd.DataFrame(data)
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>animals</th>
      <th>date</th>
      <th>other</th>
      <th>people</th>
      <th>user_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>[{'name': 'faith', 'type': 'cat'}, {'name': 's...</td>
      <td>2021-01-01</td>
      <td>{'mood': 'happy'}</td>
      <td>[{'interests': [{'geetar': {'favorite': 'van h...</td>
      <td>FDSA1234</td>
    </tr>
    <tr>
      <th>1</th>
      <td>[{'name': 'felix', 'type': 'ardvark'}]</td>
      <td>2021-01-02</td>
      <td>NaN</td>
      <td>[{'interests': ['motorcycles', {'geetar': {'fa...</td>
      <td>ASDF4321</td>
    </tr>
  </tbody>
</table>
</div>



Each merged table is associated with a compound tag of a specific format:
- the ```<``` delimiter separates a parent (left) from a child (right) table where the right table is a subarray under the parent table (```{a:[{b:c}]}``` -> ```a<b```)
    - to track what index of the array the row is respective to, there is a corresponding ```subarray_IDX``` feature
    - the ```FK``` of the child table on the right of a ```<``` maps to the PK of the table on the left of a ```<``` (the parent table)
- the items inbetween the ```<``` delimiters give lower-level table details
    - the left of a ```_``` is the 'overall feature' the table describes, being the key in the original object that maps to the subarray of information the table represents 
    - the right is the subarray 'level'
- a ```.``` in a column name indicates that the feature was found in a nested object (```{a:{b:c}}``` -> ```a.b=c```)
