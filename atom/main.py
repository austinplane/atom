import os
import json
import typer
from rich.console import Console
import subprocess
from datetime import datetime
import pickle
import atexit
import pdb
from typing import List
from typing_extensions import Annotated
from enum import Enum
from .node import Node, import_tree
from .display import get_node_display, get_tree_string

class Order_Type(str, Enum):
    TIME = 'time'

console = Console()
app = typer.Typer()
pickle_path = os.path.expanduser('~/code/atom/tree.pkl')

state = {
        'abs_base': None,
        'rel_base': None,
        'archive': None,
        }

def change_pickle_path(path):
    global pickle_path
    pickle_path = path

def run_at_exit():
    global state
    if state['abs_base'] is None: return

    with open(pickle_path, 'wb') as f:
        pickle.dump(state, f)

atexit.register(run_at_exit)


@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    """
    CLI todo app.
    """

    global state
    if not os.path.exists(pickle_path):
        state['abs_base'] = Node('base')
    else:
        with open(pickle_path, 'rb') as f:
            state = pickle.load(f)

    if ctx.invoked_subcommand is None:
        b = state['abs_base']
        typer.echo("\nAvailable root nodes:")
        if b is not None:
            for child in b.children:
                console.print(get_node_display(child))
            typer.echo("")
        else:
            typer.echo("No base node found.")


@app.command()
def status():
    """
    Display the status of atom.
    """
    global state
    b = state['rel_base'] if state['rel_base'] else state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return
    typer.echo(f'\nNode checked out: {b.id if not b.is_base() else "base"}\n')


@app.command()
def checkout(id: int):
    """
    Check out a node for processing.
    """

    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    if id == 0:
        base()
        return

    node = b.get_by_id(id)
    if node is None:
        typer.echo(f"Node {id} does not exist.")
        return

    state['rel_base'] = node
    typer.echo(f'\nNode {id} is now root.\n')


@app.command()
def base():
    """
    Checkout base node.
    """
    global state
    state['rel_base'] = None
    typer.echo('\nRoot reset to base node.\n')


@app.command()
def up():
    """
    Checks out the (first) parent of the current root node.
    """

    global state
    b = state['rel_base'] if state['rel_base'] else state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    id = b.id
    if b.has_parents():
        state['rel_base'] = b.parents[0]
        id = b.parents[0].id

    typer.echo(f'\nNode {id} is now root.\n')
    

@app.command()
def add(name: str):
    """
    Adds a new node to the currently checked out node.
    """

    global state
    b = state['rel_base'] if state['rel_base'] else state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = Node(name, b)
    result = b.try_link_child(node)
    if not result:
        print(f"Could not add node {name}")


@app.command()
def remove(id: int):
    """
    Removes node with id and unlinks from parents/children.
    """
    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = b.get_by_id(id)
    if node is None:
        typer.echo(f"Node {id} does not exist.")
        return

    node.remove_node()


@app.command()
def link(parent_id: int, child_id: int):
    """
    Links parent to child by id.
    """
    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    parent = b.get_by_id(parent_id)
    child = b.get_by_id(child_id)

    if parent is None:
        typer.echo("Parent node does not exist.")

    if child is None:
        typer.echo("Child node does not exist.")

    if not parent.try_link_child(child):
        print(f"Linking parent {parent_id} to child {child_id} failed.")


@app.command()
def unlink(parent_id: int, child_id: int):
    """
    Unlinks parent to child by id.
    """
    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    parent = b.get_by_id(parent_id)
    child = b.get_by_id(child_id)

    if parent is None:
        typer.echo("Parent node does not exist.")

    if child is None:
        typer.echo("Child node does not exist.")

    if not parent.try_unlink_child(child):
        print(f"Unlinking parent {parent_id} from child {child_id} failed.")


