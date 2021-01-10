# gameboard.py
import random

class gameboard:
	# When actually playing, the user sees up to 20 rows
	# 24 rows to avoid boundary errors
	ROWS = 24
	COLUMNS = 10

	def __init__(self, randomizer):
		self.board = []
		self.randomizer = randomizer

	def create_board(self):
		'''Creates an empty game board'''
		self.board = [ ['X' for i in range(self.COLUMNS)] for i in range(self.ROWS) ] 
		self.current_piece = None
		self.location = []
		self.corner = []

	def get_board(self):
		return self.board

	def place_piece(self, piece: "piece"):
		'''Places a piece into the game board'''
		self.current_piece = piece
		self.location.clear()
		# Handles condition where the board is stacked too high,
		# allowing pieces to spawn above visible rows
		stacked_high = False
		for i in range(2):
			for j in range(3):
				if self.board[i+4][j+3] != 'X':
					stacked_high = True
					break

		if self.current_piece.size == 3:
			if stacked_high == True:
				self.corner = [2, 3]
			else:
				self.corner = [4, 3]
			for i in range(2):	# Access the row from small board
				for j in range(3):	# Access the column / piece
					# only allows pieces, not 'X' to be placed
					if piece.test_board[i][j] == piece.piece:
						self.board[i+self.corner[0]][j+self.corner[1]] = piece.test_board[i][j]
						self.location.append([i+self.corner[0], j+self.corner[1]])
		
		#handle if the piece is I and O block
		else:
			if stacked_high == True:
				self.corner = [1, 3]
			else:
				self.corner = [3, 3]
			for i in range(3):
				for j in range(4):
					if piece.test_board[i][j] == piece.piece:
						self.board[i+self.corner[0]][j+self.corner[1]] = piece.test_board[i][j]
						self.location.append([i+self.corner[0], j+self.corner[1]])


	def hard_drop(self):
		'''
		instantly drops the piece to the bottom
		and locks it
		'''
		while self.current_piece.locked != True:
			self.drop_piece()
	
	def clear_rows(self):
		'''
		Checks to see if any lines can be cleared
		in the board, and clears them
		'''
		clear_count = 0
		lowest_row = 0
		for loc in self.location:
			if 'X' not in self.board[loc[0]]:
				if lowest_row < loc[0]:
					clear_count += 1
					lowest_row = loc[0]

		if clear_count > 0:
			for i in range(lowest_row):
				if lowest_row-i > clear_count:
					for j in range(len(self.board[0])):
						self.board[lowest_row-i][j] = self.board[lowest_row-i-clear_count][j]
				else:
					for j in range(len(self.board[0])):
						self.board[lowest_row-i][j] = 'X'


	def drop_piece(self):
		''' 
		Takes the piece that isn't locked and drops it by one place. 
		If something is already below it, lock the piece.
		'''
		droppable = True
		for loc in self.location:
			if loc[0] == 23:
				droppable = False
				break
			elif self.board[loc[0]+1][loc[1]] not in ['X', self.current_piece.piece]:
				droppable = False
				break

		if droppable == True:
			self.corner[0] += 1
			for loc in self.location:
				self.board[loc[0]][loc[1]] = 'X'
			temp = []
			for loc in self.location:
				self.board[loc[0]+1][loc[1]] = self.current_piece.piece
				temp.append([loc[0]+1, loc[1]])
			self.location = temp
		
		else:
			for loc in self.location:
				self.board[loc[0]][loc[1]] += "X"
			self.current_piece.locked = True

	def move(self, right: bool):
		'''
		Checks if the left or right location is valid
		then moves the piece left or right based on input
		'''
		# Checks if the piece can move right
		is_valid = True
		if right == True:
			for loc in self.location:
				if loc[1] == len(self.board[0])-1:
					is_valid = False
					break
				elif self.board[loc[0]][loc[1]+1] not in ['X', self.current_piece.piece]:
					is_valid = False
					break
		# Checks if the piece can move left
		elif right == False:
			for loc in self.location:
				if loc[1] == 0:
					is_valid = False
					break
				elif self.board[loc[0]][loc[1]-1] not in ['X', self.current_piece.piece]:
					is_valid = False
					break
		# move the piece left or right based on whether bool "right" is true or false
		if is_valid == True:
			increment = -1
			if right == True:
				increment = 1
				if self.current_piece.size == 3:
					if self.corner[1] < 7:
						self.corner[1] += 1
				else:
					if self.corner[1] < 6:
						self.corner[1] += 1

			else:
				if self.corner[1] > 0:
					self.corner[1] -= 1
			for loc in self.location:
				self.board[loc[0]][loc[1]] = 'X'
			temp = []
			for loc in self.location:
				self.board[loc[0]][loc[1]+increment] = self.current_piece.piece
				temp.append([loc[0], loc[1]+increment])
			self.location = temp

	def get_next(self):
		"""places the next piece in the board if current is locked"""
		piece_string = self.randomizer.get_next_piece()
		p = piece(piece_string)
		p.build_piece()
		self.place_piece(p)

	def rotate_piece(self):
		new_location = []
		self.current_piece.rotate()
		# get the location of the piece
		for i in range(len(self.current_piece.test_board)):
			for j in range(len(self.current_piece.test_board[0])):
				if self.current_piece.test_board[i][j] == self.current_piece.piece:
					if self.board[self.corner[0] + i][self.corner[1] + j] in \
					[self.current_piece.piece, "X"]:
						new_location.append([self.corner[0]+i, self.corner[1]+j])

		if len(new_location) == 4:
			for i in range(len(self.current_piece.test_board)):
				for j in range(len(self.current_piece.test_board[0])):
					if self.board[self.corner[0] + i][self.corner[1] + j] == self.current_piece.piece:
						self.board[self.corner[0] + i][self.corner[1] + j] = 'X'
			self.location = new_location
			for loc in self.location:
				self.board[loc[0]][loc[1]] = self.current_piece.piece
		else:
			# rotate the example piece back to the original position
			# since it failed to be mapped into the new position
			for i in range(3):
				self.current_piece.rotate()

	def check_game_over(self) -> bool:
		'''returns true if the game is over'''
		game_over = False
		for i in range(3):
			for j in range(self.COLUMNS):
				# search board bottom up; piece will likely be lower in the board
				if self.board[3-i][j] != 'X':
					# if the len of string is > 1, it's locked
					if len(self.board[3-i][j]) == 2:
						game_over = True
						break
		if game_over == True:
			return True
		return False

