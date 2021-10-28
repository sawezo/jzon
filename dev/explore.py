# # standard
# import os
# import json
# import itertools
# import copy
# import pprint
from typing import Union, List, Dict, Any, Tuple

# # data science
# import pandas as pd

# # visualization
# import pydot
# from IPython.display import Image

# # configurations
# pretty = pprint.PrettyPrinter()


def compile_nested_keys(data:Union[Dict[str, Any], List[Any]], 
                        level2keys:Dict[str, List[str]]=dict(), 
                        key2value_list:Dict[str, List[Any]]=dict(), 
                        level=0, current_parent="ROOT") -> Tuple[List[str], Dict[str, List[str]], Dict[str, List[Any]]]:
    """
    generates a list of data keys and organizes the keys by index level in the data 
    
    as this is intended for json data, only lists and dicts are considered valid substructures

    the key2value_list only maps a key to individual specific values; not to subkeys
    """
    if isinstance(data, dict): # if the data is a dictionary, save the keys
        level2keys[level] = [key.lower() for key in list(data.keys())] 
        
        # pass each value through this function again in case there is nested data
        for _ in map(lambda KV: compile_nested_keys(KV[1], level2keys, key2value_list, 
                                                    level=level+1, current_parent=KV[0]), 
                     data.items()):
            continue


    elif isinstance(data, list):
        for _ in map(lambda x: compile_nested_keys(x, level2keys, key2value_list, 
                                                   level=level, current_parent=current_parent), 
                     data):
            continue  

    else: # there is only a single value which will be ignored
        if data != None: # ignoring missing data
            try:
                key2value_list[current_parent].add(data)
            except KeyError: # this key has not yet been added to the key to unique values mapping
                key2value_list[current_parent] = {data}
                
    
    unique_keys =  [k for keys in level2keys.values() for k in keys]
    return unique_keys, level2keys, key2value_list   

# def MissingPercentageByColumn(DF, return_col2percentage=False):
#     """
#     Function prints a missing data percentage by column. 
#     """
#     print("\n missing percentages by columns")
#     print("------------------------------")
    
#     # Printing the number of rows and the percentage of missing data by column. 
#     pd.set_option('display.max_rows', None)
#     missing_percentage_DF = DF.isnull().mean().sort_values()
#     display(missing_percentage_DF)
#     pd.set_option('display.max_rows', 100)
    
#     if return_col2percentage == True:
#         return missing_percentage_DF.to_dict()

# def show_unique_values_by_key(key2value_list, document2data):
#     """
#     Function prints the unique values over each key in the data files of interest, to get an idea 
#     of what the unique values look like. 
#     """
#     # Some of the keys have way to many unique values. First I filter out the ones that are not unique. 
#     for feature, value_set in key2value_list.items():
#         if len(value_set) == len(document2data.keys()):
#             print("Feature '{feat}' is unique to each data file.".format(feat=feature))

#         else:
#             print("There are {num} unique features for key '{feat}'.".format(num=len(value_set), feat=feature))
#             print("A few example values:")
#             for set_index, example_value in enumerate(itertools.islice(value_set, 3)):
#                 print("\t", example_value)
#             print("============================================================")

# def AssessDuplicates(contract2DATA, feature, only_show_example_at_feature=False):
#     """
#     Function assists in the assessment of duplicated key values. 
#     Note this function works off of the read in contract2DATA structure, thus 'feature' should not be lowercase/ should
#     match the raw data typeset (legalbusinessname vs. legalBusinessName).
#     """
#     feature_pool = []
#     duplicated = []
#     for contract in contract2DATA.keys():
#         # try: (ADD)
#         if type(feature) == str:
#             feature_value = contract2DATA[contract][feature]
#         elif len(feature) ==2:
#             feature_value = contract2DATA[contract][feature[0]][feature[1]]
#         elif len(feature) ==3:
#             feature_value = contract2DATA[contract][feature[0]][feature[1]][feature[2]]

#         if feature_value in feature_pool:
#             duplicated.append(feature_value)
#         else:
#             feature_pool.append(feature_value)
#         # except KeyError: # This feature was not in this contract. DEV: left out for now, only running constants through here. (ADD)
#         #     print(contract)
#         #     sys.exit()

#     print("There are", len(duplicated), "duplicated '{feat}' values in total.".format(feat=feature))

