import board
import math

#Propegate changes when a cheaper path to a node is found
def update_existing_node(new_parent, new_path, existing_node):
	if existing_node.g > new_path + existing_node.cost:
		existing_node.g = new_path + existing_node.cost
		existing_node.parent = new_parent
		# Update child nodes aswell
		for kid in existing_node.kids:
			update_existing_node(existing_node, existing_node.g, kid)


# Get the minimum cost node from the open set
def extract_min(nodes):
	min_score = math.inf
	min_index = 0
	for i, node in enumerate(nodes):
		if min_score > node.g + node.h:
			min_score = node.g + node.h
			min_index = i

	return nodes.pop(min_index)

# Backtrack from the goal node, add each node to the path list
def build_path(node):
	path = []
	# Start node got no parent
	while(node.parent.parent != None):
		node = node.parent
		path.append((node.x, node.y))
	return path

# Main algorithm
def a_star(board):

	#Initialize
	closed = []
	open_nodes = [board.get_start_node()]

	while open_nodes:

		# Get next node to explore
		current = extract_min(open_nodes)

		# If it is a solution, we are finished
		if board.is_goal_node(current):
			return build_path(current)

		# Get adjecent nodes
		neighbours = board.get_neighbour_nodes(current)

		# Marked the current node as closed
		closed.append(current)

		# Iterate over the newly found nodes
		for node in neighbours:

			# If it is already explored, ignore it
			if node in closed:
				continue

			# Set heuristic function
			node.h = board.get_distance_to_goal(node)

			# If it is already found, check if this is a better path
			if node in open_nodes:
				update_existing_node(current, current.g, node)
				continue

			# Add new node to open set
			node.g = node.cost + current.g
			open_nodes.append(node)
			
	# No path found ¯\_(ツ)_/¯
	return None

def main():
	txtfiles = [
		"board-1-0.txt",
		"boards/board-1-1.txt",
		"boards/board-1-2.txt",
		"boards/board-1-3.txt",
		"boards/board-1-4.txt",
		"boards/board-2-1.txt",
		"boards/board-2-2.txt",
		"boards/board-2-3.txt",
		"boards/board-2-4.txt"
	]
	for txt in txtfiles:
		b = board.Board(txt)
		solution = a_star(b)
		b.print_board([])
		print()
		b.print_board(solution)
		print()

if __name__ == "__main__":
	main()
	