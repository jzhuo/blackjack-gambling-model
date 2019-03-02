

class QLearning():

	def __init__(self):
		self.s = [] # game states represented as a matrix
		self.a = [] # actions represented as a list
		self.q = [] # q values represented as a matrix
		self._initialize_model()

	# initializes the model with the necessary attributes
	def _initialize_model(self):
		self.initialize_states()
		self._initialize_actions()
		self.initialize_q_matrix()

	# initializes the states in the model
	def _initialize_states(self):
		self.s = self._compute_states()

	# initializes the actions in the model
	def _initialize_actions(self):
		self.a = self._compute_actions()

	# initializes the q value matrix in the model
	def _initialize_q_matrix(self):
		[[0 for action in self.a] for state in self.s]
	
	# computes the states of the game of blackjack
	def _compute_states(self):

		cardsList = ['A'] + [str(cardRank) for cardRank in range(2, 11)] + ["J", "Q", "K"]

		pass

	# computes the actions in the game of blackjack
	def _compute_actions(self):
		actions = ['Hit', 'Stand']
		return actions

	# computes the correct value for the card in the deck for initial hand
	def _get_card_value(self, card):

		if card == 'A':
			return 11 # always count A





if __name__ == "__main__":
	pass