#     # Printing an example of the duplicated value. Note this is only printed at the specified feature 
#     # if  'only_show_example_at_feature' is True.
#     try:
#         duplicated_example = duplicated[0]
#         if type(feature) == str:
#             if only_show_example_at_feature:
#                 corresponding_files = [contract2DATA[file][feature]
#                                         for file in contract2DATA.keys()
#                                         if contract2DATA[file][feature]==duplicated_example]
#             else:
#                 corresponding_files = [contract2DATA[file]
#                                         for file in contract2DATA.keys()
#                                         if contract2DATA[file][feature]==duplicated_example]

#         elif len(feature) == 2:
#             if only_show_example_at_feature:
#                 corresponding_files = [contract2DATA[file][feature[0]][feature[1]]
#                                         for file in contract2DATA.keys()
#                                         if contract2DATA[file][feature[0]][feature[1]]==duplicated_example]
#             else:
#                 corresponding_files = [contract2DATA[file]
#                                         for file in contract2DATA.keys()
#                                         if contract2DATA[file][feature[0]][feature[1]]==duplicated_example]
#         elif len(feature) == 3:
#             if only_show_example_at_feature:
#                 corresponding_files = [contract2DATA[file][feature[0]][feature[1]][feature[2]] 
#                                         for file in contract2DATA.keys()
#                                         if contract2DATA[file][feature[0]][feature[1]][feature[2]]==duplicated_example]
#             else:
#                 corresponding_files = [contract2DATA[file] 
#                                         for file in contract2DATA.keys()
#                                         if contract2DATA[file][feature[0]][feature[1]][feature[2]]==duplicated_example]
#         print("\n\nThis example duplicated '{feat}' appears".format(feat=feature), len(corresponding_files), "times.")
#         for file in corresponding_files:
#             pretty.pprint(file)
#     except IndexError: # There were no duplicated examples. 
#         pass

# def CheckConstantFeatures(contract2DATA, contract2level2keys, max_level):
#     """
#     Function checks what features are never missing over all data files, and
#     how many unique feature counts there are at each level over all data files. 
#     """
#     constant_features = set() # A set of all features that always occur. 
#     for level in list(range(max_level)):
#         print("Index Level: ", level)

#         keys_at_level = []
#         for contract in contract2DATA.keys():
#             try:
#                 keys_at_level.append(set(contract2level2keys[contract][level]))
#             except KeyError: # No key exists at this level for this contract.
#                 pass

#         constant_keys_at_level = set.intersection(*keys_at_level)
#         print("There are {num} constant keys, listed below: ".format(num=len(constant_keys_at_level)))

#         pretty.pprint(constant_keys_at_level)
#         constant_features.update(constant_keys_at_level)
        
        
#         # Assessing how many unique feature counts there are at this level over each data file. 
#         try: 
#             unique_level_keys = set([str(contract2level2keys[contract][level]) 
#                                      for contract in list(contract2DATA.keys())])
#         except KeyError:
#             pass
#         print("Number of unique feature counts at this level: ", len(unique_level_keys))
#         print("==============================")


#     return constant_features

# def CountFeatureOccurances(attributes, contract2DATA, contract2keys):
#     """
#     Function counts the occurances of each specified feature regardless of level. 
#     """
#     attribute2tally = {}
#     for contract in contract2DATA.keys():
#         for attribute in attributes:
#             if {attribute.lower()}.issubset(contract2keys[contract]):

#                 try:
#                     attribute2tally[attribute.lower()] += 1
#                 except KeyError: # This attribute has not been seen yet.
#                     attribute2tally[attribute.lower()] = 1
       
    
#     return attribute2tally


# def IterateDataNodes(key2children_chain, data):
#     """
#     Function iterates through the nodes of a data file and compiles a tree structure for the data. 
#     """
#     for key in data.keys(): # For each node in the current data scope.
#         if type(data[key]) == dict:
#             key2children_chain[key] = IterateDataNodes({}, data[key])        
        
        
#         elif type(data[key]) == list:

#             list_item_subtrees = []
#             for list_item in data[key]:
#                 # If there is a single value at this node, we ignore it; the parent will still be drawn
#                 # since we set the key (parent) to an empty dictionary at the least.
#                 if (type(list_item) in [int, float, str, bool] or data[key]==None): 
#                     list_item_subtrees.append({key:"VALUELIST"})

