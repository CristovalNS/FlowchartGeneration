import os
import random
import re
from graphviz import Digraph
from PIL import Image

def get_last_flowchart_index(directories, file_pattern):
    """Checks the last index of the generated flowcharts"""
    max_index = 0
    pattern = re.compile(r"(?:flowchart_|graphviz_code_|mermaid_code_)(\d+)\.(?:png|dot|txt)")

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)  
            continue

        existing_files = os.listdir(directory)

        for filename in existing_files:
            match = pattern.match(filename)
            if match:
                max_index = max(max_index, int(match.group(1)))

    return max_index  


def resize_image(image_path, output_size=(512, 512)):
    """Resize image to target size while maintaining aspect ratio."""
    with Image.open(image_path) as img:
        img.thumbnail(output_size, Image.Resampling.LANCZOS)

        # Create white background to place the image on (centered)
        final_img = Image.new("RGB", output_size, "white")
        final_img.paste(
            img, ((output_size[0] - img.width) // 2, (output_size[1] - img.height) // 2)
        )
        final_img.save(image_path)  # Overwrite the original image
        return final_img.size


def generate_linear_flowchart(num_flowcharts, min_nodes, max_nodes):
    """Generates linear flowcharts with adjustable DPI and size for readability."""
    # Define directories
    flowchart_img_dir = "main_linear_flowchart_generation/flowchart_img"
    mermaid_txt_dir = "main_linear_flowchart_generation/mermaid_txt"
    graphviz_txt_dir = "main_linear_flowchart_generation/graphviz_txt"

    # Ensure directories exist
    os.makedirs(flowchart_img_dir, exist_ok=True)
    os.makedirs(mermaid_txt_dir, exist_ok=True)
    os.makedirs(graphviz_txt_dir, exist_ok=True)

    # Get last used flowchart index (checks images, Graphviz, and Mermaid)
    last_index = get_last_flowchart_index(
        [flowchart_img_dir, mermaid_txt_dir, graphviz_txt_dir], 
        r"flowchart_(\d+)\.png|graphviz_code_(\d+)\.dot|mermaid_code_(\d+)\.txt"
    )
    start_index = last_index + 1  # Continue from the next number

    for flowchart_index in range(start_index, start_index + num_flowcharts):
        num_nodes = random.randint(min_nodes, max_nodes)

        # Determine flow direction
        direction = "LR" if flowchart_index % 2 == 1 else "TB"  # Horizontal for odd, vertical for even
        dot = Digraph(comment=f'Linear Flowchart {flowchart_index}', format='png')
        dot.attr(rankdir=direction)

        # ** Set DPI and Size for Better Quality **
        dot.attr(dpi="600")  # High DPI for better text quality
        dot.attr(size="6,6")  # Limit image size for clarity
        dot.attr(fontname="Arial", fontsize="16")  # Better text readability
        dot.attr(nodesep="0.5", ranksep="0.5")  # Adjust spacing between nodes

        # Generate Mermaid code
        mermaid_code = f"flowchart {direction}\n"

        # Initialize node tracking
        i = 1
        previous_node = None
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
                    dot.node(node_name, label=f"Process {i-1}", shape="box")
                    mermaid_code += f"    {node_name}[Process {i-1}]\n"
                    dot.edge(previous_node, node_name)
                    mermaid_code += f"    {previous_node} --> {node_name}\n"
                    previous_node = node_name

                else:
                    choice = random.choice(["process_only", "include_io"])

                    if choice == "process_only":
                        dot.node(node_name, label=f"Process {i-1}", shape="box")
                        mermaid_code += f"    {node_name}[Process {i-1}]\n"
                        dot.edge(previous_node, node_name)
                        mermaid_code += f"    {previous_node} --> {node_name}\n"
                        previous_node = node_name

                    elif choice == "include_io":
                        if i == num_nodes - 1:
                            dot.node(node_name, label=f"I/O {i-1}", shape="parallelogram")
                            mermaid_code += f"    {node_name}[/{i-1} I/O/]\n"
                            dot.edge(previous_node, node_name)
                            mermaid_code += f"    {previous_node} --> {node_name}\n"
                            previous_node = node_name

                        else:
                            dot.node(node_name, label=f"I/O {i-1}", shape="parallelogram")
                            mermaid_code += f"    {node_name}[/{i-1} I/O/]\n"
                            dot.edge(previous_node, node_name)
                            mermaid_code += f"    {previous_node} --> {node_name}\n"

                            process_node = str(i + 1)
                            dot.node(process_node, label=f"Process {i}", shape="box")
                            mermaid_code += f"    {process_node}[Process {i}]\n"
                            dot.edge(node_name, process_node)
                            mermaid_code += f"    {node_name} --> {process_node}\n"

                            previous_node = process_node
                            i += 1

            i += 1

        # Save Graphviz
        graphviz_text_path = os.path.join(
            graphviz_txt_dir,
            f"graphviz_code_{flowchart_index}.dot"
        )
        with open(graphviz_text_path, "w") as graphviz_file:
            graphviz_file.write(dot.source)

        # Save flowchart
        flowchart_image_path = os.path.join(
            flowchart_img_dir,
            f"flowchart_{flowchart_index}"
        )  # No .png, Graphviz appends automatically

        dot.render(flowchart_image_path, cleanup=True)

        # Resize the image to 512x512
        image_path_with_extension = flowchart_image_path + ".png"
        resized_size = resize_image(image_path_with_extension, output_size=(512, 512))
        print(f"Flowchart {flowchart_index} resized image size: {resized_size[0]}x{resized_size[1]} pixels")

        # Save Mermaid
        mermaid_text_path = os.path.join(
            mermaid_txt_dir,
            f"mermaid_code_{flowchart_index}.txt"
        )
        with open(mermaid_text_path, "w") as mermaid_file:
            mermaid_file.write(mermaid_code)

        # Debugging messages
        print(f"Flowchart {flowchart_index} image saved to: {flowchart_image_path}.png")
        print(f"Flowchart {flowchart_index} Mermaid code saved to: {mermaid_text_path}")
        print(f"Flowchart {flowchart_index} Graphviz code saved to: {graphviz_text_path}")

# Generate the results (Can control variables here)
if __name__ == "__main__":
    num_flowcharts = 2  # Number of new flowcharts to generate
    min_nodes = 10       # Minimum number of nodes
    max_nodes = 10      # Maximum number of nodes
    generate_linear_flowchart(num_flowcharts, min_nodes, max_nodes)
