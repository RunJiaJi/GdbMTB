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
    
    return root


