
import networkx as nx
import itertools
from networkx.algorithms.shortest_paths import floyd_warshall
from collections import defaultdict
from student_utils import *


def ptp_solver(G: nx.DiGraph, H: list, s: int, alpha: float):
    # Step 1: Precompute all-pairs shortest path lengths
    all_pairs_shortest = dict(floyd_warshall(G, weight='weight'))

    # Step 2: Initial tour includes only home, supermarket, and back
    tour = [0, s, 0]
    nodes_in_tour = set(tour)

    def compute_cost(tour):
        car_cost = sum(G[tour[i]][tour[i+1]]['weight'] for i in range(len(tour) - 1))
        walk_cost = sum(min(all_pairs_shortest[h][p] for p in tour) for h in H)
        return alpha * car_cost + walk_cost

    def best_insertion(tour, v):
        best_cost = float('inf')
        best_tour = None
        for i in range(1, len(tour)):  # do not break start/end at 0
            new_tour = tour[:i] + [v] + tour[i:]
            if all(G.has_edge(new_tour[j], new_tour[j+1]) for j in range(len(new_tour)-1)):
                cost = compute_cost(new_tour)
                if cost < best_cost:
                    best_cost = cost
                    best_tour = new_tour
        return best_tour, best_cost

    # Step 3: Insert nodes greedily
    improving = True
    while improving:
        improving = False
        best_change = (None, float('inf'))
        for v in G.nodes:
            if v not in nodes_in_tour:
                new_tour, new_cost = best_insertion(tour, v)
                if new_cost < compute_cost(tour):
                    best_change = (new_tour, new_cost)
                    improving = True
        if improving and best_change[0] is not None:
            tour = best_change[0]
            nodes_in_tour = set(tour)

    # Step 4: Assign pickup locations
    pickup_dict = defaultdict(list)
    for h in H:
        best_p = min(tour, key=lambda p: all_pairs_shortest[h][p])
        pickup_dict[best_p].append(h)

    return tour, dict(pickup_dict)


if __name__ == "__main__":
    pass
