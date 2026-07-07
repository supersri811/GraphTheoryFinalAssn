import numpy as np
import random
import copy
import math
import heapq

# --- OPTIMIZED DIJKSTRA'S ALGORITHM (O(E log V)) ---
def algo(adjmat, matrix, startnode=-1):
    m = len(adjmat)
    distances = [float('inf')] * m
    path = [[] for _ in range(m)]
    
    if startnode != -1:
        start_idx = startnode - 1
        distances[start_idx] = 0
        path[start_idx] = [startnode]
        pq = [(0, start_idx)]
    else:
        return distances, path

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        if current_dist > distances[current_node]:
            continue

        for neighbor in adjmat[current_node]:
            weight = matrix[current_node][neighbor]
            if weight < 0:
                continue 

            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                path[neighbor] = path[current_node] + [neighbor + 1]
                heapq.heappush(pq, (new_dist, neighbor))
                
    return distances, path

# --- UNION-FIND DATA STRUCTURE FOR MST ---
class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True
        return False

# ==========================================
# MAIN SCRIPT
# ==========================================
m = 500  # number of nodes = 500
cost = 0
matrix = -np.ones((m, m))
adjmat = []
limits = np.zeros(m)
arr1 = []
c = []
edges = 0

# -------------- PART 1: Initializing the matrix and adjacency list --------------
for i in range(0, m):
    arr1.append(i)
    if random.random() < 0.01:
        c.append(random.randint(10, 25))
    else:
        c.append(random.randint(0, 6))

for j in range(0, m):
    arr = []
    adjmat.append([])
    d = 0
    for k in range(0, j):
        matrix[j][k] = matrix[k][j]
        if matrix[j][k] > 0:
            d += 1
            adjmat[j].append(k)
            
    extranode = random.randint(0, j)
    if extranode not in adjmat[j]:
        matrix[j][extranode] = random.randint(50, 200)
        matrix[extranode][j] = matrix[j][extranode]
        adjmat[j].append(extranode)
        adjmat[extranode].append(j)
        
    if c[j] - d > 0:
        for loopcount in range(0, c[j] - d):
            arr2 = [y for y in arr1 if y > j]
            if len(arr1) == 0 or len(arr2) == 0:
                break
            o = random.choice(arr2)
            arr.append(o)
            adjmat[j].append(o)
            d += 1
            matrix[j][arr[-1]] = random.randint(5, 15)
            cost += matrix[j][arr[-1]]
            edges += 1
            limits[arr[-1]] += 1
            limits[j] += 1
            if (limits[arr[-1]] >= c[arr[-1]]):
                if arr[-1] in arr1:
                    arr1.remove(arr[-1])
            if (limits[j] >= c[j]):
                if j in arr1:
                    arr1.remove(j)
    matrix[j][j] = 0

actualmat = []
for j in range(0, m):
    for i in range(0, j):
        if matrix[j][i] > 0:
            actualmat.append([i, j, int(matrix[j][i])])

# -------------- TASK 1: Minimum Spanning Tree (Optimized) --------------
print("\n--- Task 1: Calculation of Minimum Spanning Tree ---")
actualmat.sort(key=lambda edge: edge[2])
uf = UnionFind(m)
roads = []
mstcost = 0
count = [0] * m

for edge in actualmat:
    v1, v2, weight = edge
    if uf.union(v1, v2):
        mstcost += weight
        roads.append([v1, v2])
        count[v1] += 1
        count[v2] += 1
        if len(roads) == m - 1:
            break

print("Original Cost = {}".format(cost))
print("MST Cost = {}".format(mstcost))
print("Cost saved = {:.2f}%".format(((cost - mstcost) / cost) * 100))
print("[All {} structural spans successfully calculated]".format(len(roads)))

# -------------- TASK 2: Strategic City Identification --------------
print("\n--- Task 2: Strategic City Identification ---")
edgenum = []
for r in range(0, len(adjmat)):
    edgenum.append([len(adjmat[r]), r])
edgenum.sort(key=lambda item: item[0])
u = 10 if len(edgenum) > 10 else len(edgenum)
for v in range(0, u):
    print("Rank {} -> City {} -> Degree {}".format(v + 1, edgenum[-(v + 1)][1] + 1, edgenum[-(v + 1)][0]))

adjmat_copy = copy.deepcopy(adjmat)
matrix_copy = copy.deepcopy(matrix)

