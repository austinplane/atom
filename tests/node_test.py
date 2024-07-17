import pytest

from atom.node import Node

def create_tree_base_only():
    return Node('base')

def create_tree_base_with_one_root():
    base = create_tree_base_only()
    Node('rootA', base)
    return base

def create_tree_base_with_two_root():
    base = create_tree_base_only()
    Node('rootA', base)
    Node('rootB', base)
    return base

def add_one_child(base, parent):
    Node('child', base, parent)

def add_two_child(base, parent):
    Node('child', base, parent)
    Node('child', base, parent)

def create_tree_base_with_one_root_one_child():
    base = create_tree_base_with_one_root()
    parent = base.children[0]
    add_one_child(base, parent)
    return base

def create_tree_base_with_one_root_two_child():
    base = create_tree_base_with_one_root()
    parent = base.children[0]
    add_two_child(base, parent)
    return base

def create_tree_base_with_two_root_one_child():
    base = create_tree_base_with_two_root()
    parent = base.children[0]
    add_one_child(base, parent)
    parent = base.children[1]
    add_one_child(base, parent)
    return base

def create_tree_base_with_two_root_two_child():
    base = create_tree_base_with_two_root()
    parent = base.children[0]
    add_two_child(base, parent)
    parent = base.children[1]
    add_two_child(base, parent)
    return base

# tree base only
expected_values_0 = {
        'next_id': 1,
        'is_node_base': True,
        'all_sorted': [0],
        'has_parents': [False],
        'has_children': [False],
        'is_leaf': [True],
        'is_base_at_first_root': None,
        'is_node_first_root': None,
        'last_child': None,
        'parent_id_of_root_children': [],
        'child_ids_of_roots': [],
        }

# tree base + one root
expected_values_1 = {
        'next_id': 2,
        'is_node_base': True,
        'all_sorted': [0, 1],
        'has_parents': [False, True],
        'has_children': [True, False],
        'is_leaf': [False, True],
        'is_base_at_first_root': False,
        'is_node_first_root': True,
        'last_child': 1,
        'parent_id_of_root_children': [],
        'child_ids_of_roots': [],
        }

# tree base + two root
expected_values_2 = {
        'next_id': 3,
        'is_node_base': True,
        'all_sorted': [0, 1, 2],
        'has_parents': [False, True, True],
        'has_children': [True, False, False],
        'is_leaf': [False, True, True],
        'is_base_at_first_root': False,
        'is_node_first_root': True,
        'last_child': 2,
        'parent_id_of_root_children': [],
        'child_ids_of_roots': [],
        }

# tree base + one root + one child
expected_values_3 = {
        'next_id': 3,
        'is_node_base': True,
        'all_sorted': [0, 1, 2],
        'has_parents': [False, True, True],
        'has_children': [True, True, False],
        'is_leaf': [False, False, True],
        'is_base_at_first_root': False,
        'is_node_first_root': True,
        'last_child': 2,
        'parent_id_of_root_children': [1],
        'child_ids_of_roots': [2],
        }

# tree base + one root + two child
expected_values_4 = {
        'next_id': 4,
        'is_node_base': True,
        'all_sorted': [0, 1, 2, 3],
        'has_parents': [False, True, True, True],
        'has_children': [True, True, False, False],
        'is_leaf': [False, False, True, True],
        'is_base_at_first_root': False,
        'is_node_first_root': True,
        'last_child': 3,
        'parent_id_of_root_children': [1, 1],
        'child_ids_of_roots': [2, 3],
        }

# tree base + two root + one child
expected_values_5 = {
        'next_id': 5,
        'is_node_base': True,
        'all_sorted': [0, 1, 2, 3, 4],
        'has_parents': [False, True, True, True, True],
        'has_children': [True, True, True, False, False],
        'is_leaf': [False, False, False, True, True],
        'is_base_at_first_root': False,
        'is_node_first_root': True,
        'last_child': 4,
        'parent_id_of_root_children': [1, 2],
        'child_ids_of_roots': [3, 4],
        }

