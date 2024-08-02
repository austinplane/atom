from rich.text import Text

accent = "cyan"
time_accent = "yellow"

indents_lookup = {
        "blank": Text("    "),
        "extend": Text(" │  "),
        "split": Text(" ├──"),
        "terminal": Text(" └──"),
        "newline": Text("\n")
        }

def get_checkbox(node):
    if node.is_completed(): return '[x]'
    if node.is_in_progress(): return '[~]'
    if node.is_inactive(): return '[ ]'

def get_node_display(node, show_time=False):
    if len(node.alias) == 0:
        id = Text(f'({node.id})')
    else:
        id = Text(f'({node.id}:{node.alias[0]})')
    id.stylize(accent)

    if show_time:
        time, is_complete, nodes_missing = node.est_time_for_completion()
        if not is_complete:
            time = '?'

        time = Text(f' {time} mins')
        time.stylize(time_accent)
        id += time

    name = Text(node.name)

    checkbox = Text(get_checkbox(node))
    checkbox.stylize(accent, 0, 1)
    checkbox.stylize(accent, -1)

    space = Text(" ")

    return checkbox + space + name + space + id

def get_tree_string(node, show_time=False):
    def traverse(node, stack, sb):
        indents = []
        size = len(stack)
        if size != 0:
            for e in stack[:-1]:
                if e:
                    indents.append(indents_lookup["extend"])
                else:
                    indents.append(indents_lookup["blank"])

            if stack[-1]:
                indents.append(indents_lookup["split"])
            else:
                indents.append(indents_lookup["terminal"])

            if len(node.parents) > 1:
                i = len(indents) - 1
                indents[i] = indents[i][:2] + '··'

        for i in indents:
            sb.append(i)

        sb.append(get_node_display(node, show_time))
        sb.append(indents_lookup["newline"])

        if node.num_children() > 0:
            for child in node.children[:-1]:
                traverse(child, stack + [True], sb)
            traverse(node.children[-1], stack + [False], sb)
    
    sb = []
    traverse(node, [], sb)

    combined = Text()
    for s in sb:
        combined += s
    return combined
