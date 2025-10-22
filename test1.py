#!/usr/bin/env python3
"""
SNACS 2025 - Assignment 2 (Practical parts Q3.1 - Q3.6 + bonus)
Unified script to:
 - parse twitter-small.tsv / twitter-larger.tsv (and larger) into a weighted directed mention graph CSV
 - compute graph statistics (nodes, edges, SCC/WCC counts and sizes, density, avg clustering)
 - compute approx average shortest-path distance using a connected BFS sample (giant component sampling)
 - plot degree distributions as scatterplots (log-log axes), distance distribution (log y), and weight distribution
 - compute centralities (degree, betweenness, closeness) and top-20 lists + Spearman similarity
 - apply community detection (greedy modularity on undirected giant component) and summarize communities
 - supports streaming / thresholding for large files
Author: [Your name]
Date: 2025-10
"""

import re
import csv
import argparse
from collections import defaultdict, Counter, deque
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
from math import log10
from tqdm import tqdm
from scipy.stats import spearmanr

# -----------------------
# Configuration / Regex
# -----------------------
USERNAME_REGEX = re.compile(r'@([A-Za-z0-9_]{1,15})')  # valid Twitter usernames
DEFAULT_INPUT = "twitter-small.tsv"
DEFAULT_OUTPUT = "twitter_graph.csv"

# -----------------------
# Utilities
# -----------------------
def parse_twitter_to_edge_weights(input_path,
                                  output_csv_path=DEFAULT_OUTPUT,
                                  min_mentions_threshold=1,
                                  max_lines=None,
                                  verbose=True):
    """
    Parse the raw twitter tsv and write a weighted directed edge csv with header:
      source,target,weight
    - min_mentions_threshold: filter edges with weight < threshold before writing to CSV (useful for large datasets)
    - max_lines: optional, stop after max_lines lines (for debugging)
    Returns: edges dict {(src, tgt): weight}, and set of nodes
    """
    edges = defaultdict(int)
    nodes = set()
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as fh:
        it = enumerate(fh, start=1)
        if max_lines:
            it = ((i, line) for i, line in it if i <= max_lines)
        for line_num, line in (tqdm(it) if verbose else it):
            line = line.rstrip('\n')
            if not line:
                continue
            # expect at least 3 fields: timestamp, user, content; split only on first two tabs
            parts = line.split('\t', 2)
            if len(parts) < 3:
                # malformed line
                continue
            timestamp, user, content = parts
            user = user.strip().lower()
            if not user:
                continue
            mentions = USERNAME_REGEX.findall(content)
            if not mentions:
                continue
            # accumulate edges
            for mention in mentions:
                mention = mention.lower().strip()
                if mention and mention != user:
                    edges[(user, mention)] += 1
                    nodes.add(user)
                    nodes.add(mention)
    # Apply threshold and write CSV
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as out:
        writer = csv.writer(out)
        writer.writerow(['source', 'target', 'weight'])
        count_written = 0
        for (src, tgt), w in edges.items():
            if w >= min_mentions_threshold:
                writer.writerow([src, tgt, w])
                count_written += 1
    if verbose:
        print(f"[i] Parsed {input_path} -> {output_csv_path}")
        print(f"[i] Total unique edges (before threshold): {len(edges)}")
        print(f"[i] Unique edges written (w >= {min_mentions_threshold}): {count_written}")
        print(f"[i] Unique nodes encountered: {len(nodes)}")
    # Return filtered edges dict for immediate use as well
    if min_mentions_threshold > 1:
        edges = {k: v for k, v in edges.items() if v >= min_mentions_threshold}
    return edges, nodes

def load_graph_from_csv(edge_csv, directed=True):
    """Load a NetworkX DiGraph from the CSV written by parse_twitter_to_edge_weights"""
    df = pd.read_csv(edge_csv)
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    # Add weighted edges
    for _, row in df.iterrows():
        src = str(row['source'])
        tgt = str(row['target'])
        w = float(row['weight'])
        if G.has_edge(src, tgt):
            G[src][tgt]['weight'] += w
        else:
            G.add_edge(src, tgt, weight=w)
    return G

