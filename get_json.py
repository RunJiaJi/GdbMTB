from collections import defaultdict
import json

def add_to_tree(tree, taxa_list):
    for taxa in taxa_list:
        tree = tree[taxa]  # Traverse down the tree
    return tree

def parse_classification(data):
    tree = lambda: defaultdict(tree)
    root = tree()

    for genome, classification in data.items():
        taxa_list = classification.split(';')
        node = add_to_tree(root, taxa_list)
        node['genomes'] = node.get('genomes', []) + [genome]
    
    tree_json = json.dumps(root, indent=4)
    return tree_json

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


