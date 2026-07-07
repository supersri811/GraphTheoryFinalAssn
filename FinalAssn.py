import numpy as np
import random
import copy
from numpy import sort
import math

# performs the dijkstra's algorithm (very inefficient implementation ikk) with a start node and returns the list of distances of all other nodes from it
def algo(queue,distances,adjmat,matrix,startnode=-1):
    history=[]
    visit=[]
    path = []
    for i in range(0,len(distances)):
        path.append([startnode])
    if startnode!=-1:
        distances[startnode-1] = 0
        queue = {startnode-1:0}
        history.append(startnode-1)
        visit.append(0)
    while queue!={}:
        p = history.pop(0)
        c = [p,queue.pop(p)]
        for element in adjmat[p]:
            if distances[element] > c[1] + matrix[c[0]][element] or distances[element] <0:
                distances[element] = c[1] + matrix[c[0]][element]
                path[element] = path[p]+[element+1]
                queue[element] = c[1]+matrix[c[0]][element]
                if element not in history:
                    history.append(element)
                visit.append(element)
    return distances,path

m=500 # number of nodes = 500
c=0
d=0
# i assume that any node becomes a cluster if the number of it's neighbours and their neighbours till a depth d is greater than a theshold t
depth =2 # increasing depth includes more extramat[x]s which can reach the node in d moves
threshold = 5 # incresing the threshold makes it harder to find clusters and therefore decreases their number

visited=[]
clustersizes = []
matrix = -np.ones((m, m))

adjmat = []
clusternum=0
limits = np.zeros(m)
max = 4
v=0
cost =0
visited = np.zeros(m)
arr1 =[]
c = []
edges =0
#-------------- PART 1 initialising the matrix and the adjacency list --------------
for i in range(0,m):
    arr1.append(i)
    if random.random()<0.01:
        c.append(random.randint(10, 25))
    else:
        c.append(random.randint(0, 6))
    # c[i] denotes the number of neighbours the i+1th node has
    # feel free to experiment with different values of limits to see how it affects the results
extranode = 0
for j in range(0,m):
    arr = []
    adjmat.append([])
    d=0
    for k in range(0,j):
        matrix[j][k] = matrix[k][j] #ensures connections are bidirectional and symmetrical
        if matrix[j][k] > 0:
            d+=1
            adjmat[j].append(k)
    extranode = random.randint(0,j)
    if extranode not in adjmat[j]:
        matrix[j][extranode] = random.randint(50,200)
        matrix[extranode][j] = matrix[j][extranode]
        adjmat[j].append(extranode)
        adjmat[extranode].append(j)
    if c[j]-d>0:
        for loopcount in range(0,c[j]-d):
            arr2  =[y for y in arr1 if y>j]
            if len(arr1)==0 or len(arr2)==0:
                break
            o = random.choice(arr2)
            arr.append(o)
            adjmat[j].append(o)
            d+=1
            matrix[j][arr[-1]] = random.randint(5,15) #distances between cities are random and i wanted to keep them small


            cost+=matrix[j][arr[-1]]
            edges+=1
            limits[arr[-1]]+=1
            limits[j]+=1
            if (limits[arr[-1]]>=c[arr[-1]]):
                if arr[-1] in arr1:
                    arr1.remove(arr[-1])
            if (limits[j]>=c[j]):
                if j in arr1:
                    arr1.remove(j)
    matrix[j][j] = 0
actualmat = []
for j in range(0,m):
    for i in range(0,j):
        if matrix[j][i]>0:
            actualmat.append([i,j,int(matrix[j][i])])

# Task 1: Start of MST Calculation
print("Task 1: Calculation of Minimum Spanning Tree")
actualmat.sort(key=lambda edge: edge[2])
print(actualmat)
extramat = []
i=0
a=0
t=-1
roads = []
mstcost=0
count = []
for u in range(0,m):
    count.append(0)
