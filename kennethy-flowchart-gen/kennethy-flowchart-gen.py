import os
import random
import re
from graphviz import Digraph

def generate_flowchart(num_flowcharts, min_nodes, max_nodes):
    os.makedirs("kennethy_flowchart_gen/mermaid_txt", exist_ok=True)
    os.makedirs("kennethy_flowchart_gen/flowchart_img", exist_ok=True)
    paths = []

    for flowchart_index in range(1, num_flowcharts + 1):
        num_nodes = random.randint(min_nodes, max_nodes)
        mermaid_code = "flowchart TD\n"

        count_process, count_io, count_decision = 1, 1, 1
        leaf = []
        decision_leaf = []
        for node in range(num_nodes):
            node_name = str(node)
            if node == 0:
                mermaid_code += f"    {node_name}(Start)\n"
                leaf.append(node)
                continue
            elif node == num_nodes - 1:
                mermaid_code += f"    {node_name}(End)\n"
                for l in leaf:
                    mermaid_code += f"    {str(l)} --> {node_name}\n"
                continue

            choices = ["process", "io", "decision"]
            if node == num_nodes - 2:
                choices = ["process", "io"]
            choice = random.choice(choices)

            def add_edge_to_node(node):
                if decision_leaf:
                    leaf_remove = random.randint(0, len(decision_leaf) - 1)
                    line = f"    {str(decision_leaf[leaf_remove])} --> {str(node)}\n"
                    decision_leaf.remove(decision_leaf[leaf_remove])
                    return line
                leaf_remove = random.randint(0, len(leaf) - 1)
                line = f"    {str(leaf[leaf_remove])} --> {str(node)}\n"
                leaf.remove(leaf[leaf_remove])
                return line


            if choice == "process":
                count_process += 1
                mermaid_code += f"    {node_name}[Process {count_process}]\n"
                mermaid_code += add_edge_to_node(node)
                leaf.append(node)
            if choice == "io":
                count_io += 1
                mermaid_code += f"    {node_name}[/IO {count_io}/]\n"
                mermaid_code += add_edge_to_node(node)
                leaf.append(node)
            if choice == "decision":
                count_decision += 1
                mermaid_code += f"    {node_name}{{Decision {count_decision}}}\n"
                mermaid_code += add_edge_to_node(node)
                decision_leaf.append(f"{node} -- Yes")
                decision_leaf.append(f"{node} -- No")

        # Save the Mermaid code to a text file
        mermaid_text_path = os.path.join(
            "kennethy_flowchart_gen/mermaid_txt",
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
            "kennethy_flowchart_gen/flowchart_img",
            f"flowchart_{f_num}"
        )
        dot.render(flowchart_image_path, cleanup=True)
        print(f"Flowchart {f_num} image saved to: {flowchart_image_path}.png")


num_flowcharts = 5  # Number of flowcharts to generate
min_nodes = 5        # Minimum number of nodes
max_nodes = 15       # Maximum number of nodes
mermaid_path = generate_flowchart(num_flowcharts, min_nodes, max_nodes)
draw_flowchart(mermaid_path)