@app.command()
def reparent(child_ids: List[int],
             parent_id: Annotated[int, typer.Option(help='ID of the parent node.')] = None):
    """
    Reparents child ids to parent id (default = current root).
    Child nodes must have only one parent.
    """
    if parent_id and parent_id <= 0:
        typer.echo('Parent ID must be a positive integer.')
        return

    if child_ids is None or len(child_ids) == 0:
        typer.echo('Child ID list cannot be empty.')

    global state
    b = state['rel_base'] if state['rel_base'] else state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    child_nodes = []
    for id in child_ids:
        if id <= 0:
            typer.echo('Each child ID must be a positive integer.')
            return
        node = b.get_by_id(id)
        if not node:
            typer.echo(f'Node {id} could not be found!')
            return
        if len(node.parents) > 1:
            typer.echo(f'Child node {id} cannot have more than one parent!')
        child_nodes.append(node)

    parent = b
    if parent_id:
        parent = b.get_by_id(parent_id)
        if not parent:
            typer.echo(f'Parent node {parent_id} could not be found!')

    for child in child_nodes:
        prev_parent = child.parents[0]
        prev_parent.try_unlink_child(child)
        parent.try_link_child(child)


@app.command()
def complete(id: int):
    """
    Marks the current node as completed.
    """

    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = b.get_by_id(id)
    if node is None:
        typer.echo(f"Node {id} does not exist.")
        return

    node.mark_state(datetime.now())


@app.command()
def incomplete(id: int):
    """
    Marks the current node as incomplete.
    """

    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = b.get_by_id(id)
    if node is None:
        typer.echo(f"Node {id} does not exist.")
        return

    node.mark_state(None)


@app.command()
def set_estimate(est: float, id: Annotated[int, typer.Option(help='ID of the node.')] = None):
    """
    Sets the estimated time in minutes to complete the node.
    """
    if id and id <= 0:
        typer.echo('ID must be a positive integer.')
        return

    if est <= 0:
        typer.echo('Estimate must be greater than 0.')
        return

    global state
    b = state['rel_base'] if state['rel_base'] else state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    if id is not None:
        node = b.get_by_id(id)
    else:
        node = b

    if not node.is_leaf():
        typer.echo("Can only set estimated times for leaf nodes.")
        return
    node.est_time_to_complete = est

@app.command()
def get_estimate(id: Annotated[int, typer.Option(help='ID of the node.')] = None):
    """
    Gets the estimated time in minutes to complete the node.
    """
    if id and id <= 0:
        typer.echo('ID must be a positive integer.')
        return

    global state
    b = state['rel_base'] if state['rel_base'] else state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    if id is not None:
        node = b.get_by_id(id)
    else:
        node = b

    time, is_complete, missing_nodes = node.est_time_for_completion()
    print(f'Estimated time to complete node: {time} mins.')

    if not is_complete:
        if node.is_leaf():
            print(f"Please set this leaf node's estimated time using set-estimate")
        else:
            print(f"Est. time for nodes {missing_nodes} is missing.")


@app.command()
def order(type: Order_Type):
    """
    Orders leaf nodes by the passed parameter type.
    """
    global state
    b = state['rel_base'] if state['rel_base'] else state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    nodes = b.descendants()
    nodes = [node for node in nodes if 
             (node.is_leaf() and node.est_time_to_complete != 0 and not node.is_completed())]

    if type is Order_Type.TIME:
        nodes.sort(key=lambda x: x.est_time_to_complete)
        for node in nodes:
            console.print(get_node_display(node, True))


@app.command()
def tree(id: Annotated[int, typer.Option(help='ID of tree root.')] = None,
         time: Annotated[bool, typer.Option(help='show est. times for each node.')] = False):
    """
    Displays a tree rooted at the node id.
    """

    if id and id <= 0:
        typer.echo('ID must be a positive integer.')
        return

    global state
    b = state['rel_base'] if state['rel_base'] else state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    #If the base node is checked out, only print the root nodes unless a nonzero id is passed in as option
    if id == 0 or b == state['abs_base'] and id == None:
        typer.echo("\nAvailable root nodes:")
        for child in state['abs_base'].children:
            console.print(get_node_display(child))
        typer.echo("")
        return


    #If id is not given, display the tree from the currently checked out node
    if id is None:
        console.print(get_tree_string(b, time))
        return

    #Display the tree from an arbitrary root (except 0)
    node = b.get_by_id(id)
    if node is None:
        typer.echo(f"Node {id} does not exist.")
        return

    console.print(get_tree_string(node, time))


