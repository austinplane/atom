import pickle
import math
from datetime import datetime
from .traversal import *
import pdb


class Node:

    def __init__(self, name, base=None):
        self.id = 0 if base is None else base.next_id()
        self.name = name
        self.alias = []
        self.created = datetime.now()
        self.completed = None #timestamp, not a boolean
        self.est_time_to_complete = 0
        self.cumul_time = 0
        self.start_time = 0
        self.children = []
        self.parents = []


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
        return len(self.parents) == 1 and self.parents[0].id == 0


    def get_by_id(self, id):
        for node in self.all_sorted():
            if node.id == id:
                return node

        return None


    def get_by_name(self, name):
        for node in self.all_sorted():
            if node.name == name:
                return node

        return None


    def change_name(self, name):
        self.name = name


    def get_by_alias(self, alias):
        for node in self.all_sorted():
            if alias in node.alias:
                return node

        return None


    def try_add_alias(self, alias):
        if alias in self.alias:
            print("Alias already given to node.")
            return False
        self.alias.append(alias)
        return True


    def try_remove_alias(self, alias):
        if alias not in self.alias:
            print("Node does not have this alias.")
            return False
        self.alias.remove(alias)
        return True


    def has_parents(self):
        return len(self.parents) > 0


    def has_parent(self, node):
        return node in self.parents


    def has_children(self):
        return len(self.children) > 0


    def has_child(self, node):
        return node in self.children


    def num_children(self):
        return len(self.children)


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


    def roots_sorted(self):
        roots = []

        def callback(node, _):
            if node.is_root():
                roots.append(node)

        traverse_ancestors(self, callback)

        roots.sort(key=lambda n: n.id)
        return roots


    def roots_all_sorted(self):
        if self.id == 0:
            return self.children

        roots = []
        all = self.all_sorted()
        for n in all:
            if n.is_root():
                roots.append(n)

        roots.sort(key=lambda n: n.id)
        return roots


    def leaves_sorted(self):
        leaves = []
        def callback(node, _):
            if node.is_leaf():
                leaves.append(node)

        traverse_descendants(self, callback)
        leaves.sort(key=lambda n: n.id)
        return leaves


    def leaves_all_sorted(self):
        leaves = []
        for node in self.all_sorted():
            if node.is_leaf():
                leaves.append(node)

        leaves.sort(key=lambda n: n.id)
        return leaves

    
    def mark_state(self, state):
        if self.is_base(): return

        self.completed = state 
        for node in self.descendants():
            node.completed = state

        def backprop(node, now):
            if node.is_base(): return

            all_children_complete = True
            for child in node.children:
                if not child.is_completed():
                    all_children_complete = False
                    break

            if node.is_completed() is not all_children_complete:
                if all_children_complete:
                    node.completed = state 
                else:
                    node.completed = None

            for p in node.parents:
                backprop(p, state)

        for leaf in self.leaves_sorted():
            for p in leaf.parents:
                backprop(p, state)


    def is_completed(self):
        return self.completed is not None


    def time_for_completion(self):
        if self.completed == None:
            print("Node has not been completed yet!")
            return math.inf

        time = self.completed - self.created
        return time.total_seconds() / 60


    def est_time_for_completion(self):
        if self.is_leaf():
            full_estimate = self.est_time_to_complete != 0
            return self.est_time_to_complete, full_estimate, [] if full_estimate else [self.id]

        estimate = 0
        full_estimate = True
        nodes_without_estimate = []
        def callback(node, _):
            nonlocal estimate, full_estimate
            if not node.is_leaf(): return
            if node.est_time_to_complete == 0:
                full_estimate = False
                nodes_without_estimate.append(node.id)
                return
            estimate += node.est_time_to_complete

        traverse_descendants(self, callback)

        return estimate, full_estimate, nodes_without_estimate


    def start(self):
        self.start_time = datetime.now()


    def stop(self):
        added_time = (datetime.now() - self.start_time).total_seconds() / 60
        self.cumul_time += added_time
        self.start_time = None
        return added_time


    def is_in_progress(self):
        if self.is_base() or self.is_completed():
            return False
        for d in self.descendants():
            if d.is_completed():
                return True
        return False


    def is_inactive(self):
        return not self.is_completed() and not self.is_in_progress()


    def copy(self, children_length=0, parents_length=0):
        node = Node(self.name)
        node.id = self.id
        node.alias = self.alias
        node.created = self.created
        node.completed = self.completed
        node.est_time_to_complete = self.est_time_to_complete
        node.cumul_time = self.cumul_time
        node.children = [0 for _ in range(children_length)]
        node.parents = [0 for _ in range(parents_length)]
        return node


    def deepcopy_multitree(self):
        nodes = self.all_sorted()
        lookup = {node.id: node.copy(children_length=len(node.children), parents_length=len(node.parents))
                  for node in nodes}

        for node in nodes:
            for i, p in enumerate(node.parents):
                lookup[node.id].parents[i] = lookup[p.id]
            for i, c in enumerate(node.children):
                lookup[node.id].children[i] = lookup[c.id]

        return lookup[self.id]


    def get_tree(self):
        root = self.deepcopy_multitree()
        root.parents = []

        def callback(node, _):
            for child in node.children:
                child.parents = [node]

        traverse_descendants(root, callback)
        
        return root


    def has_backedge(self):
        if self.is_base() and not self.has_children(): return False

        roots = self.roots_all_sorted()
        if len(roots) == 0:
            roots.append(self)

        found = False

        def callback(node, search_state, stop_func):
            nonlocal found
            if search_state == SearchState.GRAY:
                found = True
                stop_func()

        for root in roots:
            depth_first_search(root, callback) 
            if found:
                break

        return found

    
    def has_diamond(self):
        roots = self.roots_all_sorted()
        if len(roots) == 0: return False

        found = False

        def callback(node, search_state, stop_func):
            nonlocal found
            if search_state == SearchState.BLACK:
                found = True
                stop_func()

        for root in roots:
            depth_first_search(root, callback) 
            if found:
                break

        return found


    def validate_new_link(self, dest):
        if dest.is_base(): return False

        has_child = self.has_child(dest)
        has_parent = dest.has_parent(self)
        if has_child != has_parent:
            print(f"Parent/child out of sync. Source node has child? {has_child}. Dest node has parent? {has_parent}\n")
            return False
        if has_child:
            print("Source already has Dest as child.\n")
            return False

        parent = self.deepcopy_multitree()
        child = dest.deepcopy_multitree()
        parent.children.append(child)
        child.parents.append(parent)

        if parent.has_backedge():
            print("Backedges not allowed.\n")
            return False

        if parent.has_diamond():
            print("Diamond relationships are not allowed.\n")
            return False
        
        return True


    def try_link_child(self, child):
        if not self.validate_new_link(child):
            return False

        self.children.append(child)
        child.parents.append(self)
        return True


    def try_unlink_child(self, child):
        if self.has_child(child) != child.has_parent(self):
            print(f"Parent/child out of sync. Source node has child? {has_child}. Dest node has parent? {has_parent}\n")
            return False

        if not self.has_child(child):
            print(f"Node {child.id} is not a child of Node {self.id}")
            return False

        self.children.remove(child)
        child.parents.remove(self)
        return True


    def remove_node(self):
        for parent in self.parents:
            parent.try_unlink_child(self)

        for child in self.children:
            self.try_unlink_child(child)

        if len(self.parents) > 0 or len(self.children) > 0:
            print(f"Not able to fully remove node {self.id}")


    def export_as_base(self):
        nodes = []

        def traverse(node):
            nodes.append(node.to_dict())
            for child in node.children:
                traverse(child)

        traverse(self)
        return nodes


    def __str__(self):
        return f""" 
        ===== Node {self.id} =====
             Name: {self.name}
            Alias: {self.alias}
          Created: {self.created}
        Completed: {self.completed}
        Est. time: {self.est_time_to_complete}
      Cumul. time: {self.cumul_time}
          Parents: {[p.name for p in self.parents]}
         Children: {[c.name for c in self.children]}"""


    def to_dict(self):
        return {
                'id': self.id,
                'name': self.name,
                'alias': self.alias,
                'created': self.created.isoformat() if self.created else None,
                'completed': self.completed.isoformat() if self.completed else None,
                'cumul_time': self.cumul_time,
                'parents': [parent.id for parent in self.parents],
                'children': [child.id for child in self.children],
                'est_time': self.est_time_to_complete,
                }

    
    def data_from_dict(self, data):
        self.id = data['id']
        self.alias = data['alias']
        self.created = datetime.fromisoformat(data['created']) if data['created'] else None
        self.completed = datetime.fromisoformat(data['completed']) if data['completed'] else None
        self.est_time_to_complete = data['est_time']
        self.cumul_time = data['cumul_time']

    def connections_from_dict(self, data, nodes):
        for node in nodes:
            if node.id in data['children']:
                self.try_link_child(node)

def import_tree(node_data: list):
    node_data.sort(key=lambda x: x['id'])

    nodes = [Node(node['name']) for node in node_data]
    for i, node in enumerate(nodes):
        node.data_from_dict(node_data[i])
    for i, node in enumerate(nodes):
        node.connections_from_dict(node_data[i], nodes)

    return nodes[0]


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

