from __future__ import annotations


class Node():
    def __init__(self, name: str, flow_rate: int):
        self.name: str = name
        self.flow: int = flow_rate
        self.connections: dict[str, tuple[int, Node]] = {}
        self.distant_connections: dict[str, tuple[int, Node]] = {}
    
    def AddNode(self, node: Node):
        self.connections[node.name] = (1, node)

    def PruneConnection(self, pruned_node_name: str, new_nodes: list[tuple[int, Node]]):
        pruned_weight = self.connections[pruned_node_name][0]
        
        for [weight, node] in new_nodes:
            if node.name == self.name:
                continue

            if node.name in self.connections:
                if pruned_weight + weight < self.connections[node.name][0]:
                    self.connections[node.name] = (pruned_weight + weight, node)
            else:
                self.connections[node.name] = (pruned_weight + weight, node)
        
        del self.connections[pruned_node_name]
    
    def UpdateMap(self, sender: str, node_map: dict[str, tuple[int, Node]]):
        if sender not in self.connections:
            return

        map_modified = False
        additional_weight = self.connections[sender][0]
        for weight, node in node_map.values():
            if node.name in self.connections or node.name == self.name:
                continue

            if node.name not in self.distant_connections:
                self.distant_connections[node.name] = (weight + additional_weight, node)
                map_modified = True
            elif weight + additional_weight < self.distant_connections[node.name][0]:
                self.distant_connections[node.name] = (weight + additional_weight, node)
                map_modified = True

        if map_modified:
            for _, node in self.connections.values():
                node.UpdateMap(self.name, {**self.connections, **self.distant_connections})
    
    def SeedMapUpdate(self):
        for _, node in self.connections.values():
            node.UpdateMap(self.name, self.connections)


def CalculateMaxPressure(time_left: int, current_node: Node, vizitable_nodes: list[str]) -> int:
    combined_connections = {**current_node.connections, **current_node.distant_connections}
    max_flow = 0

    for node_name in vizitable_nodes:
        if time_left > combined_connections[node_name][0] + 1:
            new_time_left = time_left - (combined_connections[node_name][0] + 1)
            new_current_node = combined_connections[node_name][1]
            left_nodes = vizitable_nodes.copy()
            left_nodes.remove(node_name)
            current_flow = new_time_left * new_current_node.flow + CalculateMaxPressure(new_time_left, new_current_node, left_nodes)
            if current_flow > max_flow:
                max_flow = current_flow
    
    return max_flow

def CalculateMaxPressureForTwo(time_left: list[int], current_node: list[Node], vizitable_nodes: list[str]) -> int:
    combined_connections = []
    max_flow = 0
    for c_node in current_node:
        combined_connections.append({**c_node.connections, **c_node.distant_connections})

    for node_name in vizitable_nodes:
        new_time_left = time_left.copy()
        new_current_node = current_node.copy()
        left_nodes = vizitable_nodes.copy()
        left_nodes.remove(node_name)

        i = 0
        if time_left[1] > time_left[0]:
            i = 1
        
        if time_left[i] > combined_connections[i][node_name][0] + 1:
            new_time_left[i] = time_left[i] - (combined_connections[i][node_name][0] + 1)
            new_current_node[i] = combined_connections[i][node_name][1]
            current_flow = new_time_left[i] * new_current_node[i].flow + CalculateMaxPressureForTwo(new_time_left, new_current_node, left_nodes)
            if current_flow > max_flow:
                max_flow = current_flow
    
    return max_flow


f = open("input.txt")
node_dict: dict[str, tuple[Node, list[str]]] = {}
for line in f.readlines():
    line = line.strip().split("; ")
    name = line[0][6:8]
    flow_rate = int(line[0][23:])
    connections = line[1].split(", ")
    connections[0] = connections[0][-2:]
    node_dict[name] = (Node(name, flow_rate), connections)

for (node, connections) in node_dict.values():
    for name in connections:
        node.AddNode(node_dict[name][0])

graph: dict[str, Node] = {}
for (pruning_node, _) in node_dict.values():
    if pruning_node.flow == 0 and pruning_node.name != "AA":
        for [_, node] in pruning_node.connections.values():
            node.PruneConnection(pruning_node.name, list(pruning_node.connections.values()))
    else:
        graph[pruning_node.name] = pruning_node

graph["AA"].SeedMapUpdate()

node_names = list(graph.keys())
node_names.remove("AA")
print(CalculateMaxPressure(30, graph["AA"], node_names))
print(CalculateMaxPressureForTwo([26, 26], [graph["AA"], graph["AA"]], node_names))