import os
import random
import re
from graphviz import Digraph


def generate_flowchart(num_flowcharts, min_nodes, max_nodes, cyclical=True, no_decision=False, isTD=False, no_inputs=False):
    os.makedirs("mermaid_txt", exist_ok=True)
    os.makedirs("flowchart_img", exist_ok=True)
    paths = []

    for flowchart_index in range(1, num_flowcharts + 1):
        num_nodes = random.randint(min_nodes, max_nodes)
        if isTD:
            mermaid_code = "flowchart TD\n"
        else:
            mermaid_code = "flowchart LR\n"

        count_process, count_io, count_decision = 0, 0, 0
        # list of all nodes that have no child, plus a label if it is a decision node
        leaf = []
        # direct parents of each node, will be useful to make sure all nodes can lead to end
        parents = {str(i): [] for i in range(num_nodes)}

        for node in range(num_nodes):
            node_name = str(node)

            if node == 0:
                mermaid_code += f"    {node_name}((Start))\n"
                leaf.append([node_name])
                continue

            elif node == num_nodes - 1:
                mermaid_code += f"    {node_name}((End))\n"
                leaf_to_end = leaf[-1]
                mermaid_code += f"    {''.join(leaf_to_end)} --> {str(node_name)}\n"
                parents[node_name] += leaf_to_end[0]
                leaf.remove(leaf_to_end)

                def getAllParents(node, do_not_visit=None):
                    # returns all ancestors of a node
                    if do_not_visit is None:
                        do_not_visit = []
                    to_return = []
                    to_return = list(set(to_return + parents[str(node)]))
                    for p in parents[str(node)]:
                        if p in do_not_visit:
                            continue
                        # makes it so that you can no longer visit this node
                        # this prevents infinite recursion in a cycle in the graph
                        to_return = list(set(to_return + getAllParents(p, do_not_visit + [str(node)])))
                    return to_return
                for l in leaf:
                    # makes sure you can only go to ancestors of end node, preventing loops that cannot go to the end node
                    old_choices_from_parents = getAllParents(node_name) + [node_name]
                    leaf_parents = []
                    if not cyclical:
                        leaf_parents = getAllParents(l[0])
                    # removes:
                    # - direct children of the leaf to prevent a decision to both go to the same node
                    # - itself
                    # - its parents
                    choices_from_parents = [i for i in old_choices_from_parents if l[0] not in parents[str(i[0])] + [i[0]] and i not in leaf_parents]
                    random_node = random.choice(choices_from_parents)
                    mermaid_code += f"    {''.join(l)} --> {str(random_node)}\n"
                    parents[str(random_node)] += l[0]
                continue

            if no_decision or (node == num_nodes - 2 and not cyclical):
                if no_inputs:
                    choice = "process"
                else:
                    choice = random.choice(["process", "io"])
            else:
                if no_inputs:
                    choice = ["process", "decision"]
                else:
                    choice = random.choice(["process", "io", "decision"])

            def add_edge_to_node(node):
                leaf_remove = random.choice(leaf)
                line = f"    {''.join(leaf_remove)} --> {str(node)}\n"
                parents[str(node)] += str(leaf_remove[0])
                leaf.remove(leaf_remove)
                return line

            if choice == "process":
                count_process += 1
                mermaid_code += f"    {node_name}[Process {count_process}]\n"
                mermaid_code += add_edge_to_node(node_name)
                leaf.append([node_name])
            if choice == "io":
                count_io += 1
                mermaid_code += f"    {node_name}[/I/O {count_io}/]\n"
                mermaid_code += add_edge_to_node(node_name)
                leaf.append([node_name])
            if choice == "decision":
                count_decision += 1
                mermaid_code += f"    {node_name}{{Decision {count_decision}}}\n"
                mermaid_code += add_edge_to_node(node_name)
                temp = random.randint(0, 1)
                leaf.append([node_name, f" -- {'Yes' if not temp else 'No'}"])
                leaf.append([node_name, f" -- {'Yes' if temp else 'No'}"])

        # Save the Mermaid code to a text file
        mermaid_text_path = os.path.join(
            "mermaid_txt",
            f"mermaid_code_{flowchart_index}.txt"
        )
        with open(mermaid_text_path, "w") as mermaid_file:
            mermaid_file.write(mermaid_code)

        # Debugging messages
        print(f"Flowchart {flowchart_index} Mermaid code saved to: {mermaid_text_path}")
        paths.append(mermaid_text_path)
    return paths


def draw_flowchart(mermaid_text_paths):
    for mermaid_text_path in mermaid_text_paths:
        with open(mermaid_text_path, "r") as mermaid_file:
            mermaid_code = mermaid_file.readlines()
        mermaid_file.close()
        f_num = re.match(r".*_(\d+).txt", mermaid_text_path)[1]
        dot = Digraph(comment=f'Horizontal Branching Flowchart {f_num}', format='png')
        if mermaid_code[0].strip().split()[1] == 'TD':
            dot.attr(rankdir='TD')
        else:
            dot.attr(rankdir='LR')
        for line in mermaid_code:
            stripped = line.strip()
            if line[:9] == "flowchart":
                continue

            # Checks IO
            # This has to go before process because the syntax is more specific
            m = re.match(r'(.+)\[/(.+)/]', stripped)
            if m:
                dot.node(m[1], label=m[2], shape="parallelogram")
                continue

            # Checks process
            m = re.match(r'(.+)\[(.+)]', stripped)
            if m:
                dot.node(m[1], label=m[2], shape="box")
                continue

            # Checks decision
            m = re.match(r'(.+)\{(.+)}', stripped)
            if m:
                dot.node(m[1], label=m[2], shape="diamond")
                continue

            # Checks start and end
            m = re.match(r'(.+)\(\((.+)\)\)', stripped)
            if m:
                dot.node(m[1], label=m[2], shape="oval")
                continue

            # Checks labelled links
            m = re.match(r'(.+)--(.+)-->(.+)', stripped)
            if m:
                dot.edge(m[1].strip(), m[3].strip(), m[2].strip())
                continue

            # Checks unlabelled links
            m = re.match(r'(.+)-->(.+)', stripped)
            if m:
                dot.edge(m[1].strip(), m[2].strip())
                continue

        flowchart_image_path = os.path.join(
            "flowchart_img",
            f"flowchart_{f_num}"
        )
        dot.render(flowchart_image_path, cleanup=True)
        print(f"Flowchart {f_num} image saved to: {flowchart_image_path}.png")


num_flowcharts = 5  # Number of flowcharts to generate
min_nodes = 5  # Minimum number of nodes
max_nodes = 15  # Maximum number of nodes
mermaid_path = generate_flowchart(num_flowcharts, 5, max_nodes, cyclical=False, isTD=False)
draw_flowchart(mermaid_path)
