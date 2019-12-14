# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)

import collections
import queue
import heapq
import copy
import time
class SearchTree:
    def __init__(self, start, end):
        self.root_key = start
        self.goal_key = end
        self.tree = dict()

    def insert(self, cell_coor, nlist):
        self.tree[cell_coor] = nlist

    def recursive_path(self,node_key, path, visited):
        if node_key in visited:
            return False
        visited[node_key] = True
        #path.append(((int(node_key/maze_size[0])), node_key % maze_size[0]))
        path.append( node_key )
        #print ( node_key % self.maze_size[0], (int (node_key/self.maze_size[0]) )) 
        if node_key == self.root_key:
            #print(path)
            return True
        if node_key not in self.tree:
            path.pop()
            return False
            #print(a, i)
        b = self.recursive_path(self.tree[node_key], path, visited)
            #print(path)
        if b:
            return True
        path.pop()
        return False

    def find_path(self, start, goal):
        self.root_key = start
        path = list()
        visited = dict()
        self.recursive_path(goal, path, visited)
        return path



def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)


def bfs(maze):
    current_pos = maze.getStart()
    goal_pos = maze.getObjectives()[0]
    maze_size = maze.getDimensions()
    path = []

    visited = dict()

    search_tree = SearchTree(current_pos, goal_pos)
    search_tree.insert(current_pos, None)
    #Queue to keep track of all paths taken
    q = collections.deque()
    q.append(current_pos)

    while (q):
        #pop the first path in the queue 
        current_pos = q.popleft()
        #get current position as last node in path

        if current_pos == goal_pos:
            break

        elif current_pos not in visited:
            #For each neighbor check if move is possible, make new path and added it to the queue 
            possible_moves = maze.getNeighbors(current_pos[0], current_pos[1])
            for i in possible_moves: 
                q.append(i)
                if i not in visited: #if not overwrite most efficient, o(n)
                    search_tree.insert(i, current_pos)
            visited[current_pos] = True
    path = search_tree.find_path(maze.getStart(),goal_pos)
    path.reverse()
    return path, len(visited)

    print ("Error: Nothing returned")
    
    return [], 0


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    current_pos = maze.getStart()
    goal_pos = maze.getObjectives()[0]
    maze_size = maze.getDimensions()
    path = []


    #Set to keep track of visited nodes
    visited = dict()

    search_tree = SearchTree(current_pos, goal_pos)
    search_tree.insert(current_pos, None)
    #Queue to keep track of all paths taken
    q = collections.deque()
    q.append(current_pos)

    while (q):
        current_pos = q.pop()

        if current_pos == goal_pos:
            break

        elif current_pos not in visited:
            #For each neighbor check if move is possible, make new path and added it to the queue 
            possible_moves = maze.getNeighbors(current_pos[0], current_pos[1])
            
            for i in possible_moves: 
                q.append(i)
                if i not in visited: #if not overwrite most efficient, o(n)
                    search_tree.insert(i, current_pos)
            visited[current_pos] = True
    path = search_tree.find_path(maze.getStart(), goal_pos)
    path.reverse()
    return path, len(visited)

    print ("Error: Nothing returned")
    
    return [], 0


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    current_pos = maze.getStart()
    goal_pos = maze.getObjectives()[0]
    maze_size = maze.getDimensions()


    #Set to keep track of visited nodes
    visited = dict()

    search_tree = SearchTree(current_pos, goal_pos)
    search_tree.insert(current_pos, None)
    #Queue to keep track of all paths taken
    q = collections.deque()
    q.append(current_pos)

    while (q):
        #pop the first path in the queue 
        current_pos = q.pop()
        #get current position as last node in path

        if current_pos == goal_pos:
            break

        elif current_pos not in visited:
            #For each neighbor check if move is possible, make new path and added it to the queue 
            possible_moves = maze.getNeighbors(current_pos[0], current_pos[1])
            possible_moves = sort_list(goal_pos, possible_moves)
            for i in possible_moves: 
                q.append(i)
                if i not in visited:
                    search_tree.insert(i, current_pos)
            visited[current_pos] = True
    path = search_tree.find_path(maze.getStart(),goal_pos)
    path.reverse()
    return path, len(visited)

