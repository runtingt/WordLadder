import numpy as np
from collections import defaultdict, deque
from pyvis.network import Network

# Get the dictionary
with open("dict.txt") as input_file:
    word_list = [line for line in input_file.read().strip().split(',')]

# Function to backtrack through a path
def backtrace(parent, begin_word, end_word):
    path = [end_word]
    while path[-1] != begin_word:
        path.append(parent[path[-1]])
    path.reverse()
    return path

# Get the length of the word ladder
def ladder_length(begin_word, end_word, word_list):
    # Check a solution is possible
    if end_word not in word_list:
        return 0

    # Create a blank dictionary of neighbours
    neighbours = defaultdict(list)
    
    # Get all the pattern : [words] combinations
    for word in word_list:
        for j in range(len(word)):
            pattern = word[:j] + "*" + word[j+1:]
            neighbours[pattern].append(word)
            
    # Track the visited words, track the search queue and score
    visited = set([begin_word])
    q = deque([begin_word])
    score = 1
    
    # Search until the queue is empty
    parent = {}
    shortest_paths = []
    while q:
        for i in range(len(q)):
            # Breadth first search
            word = q.popleft()
            if word == end_word:
                return score, backtrace(parent, begin_word, end_word)
            # Get the neighbours of the search word
            for j in range(len(word)):
                pattern = word[:j] + "*" + word[j+1:]
                for neighbour in neighbours[pattern]:
                    if neighbour not in visited:
                        parent[neighbour] = word
                        visited.add(neighbour)
                        q.append(neighbour)
        score += 1         
            
    # If we don't find anything, exit with a score of 0
    print(shortest_paths)
    return 0

# Get all possible paths of length shortest
def get_paths(begin_word, end_word, word_list, shortest):
    # Initiliase a search tree and a set of visited nodes
    to_search = [(begin_word,)]
    visited = set([begin_word])
    all_paths = set()
    
    # Create a blank dictionary of neighbours
    neighbours = defaultdict(list)
    
    # Get all the pattern : [words] combinations
    for word in word_list:
        for j in range(len(word)):
            pattern = word[:j] + "*" + word[j+1:]
            neighbours[pattern].append(word)
    
    while to_search:
        # Get the path to search
        path = to_search.pop()
        
        # Check the path can still lead to a solution in time
        path_okay = True
        target = np.array([char for char in end_word])
        for index, word in enumerate(path):
            if (len(target) 
                - np.sum(np.array([char for char in word] == target)) 
                > shortest-index-1):
                path_okay = False
        
        if len(path) <= shortest and path_okay:
            # Check if we have reached the end
            if path[-1] == end_word:
                all_paths.add(path)
                continue # Skip the iterations below
            
            # Add the neighbours to the search tree
            word = path[-1]
            for j in range(len(word)):
                pattern = word[:j] + "*" + word[j+1:]
                for neighbour in neighbours[pattern]:
                    if neighbour not in path:
                        visited.add(neighbour)
                        to_search.append((*path, neighbour))
    
    return all_paths


def solve(start, target):
    # Get a shortest path, use this to find all other shortest paths
    try:
        score, path = ladder_length(start, target, word_list) 
        paths = get_paths("hide", "eggs", word_list, score)
    except TypeError:
        print("No solution found")
    
    # Display results
    print("Possible shortest paths:")
    for path in paths:
        print(path)
    print("Best Score:", score-1)
    
    # Create a blank dictionary of neighbours
    neighbours = defaultdict(list)
    # Get all the pattern : [words] combinations
    for word in word_list:
        for j in range(len(word)):
            pattern = word[:j] + "*" + word[j+1:]
            neighbours[pattern].append(word)
            
    # Create a graph with the word list as nodes
    net = Network(height="100%", width="100%", notebook=True)
    net.add_node(start, color="red")
    net.add_node(target, color="green")
    net.set_template('larger_template.html')
    net.write_html('larger_template.html')
    
    # Add edges between words that differ by one from the target
    nodes = set(np.array(list(paths)).flatten())
    net.add_nodes(list(nodes), color=["pink"]*len(nodes))   
        
    # Add nodes and edges to the graph that are neighbours to these nodes
    for word in nodes:
        net.add_node(word)
        for j in range(len(word)):
            pattern = word[:j] + "*" + word[j+1:]
            for neighbour in neighbours[pattern]:
                if neighbour != word:
                    net.add_node(neighbour)
                    if neighbour in nodes:
                        net.add_edge(word, neighbour, color="pink")
                    else:
                        net.add_edge(word, neighbour, color="black")
    net.toggle_physics(True)
    return net
    
    

if __name__ == "__main__":
    # Get inputs
    start = "hide"
    target = "eggs"
    
    # For testing multiple shortest paths
    word_list.append("emgs")
    word_list.append("emds")
    word_list.append("amds")
    
    # Get a shortest path, use this to find all other shortest paths
    score, path = ladder_length(start, target, word_list) 
    paths = get_paths("hide", "eggs", word_list, score)
    
    # Display results
    print("Possible shortest paths:")
    for path in paths:
        print(path)
    print("Best Score:", score-1)
    
    # Create a blank dictionary of neighbours
    neighbours = defaultdict(list)
    # Get all the pattern : [words] combinations
    for word in word_list:
        for j in range(len(word)):
            pattern = word[:j] + "*" + word[j+1:]
            neighbours[pattern].append(word)
    
    # Create a graph with the word list as nodes
    net = Network(height="100%", width="100%", notebook=True)
    net.add_node(start, color="red")
    net.add_node(target, color="green")
    net.set_template('larger_template.html')
    net.write_html('larger_template.html')
    
    # Add edges between words that differ by one from the target
    nodes = set(np.array(list(paths)).flatten())
    net.add_nodes(list(nodes), color=["pink"]*len(nodes))
    
    # Add nodes and edges to the graph that are neighbours to these nodes
    for word in nodes:
        net.add_node(word)
        for j in range(len(word)):
            pattern = word[:j] + "*" + word[j+1:]
            for neighbour in neighbours[pattern]:
                if neighbour != word:
                    net.add_node(neighbour)
                    if neighbour in nodes:
                        net.add_edge(word, neighbour, color="pink")
                    else:
                        net.add_edge(word, neighbour, color="black")
      
    # Display the graph
    net.toggle_physics(True)
    net.show("graph1.html")