#                 elif type(list_item) == dict:
#                     list_item_subtrees.append(IterateDataNodes({}, list_item))
#                 else:
#                     print(type(list_item))        
#                     sys.exit("Missing data type catch in IterateDataNodes. (a)")

#                 # Now to compile the subtrees (one for each list element at this data key) and -
#                 # get a single data tree to add at this data key of interest where a list once was. 
#                 merged_subtree = list_item_subtrees[0] # Merging the other subtrees into this one.
#                 for subtree_index in range(len(list_item_subtrees)):
#                     if subtree_index == 0: # No point to merging it into itself.
#                         continue
#                     else: # Updating the current merged subtree with the new subtree. 
#                         merged_subtree = MergeFileTrees(merged_subtree, 
#                                                         list_item_subtrees[subtree_index])
            
#                 key2children_chain[key] = merged_subtree


#         elif (type(data[key]) in [int, float, str, bool] or data[key]==None):
#             key2children_chain[key] = 'VALUE'
        
        
#         else:
#             print(type(data[key]))        
#             sys.exit("Missing data type catch in IterateDataNodes. (b)")


#     return key2children_chain

# def IterateDataNodes(key2children_chain, data):
#     """
#     Function iterates through the nodes of a data file and compiles a tree structure for the data. 
#     """
#     try:
#         for key in data.keys(): # For each node in the current data scope.
#             if (type(data[key]) == dict) or (str(type(data[key]))=="<class 'collections.OrderedDict'>"):
#                 key2children_chain[key] = IterateDataNodes({}, data[key])        
            
#             elif type(data[key]) == list:

#                 list_item_subtrees = []
#                 for list_item in data[key]:
#                     # If there is a single value at this node, we ignore it; the parent will still be drawn
#                     # since we set the key (parent) to an empty dictionary at the least.
#                     if (type(list_item) in [int, float, str, bool] or data[key]==None): 
#                         list_item_subtrees.append({key:"VALUELIST"})

#                     elif type(list_item) == dict:
#                         list_item_subtrees.append(IterateDataNodes({}, list_item))
#                     else:
#                         print(type(list_item))        
#                         sys.exit("Missing data type catch in IterateDataNodes. (a)")

#                     # Now to compile the subtrees (one for each list element at this data key) and -
#                     # get a single data tree to add at this data key of interest where a list once was. 
#                     merged_subtree = list_item_subtrees[0] # Merging the other subtrees into this one.
#                     for subtree_index in range(len(list_item_subtrees)):
#                         if subtree_index == 0: # No point to merging it into itself.
#                             continue
#                         else: # Updating the current merged subtree with the new subtree. 
#                             merged_subtree = MergeFileTrees(merged_subtree, 
#                                                             list_item_subtrees[subtree_index])
                
#                     key2children_chain[key] = merged_subtree


#             elif (type(data[key]) in [int, float, str, bool] or data[key]==None):
#                 # Adding the value and data type to the node in the tree for data management.  
#                 data_value = data[key]
#                 data_type = str(type(data_value)).split(" ")[1][1:-2]
#                 node_tag = key+"|"+data_type+"|"+str(data_value)
#                 key2children_chain[node_tag] = "VALUE"
                
#             else:
#                 print(type(data[key]))        
#                 sys.exit("Missing data type catch in IterateDataNodes. (b)")

#     except AttributeError: # If the data was not a dictionary. 
#         pass
        
#     return key2children_chain

# def IterateDataNodes(key2children_chain, data):
#     """
#     Function iterates through the nodes of a data file and compiles a tree structure for the data. 
#     """
#     for key in data.keys(): # For each node in the current data scope.
#         if (type(data[key]) == dict) or (str(type(data[key]))=="<class 'collections.OrderedDict'>"):
#             key2children_chain[key] = IterateDataNodes({}, data[key])        
        
        
#         elif type(data[key]) == list:

#             list_item_subtrees = []
#             for list_item in data[key]:
#                 # If there is a single value at this node, we ignore it; the parent will still be drawn
#                 # since we set the key (parent) to an empty dictionary at the least.
#                 if (type(list_item) in [int, float, str, bool] or data[key]==None): 
#                     list_item_subtrees.append({key:"VALUELIST"})