def astar(maze):
    goals = maze.getObjectives()
    start = maze.getStart()
    dots = goals.copy()
    dots.append(start)
    span_tree = dict.fromkeys(dots)

    explored_goals = dict.fromkeys(dots, False)
    start_time = time.time()
    for source in dots:
        span_tree[source] = {}
        for dest in goals :
            if source != dest:
                res = helper_astar(maze, source, dest)
                path = res[0]
                span_tree[source][dest] = path
    last_goal = maze.getStart()
    frontier = []
    f_n = 0
    g_n = 0
    explored_queue = collections.deque()
    
    states = 0
    results = []
    heapq.heappush(frontier, [f_n, g_n,(last_goal, explored_queue.copy(), explored_goals.copy())])
    while frontier:
        states += 1
        curr = heapq.heappop(frontier)
        g_n = curr[1]
        last_goal = curr[2][0]
        explored_queue = curr[2][1]
        explored_goals = curr[2][2]
        explored_queue.append(last_goal)
        explored_goals[last_goal] = True
        if is_completed(explored_goals):
            break

        for edge in span_tree[last_goal].keys():
            if explored_goals[edge] == False:
                temp = len(span_tree[last_goal][edge])
                explored_goals[edge] = True
                f_n = MST(explored_goals.copy(), span_tree.copy()) + g_n + temp
                explored_goals[edge] = False
                heapq.heappush(frontier, [f_n ,g_n + temp, (edge, explored_queue.copy(), explored_goals.copy())])
    print(explored_queue)
    print ('Time: ' + str(time.time() - start_time))
    path = []
    prev = explored_queue.popleft()
    curr = explored_queue.popleft()
    while explored_queue:
        if path:
            path.pop(0)
        path = span_tree[prev][curr] + path
        prev = curr
        curr = explored_queue.popleft()
    if path:
            path.pop(0)
    path = span_tree[prev][curr] + path 
    path.reverse()
   
    return path, states

def helper_astar(maze, start, end):
    curr = start
    goal = end
    maze_size = maze.getDimensions()

    visited = {}
    tree = SearchTree(curr, goal)
    frontier = []

    g_n = 1
    f_n = g_n + calc_manhattan(curr, goal)
    heapq.heappush(frontier,[f_n, g_n, curr])
    fin_g = goal
    while frontier:
        current_node = heapq.heappop(frontier)
        curr = current_node[2]
        g_n = current_node[1]

        if curr == goal:
            break

        h_n = calc_manhattan(goal, curr)
        f_n = g_n + h_n

        if curr not in visited:
            visited[curr] = f_n
            g_n += 1
            for neighbor in maze.getNeighbors(curr[0], curr[1]):
                f_n = g_n + calc_manhattan(goal, neighbor)
                if neighbor not in visited:
                    heapq.heappush(frontier, [f_n, g_n, neighbor])
                    tree.insert(neighbor, curr)
    return tree.find_path(start, goal) , goal, len(visited)

def neighbor_list(maze, current_pos):
    return maze.getNeighbors(current_pos[0], current_pos[1])

def sort_list(goal, neighbor_list):
    new_list = []
    sorted_list = []
    for i in neighbor_list:
        dist = calc_manhattan(goal, i)
        new_list.append((dist, i))
    new_list.sort(reverse=True)
    for i in new_list:
        sorted_list.append(i[1])
    return sorted_list

def calc_manhattan(goal, coordinate):
    dist = abs(goal[0] - coordinate[0]) + abs(goal[1] - coordinate[1])
    return dist

def is_completed(explored):
    keys = explored.keys()
    for key in keys:
        if explored[key] == False:
            return False
    return True

class Uptree:
    def __init__(self, goals):
        self.tree = dict.fromkeys(goals, -1)
    def find(self, key):
        if self.tree[key] == -1:
            return key
        rootVal = self.find(self.tree[key])
        self.tree[key] = rootVal
        return rootVal
    def union(self, left, right):
        right_root = self.find(right)
        self.tree[right_root] = self.find(left)

def MST(explored_map, path_map):
    vertices = []
    for goal in explored_map:
        if explored_map[goal] == False:
            vertices.append(goal)
    frontier = []
    for source in vertices:
        for dest in vertices:
            if source != dest:
                heapq.heappush(frontier, [len(path_map[source][dest]), source, dest])
    edge_lim = len(vertices) - 1
    retVal = 0
    edge_num = 0
    tree = Uptree(vertices)
    while frontier and edge_num != edge_lim:
        edge = heapq.heappop(frontier)
        source = edge[1]
        dest = edge[2]
        if tree.find(source) !=  tree.find(dest):
            tree.union(source, dest)
            retVal += len(path_map[source][dest])
            edge_num += 1
    return retVal