while len(extramat)< m-1:
    if t==0:
        break
    t=0
    for x in range(0,len(actualmat)):
        l1=-1
        l2=-1
        v1 = actualmat[x][0]
        v2 = actualmat[x][1]
        for z in range(0,len(extramat)):
            if v1 in extramat[z]:
                l1 = z
            if v2 in extramat[z]:
                l2 = z
        if l1==-1 and l2==-1:
            extramat.append([v1,v2])
            mstcost+=actualmat[x][2]
            roads.append([v1,v2])
            count[v1]+=1
            count[v2]+=1
        elif l1==-1 and l2>=0:
            extramat[l2].append(v1)
            mstcost += actualmat[x][2]
            roads.append([v1, v2])
            count[v1]+=1
            count[v2]+=1
        elif l1>=0 and l2==-1:
            extramat[l1].append(v2)
            mstcost += actualmat[x][2]
            roads.append([v1, v2])
            count[v1]+=1
            count[v2]+=1
        elif l1==l2:
            continue
        elif l1>=0 and l2>=0:
            extramat[l1].extend(extramat[l2])
            extramat.pop(l2)
            mstcost += actualmat[x][2]
            roads.append([v1, v2])
            count[v1]+=1
            count[v2]+=1
        t=1
print(extramat)
print("Original Cost = {}".format(cost))
print("MST Cost = {}".format(mstcost))
print("Cost saved = {}%".format(((cost-mstcost)/cost)*100))
print("Selected Roads:")
for element in roads:
    print(element)
print("[All {} structural spans successfully written to path buffer]".format(len(roads)))
edgenum = []
# Task 2: City Ranking by Connectivity
print("Task 2: Strategic City Identification:")
for r in range(0,len(adjmat)):
    edgenum.append([len(adjmat[r]),r])
edgenum.sort(key=lambda item: item[0])
if len(edgenum)>10:
    u = 10
else:
    u = len(edgenum)
for v in range(0,u):
    print("Rank {} -> City {} -> Degree {}".format(v+1,edgenum[-(v+1)][1],edgenum[-(v+1)][0]))
adjmat_copy = adjmat.copy()
matrix_copy = copy.deepcopy(matrix)
# Task 3: Disaster Simulation and Pathfinding
print("Task 3: Disaster Recovery Routing")
input1 = input("Would you want to remove a city from the network or a road? (c/r): ")
if input1 == "c":
    input2 = int(input("Enter the city you want to remove: "))
    adjmat[input2-1] = []
    for x in range(0,len(adjmat)):
        adjmat[x] = [node for node in adjmat[x] if node != input2-1]
    for x in range(0,len(matrix)):
        matrix[x][input2-1] = -1
        matrix[input2-1][x] = -1
elif input1 == "r":
    again = 1
    while again:
        print("Enter the road connecting two cities you want to remove : ")
        input3 = int(input("Enter first city in the road (1-500): "))
        print(adjmat[input3-1]+np.ones((1,len(adjmat[input3-1]))))
        input4 = int(input("Enter second city in the road (1-500): "))
        matrix[input3-1][input4-1] = -1
        matrix[input4-1][input3-1] = -1
        if input4-1 in adjmat[input3-1]:
            adjmat[input3-1].remove(input4-1)
        if input3-1 in adjmat[input4-1]:
            adjmat[input4-1].remove(input3-1)
        e=input("Remove another road? (y/n): ")
        if e == "y":
            again = 1
        else:
            again = 0
selectedNode = int(input("Select source node A (1-500): "))
selectedNode1 = int(input("Select source node B (1-500): "))
destinationNode = int(input("Select destination node C (1-500): "))
queue = {}
distances = 10000000 * np.ones(m)
[d,path] = algo(queue, distances, adjmat, matrix, startnode=selectedNode)
queue = {}
distances = 10000000 * np.ones(m)
[d1,path1] = algo(queue, distances, adjmat, matrix, startnode=selectedNode1)
for x in range(0, len(d)):
    if d[x] == 10000000:
        d[x] = float('inf')
    else:
        d[x] = int(d[x])