class randomizer:
	PIECE_MAP = {0:'S', 1:'L', 2:'J', 3:'T', 4:'Z', 5:'O', 6:'I'}

	def __init__(self):
		self.pieces = []

	def get_next_piece(self):
		if len(self.pieces) == 0:
			self.load_pieces()
			return self.PIECE_MAP[self.pieces.pop(0)]
		else:	
			return self.PIECE_MAP[self.pieces.pop(0)]

	def load_pieces(self):
		for num in range(7):
			self.pieces.append(num)
			self.pieces.append(num)
		random.shuffle(self.pieces)

	def next_five(self):
		'''returns the next 5 pieces for the user to see'''
		return self.pieces[0:5]

class piece:
	def __init__(self, piece):
		self.piece = piece
		self.size = 3
		self.test_board = [['X' for i in range(self.size)] for i in range(self.size)]
		self.locked = False
		self.locked_counter = 10
		self.method_map = {"S": self.create_S, "L":self.create_L, "J":self.create_J,
							"T":self.create_T, "Z":self.create_Z, "O":self.create_O,
							"I":self.create_I}

	def build_piece(self):
		"""Maps the piece given to the method needed to build
		   the piece""" 
		self.method_map[self.piece]()

	def create_S(self):
		self.test_board[0][1] = 'S'
		self.test_board[0][2] = 'S'
		self.test_board[1][0] = 'S'
		self.test_board[1][1] = 'S'

	def create_L(self):
		self.test_board[0][2] = 'L'
		self.test_board[1][0] = 'L'
		self.test_board[1][1] = 'L'
		self.test_board[1][2] = 'L'

	def create_J(self):
		self.test_board[0][0] = 'J'
		self.test_board[1][0] = 'J'
		self.test_board[1][1] = 'J'
		self.test_board[1][2] = 'J'

	def create_T(self):
		self.test_board[0][1] = 'T'
		self.test_board[1][0] = 'T'
		self.test_board[1][1] = 'T'
		self.test_board[1][2] = 'T'

	def create_Z(self):
		self.test_board[0][0] = 'Z'
		self.test_board[0][1] = 'Z'
		self.test_board[1][1] = 'Z'
		self.test_board[1][2] = 'Z'

	def create_O(self):
		self.size = 4
		self.test_board = [['X' for i in range(self.size)] for i in range(self.size)]
		self.test_board[1][1] = 'O'
		self.test_board[1][2] = 'O'
		self.test_board[2][1] = 'O'
		self.test_board[2][2] = 'O'

	def create_I(self):
		self.size = 4
		self.test_board = [['X' for i in range(self.size)] for i in range(self.size)]
		self.test_board[1][0] = 'I'
		self.test_board[1][1] = 'I'
		self.test_board[1][2] = 'I'
		self.test_board[1][3] = 'I'


	def rotate(self):
		# 00, 01, 02 -->  20, 10, 00
		# 10, 11, 12	  21, 11, 01
		# 20, 21, 22	  22, 12, 02
		# rotate 2D array
		rotated = [['X' for i in range(self.size)] for i in range(self.size)]
		# transpose matrix 
		for i in range(self.size):
			for j in range(self.size):
				rotated[i][j] = self.test_board[j][i]
				rotated[j][i] = self.test_board[i][j]
		self.test_board = list(rotated)
		# flip matrix
		for i in range(self.size):
			for j in range(int(self.size/2)):
				temp = self.test_board[i][j]
				rotated[i][j] = self.test_board[i][self.size-1-j]
				rotated[i][self.size-1-j] = temp

	def get_piece(self):
		return self.test_board