# -----------------------
# Graph Statistics
# -----------------------
def compute_basic_stats(G):
    n = G.number_of_nodes()
    m = G.number_of_edges()
    density = nx.density(G)
    return {'nodes': n, 'edges': m, 'density': density}

def compute_components_stats(G):
    strong = list(nx.strongly_connected_components(G))
    weak = list(nx.weakly_connected_components(G))
    strong_sizes = sorted([len(s) for s in strong], reverse=True)
    weak_sizes = sorted([len(s) for s in weak], reverse=True)
    return {
        'num_strong': len(strong),
        'strong_sizes': strong_sizes,
        'num_weak': len(weak),
        'weak_sizes': weak_sizes
    }

def average_clustering_undirected(G):
    # convert to undirected and compute average clustering
    return nx.average_clustering(G.to_undirected()) if G.number_of_nodes() > 0 else 0.0

# -----------------------
# Connected BFS sampling (for a connected approximation sample)
# -----------------------
def bfs_sample_subgraph(G_undirected, sample_size=1000, seed_node=None):
    """
    Return a subgraph of G_undirected that is built by BFS from seed_node
    until sample_size unique nodes collected. Ensures the sample is connected.
    If seed_node is None, pick a node with highest degree as seed (more likely to reach many nodes).
    """
    if G_undirected.number_of_nodes() == 0:
        return G_undirected.copy()
    if seed_node is None:
        # choose high-degree node to encourage a big reachable set
        seed_node = max(G_undirected.degree, key=lambda x: x[1])[0]
    visited = set()
    q = deque([seed_node])
    visited.add(seed_node)
    while q and len(visited) < sample_size:
        v = q.popleft()
        for nb in G_undirected.neighbors(v):
            if nb not in visited:
                visited.add(nb)
                q.append(nb)
                if len(visited) >= sample_size:
                    break
    return G_undirected.subgraph(visited).copy()

def approx_avg_distance_connected_sample(G_undirected, sample_size=200, verbose=True):
    """
    Approximate average shortest-path distance by BFS sampling from nodes in a connected sample.
    - We first build a connected BFS sample of size sample_size (or fewer)
    - Then compute single-source shortest path lengths from each node in that sample
      and average distances (excluding zero distances to self)
    """
    if G_undirected.number_of_nodes() == 0:
        return 0.0
    sample_sub = bfs_sample_subgraph(G_undirected, sample_size=sample_size)
    nodes = list(sample_sub.nodes())
    total_d = 0
    count = 0
    for u in nodes:
        lengths = nx.single_source_shortest_path_length(sample_sub, u)
        for v, d in lengths.items():
            if u != v:
                total_d += d
                count += 1
    avg = (total_d / count) if count > 0 else 0.0
    if verbose:
        print(f"[i] Connected sample nodes: {sample_sub.number_of_nodes()}, edges: {sample_sub.number_of_edges()}")
        print(f"[i] Approximated average distance (sample_size={sample_size}): {avg:.4f}")
    return avg, sample_sub

# -----------------------
# Degree distributions plotting (scatter) with log-log axes
# -----------------------
def plot_degree_scatter_log(G, dataset_tag="dataset", save_prefix="degree_scatter"):
    """
    Plot degree-value vs count as a scatter plot with log-log axes for both in-degree and out-degree.
    Each point is (degree, count_of_nodes_with_that_degree).
    """
    indeg = dict(G.in_degree())
    outdeg = dict(G.out_degree())

    indeg_counts = Counter(indeg.values())
    outdeg_counts = Counter(outdeg.values())

    # prepare arrays (ignore degree 0 if you want, but we'll keep them)
    degs_in = np.array(sorted(indeg_counts.keys()))
    counts_in = np.array([indeg_counts[d] for d in degs_in])

    degs_out = np.array(sorted(outdeg_counts.keys()))
    counts_out = np.array([outdeg_counts[d] for d in degs_out])

    plt.figure(figsize=(10, 5))
    # in-degree scatter
    plt.subplot(1, 2, 1)
    plt.scatter(degs_in, counts_in, s=20, alpha=0.7)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('In-degree (log scale)')
    plt.ylabel('Count of nodes (log scale)')
    plt.title(f'In-degree scatter (log-log) - {dataset_tag}')

    # out-degree scatter
    plt.subplot(1, 2, 2)
    plt.scatter(degs_out, counts_out, s=20, alpha=0.7)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Out-degree (log scale)')
    plt.ylabel('Count of nodes (log scale)')
    plt.title(f'Out-degree scatter (log-log) - {dataset_tag}')

    plt.tight_layout()
    fname = f'{save_prefix}_{dataset_tag}.png'
    plt.savefig(fname, dpi=200)
    plt.close()
    print(f"[i] Saved degree scatter (log-log) to {fname}")