for x in range(0, len(d1)):
    if d1[x] == 10000000:
        d1[x] = float('inf')
    else:
        d1[x] = int(d1[x])
exitNode = destinationNode
if math.isinf(d[exitNode - 1]):
    print("No valid route from {} to {} after disaster.".format(selectedNode, exitNode))
else:
    print(
        "Source A Path: Distance = {} km".format(d[exitNode - 1]))
    for s in range(0,len(path[exitNode - 1])):
        if s ==0:
            print("Path: ",end="")
        if s == len(path[exitNode - 1])-1:
            print("{}".format(path[exitNode - 1][s]))
        else:
            print("{} -> ".format(path[exitNode - 1][s]),end="")
if math.isinf(d1[exitNode - 1]):
    print("No valid route from {} to {} after disaster.".format(selectedNode1, exitNode))
else:
    print("Source B Path: Distance = {} km".format(d1[exitNode - 1]))
    for s in range(0,len(path1[exitNode - 1])):
        if s ==0:
            print("Path: ",end="")
        if s == len(path1[exitNode - 1])-1:
            print("{}".format(path1[exitNode - 1][s]))
        else:
            print("{} -> ".format(path1[exitNode - 1][s]),end="")
# Task 4: Traffic congestion analysis and detour routing
print("Task 4: Traffic Aware Smart Routing")
graphedges = []
points = []
for f in range(0,m):
    points.append([])
    if count[f] == 1:
        graphedges.append(f)
for g in range(0,m):
    queue = {}
    distances = 10000000 * np.ones(m)
    [d3, path] = algo(queue, distances, adjmat_copy, matrix_copy, startnode=g+1)
    max_dist = 0
    min_dist = 10000000
    clean_distances = [d for d in d3 if d < 10000000]
    total_dist = sum(clean_distances)
    points[g] = [int(total_dist/m-1),g]

points.sort(key=lambda item: item[0])
print(points)

print("Real time traffic management")
print("Most congested cities are:")
for i in range(0,10):
    print("City {}".format(points[-i-1][1]))
points_sum = 0
min_points = 10000000
for b in range(0,m):
    points_sum+=points[b][0]
    if points[b][0] < min_points:
        min_points = points[b][0]
points_avg = points_sum/m
print("Enter the path to find delay in:")
node1 = int(input("Enter city A:"))-1
node2 = int(input("Enter city B:"))-1
queue = {}
distances = 10000000 * np.ones(m)
[d4, path5] = algo(queue, distances, adjmat_copy, matrix_copy, startnode=node1+1)
normaldist = d4[node2]
# Penalty calculation applied to every edge
for j in range(0,m):
    for i in range(0,m):
        if matrix_copy[j][i]>=0:
            matrix_copy[j][i] = matrix_copy[j][i]*(1+(points[j][0]+points[i][0]-2*min_points)/(2*points_avg))

queue = {}
delaydist=0
if len(path5[node2])!=1:
    for j in range(1,len(path5[node2])):
        delaydist+=matrix_copy[path5[node2][j-1]-1][path5[node2][j]-1]
distances = 10000000 * np.ones(m)
# Re-run Dijkstra with new traffic penalties to find detour
[d5, path] = algo(queue, distances, adjmat_copy, matrix_copy, startnode=node1+1)
new_dist = d5[node2]
print("Normal route:")
print("Distance = {:.2f} km".format(normaldist))
print("Distance in normal route considering traffic:")
print("Distance = {:.2f} km".format(delaydist))
print("Considering traffic in new shortest path:")
print("Distance = {:.2f} km".format(new_dist))
print("Time saved through alternative path = {:.2f}%".format(((-(new_dist-delaydist)/delaydist))*100))
print("System actively calculated congestion bypass routes based on elevated edge penalties")
print("Thank you for your time!")