# -------------- TASK 3: Disaster Recovery Routing --------------
print("\n--- Task 3: Disaster Recovery Routing ---")
input1 = input("Would you want to remove a city from the network or a road? (c/r): ").strip().lower()
if input1 == "c":
    input2 = int(input("Enter the city you want to remove (1-500): "))
    adjmat[input2 - 1] = []
    for x in range(0, len(adjmat)):
        adjmat[x] = [node for node in adjmat[x] if node != input2 - 1]
    for x in range(0, len(matrix)):
        matrix[x][input2 - 1] = -1
        matrix[input2 - 1][x] = -1
elif input1 == "r":
    again = True
    while again:
        print("Enter the road connecting two cities you want to remove:")
        input3 = int(input("Enter first city in the road (1-500): "))
        input4 = int(input("Enter second city in the road (1-500): "))
        matrix[input3 - 1][input4 - 1] = -1
        matrix[input4 - 1][input3 - 1] = -1
        if input4 - 1 in adjmat[input3 - 1]:
            adjmat[input3 - 1].remove(input4 - 1)
        if input3 - 1 in adjmat[input4 - 1]:
            adjmat[input4 - 1].remove(input3 - 1)
        e = input("Remove another road? (y/n): ").strip().lower()
        if e != "y":
            again = False

selectedNode = int(input("Select source node A (1-500): "))
selectedNode1 = int(input("Select source node B (1-500): "))
destinationNode = int(input("Select destination node C (1-500): "))

[d, path] = algo(adjmat, matrix, startnode=selectedNode)
[d1, path1] = algo(adjmat, matrix, startnode=selectedNode1)

exitNode = destinationNode

if math.isinf(d[exitNode - 1]):
    print("No valid route from {} to {} after disaster.".format(selectedNode, exitNode))
else:
    print("Source A Path: Distance = {} km".format(d[exitNode - 1]))
    print("Path: " + " -> ".join(map(str, path[exitNode - 1])))

if math.isinf(d1[exitNode - 1]):
    print("No valid route from {} to {} after disaster.".format(selectedNode1, exitNode))
else:
    print("Source B Path: Distance = {} km".format(d1[exitNode - 1]))
    print("Path: " + " -> ".join(map(str, path1[exitNode - 1])))


# -------------- TASK 4: Traffic Aware Smart Routing --------------
print("\n--- Task 4: Traffic Aware Smart Routing ---")
points = []
for g in range(0, m):
    [d3, _] = algo(adjmat_copy, matrix_copy, startnode=g + 1)
    clean_distances = [dist for dist in d3 if dist < float('inf')]
    total_dist = sum(clean_distances)
    points.append([int(total_dist / m - 1), g])

points.sort(key=lambda item: item[0])

print("Most congested cities are:")
for i in range(0, 10):
    print("City {}".format(points[-i - 1][1] + 1))

points_sum = sum([p[0] for p in points])
min_points = min([p[0] for p in points])
points_avg = points_sum / m

print("\nEnter the path to find delay in:")
node1 = int(input("Enter city A (1-500): ")) - 1
node2 = int(input("Enter city B (1-500): ")) - 1

[d4, path5] = algo(adjmat_copy, matrix_copy, startnode=node1 + 1)
normaldist = d4[node2]

# Apply the refined traffic penalty to all roads
for j in range(0, m):
    for i in range(0, m):
        if matrix_copy[j][i] >= 0:
            matrix_copy[j][i] = matrix_copy[j][i] * (1 + (points[j][0] + points[i][0] - 2 * min_points) / (2 * points_avg))

delaydist = 0
if len(path5[node2]) > 1:
    for j in range(1, len(path5[node2])):
        delaydist += matrix_copy[path5[node2][j - 1] - 1][path5[node2][j] - 1]

# Calculate new optimal route based on traffic penalties
[d5, path_new] = algo(adjmat_copy, matrix_copy, startnode=node1 + 1)
new_dist = d5[node2]

print("\nNormal route (empty roads):")
print("Distance = {:.2f} km".format(normaldist))

print("\nOriginal route tracking through current traffic:")
print("Effective Distance = {:.2f} km".format(delaydist))

print("\nConsidering traffic in newly generated shortest path:")
print("Effective Distance = {:.2f} km".format(new_dist))

if delaydist > 0:
    print("\nTime saved through alternative path = {:.2f}%".format(((delaydist - new_dist) / delaydist) * 100))
    print("New Path: " + " -> ".join(map(str, path_new[node2])))
else:
    print("\nNo valid path found.")

print("\nSystem actively calculated congestion bypass routes based on elevated edge penalties.")
print("Thank you for your time!")