# -----------------------
# Distance distribution plotting (log y)
# -----------------------
def plot_distance_distribution_log_y(G_undirected, dataset_tag="dataset", sample_bfs_size=500, save_prefix="distance_dist"):
    """
    Compute distances inside giant component (or BFS connected sample) and plot frequency vs distance.
    Use log scale on y-axis to aid readability for long tail.
    For big graphs, we use a BFS sample to get connected nodes and compute distances between them.
    """
    if G_undirected.number_of_nodes() == 0:
        print("[i] Empty graph for distances")
        return

    # ensure connected sample
    sample_sub = bfs_sample_subgraph(G_undirected, sample_bfs_size)
    dist_counts = Counter()
    for u in sample_sub.nodes():
        lengths = nx.single_source_shortest_path_length(sample_sub, u)
        for v, d in lengths.items():
            if u != v:
                dist_counts[d] += 1

    distances = sorted(dist_counts.items())
    x = [d for d, cnt in distances]
    y = [cnt for d, cnt in distances]

    plt.figure(figsize=(8, 6))
    plt.bar(x, y, edgecolor='black')
    plt.yscale('log')
    plt.xlabel('Shortest path distance')
    plt.ylabel('Frequency (log scale)')
    plt.title(f'Distance distribution (sample size {sample_sub.number_of_nodes()}) - {dataset_tag}')
    fname = f'{save_prefix}_{dataset_tag}.png'
    plt.tight_layout()
    plt.savefig(fname, dpi=200)
    plt.close()
    print(f"[i] Saved distance distribution plot to {fname}")

# -----------------------
# Weight distribution plot
# -----------------------
def plot_weight_distribution(edges_dict, dataset_tag="dataset", save_prefix="weight_dist"):
    """
    edges_dict: dict {(u,v): weight} or a pandas Series of weights.
    Plot frequency of weights (counts) on linear x but log-y to see tails, or log-log if requested.
    """
    if isinstance(edges_dict, dict):
        weights = list(edges_dict.values())
    elif isinstance(edges_dict, (list, np.ndarray, pd.Series)):
        weights = list(edges_dict)
    else:
        weights = []

    if not weights:
        print("[i] No weights to plot")
        return

    counts = Counter(weights)
    ws = sorted(counts.keys())
    cs = [counts[w] for w in ws]

    plt.figure(figsize=(8, 6))
    plt.scatter(ws, cs, s=20, alpha=0.7)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Edge weight (number of mentions) [log]')
    plt.ylabel('Frequency of weight [log]')
    plt.title(f'Edge weight distribution (log-log) - {dataset_tag}')
    fname = f'{save_prefix}_{dataset_tag}.png'
    plt.tight_layout()
    plt.savefig(fname, dpi=200)
    plt.close()
    print(f"[i] Saved weight distribution (log-log) to {fname}")

