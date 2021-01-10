import pygame
import math
import time
import gameboard as gb

class view:
	def __init__(self, gb):
		self.gameboard = gb
		self.window_width = 1000
		self.window_height = 800
		self.window_size = (self.window_width, self.window_height)
		self.running = True
		pass


	def update_board(self, gb: "Gameboard()"):
		self.gameboard = gb


	def _draw_lines(self):
		surface = pygame.display.get_surface()
		y = math.floor((self.window_height - (self.window_height*0.9))/2)
		x = math.floor((self.window_width - ((self.window_height*0.9)/20)*10)/2)
		increment = 0
		# start at 4 because there are 24 rows but user sees 20
		for row in range(4, len(self.gameboard.get_board())+1):
			# draws the x axis
			x_stop = x + math.floor(((self.window_height*0.9)/20))*10
			pygame.draw.line(surface, (60, 60, 60), (x, y + increment), 
							(x_stop, y + increment))

			# draws the y axis 
			y_stop = y + math.floor((self.window_height*0.9)/20)*20
			if row <= 4 + 10:
				pygame.draw.line(surface, (60, 60, 60), (x + increment, y), 
							(x + increment, y_stop))

			# any rescale is based ONLY on the window height
			increment += math.floor((self.window_height*0.9)/20)

	def _draw_blocks(self):
		"""Loops through the game board and draws the blocks"""
		surface = pygame.display.get_surface()
		colors = {"J": (15, 105, 245), "I": (85, 235, 255), 
				  "L":(255, 170, 0), "S": (45, 255, 55), "Z": (255, 4, 0),
				  "O": (238, 255, 0), "T": (245, 0, 255)}
		y = math.floor((self.window_height - (self.window_height*0.9))/2)
		x = math.floor((self.window_width - ((self.window_height*0.9)/20)*10)/2)
		increment = math.floor((self.window_height*0.9)/20)
		# loops through board and draws to the correct spot
		for i in range(4, len(self.gameboard.get_board())):
			for j in range(len(self.gameboard.get_board()[i])):
				x_incremented = math.floor(x + (increment * j))
				y_incremented = math.floor(y + (increment * (i-4)))
				if self.gameboard.get_board()[i][j][0] in colors:
					pygame.draw.rect(surface, colors[self.gameboard.get_board()[i][j][0]],
									(x_incremented, y_incremented, increment, increment))
									# x, y, x_wid, y_len
				else:
					pygame.draw.rect(surface, (0,0,0),
									(x_incremented, y_incremented, increment, increment))

	def _draw_start(self):
		pass

	def _restart(self):
		pass

	def _draw_ghost(self):
		''' 
		Future feature, draws the ghost piece for
		the user to see where the piece will land
		'''
		pass

	def _resize_surface(self, size: (int, int)):
		surface = pygame.display.get_surface()
		self.window_width = size[0]
		self.window_height = size[1]
		self.window_size = (self.window_width, self.window_height)
		pygame.display.set_mode(size, pygame.RESIZABLE)

	def _handle_events(self, frame):

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.VIDEORESIZE:
				self._resize_surface(event.size)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.gameboard.hard_drop()
					if self.gameboard.current_piece.locked == True:
						self.gameboard.clear_rows()
						self.gameboard.get_next()
				elif event.key == pygame.K_UP:
					self.gameboard.rotate_piece()

		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT]:
			if (frame % 3 == 0):
				self.gameboard.move(True)
		if keys[pygame.K_LEFT]:
			if (frame % 3 == 0):
				self.gameboard.move(False)
		if keys[pygame.K_DOWN]:
			if (frame % 3 == 0):
				self.gameboard.drop_piece()

	def _redraw(self):
		self._draw_blocks()
		self._draw_lines()

	def run(self):
		pygame.init()
		pygame.display.set_caption("Tetris")
		pygame.display.set_mode((self.window_size))

		# watch out for this line
		#pygame.key.set_repeat(100, 50)

		clock = pygame.time.Clock()
		self._resize_surface(self.window_size)

		counter = 0
		while self.running:
			self._handle_events(counter)
			self._redraw()

			if counter == 30:
				self.gameboard.drop_piece()
				if self.gameboard.current_piece.locked == True:
					self.gameboard.clear_rows()
					self.gameboard.get_next()
				counter = 0
			if self.gameboard.check_game_over() == True:
				# draw game over and click to play again
				pygame.time.wait(45)
				self.running = False
			clock.tick(60)
			pygame.display.update()
			counter += 1


def main():
	randomizer = gb.randomizer()
	board = gb.gameboard(randomizer)
	board.create_board()
	board.get_next()

	v = view(board)
	v.run()


if __name__ == '__main__':
	main()
