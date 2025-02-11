import os
import random
from graphviz import Digraph

def generate_horizontal_branching_flowchart(num_flowcharts, min_nodes, max_nodes):
    # Ensure directories exist
    os.makedirs("cyclical_branching_flowcharts/H_branching_system_flowchart_test_files/flowchart_img", exist_ok=True)
    os.makedirs("cyclical_branching_flowcharts/H_branching_system_flowchart_test_files/mermaid_txt", exist_ok=True)

    for flowchart_index in range(1, num_flowcharts + 1):
        num_nodes = random.randint(min_nodes, max_nodes)
        dot = Digraph(comment=f'Horizontal Branching Flowchart {flowchart_index}', format='png')

        # Set graph direction to Left to Right
        dot.attr(rankdir='LR')

        # Generate Mermaid code
        mermaid_code = "flowchart LR\n"

        previous_nodes = ["1"]  # Start with the first node
        all_nodes = ["1"]       # Track all created nodes for potential loops

        for i in range(1, num_nodes + 1):
            node_name = str(i)

            # Start Node
            if i == 1:
                dot.node(node_name, label="Start", shape="oval")
                mermaid_code += f"    {node_name}((Start))\n"

            # End Node
            elif i == num_nodes:
                dot.node(node_name, label="End", shape="oval")
                mermaid_code += f"    {node_name}((End))\n"
                for prev_node in previous_nodes:
                    dot.edge(prev_node, node_name)
                    mermaid_code += f"    {prev_node} --> {node_name}\n"

            else:
                # Ensure at least one process before any decision
                if i == 2 or random.choice(["process", "decision"]) == "process":
                    dot.node(node_name, label=f"Process {i-1}", shape="box")
                    mermaid_code += f"    {node_name}[Process {i-1}]\n"

                    for prev_node in previous_nodes:
                        dot.edge(prev_node, node_name)
                        mermaid_code += f"    {prev_node} --> {node_name}\n"

                    previous_nodes = [node_name]
                    all_nodes.append(node_name)

                else:
                    dot.node(node_name, label=f"Decision {i-1}", shape="diamond")
                    mermaid_code += f"    {node_name}{{Decision {i-1}}}\n"

                    # Create Yes/No paths
                    yes_node = f"{i}_yes"
                    no_node = f"{i}_no"

                    dot.node(yes_node, label=f"Yes Path {i}", shape="box")
                    dot.node(no_node, label=f"No Path {i}", shape="box")

                    mermaid_code += f"    {yes_node}[Yes Path {i}]\n"
                    mermaid_code += f"    {no_node}[No Path {i}]\n"

                    # Connect decision to Yes/No paths
                    for prev_node in previous_nodes:
                        dot.edge(prev_node, node_name)
                        mermaid_code += f"    {prev_node} --> {node_name}\n"

                    dot.edge(node_name, yes_node, label="Yes")
                    dot.edge(node_name, no_node, label="No")

                    mermaid_code += f"    {node_name} -- Yes --> {yes_node}\n"
                    mermaid_code += f"    {node_name} -- No --> {no_node}\n"

                    # Ensure Yes/No paths lead somewhere
                    if len(all_nodes[:-1]) > 0:  # Check if there are nodes to loop back to
                        decision_path = random.choice(["continue", "loop"])
                    else:
                        decision_path = "continue"  # Default to continue if no nodes available to loop

                    if decision_path == "continue":
                        # Both Yes/No paths will continue to the next nodes
                        previous_nodes = [yes_node, no_node]
                    elif decision_path == "loop":
                        # Loop Yes path back to an earlier node and continue No path
                        loop_target = random.choice(all_nodes[:-1])  # Exclude the latest node to prevent trivial loops
                        dot.edge(yes_node, loop_target, label="Loop Back")
                        mermaid_code += f"    {yes_node} -- Loop Back --> {loop_target}\n"

                        # Continue No path to the next process/decision
                        previous_nodes = [no_node]

                    all_nodes.extend([yes_node, no_node])

        # Save the flowchart image
        flowchart_image_path = os.path.join(
            "cyclical_branching_flowcharts/H_branching_system_flowchart_test_files/flowchart_img",
            f"branching_flowchart_{flowchart_index}.png"
        )
        dot.render(flowchart_image_path, cleanup=True)

        # Save the Mermaid code to a text file
        mermaid_text_path = os.path.join(
            "cyclical_branching_flowcharts/H_branching_system_flowchart_test_files/mermaid_txt",
            f"mermaid_code_{flowchart_index}.txt"
        )
        with open(mermaid_text_path, "w") as mermaid_file:
            mermaid_file.write(mermaid_code)

        # Debugging messages
        print(f"Flowchart {flowchart_index} image saved to: {flowchart_image_path}")
        print(f"Flowchart {flowchart_index} Mermaid code saved to: {mermaid_text_path}")

# Generate the results
if __name__ == "__main__":
    num_flowcharts = 5  # Number of flowcharts to generate
    min_nodes = 5       # Minimum number of nodes
    max_nodes = 10      # Maximum number of nodes
    generate_horizontal_branching_flowchart(num_flowcharts, min_nodes, max_nodes)