# -----------------------
# Centralities and ranking comparison
# -----------------------
def compute_and_report_centralities(G_directed, topk=20, dataset_tag="dataset"):
    """
    Compute degree (in/out), betweenness (approx for speed if needed), closeness.
    Return top lists and spearman correlations.
    """
    # Use giant weakly connected component for centrality computations where appropriate
    largest_w = max(nx.weakly_connected_components(G_directed), key=len)
    G_giant = G_directed.subgraph(largest_w).copy()

    # degree centrality (we'll provide both in-degree and out-degree)
    in_degree = dict(G_giant.in_degree())
    out_degree = dict(G_giant.out_degree())

    deg_centrality = nx.degree_centrality(G_giant)   # normalized degree (in+out)
    # For clarity, also compute in-degree centrality normalized by (n-1)
    n = G_giant.number_of_nodes()
    in_deg_centrality = {n_: v / (n-1) if n > 1 else 0.0 for n_, v in in_degree.items()}
    out_deg_centrality = {n_: v / (n-1) if n > 1 else 0.0 for n_, v in out_degree.items()}

    # betweenness centrality - expensive; if giant too large, compute approximate with k random samples
    if G_giant.number_of_nodes() <= 2000:
        bet_centrality = nx.betweenness_centrality(G_giant, weight='weight', normalized=True)
    else:
        # Use approximated betweenness sampling k nodes
        k = 200  # number of node pairs to sample - adjust as needed
        bet_centrality = nx.betweenness_centrality(G_giant, k=k, weight='weight', normalized=True, seed=42)

    # closeness centrality
    closeness = nx.closeness_centrality(G_giant)

    # Combine into DataFrame
    df = pd.DataFrame({
        'in_degree': pd.Series(in_degree),
        'out_degree': pd.Series(out_degree),
        'deg_centrality': pd.Series(deg_centrality),
        'in_deg_centrality': pd.Series(in_deg_centrality),
        'out_deg_centrality': pd.Series(out_deg_centrality),
        'betweenness': pd.Series(bet_centrality),
        'closeness': pd.Series(closeness)
    }).fillna(0.0)

    top_in = df['in_degree'].nlargest(topk)
    top_out = df['out_degree'].nlargest(topk)
    top_deg = df['deg_centrality'].nlargest(topk)
    top_bet = df['betweenness'].nlargest(topk)
    top_close = df['closeness'].nlargest(topk)

    # Rank similarity (Spearman) across degree-centrality (deg_centrality), betweenness, closeness
    # We compute Spearman over all nodes in giant, not just top-k
    spearman_deg_bet = spearmanr(df['deg_centrality'], df['betweenness']).correlation
    spearman_deg_close = spearmanr(df['deg_centrality'], df['closeness']).correlation
    spearman_bet_close = spearmanr(df['betweenness'], df['closeness']).correlation

    print("[i] Top nodes by in-degree (count):")
    print(top_in)
    print("\n[i] Top nodes by out-degree (count):")
    print(top_out)
    print("\n[i] Top nodes by degree centrality (normalized):")
    print(top_deg)
    print("\n[i] Top nodes by betweenness:")
    print(top_bet)
    print("\n[i] Top nodes by closeness:")
    print(top_close)

    print("\nSpearman correlations (deg vs bet, deg vs close, bet vs close):")
    print(f"deg vs bet: {spearman_deg_bet:.3f}")
    print(f"deg vs close: {spearman_deg_close:.3f}")
    print(f"bet vs close: {spearman_bet_close:.3f}")

    return {
        'df': df,
        'top_in': top_in,
        'top_out': top_out,
        'top_deg': top_deg,
        'top_bet': top_bet,
        'top_close': top_close,
        'spearman': (spearman_deg_bet, spearman_deg_close, spearman_bet_close),
        'G_giant': G_giant
    }

# -----------------------
# Community detection
# -----------------------
def detect_communities_greedy(G_directed, top_k_communities=5):
    """
    Apply greedy modularity community detection on the undirected giant component.
    Returns a list of communities (as sets). Then report top communities by size.
    """
    largest_w = max(nx.weakly_connected_components(G_directed), key=len)
    G_giant = G_directed.subgraph(largest_w).to_undirected().copy()
    # greedy_modularity_communities needs NetworkX >= 2.1
    communities = list(nx.algorithms.community.greedy_modularity_communities(G_giant))
    communities_sorted = sorted(communities, key=lambda c: len(c), reverse=True)
    print(f"[i] Found {len(communities)} communities in giant component (undirected).")
    for i, comm in enumerate(communities_sorted[:top_k_communities], start=1):
        print(f"  Community {i}: size={len(comm)}  (sample members: {list(comm)[:10]})")
    return communities_sorted

