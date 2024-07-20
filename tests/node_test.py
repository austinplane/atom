from datetime import datetime, timedelta
import pytest
import random
import pdb

from atom.node import Node

def create_tree_base_only():
    return Node('base')

def create_tree_base_with_one_root():
    base = create_tree_base_only()
    rootA = Node('rootA', base)
    if base.validate_new_link(rootA):
        base.children.append(rootA)
        rootA.parents.append(base)
    return base

def create_tree_base_with_two_root():
    base = create_tree_base_only()
    rootA = Node('rootA', base)
    if base.validate_new_link(rootA):
        base.children.append(rootA)
        rootA.parents.append(base)

    rootB = Node('rootB', base)
    if base.validate_new_link(rootB):
        base.children.append(rootB)
        rootB.parents.append(base)
    return base

def add_one_child(base, parent):
    child = Node('child', base)
    if parent.validate_new_link(child):
        parent.children.append(child)
        child.parents.append(parent)

def add_two_child(base, parent):
    childA = Node('child', base)
    if parent.validate_new_link(childA):
        parent.children.append(childA)
        childA.parents.append(parent)

    childB = Node('child', base)
    if parent.validate_new_link(childB):
        parent.children.append(childB)
        childB.parents.append(parent)

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
        'last_node_ancestors': [],
        'all_node_ancestors': [[]],
        'base_node_descendants': [],
        'all_node_descendants': [[]],
        'all_node_roots': [[]],
        'all_roots':[[]],
        'base_leaves': [0],
        'last_node_leaves': [0],
        'base_leaves_all': [0],
        'only_root_completed': None,
        'root_one_child_completed': None,
        'root_two_child_completed': None,
        'only_root_completed_in_progress': None,
        'root_one_child_completed_in_progress': None,
        'root_two_child_completed_in_progress': None,
        'only_root_not_completed': None,
        'root_one_child_not_completed': None,
        'only_root_not_completed_in_progress': None,
        'root_one_child_not_completed_in_progress': None,
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
        'last_node_ancestors': [0],
        'all_node_ancestors': [[], [0]],
        'base_node_descendants': [1],
        'all_node_descendants': [[1], []],
        'all_node_roots': [[], [1]],
        'all_roots':[[1], [1]],
        'base_leaves': [1],
        'last_node_leaves': [1],
        'base_leaves_all': [1],
        'only_root_completed': [False, True],
        'root_one_child_completed': None,
        'root_two_child_completed': None,
        'only_root_completed_in_progress': [False, False],
        'root_one_child_completed_in_progress': None,
        'root_two_child_completed_in_progress': None,
        'only_root_not_completed': [False, False],
        'root_one_child_not_completed': None,
        'only_root_not_completed_in_progress': [False, False],
        'root_one_child_not_completed_in_progress': None,
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
        'last_node_ancestors': [0],
        'all_node_ancestors': [[], [0], [0]],
        'base_node_descendants': [1, 2],
        'all_node_descendants': [[1, 2], [], []],
        'all_node_roots': [[], [1], [2]],
        'all_roots':[[1, 2], [1, 2], [1, 2]],
        'base_leaves': [1, 2],
        'last_node_leaves': [2],
        'base_leaves_all': [1, 2],
        'only_root_completed': [False, True, False],
        'root_one_child_completed': None,
        'root_two_child_completed': None,
        'only_root_completed_in_progress': [False, False, False],
        'root_one_child_completed_in_progress': None,
        'root_two_child_completed_in_progress': None,
        'only_root_not_completed': [False, False, True],
        'root_one_child_not_completed': None,
        'only_root_not_completed_in_progress': [False, False, False],
        'root_one_child_not_completed_in_progress': None,
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
        'last_node_ancestors': [1, 0],
        'all_node_ancestors': [[], [0], [1, 0]],
        'base_node_descendants': [1, 2],
        'all_node_descendants': [[1, 2], [2], []],
        'all_node_roots': [[], [1], [1]],
        'all_roots':[[1], [1], [1]],
        'base_leaves': [2],
        'last_node_leaves': [2],
        'base_leaves_all': [2],
        'only_root_completed': [False, True, True],
        'root_one_child_completed': [False, True, True],
        'root_two_child_completed': None,
        'only_root_completed_in_progress': [False, False, False],
        'root_one_child_completed_in_progress': [False, False, False],
        'root_two_child_completed_in_progress': None,
        'only_root_not_completed': [False, False, False],
        'root_one_child_not_completed': [False, False, False],
        'only_root_not_completed_in_progress': [False, False, False],
        'root_one_child_not_completed_in_progress': [False, False, False],
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
        'last_node_ancestors': [1, 0],
        'all_node_ancestors': [[], [0], [1, 0], [1, 0]],
        'base_node_descendants': [1, 2, 3],
        'all_node_descendants': [[1, 2, 3], [2, 3], [], []],
        'all_node_roots': [[], [1], [1], [1]],
        'all_roots':[[1], [1], [1], [1]],
        'base_leaves': [2, 3],
        'last_node_leaves': [3],
        'base_leaves_all': [2, 3],
        'only_root_completed': [False, True, True, True],
        'root_one_child_completed': [False, False, True, False],
        'root_two_child_completed': [False, True, True, True],
        'only_root_completed_in_progress': [False, False, False, False],
        'root_one_child_completed_in_progress': [False, True, False, False],
        'root_two_child_completed_in_progress': [False, False, False, False],
        'only_root_not_completed': [False, False, False, False],
        'root_one_child_not_completed': [False, False, False, True],
        'only_root_not_completed_in_progress': [False, False, False, False],
        'root_one_child_not_completed_in_progress': [False, True, False, False],
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
        'last_node_ancestors': [2, 0],
        'all_node_ancestors': [[], [0], [0], [1, 0], [2, 0]],
        'base_node_descendants': [1, 3, 2, 4],
        'all_node_descendants': [[1, 3, 2, 4], [3], [4], [], []],
        'all_node_roots': [[], [1], [2], [1], [2]],
        'all_roots':[[1, 2], [1, 2], [1, 2], [1, 2], [1, 2]],
        'base_leaves': [3, 4],
        'last_node_leaves': [4],
        'base_leaves_all': [3, 4],
        'only_root_completed': [False, True, False, True, False],
        'root_one_child_completed': [False, True, False, True, False],
        'root_two_child_completed': None,
        'only_root_completed_in_progress': [False, False, False, False, False],
        'root_one_child_completed_in_progress': [False, False, False, False, False],
        'root_two_child_completed_in_progress': None,
        'only_root_not_completed': [False, False, True, False, True],
        'root_one_child_not_completed': [False, False, True, False, True],
        'only_root_not_completed_in_progress': [False, False, False, False, False],
        'root_one_child_not_completed_in_progress': [False, False, False, False, False],
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
        'last_node_ancestors': [2, 0],
        'all_node_ancestors': [[], [0], [0], [1, 0], [1, 0], [2, 0], [2, 0]],
        'base_node_descendants': [1, 3, 4, 2, 5, 6],
        'all_node_descendants': [[1, 3, 4, 2, 5, 6], [3, 4], [5, 6], [], [], [], []],
        'all_node_roots': [[], [1], [2], [1], [1], [2], [2]],
        'all_roots':[[1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2], [1, 2]],
        'base_leaves': [3, 4, 5, 6],
        'last_node_leaves': [6],
        'base_leaves_all': [3, 4, 5, 6],
        'only_root_completed': [False, True, False, True, True, False, False],
        'root_one_child_completed': [False, False, False, True, False, False, False],
        'root_two_child_completed': [False, True, False, True, True, False, False],
        'only_root_completed_in_progress': [False, False, False, False, False, False, False],
        'root_one_child_completed_in_progress': [False, True, False, False, False, False, False],
        'root_two_child_completed_in_progress': [False, False, False, False, False, False, False],
        'only_root_not_completed': [False, False, True, False, False, True, True],
        'root_one_child_not_completed': [False, False, True, False, True, True, True],
        'only_root_not_completed_in_progress': [False, False, False, False, False, False, False],
        'root_one_child_not_completed_in_progress': [False, True, False, False, False, False, False],
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
        base = tree_setup()
        assert base.next_id() == expected_values['next_id']

    def test_is_node_base(self, tree_setup, expected_values):
        base = tree_setup()
        assert base.is_base() == expected_values['is_node_base']

    def test_all_sorted(self, tree_setup, expected_values):
        base = tree_setup()
        ids = [node.id for node in base.all_sorted()]
        assert ids == expected_values['all_sorted']

    def test_get_by_id(self, tree_setup, expected_values):
        base = tree_setup()
        rand_id = random.randint(0, len(base.all_sorted()) - 1)
        assert base.get_by_id(rand_id).id == rand_id

    def test_get_by_id_does_not_exist(self, tree_setup, expected_values):
        base = tree_setup()
        assert base.get_by_id(1000) is None

    def test_has_parents(self, tree_setup, expected_values):
        base = tree_setup()
        has_parents = [node.has_parents() for node in base.all_sorted()]
        assert has_parents == expected_values['has_parents']

    def test_has_parent_first_root(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]

        has_parent = first_root.has_parent(base)
        assert has_parent

    def test_has_children(self, tree_setup, expected_values):
        base = tree_setup()
        has_children = [node.has_children() for node in base.all_sorted()]
        assert has_children == expected_values['has_children']

    def test_has_child(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        has_child = base.has_child(first_root)
        assert has_child

    def test_is_leaf(self, tree_setup, expected_values):
        base = tree_setup()
        is_leaf = [node.is_leaf() for node in base.all_sorted()]
        assert is_leaf == expected_values['is_leaf']

    def test_is_first_root_base(self, tree_setup, expected_values):
        base = tree_setup()
        root = base.children[0] if len(base.children) > 0 else None
        
        if root is None:
            assert expected_values['is_base_at_first_root'] is None
            return

        assert root.is_base() == expected_values['is_base_at_first_root']

    def test_is_node_first_root(self, tree_setup, expected_values):
        base = tree_setup()
        root = base.children[0] if len(base.children) > 0 else None

        if root is None:
            assert expected_values['is_base_at_first_root'] is None
            return

        assert root.is_root() == expected_values['is_node_first_root']

    def test_roots_parent_id(self, tree_setup, expected_values):
        base = tree_setup()

        first_root = base.children[0] if len(base.children) > 0 else None
        second_root = base.children[1] if len(base.children) > 1 else None

        if first_root is None:
            return

        assert len(first_root.parents) == 1 and first_root.parents[0].id == 0

        if second_root is None:
            return

        assert len(second_root.parents) == 1 and second_root.parents[0].id == 0
        
    def test_parent_id_of_root_children(self, tree_setup, expected_values):
        base = tree_setup()

        first_root = base.children[0] if len(base.children) > 0 else None
        second_root = base.children[1] if len(base.children) > 1 else None

        root_children = []
        if first_root:
            root_children += first_root.children
        if second_root:
            root_children += second_root.children

        ids = [child.parents[0].id for child in root_children]
        assert ids == expected_values['parent_id_of_root_children']

    def test_child_ids_of_roots(self, tree_setup, expected_values):
        base = tree_setup()

        first_root = base.children[0] if len(base.children) > 0 else None
        second_root = base.children[1] if len(base.children) > 1 else None

        child_ids = []
        if first_root:
            child_ids += [child.id for child in first_root.children]
        if second_root:
            child_ids += [child.id for child in second_root.children]

        assert child_ids == expected_values['child_ids_of_roots']

    def test_last_node_ancestors(self, tree_setup, expected_values):
        base = tree_setup()

        last_node = base.all_sorted()[-1]
        ancestor_ids = [node.id for node in last_node.ancestors()]
        assert ancestor_ids == expected_values['last_node_ancestors']

    def test_all_node_ancestors(self, tree_setup, expected_values):
        base = tree_setup()

        all_nodes = base.all_sorted()
        ancestor_ids = [[ancestor.id for ancestor in node.ancestors()] for node in all_nodes]
        assert ancestor_ids == expected_values['all_node_ancestors']

    def test_base_node_descendants(self, tree_setup, expected_values):
        base = tree_setup()

        descendant_ids = [node.id for node in base.descendants()]
        assert descendant_ids == expected_values['base_node_descendants']

    def test_all_node_descendants(self, tree_setup, expected_values):
        base = tree_setup()

        all_nodes = base.all_sorted()
        descendant_ids = [[descendant.id for descendant in node.descendants()] for node in all_nodes]
        assert descendant_ids == expected_values['all_node_descendants']

    def test_all_node_roots(self, tree_setup, expected_values):
        base = tree_setup()

        all_nodes = base.all_sorted()
        root_ids = [[root.id for root in node.roots_sorted()] for node in all_nodes]
        assert root_ids == expected_values['all_node_roots']

    def test_all_node_all_roots(self, tree_setup, expected_values):
        base = tree_setup()

        all_nodes = base.all_sorted()
        all_roots = [[root.id for root in node.roots_all_sorted()] for node in all_nodes]
        assert all_roots == expected_values['all_roots']

    def test_base_leaves(self, tree_setup, expected_values):
        base = tree_setup()

        base_leaves = [node.id for node in base.leaves_sorted()]
        assert base_leaves == expected_values['base_leaves']

    def test_last_node_leaves(self, tree_setup, expected_values):
        base = tree_setup()
        last_node = base.all_sorted()[-1]

        last_node_leaves = [node.id for node in last_node.leaves_sorted()]
        assert last_node_leaves == expected_values['last_node_leaves']

    def test_base_leaves_all(self, tree_setup, expected_values):
        base = tree_setup()

        all_leaves = [node.id for node in base.leaves_all_sorted()]
        assert all_leaves == expected_values['base_leaves_all']

    def test_last_node_leaves_all(self, tree_setup, expected_values):
        base = tree_setup()
        last_node = base.all_sorted()[-1]

        all_leaves = [node.id for node in last_node.leaves_all_sorted()]
        assert all_leaves == expected_values['base_leaves_all']

#------------------- Checking -----------------------------

    def test_is_completed(self, tree_setup, expected_values):
        base = tree_setup()

        now = datetime.now
        all_nodes = base.all_sorted()
        if len(all_nodes) == 1:
            return
        if len(all_nodes) == 2:
            rand_node = 1
        else:
            rand_node = random.randint(1, len(all_nodes) - 1)
        all_nodes[rand_node].mark_state(now)

        assert all_nodes[rand_node].is_completed()

    def test_only_root_completed(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        now = datetime.now
        first_root = base.children[0]
        first_root.mark_state(now)

        is_completed = [node.is_completed() for node in base.all_sorted()]
        assert is_completed == expected_values['only_root_completed']

    def test_root_one_child_completed(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        if not first_root.has_children(): return

        now = datetime.now
        first_root.children[0].mark_state(now)

        is_completed = [node.is_completed() for node in base.all_sorted()]
        assert is_completed == expected_values['root_one_child_completed']

    def test_root_two_child_completed(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        if not len(first_root.children) > 1: return

        now = datetime.now
        first_root.children[0].mark_state(now)
        first_root.children[1].mark_state(now)

        is_completed = [node.is_completed() for node in base.all_sorted()]
        assert is_completed == expected_values['root_two_child_completed']

    def test_only_root_completed_in_progress(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        now = datetime.now
        first_root = base.children[0]
        first_root.mark_state(now)

        is_in_progress = [node.is_in_progress() for node in base.all_sorted()]
        assert is_in_progress == expected_values['only_root_completed_in_progress']

    def test_root_one_child_completed_in_progress(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        if not first_root.has_children(): return

        now = datetime.now
        first_root.children[0].mark_state(now)

        is_in_progress = [node.is_in_progress() for node in base.all_sorted()]
        assert is_in_progress == expected_values['root_one_child_completed_in_progress']

    def test_root_two_child_completed_in_progress(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        if not len(first_root.children) > 1: return

        now = datetime.now
        first_root.children[0].mark_state(now)
        first_root.children[1].mark_state(now)

        is_in_progress = [node.is_in_progress() for node in base.all_sorted()]
        assert is_in_progress == expected_values['root_two_child_completed_in_progress']

#-------------------------- Unchecking --------------------------------

    def test_is_not_completed(self, tree_setup, expected_values):
        base = tree_setup()

        all_nodes = base.all_sorted()
        if len(all_nodes) == 1:
            return
        if len(all_nodes) == 2:
            rand_node = 1
        else:
            rand_node = random.randint(1, len(all_nodes) - 1)

        now = datetime.now
        for child in base.children:
            child.mark_state(now)
        
        all_nodes[rand_node].mark_state(None)

        assert not all_nodes[rand_node].is_completed()

    def test_only_root_not_completed(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        now = datetime.now
        for child in base.children:
            child.mark_state(now)

        first_root = base.children[0]
        first_root.mark_state(None)

        is_completed = [node.is_completed() for node in base.all_sorted()]
        assert is_completed == expected_values['only_root_not_completed']

    def test_root_one_child_not_completed(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        if not first_root.has_children(): return

        now = datetime.now
        for child in base.children:
            child.mark_state(now)
        first_root.children[0].mark_state(None)

        is_completed = [node.is_completed() for node in base.all_sorted()]
        assert is_completed == expected_values['root_one_child_not_completed']

    def test_only_root_not_completed_in_progress(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        now = datetime.now
        for child in base.children:
            child.mark_state(now)

        first_root = base.children[0]
        first_root.mark_state(now)

        is_in_progress = [node.is_in_progress() for node in base.all_sorted()]
        assert is_in_progress == expected_values['only_root_not_completed_in_progress']

    def test_root_one_child_not_completed_in_progress(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        if not first_root.has_children(): return

        now = datetime.now
        for child in base.children:
            child.mark_state(now)
        first_root.children[0].mark_state(None)

        is_in_progress = [node.is_in_progress() for node in base.all_sorted()]
        assert is_in_progress == expected_values['root_one_child_not_completed_in_progress']

    def test_copy_first_root(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return
        
        first_root = base.children[0]
        root_copy = first_root.copy()
        assert root_copy.name == first_root.name
        assert root_copy.id == first_root.id
        assert root_copy.alias == first_root.alias
        assert root_copy.created == first_root.created
        assert root_copy.completed == first_root.completed
        assert root_copy.parents == []
        assert root_copy.children == []

    def test_deepcopy_first_root(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        deep_copy = first_root.deepcopy_multitree()

        all_original = base.all_sorted()
        all_copy = deep_copy.all_sorted()

        for i in range(len(all_original)):
            assert all_original[i].name == all_copy[i].name
            assert all_original[i].id == all_copy[i].id
            assert all_original[i].alias == all_copy[i].alias
            assert all_original[i].created == all_copy[i].created
            assert all_original[i].completed == all_copy[i].completed
            assert len(all_original[i].parents) == len(all_copy[i].parents)
            assert len(all_original[i].children) == len(all_copy[i].children)

    def test_get_tree_base(self, tree_setup, expected_values):
        base = tree_setup()
        tree = base.get_tree()

        all_original = base.all_sorted()
        all_copy = tree.all_sorted()

        for i in range(len(all_original)):
            assert all_original[i].name == all_copy[i].name
            assert all_original[i].id == all_copy[i].id
            assert all_original[i].alias == all_copy[i].alias
            assert all_original[i].created == all_copy[i].created
            assert all_original[i].completed == all_copy[i].completed
            assert len(all_original[i].parents) == len(all_copy[i].parents)
            assert len(all_original[i].children) == len(all_copy[i].children)

    def test_get_tree_first_root(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        tree = first_root.get_tree()

        assert len(tree.parents) == 0
        for i in range(len(first_root.children)):
            assert tree.children[i].name == first_root.children[i].name
            assert tree.children[i].id == first_root.children[i].id
            assert tree.children[i].alias == first_root.children[i].alias
            assert tree.children[i].created == first_root.children[i].created
            assert tree.children[i].completed == first_root.children[i].completed
            assert len(tree.children[i].parents) == len(first_root.children[i].parents)
            assert len(tree.children[i].children) == len(first_root.children[i].children)

        assert tree is not first_root

    def test_detect_backedge_negative(self, tree_setup, expected_values):
        base = tree_setup()
        assert not base.has_backedge()

    def test_detect_backedge_to_first_root_positive(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        if not first_root.has_children(): return

        child = first_root.children[0]
        grandchild = Node('grandchild', base)
        child.children.append(grandchild)
        grandchild.parents.append(child)
        grandchild.children.append(first_root)
        first_root.parents.append(grandchild)

        assert base.has_backedge()
        # assert first_root.has_backedge()

    def test_detect_backedge_to_base_positive(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        if not first_root.has_children(): return

        child = first_root.children[0]
        child.children.append(base)
        base.parents.append(child)

        assert base.has_backedge()
        assert first_root.has_backedge()

    def test_detect_diamond_negative(self, tree_setup, expected_values):
        base = tree_setup()
        assert not base.has_diamond()

    def test_detect_diamond_to_first_root_positive(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        if not first_root.num_children() > 1: return

        first_child = first_root.children[0]
        second_child = first_root.children[1]

        grandchild = Node('grandchild', base)
        grandchild.parents.append(first_child)
        first_child.children.append(grandchild)
        grandchild.parents.append(second_child)
        second_child.children.append(grandchild)

        assert base.has_diamond()
        assert first_root.has_diamond()

    def test_validate_new_link_from_base_negative(self, tree_setup, expected_values):
        base = tree_setup()
        root = Node('new_root', base)
        assert base.validate_new_link(root)

    def test_validate_new_link_from_first_root_negative(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]

        child = Node('new_child', base)
        assert first_root.validate_new_link(child)

    def test_validate_new_link_from_base_to_child_negative(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        if not first_root.has_children(): return
        
        child = first_root.children[0]

        assert base.validate_new_link(child)

    def test_validate_new_link_from_first_root_to_second_child_negative(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.num_children() > 1: return

        first_root = base.children[0]
        second_root = base.children[1]
        if not second_root.has_children(): return
        
        child = second_root.children[0]

        assert first_root.validate_new_link(child)

    def test_validate_new_link_from_root_siblings_to_grandchild_positive(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        if not first_root.num_children() > 1: return
        
        first_child = first_root.children[0]
        second_child = first_root.children[1]

        grandchild = Node('grandchild', base)

        assert first_child.validate_new_link(grandchild)
        first_child.children.append(grandchild)
        grandchild.parents.append(first_child)

        assert not second_child.validate_new_link(grandchild)

    def test_validate_new_link_from_grandchild_to_root_positive(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        if not first_root.has_children(): return
        
        first_child = first_root.children[0]

        grandchild = Node('grandchild', base)

        assert first_child.validate_new_link(grandchild)
        first_child.children.append(grandchild)
        grandchild.parents.append(first_child)

        assert not grandchild.validate_new_link(first_root)

    def test_add_root_success(self, tree_setup, expected_values):
        base = tree_setup()
        root = Node('new_root', base)
        assert base.try_link_child(root)
        assert root in base.children
        assert base in root.parents

    def test_add_child_to_root_success(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]

        child = Node('new_child', base)
        assert first_root.try_link_child(child)

    def test_add_child_as_root_success(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        if not first_root.has_children(): return
        
        child = first_root.children[0]

        assert base.try_link_child(child)

    def test_add_second_root_child_to_first_root_success(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.num_children() > 1: return

        first_root = base.children[0]
        second_root = base.children[1]
        if not second_root.has_children(): return
        
        child = second_root.children[0]

        assert first_root.try_link_child(child)

    def test_add_grandchild_to_first_child_success_second_child_fail(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        if not first_root.num_children() > 1: return
        
        first_child = first_root.children[0]
        second_child = first_root.children[1]

        grandchild = Node('grandchild', base)

        assert first_child.try_link_child(grandchild)
        assert not second_child.try_link_child(grandchild)

    def test_add_grandchild_to_first_child_success_backedge_fail(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        if not first_root.has_children(): return
        
        first_child = first_root.children[0]

        grandchild = Node('grandchild', base)

        assert first_child.try_link_child(grandchild)
        assert not grandchild.try_link_child(first_root)

    def test_unlink_root_success(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        assert base.try_unlink_child(first_root)

    def test_add_root_success_remove_root_success(self, tree_setup, expected_values):
        base = tree_setup()
        root = Node('new_root', base)
        assert base.try_link_child(root)
        assert base.try_unlink_child(root)

    def test_remove_root_fail(self, tree_setup, expected_values):
        base = tree_setup()
        root = Node('new_root', base)
        assert not base.try_unlink_child(root)

    def test_unlink_child_success(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        if not first_root.has_children(): return

        first_child = first_root.children[0]

        assert first_root.try_unlink_child(first_child)

    def test_unlink_child_success_link_child_success(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        if not first_root.has_children(): return

        first_child = first_root.children[0]

        assert first_root.try_unlink_child(first_child)
        assert first_root.try_link_child(first_child)

    def test_unlink_child_success_link_child_to_different_root_success(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.num_children() > 1: return

        first_root = base.children[0]
        second_root = base.children[1]
        if not first_root.has_children(): return

        first_child = first_root.children[0]

        assert first_root.try_unlink_child(first_child)
        assert second_root.try_link_child(first_child)

    def test_unlink_child_success_link_child_to_base_success(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        if not first_root.has_children(): return

        first_child = first_root.children[0]

        assert first_root.try_unlink_child(first_child)
        assert base.try_link_child(first_child)

    def test_add_new_root_add_alias_find_by_alias_success(self, tree_setup, expected_values):
        base = tree_setup()
        root = Node('new_root', base)
        root.try_add_alias('alias')
        assert base.try_link_child(root)
        assert base.get_by_alias('alias') == root

    def test_add_new_child_of_root_add_alias_find_by_alias_success(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        child = Node('new_child', base)
        child.try_add_alias('alias')

        assert first_root.try_link_child(child)
        assert base.get_by_alias('alias') == child

    def test_add_new_child_of_root_add_alias_find_by_alias_from_root_success(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        child = Node('new_child', base)
        child.try_add_alias('alias')

        assert first_root.try_link_child(child)
        assert first_root.get_by_alias('alias') == child

    def test_add_new_child_of_root_add_alias_find_by_alias_fail(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        child = Node('new_child', base)
        child.try_add_alias('alias')

        assert first_root.try_link_child(child)
        assert not base.get_by_alias('alas') == child

    def test_time_for_completion_positive(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        time_delta = timedelta(minutes=60)
        first_root.completed = first_root.created + time_delta

        assert first_root.time_for_completion() == 60

    def test_time_for_completion_negative(self, tree_setup, expected_values):
        base = tree_setup()
        if not base.has_children(): return

        first_root = base.children[0]
        time_delta = timedelta(minutes=60)
        first_root.completed = first_root.created + time_delta

        assert not first_root.time_for_completion() == 61

