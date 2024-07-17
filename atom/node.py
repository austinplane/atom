import pickle
import math
from datetime import datetime
from traversal import *


class Node:

    def __init__(self, name, base=None, parent=None):
        self.id = 0 if base is None else base.next_id()
        self.name = name
        self.alias = ''
        self.created = datetime.now()
        self.completed = None
        self.children = []
        self.parents = []

        if base is not None:
            p = base if parent is None else parent
            self.parents.append(p)
            p.children.append(self)


    def next_id(self):
        max = 0
        for n in self.all_sorted():
            if n.id > max:
                max = n.id
        return max + 1


    def is_base(self):
        return self.id == 0


    def is_root(self):
        if self.is_base(): return False
        return self.parents[0].id == 0 and len(self.parents) == 1


    def has_parents(self):
        return len(self.parents) > 0


    def has_children(self):
        return len(self.children) > 0


    def is_leaf(self):
        return not self.has_children()
    

    def ancestors(self):
        nodes = []

        def callback(node, _):
            nodes.append(node)

        traverse_ancestors(self, callback)
        if len(nodes) > 0:
            return nodes[1:]
        return nodes


    def descendants(self):
        nodes = []

        def callback(node, _):
            nodes.append(node)
        
        traverse_descendants(self, callback)
        if len(nodes) > 0:
            return nodes[1:]
        return nodes


    def all_sorted(self):
        nodes = []

        def callback(node, search_state, _):
            if search_state == SearchState.WHITE:
                nodes.append(node)

        depth_first_search_undirected(self, callback)

        nodes.sort(key=lambda n: n.id)
        return nodes


    def roots(self):
        roots = []

        def callback(node, _):
            if node.is_root():
                roots.append(node)

        traverse_ancestors(self, callback)
        return roots


    def roots_all(self):
        if self.id == 0:
            return self.children

        roots = []
        all = self.all(self)
        for n in all:
            if n.is_root():
                roots.append(n)

        return roots


    def is_completed(self):
        return self.completed is not None


    def is_in_progress(self):
        if self.is_completed():
            return False
        for d in self.descendants():
            if d.is_completed():
                return True
        return False


    def is_inactive(self):
        return not self.is_completed and not self.is_in_progress()


    def __str__(self):
        return f""" 
        ===== Node {self.id} =====
             Name: {self.name}
            Alias: {self.alias}
          Created: {self.created}
        Completed: {self.completed}
          Parents: {[p.name for p in self.parents]}
         Children: {[c.name for c in self.children]}"""


if __name__ == '__main__':
    base = Node('/')
    root1 = Node('root1', base)
    leaf1 = Node('root1', base, root1)

    with open('node.pkl', 'wb') as f:
        pickle.dump(leaf1, f)

    with open('node.pkl', 'rb') as f:
        loaded_node = pickle.load(f)

    for n in loaded_node.all():
        print(n)

    for n in loaded_node.roots():
        print(n)