# -----------------------
# Main: Run a full pipeline
# -----------------------
def run_full_pipeline(input_tsv,
                      output_csv="mention_graph.csv",
                      min_mentions_threshold=1,
                      sample_bfs_size=500,
                      distance_sample_size=200,
                      degree_scatter_prefix="degree_scatter",
                      distance_plot_prefix="distance_dist",
                      weight_plot_prefix="weight_dist",
                      verbose=True,
                      max_lines=None):
    # 1) Parse and write CSV
    edges_dict, nodes = parse_twitter_to_edge_weights(
        input_tsv,
        output_csv,
        min_mentions_threshold=min_mentions_threshold,
        max_lines=max_lines,
        verbose=verbose
    )

    # 2) Load graph from CSV into networkx DiGraph
    G = load_graph_from_csv(output_csv, directed=True)
    stats = compute_basic_stats(G)
    if verbose:
        print(f"[i] Nodes: {stats['nodes']}  Edges: {stats['edges']}  Density: {stats['density']:.6f}")

    # 3) Components
    comps = compute_components_stats(G)
    if verbose:
        print(f"[i] Strongly connected components: {comps['num_strong']}  (largest sizes: {comps['strong_sizes'][:5]})")
        print(f"[i] Weakly connected components: {comps['num_weak']}  (largest sizes: {comps['weak_sizes'][:5]})")

    # 4) Clustering coefficient (undirected average)
    avg_clust = average_clustering_undirected(G)
    if verbose:
        print(f"[i] Average clustering coefficient (undirected): {avg_clust:.6f}")

    # 5) Giant component (undirected) for distances and plots
    largest_weak = max(nx.weakly_connected_components(G), key=len)
    G_giant = G.subgraph(largest_weak).copy()
    G_undirected = G_giant.to_undirected()

    if verbose:
        print(f"[i] Giant component nodes: {G_undirected.number_of_nodes()}, edges: {G_undirected.number_of_edges()}")

    # 6) Approx avg distance using connected BFS sample
    avg_dist, sample_sub = approx_avg_distance_connected_sample(G_undirected, sample_size=distance_sample_size, verbose=verbose)

    # 7) Degree scatter plots (log-log)
    plot_degree_scatter_log(G, dataset_tag=input_tsv.replace('.tsv',''), save_prefix=degree_scatter_prefix)

    # 8) Distance distribution (log y)
    plot_distance_distribution_log_y(G_undirected, dataset_tag=input_tsv.replace('.tsv',''), sample_bfs_size=sample_bfs_size, save_prefix=distance_plot_prefix)

    # 9) Weight distribution plot
    plot_weight_distribution(edges_dict, dataset_tag=input_tsv.replace('.tsv',''), save_prefix=weight_plot_prefix)

    # 10) Centralities and ranking similarity
    centrality_res = compute_and_report_centralities(G, topk=20, dataset_tag=input_tsv.replace('.tsv',''))

    # 11) Community detection
    comms = detect_communities_greedy(G, top_k_communities=5)

    # Return collected results
    return {
        'G': G,
        'G_giant': G_giant,
        'G_undirected': G_undirected,
        'stats': stats,
        'components': comps,
        'avg_clustering': avg_clust,
        'avg_distance': avg_dist,
        'sample_subgraph': sample_sub,
        'centrality_res': centrality_res,
        'communities': comms
    }

# -----------------------
# CLI
# -----------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SNACS practical pipeline (Q3.1-Q3.6 + bonus).")
    parser.add_argument('--input', '-i', default=DEFAULT_INPUT, help="Input twitter .tsv file")
    parser.add_argument('--output', '-o', default=DEFAULT_OUTPUT, help="Output weighted edge CSV")
    parser.add_argument('--min_weight', '-t', type=int, default=1, help="Minimum mentions threshold for edges")
    parser.add_argument('--sample_bfs_size', type=int, default=500, help="BFS sample size for distance distribution")
    parser.add_argument('--distance_sample_size', type=int, default=200, help="Sample size for avg distance approx")
    parser.add_argument('--max_lines', type=int, default=None, help="Maximum lines to parse (useful for debugging)")
    args = parser.parse_args()

    results = run_full_pipeline(
        input_tsv=args.input,
        output_csv=args.output,
        min_mentions_threshold=args.min_weight,
        sample_bfs_size=args.sample_bfs_size,
        distance_sample_size=args.distance_sample_size,
        verbose=True,
        max_lines=args.max_lines
    )