#                 elif type(list_item) == dict:
#                     list_item_subtrees.append(IterateDataNodes({}, list_item))
#                 else:
#                     print(type(list_item))        
#                     sys.exit("Missing data type catch in IterateDataNodes. (a)")

#                 # Now to compile the subtrees (one for each list element at this data key) and -
#                 # get a single data tree to add at this data key of interest where a list once was. 
#                 merged_subtree = list_item_subtrees[0] # Merging the other subtrees into this one.
#                 for subtree_index in range(len(list_item_subtrees)):
#                     if subtree_index == 0: # No point to merging it into itself.
#                         continue
#                     else: # Updating the current merged subtree with the new subtree. 
#                         merged_subtree = MergeFileTrees(merged_subtree, 
#                                                         list_item_subtrees[subtree_index])
            
#                 key2children_chain[key] = merged_subtree


#         elif (type(data[key]) in [int, float, str, bool] or data[key]==None):
#             key2children_chain[key] = 'VALUE'
        
        
#         else:
#             print(type(data[key]))        
#             sys.exit("Missing data type catch in IterateDataNodes. (b)")


#     return key2children_chain


# def MergeFileTrees(tree1, tree2):
#     """
#     Function merges two nested trees (dictionaries) into a single master tree by 
#     iterating through the information of the second tree and updating the first (master) accordingly.
#     """
#     for key in tree2: # For each key at this particular level of the dictionary. 
#         if key in tree1: # If the key is already in the first tree. 
            
#             if isinstance(tree2[key], dict): # If the value in the new tree at this key is a dictionary.
#                 if isinstance(tree2[key], dict): # If the first tree is also a dictionary at this key. 
                    
#                     # A recursive function call to merge the two nested dictionaries at this level. 
#                     tree1[key] = MergeFileTrees(tree1[key], tree2[key])
                   
#                 else: # The master tree at this key is not a dictionary, which means it must be "VALUE".
#                     tree1[key] = tree2[key]
                    
#             else: # The value at the new tree is not a dictionary/ is "VALUE".
#                 continue # We can ignore this since if we are here this key is already in the first tree. 
                
                
#         # This key is not already in the first tree, thus we add the information branch from the second tree. 
#         else: 
#             try:
#                 tree1[key] = tree2[key]
#             except TypeError: # The tree1 is a string.
#                 tree1 = tree2

            
#     return tree1

# def MergeFileTrees(tree1, tree2):
#     """
#     Function merges two nested trees (dictionaries) into a single master tree by 
#     iterating through the information of the second tree and updating the first (master) accordingly.
#     """
#     for key in tree2: # For each key at this particular level of the dictionary. 
#         if key in tree1: # If the key is already in the first tree. 
            
#             if isinstance(tree2[key], dict): # If the value in the new tree at this key is a dictionary.
#                 if isinstance(tree2[key], dict): # If the first tree is also a dictionary at this key. 
                    
#                     # A recursive function call to merge the two nested dictionaries at this level. 
#                     tree1[key] = MergeFileTrees(tree1[key], tree2[key])
                   
#                 else: # The master tree at this key is not a dictionary, which means it must be "VALUE".
#                     tree1[key] = tree2[key]
                    
#             else: # The value at the new tree is not a dictionary/ is "VALUE".
#                 continue # We can ignore this since if we are here this key is already in the first tree. 
                
                
#         # This key is not already in the first tree, thus we add the information branch from the second tree. 
#         else: 
#             try:
#                 tree1[key] = tree2[key]
#             except TypeError: # The tree1 is a string.
#                 tree1 = tree2

            
#     return tree1

# def MergeFileTrees(tree1, tree2):
#     """
#     Function merges two nested trees (dictionaries) into a single master tree by 
#     iterating through the information of the second tree and updating the first (master) accordingly.
#     """
#     for key in tree2: # For each key at this particular level of the dictionary. 
#         if key in tree1: # If the key is already in the first tree. 
            
#             if isinstance(tree2[key], dict): # If the value in the new tree at this key is a dictionary.
#                 if isinstance(tree2[key], dict): # If the first tree is also a dictionary at this key. 
                    
#                     # A recursive function call to merge the two nested dictionaries at this level. 
#                     tree1[key] = MergeFileTrees(tree1[key], tree2[key])
                   
#                 else: # The master tree at this key is not a dictionary, which means it must be "VALUE".
#                     tree1[key] = tree2[key]
                    
