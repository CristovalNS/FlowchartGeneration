import os
from graphviz import Digraph


def generate_linear_flowchart(num_nodes):
    # Initialize Graphviz Digraph
    dot = Digraph(comment='Linear Flowchart', format='png')
    
    # Generate Mermaid code
    mermaid_code = "flowchart TD\n"

    # Add nodes and edges to the flowchart
    for i in range(1, num_nodes + 1):
        node_name = str(i)
        dot.node(node_name, label=node_name)
        mermaid_code += f"    {node_name}[{node_name}]\n"
        if i > 1:
            dot.edge(str(i - 1), node_name)
            mermaid_code += f"    {i - 1} --> {i}\n"

    # Save the flowchart image
    flowchart_image_path = os.path.join("V_linear_system_flowchart_test_files/flowchart_img", "flowchart.png")
    dot.render(flowchart_image_path, cleanup=True)

    # Save the Mermaid code to a text file
    mermaid_text_path = os.path.join("V_linear_system_flowchart_test_files/mermaid_txt", "mermaid_code.txt")
    with open(mermaid_text_path, "w") as mermaid_file:
        mermaid_file.write(mermaid_code)

    print(f"Flowchart image saved to: {flowchart_image_path}")
    print(f"Mermaid code saved to: {mermaid_text_path}")


# Generate the results
if __name__ == "__main__":
    num_nodes = 5  # You can set the number of notes here
    generate_linear_flowchart(num_nodes)