import networkx as nx
import matplotlib.pyplot as plt
import re
import csv
from collections import Counter, defaultdict
import random
import pandas as pd

INPUT_FILE = "twitter-larger.tsv"
OUTPUT_FILE = "twitter-larger-graph.csv"

USERNAME_REGEX = re.compile(r'@([A-Za-z0-9_]{1,15})')

edges = defaultdict(int)

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    for line_num, line in enumerate(f):
        try:
            timestamp, user, content = line.strip().split('\t')
        except ValueError:
            continue

        user = user.strip().lower()
        if not user:
            continue

        mentions = USERNAME_REGEX.findall(content)

        for mention in mentions:
            mention = mention.lower().strip()
            if mention and mention != user:
                edges[(user, mention)] = +1


with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for (source, target), weight in edges.items():
        writer.writerow([source, target, weight])

print(f"Graph data written to {OUTPUT_FILE}")
print(f"Total unique edges: {len(edges)}")

#Q3.2
G = nx.read_weighted_edgelist('twitter-graph.csv', delimiter=',', create_using=nx.DiGraph()), 
#                               nodetype=str)
# print(f"Number of edges: {G.number_of_edges()}")
# print(f"Number of nodes: {G.number_of_nodes()}")

# strong_components = list(nx.strongly_connected_components(G))
# num_strong_components = len(strong_components)
# largest_strong_component = max(strong_components, key=len)
# size_largest_strong_component = len(largest_strong_component)

# weakly_components = list(nx.weakly_connected_components(G))
# num_weakly_components = len(weakly_components)
# largest_weakly_component = max(weakly_components, key=len)
# size_largest_weakly_component = len(largest_weakly_component)

# print(f"Number of strongly connected components: {num_strong_components}")
# print(f"Size of largest strongly connected component: {size_largest_strong_component}")
# print(f"Number of weakly connected components: {num_weakly_components}")
# print(f"Size of largest weakly connected component: {size_largest_weakly_component}")

# density = nx.density(G)
# print(f"Density of the graph: {density}")

# small_average_clustering = nx.average_clustering(G.to_undirected())
# print(f"Average clustering coefficient: {small_average_clustering}")

# largest_weakly_component = max(nx.weakly_connected_components(G), key=len)
# G_giant = G.subgraph(largest_weakly_component).copy()

# G_undirected = G_giant.to_undirected()

# print(f"Giant component - Number of nodes: {G_undirected.number_of_nodes()}, Number of edges: {G_undirected.number_of_edges()}")

# sampled_nodes = random.sample(list(G_undirected.nodes()),min(1000, G_undirected.number_of_nodes()))

# path_lengths = []

# for node in sampled_nodes:
#     lengths = nx.single_source_shortest_path_length(G_undirected, node)
#     path_lengths.extend(lengths.values())

# avg_distance = sum(path_lengths) / len(path_lengths) if path_lengths else 0
# print(f"Average distance in the giant component: {avg_distance}")


#indegree and outdegree

# def plot_degree_distributions(Graph, dataset):
#     indgree = [degree for node, degree in Graph.in_degree()]
#     outdegree = [degree for node, degree in Graph.out_degree()] 
#     plt.figure(figsize=(12, 5))

#     #indegree distribution
#     plt.subplot(1, 2, 1)
#     plt.hist(indgree, bins=50, log=True, color='skyblue', edgecolor='black')
#     plt.title(f'In-Degree Distribution ({dataset} dataset)')
#     plt.xlabel('In-Degree') 
#     plt.ylabel('Frequency (log scale)')

#     #outdegree distribution
#     plt.subplot(1, 2, 2)
#     plt.hist(outdegree, bins=50, log=True, color='salmon', edgecolor='black')
#     plt.title(f'Out-Degree Distribution ({dataset} dataset)')
#     plt.xlabel('Out-Degree')
#     plt.ylabel('Frequency (log scale)')

#     plt.tight_layout()
#     plt.savefig(f'degree_distribution_{dataset}.png')
#     plt.show()

#plot_degree_distributions(G, 'twitter-graph.csv')

#distance distribution for largest weekly conneceted componenets

def plot_distance_distribution(graph, dataset):
    #wcc- weakly connected components nodes
    largest_wcc = max(nx.weakly_connected_components(graph), key=len)
    subgraph = graph.subgraph(largest_wcc).to_undirected()

    distance_counts = Counter()
    for node in subgraph.nodes():
        lengths = nx.single_source_shortest_path_length(subgraph, node)
        for target, dist in lengths.items():
            if node != target:
                distance_counts[dist] += 1
    
    distances = sorted(distance_counts.items())
    x, y = zip(*distances)

    plt.figure(figsize=(8, 6))
    plt.bar(x, y, color='mediumseagreen', edgecolor='black')
    plt.ylabel('Frequency (log scale)')
    plt.xlabel('Distance')
    plt.title(f'Distance Distribution in Largest WCC ({dataset} dataset)')
    plt.tight_layout()
    plt.savefig(f'distance_distribution_{dataset}.png')
    plt.show()


plot_distance_distribution(G, 'twitter-larger.csv')

#Q3.3

# #degree centrality
# degree_centrality = nx.degree_centrality(G_giant)

# #betweenness centrality
# betweenness_centrality = nx.betweenness_centrality(G_giant, weight='weight', normalized=True)


# #closeness centrality
# closeness_centrality = nx.closeness_centrality(G_giant)

# #top 20 nodes for each centrality measure
# df = pd.DataFrame({

#     'Degree Centrality': pd.Series(degree_centrality),
#     'Betweenness Centrality': pd.Series(betweenness_centrality),
#     'Closeness Centrality': pd.Series(closeness_centrality)

# })

# top_20_degree = df['Degree Centrality'].nlargest(20)
# top_20_betweenness = df['Betweenness Centrality'].nlargest(20)
# top_20_closeness = df['Closeness Centrality'].nlargest(20)

# print("Top 20 nodes by Degree Centrality:")
# print(top_20_degree)    
# print("\nTop 20 nodes by Betweenness Centrality:")
# print(top_20_betweenness)
# print("\nTop 20 nodes by Closeness Centrality:")
# print(top_20_closeness)

# #rank correlation between centrality measures
# corr_degree_betweenness = df['Degree Centrality'].rank().corr(df['Betweenness Centrality'].rank(), method='pearson')
# corr_degree_closeness = df['Degree Centrality'].rank().corr(df['Closeness Centrality'].rank(), method='pearson')
# corr_betweenness_closeness = df['Betweenness Centrality'].rank().corr(df['Closeness Centrality'].rank(), method='pearson')  

# print(f"\nRank correlation between Degree and Betweenness Centrality: {corr_degree_betweenness}")
# print(f"Rank correlation between Degree and Closeness Centrality: {corr_degree_closeness}")
# print(f"Rank correlation between Betweenness and Closeness Centrality: {corr_betweenness_closeness}")

