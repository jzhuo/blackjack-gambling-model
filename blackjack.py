from deck import Deck

class Blackjack():
	"""
	Represents the game and state of Blackjack for two players.
	"""

	def __init__(self):
		self.deck = Deck()
		self.playerHand = list() # player
		self.dealerHand = list() # dealer
		self._initialize_player_1()
		self._initialize_player_2()

	# deals the first two cards to the player at the start of the game
	def _initialize_player_1(self):
		for card in range(2):
			self._deal_player_1()

	# deals the first two cards to the dealer at the start of the game
	def _initialize_player_2(self):
		for card in range(2):
			self._deal_player_2()

	# deals a card to the first player and adds the card to their hand
	def _deal_player_1(self):
		# retrieve the card to deal from deck
		card = self.deck.deal_card()
		# deals the card to the player hand
		self.playerHand.append(card)

	# deals a card to the second player and adds the card to their hand
	def _deal_player_2(self):
		# retrieve the card to deal from deck
		card = self.deck.deal_card()
		# deals the card to the player hand
		self.dealerHand.append(card)

	# plays out the game by simulating both players
	def simulate_game(self):

		# print for game visuals
		print("\n********** Begin game of Blackjack! **********\n")

		# first simulate player's decisions with the Markov Chain model
		self._simulate_player_1()

		# print for game visuals
		print()

		# if player busts, then dealer wins automatically
		if self._check_bust(self.playerHand):
			# print for game visuals
			print("\nPlayer BUSTED!")
			self._declare_winner("Dealer")
			return

		# second simulate the dealer's decisions if player isn't a bust
		self._simulate_player_2()
		# if dealer busts, then player wins automatically
		if self._check_bust(self.dealerHand):
			# print for game visuals
			print("\nDealer BUSTED!")
			self._declare_winner("Player")
			return

		# compare hands to declare winner
		winningPlayer = self._compare_hand_values(self.playerHand, self.dealerHand)
		self._declare_winner(winningPlayer)

	# simulates the first player and their actions
	def _simulate_player_1(self):
		# the model assumes this player is the dealer, with actions to Hit until card value is >= 17
		playerSum = self._calculate_sum(self.playerHand)

		# print for game visuals
		print("Player Sum:", playerSum, "Player Hand:", self.playerHand)

		while playerSum < 17:

			self._deal_player_1()

			# update the new sum
			playerSum = self._calculate_sum(self.playerHand)

			# print for game visuals
			print("Player Sum:", playerSum, "Player Hand:", self.playerHand)	

	# simulates the second player and their actions
	def _simulate_player_2(self):
		# the model assumes this player is the dealer, with actions to Hit until card value is >= 17
		dealerSum = self._calculate_sum(self.dealerHand)

		# print for game visuals
		print("Dealer Sum:", dealerSum, "Dealer Hand:", self.dealerHand)

		while dealerSum < 17:

			self._deal_player_2()

			# update the new sum
			dealerSum = self._calculate_sum(self.dealerHand)	

			# print visuals to keep track of dealer hand
			print("Dealer Sum:", dealerSum, "Dealer Hand:", self.dealerHand)

	# declares the winner of the game at the end of simulation with pretty prints
	def _declare_winner(self, winner):
		
		# print for game visuals
		print("\n******************************")
		print("The winner of the game is:", winner)
		print("******************************\n")

	# compares the hand of the two players and returns the winner
	def _compare_hand_values(self, playerHand, dealerHand):
		playerSum = self._calculate_sum(playerHand)
		dealerSum = self._calculate_sum(dealerHand)

		if playerSum > dealerSum:
			return "Player"
		if playerSum < dealerSum:
			return "Dealer"
		if playerSum == dealerSum:
			return "None. The game ended with a tie!"

	# checks to see if the player's hand is a bust
	def _check_bust(self, playerHand):

		handValue = self._calculate_sum(playerHand)

		if handValue > 21:
			return True

		return False

	# sums the value of a player's hand
	def _calculate_sum(self, hand):
		
		handValue = 0
		aceCount = 0
		
		# values of J, Q, and K is 10
		for card in hand:
			if card == 'A':
				aceCount += 1
			elif card == 'J' or card == 'Q' or card == 'K':
				handValue += 10
			else:
				handValue += int(card)

		# calculating the values for the aces
		if aceCount == 1:
			if handValue <= 10:
				handValue += 11
			else:
				handValue += 1
		elif aceCount > 1:
			handValue += self._determine_ace_value(aceCount)

		return handValue

	# determines the value of the aces if there are more than 1 in the hand
	def _determine_ace_value(self, aceCount):

		# NEED TO IMPLEMENT

		return aceCount


if __name__ == '__main__':
	game = Blackjack()
	# play the game
	game.simulate_game()