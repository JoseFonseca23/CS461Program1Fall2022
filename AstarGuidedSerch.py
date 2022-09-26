import math
import sys


# Class for the nodes used in the algorithm
class Node:
    def __init__(self, name, nodeDist, aStarVal, parent):
        self.name = name
        self.nodeDist = nodeDist
        self.aStarVal = aStarVal
        self.parent = parent


# Class for the coordinates stored
class Coordinate:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y


# Class for the towns stored
class Town:
    def __init__(self, name, adj):
        self.name = name
        self.adj = adj

    def __repr__(self):
        return self.name

    def addAdj(self, new):
        self.adj.append(new)

    def getAdj(self):
        return self.adj


# Will take in coordinates from a file and store them in a list
coordinates = []
f = open("coordinates.txt", "r")
for i in f:
    temp = i.split()
    coordinates.append(Coordinate(temp[0], temp[1], temp[2]))
f.close()

# Will take in adjacencies for each town from a file and store them in a list
# This one will take in the data just how it is stored in the file
adjacencies = []
f = open("Adjacencies.txt", "r")
for i in f:
    temp = i.split()
    adjacencies.append(Town(temp[0], temp[1:]))
f.close

# Will look for those towns that are specified in the file
# Will give them their own entry and populate them with the adjacent parent.
f = open("Adjacencies.txt", "r")
for i in f:
    temp = i.split()
    for j in temp:
        if j not in str(adjacencies):
            adjacencies.append(Town(j, temp[:1]))
        elif j == "Haven":
            adjacencies.append(Town(j, temp[:1]))
f.close

# Will look for any remaining adjacencies not already accounted for.
f = open("Adjacencies.txt", "r")
for i in f:
    temp = i.split()
    for j in adjacencies:
        parent = temp[0]
        # Check if equal to parent
        if j.name != parent:
            for k in temp:
                # Check if i appear on the sublist
                if j.name == k:
                    # IF i do I want to check if im not already in here
                    if parent not in j.getAdj():
                        j.addAdj(parent)
f.close

# Sort the adjacencies by name
adjacencies = sorted(adjacencies, key=lambda x: x.name)


# Function that will return the adjacent towns, parameter is the town that will be looked up
# If no adjacencies found then system will end with message since each entry should have at least one
def getAdjacent(lookup):
    for i in adjacencies:
        if i.name == lookup:
            return i.adj
    print ("No adjacencies found while looking up")
    sys.exit()


# Function to calculate the distance between two towns.
# Parameters are the two towns that will be calculated, will return a float.
def distance(t1, t2):
    x1 = float(t1.x)
    x2 = float(t2.x)
    y1 = float(t1.y)
    y2 = float(t2.y)
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return d


# Function that is feed a towns name and will check if it is stored in the database.
# System will end with message since each town should be properly integrated.
def checkName(town):
    for i in coordinates:
        if i.name == town:
            return i
    print ("No town found with that name")
    sys.exit()


# Function that will return the names stored within a list.
# will return a list of those names.
def getNames(li):
    names = []
    for i in li:
        names.append(i.name)
    return names


# Function that takes in a list and a name to look for the index vaule for that name.
# Will iterate through the list incrementing the index value by one until name is found.
def getIndexFromName(li, name):
    x = 0
    for i in li:
        if i.name == name:
            return x
        else:
            x += 1


# Main function
# Will take in two values, both being towns.
# The function will return a list from the closed set so that we can output the data to user.
def AStar(start, end):
    # Initializing the lists that will be used
    closedSet = []
    openSet = []
    # Will send in the fist node onto out queue which is our starting node.
    # The node will be given a name of the town, a distance of zero since it is the starting node,
    # the A* value is then calculated using our heuristic, the distance from node to end
    # Also will have a blank parent node since this is the head node.
    openSet.append(Node(start.name, 0, 0 + float(distance(start, end)), ""))

    # While our openset isn't empty will loop
    while len(openSet) != 0:
        # Our list will be a priority queue so we will sort so that we have the lowest f(n) at top of queue
        openSet = sorted(openSet, key=lambda x: x.aStarVal)
        current = openSet[0]
        # If our current node is our goal we found a path and will return the closed set.
        if current.name == end.name:
            closedSet.append(openSet[0])
            print("Found a path: ")
            return closedSet
        # If not we will generate it's neighbors and remove current from our open set onto our closed one
        adj = getAdjacent(current.name)
        closedSet.append(openSet[0])
        openSet.pop(0)

        # Finish adding out neighbors
        for i in adj:
            pName = checkName(current.name)
            iName = checkName(i)
            neighbor = Node(i, distance(pName, iName), float(distance(pName, iName)) + float(distance(iName, end)),
                            current.name)
            if neighbor.name in getNames(closedSet):
                continue
            if neighbor.name in getNames(openSet):
                x = getIndexFromName(openSet, neighbor.name)
                if neighbor.aStarVal < openSet[x].aStarVal:
                    openSet[x] = neighbor

            openSet.append(neighbor)
    # Check if out open set is empty, if so then no path found and system will exit.
    if len(openSet) == 0:
        print ("Empty set, path not found.")
        sys.exit()


def main():
    # Takes in user input and will check if the town is in the system.
    print ("Welcome! Inputs are case sensitive, and use underscore for spaces.")
    enter = raw_input("Please enter the starting town's name: ")
    start = checkName(enter)

    enter = raw_input("Please enter the ending town's name: ")
    end = checkName(enter)

    # Will run our A* function, if successful it will return a list.
    closed_set = AStar(start, end)

    # Code that will print out the result to the user
    route = []
    current = closed_set[-1]
    done = False
    while not done:
        route.append(current.name)
        for i in closed_set:
            if i.name == current.parent:
                current = i
                break
        if current.parent == "":
            route.append(current.name)
            done = True
    route.reverse()
    print ("Path found: " + " -> ".join(map(str, route)))


if __name__ == "__main__":
    main()