@app.command()
def rename(id: int, name: str):
    """
    Renames the node with the given id.
    """

    if len(name) == 0:
        typer.echo("String cannot be empty.")
        return

    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = b.get_by_id(id)
    if node is None:
        typer.echo(f"Node {id} does not exist.")
        return

    node.change_name(name)


@app.command()
def alias(id: int, name: str):
    """
    Aliases the node with the given id.
    """

    if len(name) == 0:
        typer.echo("String cannot be empty.")
        return

    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = b.get_by_id(id)
    if node is None:
        typer.echo(f"Node {id} does not exist.")
        return

    if not node.try_add_alias(name):
        typer.echo('Unable to add alias to node.')
        return


@app.command()
def unalias(id: int, name: str):
    """
    Aliases the node with the given id.
    """

    if len(name) == 0:
        typer.echo("String cannot be empty.")
        return

    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = b.get_by_id(id)
    if node is None:
        typer.echo(f"Node {id} does not exist.")
        return

    if not node.try_remove_alias(name):
        typer.echo('Unable to remove alias to node.')
        return


@app.command()
def save(path: Annotated[str, typer.Option(help='Path for save file.')] = None):
    """
    Export the multitree to json.
    """

    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    a = state['archive'] if 'archive' in state else None
    if a is None:
        typer.echo("No archive node found. Continuing with export.")

    if path is not None:
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            typer.echo('Directory for save file does not exist.')
            return
    else:
        path = '/mnt/d/OneDrive/Documents/atom_tree_bkup.json'

    main = b.export_as_base()
    archive = a.export_as_base() if a else None
    export = {
            'main': main,
            'archive': archive
            }

    with open(path, 'w') as f:
        json_str = json.dump(export, f, indent=2)


@app.command()
def load(path: Annotated[str, typer.Option(help='Path for save file.')] = None):
    """
    Import from json to build the multitree.
    """

    if path is not None:
        if not os.path.exists(path):
            typer.echo('Save file does not exist.')
            return
    else:
        path = '/mnt/d/OneDrive/Documents/atom_tree_bkup.json'

    with open(path, 'r') as f:
        imprt = json.load(f)

    main = imprt['main']
    archive = imprt['archive']

    b = import_tree(main)
    a = import_tree(archive) if archive else None

    global state
    state = {
            'abs_base': None,
            'rel_base': None,
            'archive': None,
            }
    state['abs_base'] = b
    state['archive'] = a


@app.command()
def archive(id: Annotated[int, typer.Option(help='ID of node to archive.')] = None):
    global state
    a = state['archive']
    if not a:
        a = Node('archive')
        state['archive'] = a

    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = state['rel_base']
    if id:
        if id <= 0:
            typer.echo('ID must be a positive integer.')
            return
        node = b.get_by_id(id)

    if not node:
        typer.echo(f"Node {id} does not exist.")
        return

    if not node.is_root():
        typer.echo(f'Only root nodes can be archived.')
        return
        
    node_copy = node.get_tree()
    a.try_link_child(node_copy)
    remove(node.id)


@app.command()
def unarchive(id: int):
    global state
    a = state['archive']
    if not a:
        typer.echo('No archive base node found.')
        return

    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = a.get_by_id(id)

    if not node:
        typer.echo(f"Node {id} does not exist.")
        return

    if not node.is_root():
        typer.echo(f'Only root nodes can be archived.')
        return
        
    b.try_link_child(node)
    a.try_unlink_child(node)


@app.command()
def show_archive():
    global state
    a = state['archive']
    if not a:
        typer.echo('No archive base node found.')
        return

    typer.echo("\nAvailable root nodes:")
    for child in a.children:
        console.print(get_node_display(child))
    typer.echo("")
    



# @app.command()
# def launch(file: str):
#     subprocess.run(["nvim", file])

if __name__ == '__main__':
    app()
