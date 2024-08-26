from collections import defaultdict, OrderedDict
import json

def sort_dict(tree):
    """
    Recursively sort a nested dictionary by its keys.
    """
    if isinstance(tree, dict):
        # Create an OrderedDict to maintain sorted order
        sorted_dict = OrderedDict()
        for key, value in sorted(tree.items()):
            sorted_dict[key] = sort_dict(value)  # Recursively process values
        return sorted_dict
    elif isinstance(tree, list):
        # Apply sorting to each dictionary item in the list
        return [sort_dict(item) for item in tree]
    else:
        # Return non-dict values as-is
        return tree

def add_to_tree(tree, taxa_list, genome):
    for taxa in taxa_list[:-1]:
        tree = tree[taxa]  # Traverse down the tree
    tree[taxa_list[-1]] = tree.get(taxa_list[-1], []) + [genome]
    return tree

def parse_classification(data):
    tree = lambda: defaultdict(tree)
    root = tree()

    for genome, classification in data.items():
        taxa_list = classification.split(';')
        add_to_tree(root, taxa_list, genome)
    
    tree_json = json.dumps(root, indent=4)
    tree_dict = json.loads(tree_json)
    # counted_tree, _ = count_genomes(tree_dict)
    updated_tree = sort_dict(tree_dict)
    updated_tree_json = json.dumps(updated_tree, indent=4)
    return updated_tree_json

def get_data(meta_df):
    data={}

    idList = meta_df.ID.tolist()
    taxaList = meta_df['GTDB_r220_classification'].tolist()

    for i, j in zip(idList, taxaList):
        data[i]=j
    return data

def build_tree(meta_df):
    data = get_data(meta_df)
    tree_json = parse_classification(data)
    return tree_json

def get_external_links(meta_df):
    idList = meta_df.ID.tolist()
    exLink1s = meta_df['External link 1']
    exLink2s = meta_df['External link 2']
    idToExternalLink = {}
    for idx in range(len(idList)):
        exLinks = [exLink1s[idx], exLink2s[idx]]
        idToExternalLink[idList[idx]] = exLinks
    return idToExternalLink



