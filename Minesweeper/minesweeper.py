import pygame
import random
import math
import copy

pygame.init()
#infoObject = pygame.display.Info()
pygame.display.set_caption("Basic Minesweeper")
clock = pygame.time.Clock()

class Game:
	def __init__(self, mines_num, board_size):
		self.mines_num = mines_num
		self.board_size = board_size
		self.game_state = "start"
		self.board = [ [ 0 for i in range(board_size)] for j in range(board_size) ]
		self.cur_mines = list(range(self.mines_num))
		self.base_board = []
		#self.square_size = 40

	def draw_game(self):
		gameDisplay.blit(pygame.image.load("Img/background.png"), (0, 0))
		self.mines_place()
		self.surround_nums_place()
		self.base_board = copy.deepcopy(self.board)
		for i, row in enumerate(self.board):
			for j, square in enumerate(row):
				cur_square = (40 * i, 40 * j)
				gameDisplay.blit(pygame.image.load("Img/blank.png"), cur_square)
		pygame.display.update()
	
	#Determime mine locations using reservoir sampling
	def mines_place(self):
		for i in range(self.mines_num, self.board_size ** 2):
			samp = random.randint(1, i + 1)
			#print(samp, i)
			if samp <= self.mines_num:
				random.shuffle(self.cur_mines)
				self.cur_mines.pop()
				self.cur_mines.append(i)
		#print(self.cur_mines.sort())
		for mine in self.cur_mines:
			mine_row = (mine - 1) // self.board_size
			mine_col = (mine - 1) % self.board_size
			#print(mine_row, mine_col)
			self.board[mine_row][mine_col] = "mine"

	def surround_nums_place(self):
		for i in range(self.board_size):
			for j in range(self.board_size):
				if self.board[i][j] != "mine":
					surround_mine = 0
					for row, col in (i + 1, j), (i, j + 1), (i - 1, j), (i, j - 1), (i + 1, j - 1), (i + 1, j + 1), (i - 1, j + 1), (i - 1, j - 1):
						if 0 <= row < self.board_size and 0 <= col < self.board_size:
							if self.board[row][col] == "mine":
								surround_mine = surround_mine + 1
					self.board[i][j] = surround_mine

	def board_event(self):
		for event in pygame.event.get():
			if self.game_state != "end":
				self.check_completed()
			if event.type == pygame.QUIT:
				#quit()
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN and self.game_state != "end":
				a, b = event.pos
				r_click, c_click = a // 40, b // 40
				#print(r_click, c_click)
				if 0 <= r_click < self.board_size and 0 <= c_click < self.board_size:
					if event.button == 1:
						if self.board[r_click][c_click] == "mine":
							for i, row in enumerate(self.base_board):
								for j, square in enumerate(row):
									cur_square = (40 * i, 40 * j)
									if square == "mine":
										gameDisplay.blit(pygame.image.load("Img/mine.png"), cur_square)
							self.game_state = "end"
							print("You Lose")
						else:
							self.board_spread(r_click, c_click)
					if event.button == 3:
						if isinstance(self.board[r_click][c_click], int) or self.board[r_click][c_click] == "mine":
							self.board[r_click][c_click] = "flag"
							gameDisplay.blit(pygame.image.load("Img/flag.png"), (40 * r_click, 40 * c_click))
						elif self.board[r_click][c_click] == "flag":
							self.board[r_click][c_click] = self.base_board[r_click][c_click]
							gameDisplay.blit(pygame.image.load("Img/blank.png"), (40 * r_click, 40 * c_click))
			pygame.display.update()

	def board_spread(self, r, c):
		if self.board[r][c] == 0:
			self.board[r][c] = "spread"
			gameDisplay.blit(pygame.image.load("Img/spread.png"), (40 * r, 40 * c))
			for next_row, next_col in (r + 1, c), (r, c + 1), (r - 1, c), (r, c - 1):
				if 0 <= next_row < self.board_size and 0 <= next_col < self.board_size :
					self.board_spread(next_row, next_col)
		elif isinstance(self.board[r][c], int):
			num_img = "Img/" + str(self.board[r][c]) + ".png"
			self.board[r][c] = "num_set"
			gameDisplay.blit(pygame.image.load(num_img), (40 * r, 40 * c))

	def check_completed(self):
		self.game_state = "end"
		for i, row in enumerate(self.board):
			for j, square in enumerate(row):
				if square == "mine":
					self.game_state = "start"
					break
		if self.game_state == "end":
			print("You Won")

	#def print_board(self):
	#	for row in self.board:
	#		print(row)

if __name__ == "__main__":
	print("How Many Mines?:")
	mines_num = int(input())
	print("Size of Board?:")
	board_size = int(input())
	if board_size > 20:
		print("Board Too Large")
	elif mines_num >= board_size ** 2:
		print("Too Many Mines")
	else:
		gameDisplay = pygame.display.set_mode((40 * board_size , 40 * board_size))
		game = Game(mines_num, board_size)
		game.draw_game()
		while True:
			game.board_event()
			pygame.display.update()
			clock.tick(60)
