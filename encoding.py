
from collections import defaultdict
import itertools


def completed(graph):
    """Return the same graph, with all edges specified"""
    complete_graph = defaultdict(set)
    for node, succs in graph.items():
        for succ in succs:
            complete_graph[succ].add(node)
            complete_graph[node].add(succ)
    return complete_graph

def reversed_edges(graph):
    """Return the same graph, with predecessor as values and successors as keys"""
    output = defaultdict(set)
    for node, succs in graph.items():
        for succ in succs:
            output[succ].add(node)
    return dict(output)


def hash_productions(prods):
    """Return a hash of a {node: is_produced}"""
    return sum(int(v) for v in prods.values())


def productions(graph, seeds):
    """Return {node: is_produced} and {node: produced-by-node successors}"""
    produced = defaultdict(lambda: False, {seed: True for seed in seeds})
    used_subgraph = defaultdict(set)
    revgraph = reversed_edges(graph)
    prev_hash = None
    while hash_productions(produced) != prev_hash:
        prev_hash = hash_productions(produced)
        for node, preds in revgraph.items():
            # a node is produced only if all its predecessor are
            if all(produced[pred] for pred in preds):
                produced[node] = True
                # maintain the subgraph, keeping only edges that are necessary
                for pred in preds:
                    used_subgraph[pred].add(node)
    return produced, dict(used_subgraph)


def produced_targets(produced, targets):
    """Return the set of produced target"""
    return {target for target in targets if produced[target]}


def dead_ends(used_subgraph, targets):
    """Return the set of dead-ends"""
    return {
        node for node in itertools.chain.from_iterable(used_subgraph.values())
        if node not in used_subgraph and node not in targets
    }


if __name__ == "__main__":
    GRAPH = {'M1': {'R1'}, 'M4': {'R1'}, 'R1': {'M2', 'M3'}}
    SEEDS = {'M1', 'M4'}
    TARGETS = {'M3',}
    prod, subgraph = productions(GRAPH, SEEDS)

    try:  # pretty print the graph if available
        import tergraw
        print('\n'.join(tergraw.pretty_view(GRAPH, oriented=True)))
    except ImportError:
        pass

    print('GRAPH:', GRAPH)
    print('PRODUCTIONS:', dict(prod))
    print('USED SUB   :', subgraph)
    print('PRODUCED   :', produced_targets(prod, TARGETS))
    print('DEAD-ENDS  :', dead_ends(subgraph, TARGETS))
