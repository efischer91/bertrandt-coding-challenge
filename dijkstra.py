import json, math

# Node naming
starting_node_name = "Erde"
starting_node_number = 0
goal_node_name = "b3-r7-r4nd7"
goal_node_number = 0

print("Reading in json-File.")
json_file = open("generatedGraph.json", "r")
json_dict = json.load(json_file)

adjacency_list = {}
distances_list = {}
predecessor_list = {}
edges = []
all_nodes = []

print("Create adjacency list.")
for index, node in enumerate(json_dict["nodes"]):
    node_name: str = node["label"]
    distance = math.inf

    if node_name == starting_node_name:
        starting_node_number = index
        distance = 0
    if node_name == goal_node_name:
        goal_node_number = index

    node_name = index
    all_nodes.append(int(index))
    adjacency_list[index] = []
    predecessor_list[index] = None
    distances_list[index] = distance

print("Read edges.")
for edge in json_dict["edges"]:
    edges.append(edge)
    adjacency_list[edge["source"]].append(edge["target"])
    adjacency_list[edge["target"]].append(edge["source"])

def get_edge(from_node, to_node):
    for entry in edges:
        if entry["source"] == from_node and entry["target"] == to_node:
            return entry["cost"]
        if entry["source"] == to_node and entry["target"] == from_node:
            return entry["cost"]


def update_distance(from_node, to_node):
    edge_cost = get_edge(from_node, to_node)
    new_dist = distances_list[from_node] + float(edge_cost)
    old_dist = distances_list[to_node]

    if new_dist < old_dist:
        distances_list[to_node] = new_dist
        predecessor_list[to_node] = from_node


checked_nodes = []


while len(all_nodes) != 0:
    diff_list = {x for x in distances_list if x not in checked_nodes}

    node_to_check = min(diff_list, key=distances_list.get)
    all_nodes.remove(node_to_check)
    checked_nodes.append(node_to_check)

    for neighbor in adjacency_list[node_to_check]:

        if neighbor in diff_list:
            update_distance(node_to_check, neighbor)


#print("Adjacency list: ", adjacency_list)
#print("Predecessor list: ", predecessor_list)
#print("Distances list: ", distances_list)

print("DISTANCE TO GOAL: ", distances_list[goal_node_number])

way = [goal_node_number]
u = goal_node_number

while predecessor_list[u]:
    u = predecessor_list[u]
    way.append(u)

way.reverse()
print("Way reverse: ", way)
