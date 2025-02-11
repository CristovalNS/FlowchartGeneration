import os
import random
from graphviz import Digraph

def generate_linear_flowchart(num_flowcharts, min_nodes, max_nodes):
    # Ensure directories exist
    os.makedirs("linear_flowcharts/V_linear_system_flowchart_test_files/flowchart_img", exist_ok=True)
    os.makedirs("linear_flowcharts/V_linear_system_flowchart_test_files/mermaid_txt", exist_ok=True)

    for flowchart_index in range(1, num_flowcharts + 1):
        num_nodes = random.randint(min_nodes, max_nodes)
        dot = Digraph(comment=f'Linear Flowchart {flowchart_index}', format='png')
        mermaid_code = "flowchart TD\n"

        # Initialize node tracking
        i = 1
        previous_node = None

        # Determine if this is a process-only flowchart (every 5th flowchart)
        process_only_flowchart = (flowchart_index % 5 == 0)

        while i <= num_nodes:
            node_name = str(i)

            # Start Node
            if i == 1:
                dot.node(node_name, label="Start", shape="oval")
                mermaid_code += f"    {node_name}((Start))\n"
                previous_node = node_name

            # End Node
            elif i == num_nodes:
                dot.node(node_name, label="End", shape="oval")
                mermaid_code += f"    {node_name}((End))\n"
                dot.edge(previous_node, node_name)
                mermaid_code += f"    {previous_node} --> {node_name}\n"

            else:
                if process_only_flowchart:
                    # For process-only flowcharts (every 5th flowchart)
                    dot.node(node_name, label=f"Process {i-1}", shape="box")
                    mermaid_code += f"    {node_name}[Process {i-1}]\n"

                    # Connect to the previous node
                    dot.edge(previous_node, node_name)
                    mermaid_code += f"    {previous_node} --> {node_name}\n"
                    previous_node = node_name  # Update the previous node

                else:
                    # For other flowcharts, randomly include I/O nodes
                    choice = random.choice(["process_only", "include_io"])

                    if choice == "process_only":
                        dot.node(node_name, label=f"Process {i-1}", shape="box")
                        mermaid_code += f"    {node_name}[Process {i-1}]\n"

                        # Connect to the previous node
                        dot.edge(previous_node, node_name)
                        mermaid_code += f"    {previous_node} --> {node_name}\n"
                        previous_node = node_name  # Update previous node

                    elif choice == "include_io":
                        if i == num_nodes - 1:
                            # Allow I/O node before End
                            dot.node(node_name, label=f"I/O {i-1}", shape="parallelogram")
                            mermaid_code += f"    {node_name}[/{i-1} I/O/]\n"

                            # Connect previous node to I/O
                            dot.edge(previous_node, node_name)
                            mermaid_code += f"    {previous_node} --> {node_name}\n"
                            previous_node = node_name  # I/O will connect to End

                        else:
                            # Add I/O node
                            dot.node(node_name, label=f"I/O {i-1}", shape="parallelogram")
                            mermaid_code += f"    {node_name}[/{i-1} I/O/]\n"

                            # Connect previous node to I/O
                            dot.edge(previous_node, node_name)
                            mermaid_code += f"    {previous_node} --> {node_name}\n"

                            # Add process node after I/O
                            process_node = str(i + 1)
                            dot.node(process_node, label=f"Process {i}", shape="box")
                            mermaid_code += f"    {process_node}[Process {i}]\n"

                            # Connect I/O to process
                            dot.edge(node_name, process_node)
                            mermaid_code += f"    {node_name} --> {process_node}\n"

                            previous_node = process_node  # Update previous node
                            i += 1  # Skip to account for process after I/O

            i += 1  # Move to the next node

        # Save the flowchart image
        flowchart_image_path = os.path.join(
            "linear_flowcharts/V_linear_system_flowchart_test_files/flowchart_img",
            f"flowchart_{flowchart_index}.png"
        )
        dot.render(flowchart_image_path, cleanup=True)

        # Save the Mermaid code to a text file
        mermaid_text_path = os.path.join(
            "linear_flowcharts/V_linear_system_flowchart_test_files/mermaid_txt",
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
    min_nodes = 5        # Minimum number of nodes
    max_nodes = 15       # Maximum number of nodes
    generate_linear_flowchart(num_flowcharts, min_nodes, max_nodes)
