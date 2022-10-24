"""
Author: Oğuz Gögebakan
Date: 23.10.22
Maximum Path Sum Problem

Answers:
Part 1: 1074
Part 2: 7273

Approach:
- Firstly, a function to read the txt file is developed (read_triangle). Txt file is stored in a list of lists.
- Secondly, a recursive function to analyze the triangle is developed. The function actually checks for every possible path in a recursive way.
- Thirdly, the program is tested. It worked so slow in the part 2. Thus, a memory mechanism is added to the program. For a node, it descendants's
max path sum is stored in a dictionary. So before calculating a node's descendants' max path sum, the program first checks the dictionary if it is
calculated before (This is recursion with memory (Dynamic programming)).
- Unit tests are not written since the program is quite simple. Yet, there is a mechanism which checks whether the given TXT consists of integers.
- This code will work best if the given triangle is a complete tree. This means that every node has either 2 childs or no children. Still, the code
may work if the triangle is not complete since a mechanism is developed and it runs when a node has only one child.

Comments:
- Since this is a code which uses recursion, if the given triangle is TOO big, Python's recursion stack may not be adequate. The recursion stack of
C++ is much higher.
- I could have used multiple files if the task was more complicated.
"""

import sys

"""
	This function reads the triangle and stores it in a list of lists. Every child list is one row. A node's left child is
	in the next list which has the same index with the node. Right child is also in the next list but it's index is 1 more.
	Ex: If triangle[0][0] is the node (root), its left child is triangle[1][0] and right child is triangle[1][1]
""" 
def read_triangle(filename):

	triangle = []

	with open(filename) as file:
		lines = file.readlines()
		line_counter = 0

		for line in lines:
			line_counter = line_counter + 1
			numbers_of_row_as_str = line.split(' ')
			numbers_of_row = []

			# Checking if all the numbers in a row are integers. If so, doing an int cast
			for number_as_str in numbers_of_row_as_str:
				try:
					numbers_of_row.append(int(number_as_str))
				except Exception as e:
					raise TypeError("The triangle text contains non-integer elements! Please remove the error on line %s." % (line_counter))

			triangle.append(numbers_of_row)

	return triangle

"""
	This function checks if a left child exists.
"""
def check_left_child(triangle, parent_row_count, parent_row_idx):

	try:
		triangle[parent_row_count + 1][parent_row_idx]
		return True
	except IndexError:
		return False


"""
	This function checks if a right child exists.
"""
def check_right_child(triangle, parent_row_count, parent_row_idx):

	try:
		triangle[parent_row_count + 1][parent_row_idx + 1]
		return True
	except IndexError:
		return False


"""
	
"""
def calc_max_path_recursive(triangle, memory_dict, node_row_count, node_row_idx):

	left_subtree_max = right_subtree_max = None
	memory_key = str(node_row_count) + '-' + str(node_row_idx)

	if memory_key in memory_dict:
		return memory_dict[memory_key]

	# If the node has a left child
	if check_left_child(triangle, node_row_count, node_row_idx):

		left_subtree_max = calc_max_path_recursive(triangle, memory_dict, node_row_count + 1, node_row_idx)

	# If the node has a right child
	if check_right_child(triangle, node_row_count, node_row_idx):

		right_subtree_max = calc_max_path_recursive(triangle, memory_dict, node_row_count + 1, node_row_idx + 1)

	node = triangle[node_row_count][node_row_idx]

	# If the node has at least 1 child
	if left_subtree_max or right_subtree_max:

		val_to_return = None
		
		# If there are both childs, check which value from which subtree (left or right) is bigger
		if left_subtree_max and right_subtree_max:
			val_to_return = node + left_subtree_max if left_subtree_max > right_subtree_max else node + right_subtree_max

		# If there is only one child, sum its value with the node and return
		else:
			val_to_return = node + left_subtree_max if left_subtree_max and not right_subtree_max else node + right_subtree_max

		memory_dict[memory_key] = val_to_return
		return val_to_return

	# If no left or right child (a leaf), return its value
	else:
		return node


# Read the filename from the command line (first command)
triangle = read_triangle(sys.argv[1])

# Calculate and print max path
print(calc_max_path_recursive(triangle, dict(), 0, 0))