#             else: # The value at the new tree is not a dictionary/ is "VALUE".
#                 continue # We can ignore this since if we are here this key is already in the first tree. 
                
                
#         # This key is not already in the first tree, thus we add the information branch from the second tree. 
#         else: 
#             try:
#                 tree1[key] = tree2[key]
#             except TypeError: # The tree1 is a string.
#                 tree1 = tree2

            
#     return tree1


# def CompileTreeStructure(contract2DATA, consistent_structure, root_text=None):
#     """
#     Function iterates through the nodes of a JSON file and compiles a tree mapping of parents / children. 
#     """
#     first_pass = True
#     for contract in contract2DATA.keys():
#         single_key2children_chain = IterateDataNodes({}, contract2DATA[contract])

#         # If this is the first pass, we make a structure to update with the data from each file 
#         # (for non consistent structures; this will be overwritten if the structure has
#         #  a single structure/is consistent).
#         if first_pass == True: 
#             key2children_chain = single_key2children_chain 
#             first_pass = False
#             continue # Moving to the next contract.

#         # An early killswitch to save time if applicable.
#         if consistent_structure == True:
#             key2children_chain = single_key2children_chain 
#             break
#         else: # Updating the main list with the nodes of this file. 
#             key2children_chain = MergeFileTrees(key2children_chain, single_key2children_chain)

#     # Sometimes adding a root node takes up too much space, so I add the option to ignore it here.
#     if root_text != None:
#         tree = {root_text:key2children_chain}
#     else: 
#         tree = key2children_chain


#     return tree

# def CompileTreeStructure(contract2DATA, consistent_structure, root_text=None):
#     """
#     Function iterates through the nodes of a JSON file and compiles a tree mapping of parents / children. 
#     """
#     first_pass = True
#     for contract in contract2DATA.keys():
#         single_key2children_chain = IterateDataNodes({}, contract2DATA[contract])

#         # If this is the first pass, we make a structure to update with the data from each file 
#         # (for non consistent structures; this will be overwritten if the structure has
#         #  a single structure/is consistent).
#         if first_pass == True: 
#             key2children_chain = single_key2children_chain 
#             first_pass = False
#             continue # Moving to the next contract.

#         # An early killswitch to save time if applicable.
#         if consistent_structure == True:
#             key2children_chain = single_key2children_chain 
#             break
#         else: # Updating the main list with the nodes of this file. 
#             key2children_chain = MergeFileTrees(key2children_chain, single_key2children_chain)

#     # Sometimes adding a root node takes up too much space, so I add the option to ignore it here.
#     if root_text != None:
#         tree = {root_text:key2children_chain}
#     else: 
#         tree = key2children_chain


#     return tree

# def CompileTreeStructure(contract2DATA, consistent_structure, root_text=None):
#     """
#     Function iterates through the nodes of a JSON file and compiles a tree mapping of parents / children. 
#     """
#     first_pass = True
#     for contract in contract2DATA.keys():
#         single_key2children_chain = IterateDataNodes({}, contract2DATA[contract])

#         # If this is the first pass, we make a structure to update with the data from each file 
#         # (for non consistent structures; this will be overwritten if the structure has
#         #  a single structure/is consistent).
#         if first_pass == True: 
#             key2children_chain = single_key2children_chain 
#             first_pass = False
#             continue # Moving to the next contract.

#         # An early killswitch to save time if applicable.
#         if consistent_structure == True:
#             key2children_chain = single_key2children_chain 
#             break
#         else: # Updating the main list with the nodes of this file. 
#             key2children_chain = MergeFileTrees(key2children_chain, single_key2children_chain)

#     # Sometimes adding a root node takes up too much space, so I add the option to ignore it here.
#     if root_text != None:
#         tree = {root_text:key2children_chain}
#     else: 
#         tree = key2children_chain


#     return tree


# def DrawTree(graph, tree, parent=None, features_to_show_values_for2values={}):
#     """
#     Drawing the tree of the JSON structure. 
#     Note the workaround to still show values for a feature if they were in a list 
#     within the original data structure. 
#     """
#     for key, value in tree.items():
#         if (isinstance(value, dict) and value != "VALUELIST"): # If the value is a dictionary.
#             if parent: # Ignoring a parent edge for our root node. 
#                 graph = DrawEdge(parent, key, graph)
            