# tree base + two root + two child
expected_values_6 = {
        'next_id': 7,
        'is_node_base': True,
        'all_sorted': [0, 1, 2, 3, 4, 5, 6],
        'has_parents': [False, True, True, True, True, True, True],
        'has_children': [True, True, True, False, False, False, False],
        'is_leaf': [False, False, False, True, True, True, True],
        'is_base_at_first_root': False,
        'is_node_first_root': True,
        'last_child': 6,
        'parent_id_of_root_children': [1, 1, 2, 2],
        'child_ids_of_roots': [3, 4, 5, 6],
        }

@pytest.mark.parametrize('tree_setup, expected_values', [
    (create_tree_base_only, expected_values_0),
    (create_tree_base_with_one_root, expected_values_1),
    (create_tree_base_with_two_root, expected_values_2),
    (create_tree_base_with_one_root_one_child, expected_values_3),
    (create_tree_base_with_one_root_two_child, expected_values_4),
    (create_tree_base_with_two_root_one_child, expected_values_5),
    (create_tree_base_with_two_root_two_child, expected_values_6),
    ])
class TestNode:

    def test_next_id(self, tree_setup, expected_values):
        tree = tree_setup()
        assert tree.next_id() == expected_values['next_id']

    def test_is_node_base(self, tree_setup, expected_values):
        tree = tree_setup()
        assert tree.is_base() == expected_values['is_node_base']

    def test_all_sorted(self, tree_setup, expected_values):
        tree = tree_setup()
        ids = [node.id for node in tree.all_sorted()]
        assert ids == expected_values['all_sorted']

    def test_has_parents(self, tree_setup, expected_values):
        tree = tree_setup()
        has_parents = [node.has_parents() for node in tree.all_sorted()]
        assert has_parents == expected_values['has_parents']

    def test_has_children(self, tree_setup, expected_values):
        tree = tree_setup()
        has_children = [node.has_children() for node in tree.all_sorted()]
        assert has_children == expected_values['has_children']

    def test_is_leaf(self, tree_setup, expected_values):
        tree = tree_setup()
        is_leaf = [node.is_leaf() for node in tree.all_sorted()]
        assert is_leaf == expected_values['is_leaf']

    def test_is_first_root_base(self, tree_setup, expected_values):
        tree = tree_setup()
        root = tree.children[0] if len(tree.children) > 0 else None
        
        if root is None:
            assert expected_values['is_base_at_first_root'] is None
            return

        assert root.is_base() == expected_values['is_base_at_first_root']

    def test_is_node_first_root(self, tree_setup, expected_values):
        tree = tree_setup()
        root = tree.children[0] if len(tree.children) > 0 else None

        if root is None:
            assert expected_values['is_base_at_first_root'] is None
            return

        assert root.is_root() == expected_values['is_node_first_root']

    def test_roots_parent_id(self, tree_setup, expected_values):
        tree = tree_setup()

        first_root = tree.children[0] if len(tree.children) > 0 else None
        second_root = tree.children[1] if len(tree.children) > 1 else None

        if first_root is None:
            return

        assert len(first_root.parents) == 1 and first_root.parents[0].id == 0

        if second_root is None:
            return

        assert len(second_root.parents) == 1 and second_root.parents[0].id == 0
        
    def test_parent_id_of_root_children(self, tree_setup, expected_values):
        tree = tree_setup()

        first_root = tree.children[0] if len(tree.children) > 0 else None
        second_root = tree.children[1] if len(tree.children) > 1 else None

        root_children = []
        if first_root:
            root_children += first_root.children
        if second_root:
            root_children += second_root.children

        ids = [child.parents[0].id for child in root_children]
        assert ids == expected_values['parent_id_of_root_children']

    def test_child_ids_of_roots(self, tree_setup, expected_values):
        tree = tree_setup()

        first_root = tree.children[0] if len(tree.children) > 0 else None
        second_root = tree.children[1] if len(tree.children) > 1 else None

        child_ids = []
        if first_root:
            child_ids += [child.id for child in first_root.children]
        if second_root:
            child_ids += [child.id for child in second_root.children]

        assert child_ids == expected_values['child_ids_of_roots']

    def test_last_id_ancestors(self, tree_setup, expected_values):
        pass
