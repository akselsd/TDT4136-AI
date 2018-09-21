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
# If use BFS is true, simply pop the first
# If use Djikstra is true, only use g
def extract_min(nodes):
	if USE_BFS:
		return nodes.pop(0)

	min_score = math.inf
	min_index = 0
	for i, node in enumerate(nodes):
		score = node.g
		if (not USE_DJIKSTRA and not USE_BFS):
			score+= node.h
		if min_score > score:
			min_score = score
			min_index = i

	return nodes.pop(min_index)

# Backtrack from the goal node, add each node to the path list
def build_path(node):
	path = []
	total_cost = 0
	# Start node got no parent
	while(node.parent.parent != None):
		node = node.parent
		total_cost+=node.cost
		path.append((node.x, node.y))
	return (path, total_cost)

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
			return (build_path(current), len(closed), len(open_nodes))

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


USE_BFS = False
USE_DJIKSTRA = False
ALOGITHM_NAMES = ["A*", "DJIKSTRA", "BFS"]
def main():
	global USE_BFS
	global USE_DJIKSTRA
	board.print_color_legend()
	for i in range(3):
		print("---"+ ALOGITHM_NAMES[i] + "---")
		(costs, closed, discovered) = run_algorithm()
		print(ALOGITHM_NAMES[i].rjust(10))
		print("Costs".rjust(10) + "".join([str(j).rjust(5) for j in costs]))
		print("Closed".rjust(10) + "".join([str(j).rjust(5) for j in closed]))
		print("Discovered".rjust(10) + "".join([str(j).rjust(5) for j in discovered]))
		print()
		if i == 0:
			USE_DJIKSTRA = True
		else:
			USE_DJIKSTRA = False
			USE_BFS = True



def run_algorithm():
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
	closed = []
	discovered = []
	costs = []
	for txt in txtfiles:
		b = board.Board(txt)
		((solution, cost), n_closed, n_open) = a_star(b)
		closed.append(n_closed)
		discovered.append(n_open)
		costs.append(cost)
		b.print_board(solution)
		print()
	return (costs, closed, discovered)


if __name__ == "__main__":
	main()
	