import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import random

def plot_distance_distribution(G, dataset_name="dataset", sample_nodes=300, seed=42):
    """
    Efficiently compute and plot the distance distribution in the largest weakly connected component (WCC).
    
    - Uses BFS-based sampling to approximate the distribution.
    - Draws from a subset of nodes (default 300) for speed.
    - Plots results with logarithmic y-axis for visibility.
    
    Parameters:
        G : networkx.DiGraph or Graph
            Input graph (directed or undirected)
        dataset_name : str
            Label used for plot title and filename
        sample_nodes : int
            Number of nodes to sample BFS distances from
        seed : int
            Random seed for reproducibility
    """
    random.seed(seed)

    # Step 1: Get largest weakly connected component (works even for directed graphs)
    if isinstance(G, nx.DiGraph):
        largest_wcc = max(nx.weakly_connected_components(G), key=len)
        subgraph = G.subgraph(largest_wcc).to_undirected()
    else:
        largest_cc = max(nx.connected_components(G), key=len)
        subgraph = G.subgraph(largest_cc).copy()

    print(f"[i] Largest component: {subgraph.number_of_nodes()} nodes, {subgraph.number_of_edges()} edges")

    # Step 2: Choose sample nodes (connected sample to reduce bias)
    all_nodes = list(subgraph.nodes())
    if len(all_nodes) <= sample_nodes:
        sample_nodes_list = all_nodes
    else:
        # pick one random starting node and expand via BFS until sample reached
        start_node = random.choice(all_nodes)
        visited = {start_node}
        queue = [start_node]
        while queue and len(visited) < sample_nodes:
            v = queue.pop(0)
            for nb in subgraph.neighbors(v):
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
                    if len(visited) >= sample_nodes:
                        break
        sample_nodes_list = list(visited)

    print(f"[i] Sampling {len(sample_nodes_list)} nodes for distance distribution...")

    # Step 3: Compute shortest-path distances
    distance_counts = Counter()
    for node in sample_nodes_list:
        lengths = nx.single_source_shortest_path_length(subgraph, node)
        for target, dist in lengths.items():
            if node != target:
                distance_counts[dist] += 1

    if not distance_counts:
        print("[!] No valid distances found — graph might be too small or disconnected.")
        return

    # Step 4: Prepare and plot
    distances = sorted(distance_counts.items())
    x, y = zip(*distances)

    plt.figure(figsize=(8, 6))
    plt.bar(x, y, color='mediumseagreen', edgecolor='black', alpha=0.8)
    plt.yscale('log')
    plt.xlabel('Shortest path distance')
    plt.ylabel('Frequency (log scale)')
    plt.title(f'Distance Distribution (sampled BFS) - {dataset_name}')
    plt.grid(True, which="both", linestyle='--', linewidth=0.5, alpha=0.7)

    fname = f"distance_distribution_sampled_{dataset_name}.png"
    plt.tight_layout()
    plt.savefig(fname, dpi=200)
    plt.show()
    print(f"[i] Saved distance distribution plot to {fname}")


G = nx.read_weighted_edgelist("twitter-larger-graph.csv", delimiter=",", create_using=nx.DiGraph(), nodetype=str)

plot_distance_distribution(G, dataset_name="twitter-larger", sample_nodes=400)