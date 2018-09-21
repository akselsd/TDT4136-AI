import math

WALL = "#"
START = "A"
GOAL = "B"

CHAR_TO_COST = {
	"w": 100,
	"m": 50,
	"f": 10,
	"g": 5,
	"r": 1,
	".": 1,
	"A": 0,
	"B": 0
}

CHAR_TO_STRING = {
	"w": "Water",
	"m": "Mountain",
	"f": "Forest",
	"g": "Grassland",
	"r": "Road",
	"A": "Start",
	"B": "End",
	"o": "Optimal path",
	"#": "Wall"

}

CHAR_TO_COLOR = {
	".": "30",
	"r": "30",
	"w": "34",
	"m": "92",
	"f": "32",
	"g": "33",
	"o": "35",
	"A": "31",
	"B": "36",
	"#": "37"
}
print_colors = True

class Node:

	# Initialize new node
	def __init__(self, x, y, cost, parent):
		self.parent = parent
		self.x = x
		self.y = y
		self.cost = cost
		self.g = math.inf
		self.h = math.inf
		self.kids = []

	def __hash__(self):
		return hash((self.x, self.y))

	def __cmp__(self, other):
		return cmp(self.g+self.h, other.g + other.h)

	def __eq__(self, other):
		if (other == None):
			return False
		return (self.x == other.x and self.y == other.y)

	def __str__(self):
		return "(" + str(self.x) + " ," + str(self.y) + ")"

	def __repr__(self):
		return self.__str__()


class Board:

	# Load the board into an array of strings
	def _load_board_from_file(self, txtfile):
		with open(txtfile) as f:
			for line in f.readlines():
				self._board.append(line.strip())

		self._size_y = len(self._board)
		self._size_x = len(self._board[0])

		# Assert that the board is rectangular (debugging)
		for row in self._board:
			if len(row) != self._size_x:
				print("Error loading board, board size not rectangular")
				print("Expected", self._size_x, "got", len(row),". Row: ", row)
				exit()

		# Find start and goal square
		for y in range(self._size_y):
			for x in range(self._size_x):
				if self._board[y][x] == START:
					self._start = (x, y)
				if self._board[y][x] == GOAL:
					self._goal = (x, y)

	# Decide if a square is a wall
	# Edges is treated as walls
	def _is_wall(self, x, y):
		if x < 0 or x >= self._size_x:
			return True

		if y < 0 or y >= self._size_y:
			return True

		return self._board[y][x] == WALL

	# Checks for walls in all 4 directions
	def _get_possible_directions(self, node):
		dirs = []
		for direction in [(+1, 0), (-1, 0), (0, +1), (0, -1)]:
			if not self._is_wall(
				direction[0] + node.x,
				direction[1] + node.y):
				dirs.append(direction)
		return dirs

	# Create new nodes from all possible neighbours
	def get_neighbour_nodes(self, node):
		dirs = self._get_possible_directions(node)
		neighbours = []
		for d in dirs:
			x = node.x + d[0]
			y = node.y + d[1]

			# Make new node
			neighbours.append(Node(
				x,
				y,
				CHAR_TO_COST[self._board[y][x]],
				node))

		# Add the newly created nodes as kids
		node.kids.extend(neighbours)
		return neighbours

	# Return manhatten distance to goal
	def get_distance_to_goal(self, node):
		return abs(node.x - self._goal[0]) + abs(node.y - self._goal[1])

	# Return startnode represented by A
	def get_start_node(self):
		n = Node(
			self._start[0],
			self._start[1],
			0,
			None)
		n.g = 0
		n.h = self.get_distance_to_goal(n)
		return n

	# Checks if a given node is the goal node
	def is_goal_node(self, node):
		return (node.x, node.y) == self._goal

	# Prints the board
	# @param solution is an array of (x, y) tuples 
	# that makes up the solution path
	def print_board(self, solution):
		for y in range(self._size_y):
			for x in range(self._size_x):
				if (x, y) in solution:
					char = "o"
				else:
					char = self._board[y][x]
				if print_colors:
					char = char_to_color(char)
				print(char, end ="")
			print()

	# Make new board
	def __init__(self, txtfile):
		self._board = []
		self._size_x = 0
		self._size_y = 0
		self._goal = None
		self._start = None
		self._load_board_from_file(txtfile)

# Map each board char to a ANSI-color. (For printing the board)
def char_to_color(char):
	fg = CHAR_TO_COLOR[char]
	bg = str(int(CHAR_TO_COLOR[char]) + 10)
	return "\033[" + fg + ";" + bg + "m" + char + "\033[0m"

def print_color_legend():
	print("-- Color Legend --")
	for char, string in CHAR_TO_STRING.items():
		print(char_to_color(char) + " - " + string)

