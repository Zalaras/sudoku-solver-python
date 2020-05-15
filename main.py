import csv

def read_puzzle(filename, preset_list):
	puzzle_info = []

	#Read file
	with open(filename, 'r', newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in reader:
			puzzle_info.append(row)

	#Check Sudoku format 9x9
	for x, row in enumerate(puzzle_info):
		for y, cell in enumerate(row):
			if x > 8 or y > 8:
				print('Too many rows or columns in file')
				return None

	#Convert to ints and save the coordinates list of the preset numbers
	for x, row in enumerate(puzzle_info):
		for y, cell in enumerate(row):
			if cell == '':
				puzzle_info[x][y] = 0
			else:
				try:
					cell_num = int(cell)
					if cell_num < 10 and cell_num > 0:
						puzzle_info[x][y] = cell_num
						preset_list.append((x,y))
					else:
						print('Number outside 1-9 in puzzle file')
						return None
				except ValueError as err:
					print('Non-number in puzzle, error: ', err)
					return None

	return puzzle_info

#Find which coordinates to use for which block a number is in
def find_block(x_pos, y_pos):
	#0-2x0-2, 0-2x3-5, 0-2x6-8 frist row of blocks
	#3-5x0-2, 3-5x3-5, 3x5x6-8
	#6-8x0-2, 6-8x3-5, 6-8x6-8
	if y_pos < 3:
		start_y = 0
	elif y_pos >= 3 and y_pos < 6:
		start_y = 3
	elif y_pos >= 6:
		start_y = 6

	if x_pos < 3:
		start_x = 0
	elif x_pos >= 3 and x_pos < 6:
		start_x = 3
	elif x_pos >= 6:
		start_x = 6

	return (start_x, start_y)

#Check for preset values based on list set at start
def check_preset_value(preset_list, x_pos, y_pos):
	for coords in preset_list:
		if coords[0] == x_pos and coords[1] == y_pos:
			return True
	return False

#Check row, column and block
def check_valid(puzzle_info, preset_list, x_pos, y_pos):
	#Check preset value
	# preset = check_preset_value(preset_list, x_pos, y_pos)
	# if preset:
	# 	return False
	#Check current row
	for x, cell in enumerate(puzzle_info[x_pos]):
		if cell == puzzle_info[x_pos][y_pos] and x != y_pos:
			return False
	#Check current column
	for x, row in enumerate(puzzle_info):
		if row[y_pos] == puzzle_info[x_pos][y_pos] and x != x_pos:
			return False
	#Check current block
	start_coords = find_block(x_pos, y_pos)
	for x in range(start_coords[0], start_coords[0]+3):
		for y in range(start_coords[1], start_coords[1]+3):
			if puzzle_info[x][y] == puzzle_info[x_pos][y_pos]:
				if x != x_pos and y != y_pos: #make sure not current value
					return False

	return True

#Move forward and down a row if needed
def move_forward(preset_list, x_pos, y_pos):
	new_x = x_pos
	new_y = y_pos
	preset = True

	while preset:
		new_y += 1
		if new_y > 8:
			new_y = 0
			new_x += 1
		#Skip over preset values
		preset = check_preset_value(preset_list, new_x, new_y)

	return(new_x, new_y)

#Handle moving backwards and up a row if needed
def move_backward(preset_list, x_pos, y_pos):
	new_x = x_pos
	new_y = y_pos
	preset = True

	while preset:
		new_y -= 1
		if new_y < 0:
			new_y = 8
			new_x -= 1
		#Skip over preset values
		preset = check_preset_value(preset_list, new_x, new_y)

	return(new_x, new_y)

#Increment the current value by 1, reset to 0 if need to move back
def increment_value(puzzle_info, x_pos, y_pos):
	puzzle_info[x_pos][y_pos] += 1
	if puzzle_info[x_pos][y_pos] > 9:
		puzzle_info[x_pos][y_pos] = 0
		return False
	return True

#Handle backtracing functions
def back_tracing_alg(puzzle_info, preset_list):
	solved = False
	valid = False
	current_x = 0
	current_y = 0

	#Loop until puzzle solved
	while not solved:
		increment = False
		#Check to see if current value is a preset value
		preset = check_preset_value(preset_list, current_x, current_y)
		if not preset:
			increment = increment_value(puzzle_info, current_x, current_y)

		valid = check_valid(puzzle_info, preset_list, current_x, current_y)
		if valid:
			coords = move_forward(preset_list, current_x, current_y)
			current_x = coords[0]
			current_y = coords[1]
			#If out of bounds and all above okay then exit as puzzle solved
			if current_x > 8 or current_y > 8:
				solved = True
		elif not increment:
			coords = move_backward(preset_list, current_x, current_y)
			current_x = coords[0]
			current_y = coords[1]
			if current_x < 0:
				print('Cannot be solved')
				break

def print_puzzle(puzzle_info):
	for x, row in enumerate(puzzle_info):
		for y, cell in enumerate(row):
			if y == 3 or y == 6:
				print('|', end='')
			if y == 2 or y == 5:
				print(cell, end='')
			else:
				print(cell, ' ', end='')
		print('')
		if x == 2 or x == 5:
			print('-'*23)

preset_list = []
#Read info from csv
puzzle_info = read_puzzle('Puzzle1.csv', preset_list)
#Make sure puzzle has info from reader
if puzzle_info:
	print('Unsolved')
	print_puzzle(puzzle_info)
	#Run file thorugh backtracing alg
	back_tracing_alg(puzzle_info, preset_list)
	#Output solved file
	print('\nSolved')
	print_puzzle(puzzle_info)