#             DrawTree(graph, value, key, features_to_show_values_for2values)
        
#         else: # Otherwise, if the child node is not a parent to further sub-children.
#             graph = DrawEdge(parent, key, graph) 
#             if key in features_to_show_values_for2values.keys():
#                 graph = DrawEdge(key, None, graph, 
#                                  features_to_show_values_for2values[key])

# def DrawTree(graph, tree, parent=None):
#     """
#     Drawing the tree of the JSON structure. 
#     Note the workaround to still show values for a feature if they were in a list 
#     within the original data structure. 
#     """
#     for node, child in tree.items():
#         if isinstance(child, dict): # If the child value is a dictionary.
#             if parent: # Ignoring a parent edge for our root node. 
#                 graph = DrawEdge(graph, parent, node)
            
#             graph = DrawTree(graph, child, node)
        
#         else: # Otherwise, if the child node is not a parent to further sub-children.
#             graph = DrawEdge(graph, parent, node)


#     return graph                                    

# def DrawTree(graph, tree, parent=None):
#     """
#     Drawing the tree of the JSON structure. 
#     Note the workaround to still show values for a feature if they were in a list 
#     within the original data structure. 
#     """
#     for node, child in tree.items():
#         if isinstance(child, dict): # If the child value is a dictionary.
#             if parent: # Ignoring a parent edge for our root node. 
#                 graph = DrawEdge(graph, parent, node)
            
#             graph = DrawTree(graph, child, node)
        
#         else: # Otherwise, if the child node is not a parent to further sub-children.
#             graph = DrawEdge(graph, parent, node)


#     return graph


# def DrawEdge(graph, parent, child):
#     """
#     Drawing an edge between two nodes. 
#     """
#     edge = pydot.Edge(parent.strip("ns1:"), child.strip("ns1:"))
#     graph.add_edge(edge)

#     print("drew an edge from ", parent, " to: ", child)

#     return graph

# def DrawEdge(v1, v2, graph, feature_values=None):
#     """
#     Drawing an edge between two nodes. 
#     """
#     # Drawing actual values, but only for specific features. 
#     if feature_values != None: 
#         for value in feature_values:
#             edge = pydot.Edge(v1, value, color="red")
#             graph.add_edge(edge)

#     else: # Not a special call for the drawing of individual values. 
#         # Not drawing any values, as this will be redundant. 
#         if ("VALUE" not in v2 and v1 != v2):
#             edge = pydot.Edge(v1, v2)
#             graph.add_edge(edge)


#     return graph

# def DrawEdge(graph, parent, child):
#     """
#     Drawing an edge between two nodes. 
#     """
#     # Not drawing any values, as this will be redundant. 
    
#     edge = pydot.Edge(parent.strip("ns1:"), child.strip("ns1:"))
#     graph.add_edge(edge)

#     print("drew an edge from ", parent, " to: ", child)

#     return graph


# def ShowTree(pdot):
#     """
#     Showing the constructed tree in a Jupyter Notebook. 
#     """
#     viz = Image(pdot.create_png())
#     display(viz)

# def Treeify(endpoint, sample):
#     """
#     Function draws and saves a nested data structure to an output. 
#     """
#     # Setting up the feature tree structure to visualize. 
#     tree = CompileTreeStructure(contract2DATA={"Sample":sample}, consistent_structure=True, root_text="SAMPLE")

#     # Drawing the tree.
#     graph = pydot.Dot(graph_type='digraph', rankdir="LR", prog="neato", 
#                       label=endpoint, labelloc="top")

#     graph = DrawTree(graph, tree)


#     # Showing and saving the tree. 
#     graph.write_png('../Documentation/Images/NodeStructures/{e}.png'.format(e=endpoint.replace("/", "|"))) # Saving the tree to a file. 



#     # Setting up the feature tree structure to visualize. 
#     tree = CompileTreeStructure(contract2DATA={"Sample":sample_entry}, consistent_structure=True, root_text="RECIPIENT")

#     # Drawing the tree.
#     graph = pydot.Dot(graph_type='digraph', rankdir="LR", prog="neato", 
#                     label="Key Structure in FPDS Data", labelloc="top")

#     graph = DrawTree(graph, tree)

#     # Showing and saving the tree. 
#     graph.write_png('../Documentation/Images/NodeStructures/FPDS_structure.png') # Saving the tree to a file. 