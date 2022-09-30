import numpy as np
class TreeNode:
    def __init__(self, leafID, children, lengths, binary=False):
        self.leafID = leafID
        self.children = children
        self.lengths = lengths
        self.binary = binary
    def get_num_nodes(self):
        num_nodes = 1
        if self.children:
            for i in range(len(self.children)):
                num_nodes += self.children[i].get_num_nodes()
        return num_nodes

def find_matching_parens_idx(string):
    stack_height = 1
    for i in range(len(string)):
        if string[i] == '(':
            stack_height += 1
        elif string[i] == ')':
            stack_height -= 1
        if stack_height == 0:
            return i
        else:
            i += 1
    raise IndexError("no matching parens found!")

def get_len_and_next_idx(newick_str, start_idx):
    j = start_idx
    while j <= len(newick_str):
        if j == len(newick_str) or newick_str[j] == ',':
            length = float(newick_str[start_idx:j])
            return length, j + 1
        else:
            j += 1

def newick_to_tree_rec(newick_str):
    children = []
    lengths = []
    i = 0
    while i < len(newick_str):
        if newick_str[i] == "(":
            end_idx = find_matching_parens_idx(newick_str[i+1:])
            childNode = newick_to_tree_rec(newick_str[i+1:i+1+end_idx])
            children.append(childNode)
            length, next_idx = get_len_and_next_idx(newick_str, i+1+end_idx + 2)
            lengths.append(length)
            i = next_idx
        else:
            leafID = int(newick_str[i]) #doesn't generalize to multi-digit leaf labels
            leafNode = TreeNode(leafID=leafID,children=None,lengths=None)
            children.append(leafNode)
            length, next_idx = get_len_and_next_idx(newick_str, i + 2)
            lengths.append(length)
            i = next_idx
    return TreeNode(leafID=-1, children=children, lengths=lengths)

def convert_tree_to_binary_rec(node:TreeNode):
    if node.children is None:
        node.binary = True
        return node
    elif len(node.children) == 2:
        new_left_node = convert_tree_to_binary_rec(node.children[0])
        new_right_node = convert_tree_to_binary_rec(node.children[1])
        return TreeNode(leafID=-1, children=[new_left_node, new_right_node], lengths=node.lengths, binary=True)
    elif len(node.children) > 2:
        new_left_node = convert_tree_to_binary_rec(node.children[0])
        new_right_node = TreeNode(leafID=-1, children=node.children[1:], lengths=node.lengths[1:])
        new_right_node = convert_tree_to_binary_rec(new_right_node)
        new_children = [new_left_node, new_right_node]
        new_lengths = [node.lengths[0], np.mean(node.lengths[1:])]
        return TreeNode(leafID=-1, children=new_children, lengths=new_lengths, binary=True)

def newick_to_tree(newick_str):
    if newick_str[-1] == ";":
        newick_str = newick_str[:-1]
    print("newick str: {}".format(newick_str))
    return newick_to_tree_rec(newick_str[1:-1])

def newick_to_treenode(newick_str):
    tree = newick_to_tree(newick_str)
    print("original number of nodes:{}".format(tree.get_num_nodes()))
    tree = convert_tree_to_binary_rec(tree)
    print("binary number of nodes:{}".format(tree.get_num_nodes()))
    return tree

def check_tree(node:TreeNode, level=0):
    if node.children is None:
        num_children = 0
    else:
        num_children = len(node.children)
        for i in range(num_children):
            check_tree(node.children[i], level + 1)
    print("level: {}, num_children: {}".format(level, num_children))
    print(node.lengths)
mean_newick = "((((((0:10.992344951,8:18.3469999877):0.0055844803,3:11.2841961677):0.0023049787,1:12.4539381766):0.0013692922,6:13.6323866119):0.0019777971,(2:12.3960489787,7:16.6629964286):0.0079167817):0.0028297773,((4:16.3060502795,5:14.870542213):0.0020189038,9:10.4676122362):0.0008103202)"
mean_tree = newick_to_treenode(mean_newick)
test_newick = "(0:6.0,(1:5.0,2:3.0,3:4.0):5.0,4:11.0);"
test_tree = newick_to_treenode(test_newick)
check_tree(test_tree)
