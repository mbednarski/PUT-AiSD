class TicTacToe:
	def __init__(self, player_a, player_b):
		self.p1 = player_a
		self.p2 = player_b
		self.board = ['-' for i in range(0, 9)]
		self.last_moves = []
		self.winner = None

	def print_board(self):

		print "\n:"

		for j in range(0, 9, 3):
			for i in range(3):
				if self.board[j + i] == '-':
					print "%d |" % (j + i),
				else:
					print "%s |" % self.board[j + i],

			print "\n",


	def available_positions(self):

		moves = []
		for i, v in enumerate(self.board):
			if v == '-':
				moves.append(i)
		return moves

	def put_sign(self, marker, pos):
		self.board[pos] = marker
		self.last_moves.append(pos)

	def undo(self):

		self.board[self.last_moves.pop()] = '-'
		self.winner = None

	def game_over(self):
		win_positions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

		for i, j, k in win_positions:
			if self.board[i] == self.board[j] == self.board[k] and self.board[i] != '-':
				self.winner = self.board[i]
				return True

		if '-' not in self.board:
			self.winner = '-'
			return True

		return False

	def play(self):

		for i in range(9):

			self.print_board()

			if i % 2 == 0:
				if self.p1.type == 'H':
					print "\t\t[Human's Move]"
				else:
					print "\t\t[Computer's Move]"

				self.p1.move(self)
			else:
				if self.p2.type == 'H':
					print "\t\t[Human's Move]"
				else:
					print "\t\t[Computer's Move]"

				self.p2.move(self)

			if self.game_over():
				self.print_board()
				if self.winner == '-':
					print "\nGame over with Draw"
				else:
					print "\nWinner : %s" % self.winner
				return


class Human:
	'''Class for Human player'''

	def __init__(self, marker):
		self.marker = marker
		self.type = 'H'

	def move(self, gameinstance):

		while True:

			m = raw_input("Input position:")

			try:
				m = int(m)
			except:
				m = -1

			if m not in gameinstance.available_positions():
				print "Invalid move. Retry"
			else:
				break

		gameinstance.put_sign(self.marker, m)


class AI:
	'''Class for Computer Player'''

	def __init__(self, marker):
		self.marker = marker
		self.type = 'C'

		if self.marker == 'X':
			self.opponentmarker = 'O'
		else:
			self.opponentmarker = 'X'

	def move(self, gameinstance):
		move_position, score = self.maximized_move(gameinstance)
		gameinstance.put_sign(self.marker, move_position)


	def maximized_move(self, gameinstance):
		''' Find maximized move'''
		bestscore = None
		bestmove = None

		for m in gameinstance.available_positions():
			gameinstance.put_sign(self.marker, m)

			if gameinstance.game_over():
				score = self.get_score(gameinstance)
			else:
				move_position, score = self.minimized_move(gameinstance)

			gameinstance.undo()

			if bestscore == None or score > bestscore:
				bestscore = score
				bestmove = m

		return bestmove, bestscore

	def minimized_move(self, gameinstance):
		''' Find the minimized move'''

		bestscore = None
		bestmove = None

		for m in gameinstance.available_positions():
			gameinstance.put_sign(self.opponentmarker, m)

			if gameinstance.game_over():
				score = self.get_score(gameinstance)
			else:
				move_position, score = self.maximized_move(gameinstance)

			gameinstance.undo()

			if bestscore == None or score < bestscore:
				bestscore = score
				bestmove = m

		return bestmove, bestscore

	def get_score(self, gameinstance):
		if gameinstance.game_over():
			if gameinstance.winner == self.marker:
				return 1  # Won
			elif gameinstance.winner == self.opponentmarker:
				return -1  # Opponent won
		return 0  # Draw


if __name__ == '__main__':
	player1 = Human("X")
	player2 = AI("O")
	game = TicTacToe(player1, player2)
	game.play()