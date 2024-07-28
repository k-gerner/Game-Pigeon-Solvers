def edge_square_mapping(size):
	"""
	Returns a dict mapping the edge index to the square indices
	:param int size: Number of dots in each row/col
	"""
	num_edges = 2 * (size**2 - size)
	squares_dimension = size - 1  # squares per row/col
	num_squares = (size - 1) ** 2
	edge_to_squares = {}
	for i in range(num_edges):
		if i < size**2 - size:
			# is horizontal, n-1 per row
			edge_row = i // squares_dimension  # 7 = 2
			edge_col = i % squares_dimension
			if edge_row == 0:
				# in top row of edges
				edge_to_squares[i] = [i]
			elif edge_row == size - 1:
				# in bottom row of edges
				edge_to_squares[i] = [i - squares_dimension]
			else:
				top_square = (squares_dimension * (edge_row - 1)) + edge_col
				bottom_square = (squares_dimension * edge_row) + edge_col
				edge_to_squares[i] = [top_square, bottom_square]
		else:
			# is vertical, n per row
			i_norm = i - (size**2 - size) # 17 = 5
			edge_row = i_norm // size  # 17 = 1
			edge_col = i_norm % size  # 17 = 1
			if edge_col == 0:
				# in left col of edges
				edge_to_squares[i] = [edge_row * squares_dimension]
			elif edge_col == size - 1:
				# in right col of edges
				edge_to_squares[i] = [(edge_row * squares_dimension) + (size - 2)]
			else:
				left_square = (squares_dimension * edge_row) + (edge_col - 1)
				right_square = (squares_dimension * edge_row) + edge_col
				edge_to_squares[i] = [left_square, right_square]
	return edge_to_squares


