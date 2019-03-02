from deck import Deck

class Blackjack():
	"""
	Represents the game and state of Blackjack for two players.
	"""

	def __init__(self):
		self.deck = Deck(5)
		self.playerHand = list() # player
		self.dealerHand = list() # dealer
		self.confidence = .5 # player hits if probability of bust is below confidence
		self.playerWins = 0 # number of times the player wins
		self.dealerWins = 0 # number of times the dealer wins
		self._reset_game()

	# resets the game for another run of simulation
	def _reset_game(self):
		self.deck.reset_deck(5)
		self.playerHand = list() # player
		self.dealerHand = list() # dealer
		self._initialize_player_1()
		self._initialize_player_2()

	# sets the confidence for the player in the model
	def set_confidence(self, newConfidence):
		self.confidence = newConfidence

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

	# declares the winner of the game at the end of simulation with pretty prints
	def _declare_winner(self, winner):

		if winner == "None":
			announcementString = "The game ended in a tie. NO WINNER!"
		else:
			announcementString = "The winner of the game is: " + winner
		
		# print for game visuals
		print("\n******************************")
		print(announcementString)
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
			return "None"

	# checks to see if the player's hand is a Blackjack
	def _check_blackjack(self, playerHand):
		handValue = self._calculate_sum(playerHand)

		if handValue == 21:
			return True

		return False

	# checks to see if the player's hand is a BUST
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
		handValue += self._determine_ace_value(handValue, aceCount)

		return handValue

	# determines the value of the aces if there are more than 1 in the hand
	def _determine_ace_value(self, handValue, aceCount):

		noAceValue = 0
		lowAceValue = 1
		highAceValue = 11

		if aceCount == 0:
			return noAceValue
		elif aceCount == 1:
			if handValue + highAceValue > 21:
				return lowAceValue
			else:
				return highAceValue
		elif aceCount > 1:

			lowValueCount = aceCount - 1
			highValueCount = 1

			if handValue + highAceValue + lowAceValue*lowValueCount > 21:
				return highAceValue + lowAceValue*lowValueCount
			else:
				return lowAceValue * aceCount


		return aceCount

	# computes the probability that the next hit is a BUST
	def _compute_bust_probability(self, playerHand):
		handValue = self._calculate_sum(playerHand)

		# number of cards that would make the next hit a BUST
		bustCount = 0

		for card in self.deck.cards:
			if card == "A":
				cardValue = 11
			elif card == "J" or card == "Q" or card == "K":
				cardValue = 10
			else:
				cardValue = int(card)

			if handValue + cardValue > 21:
				bustCount += 1

		# probability of bust is number of bust cards over total number of cards left
		bustProbability = bustCount / len(self.deck.cards)

		return bustProbability

	# plays out the game by simulating both players with game visuals
	def simulate_game_with_visuals(self):

		dealerWin = "Dealer"
		playerWin = "Player"

		# print for game visuals
		print("\n********** Begin simulation for one game of Blackjack! **********\n")

		# first simulate player's decisions with the probabilistic model
		self._simulate_player_1_with_visuals()

		# print for game visuals
		print("~~~~~")

		# if player busts, then dealer wins automatically
		if self._check_bust(self.playerHand):
			# print for game visuals
			print("\nPlayer is BUSTED!")
			self._declare_winner(dealerWin)
			return dealerWin
		# if player gets a Blackjack, then player wins right away
		if self._check_blackjack(self.playerHand):
			# print for game visuals
			print("\nPlayer has Blackjack!")
			self._declare_winner(playerWin)
			return	playerWin

		# second simulate the dealer's decisions if player isn't a bust
		self._simulate_player_2_with_visuals()

		# if dealer busts, then player wins automatically
		if self._check_bust(self.dealerHand):
			# print for game visuals
			print("\nDealer is BUSTED!")
			self._declare_winner(playerWin)
			return playerWin
		# if dealer gets a Blackjack, then dealer wins right away
		if self._check_blackjack(self.playerHand):
			# print for game visuals
			print("\nDealer has Blackjack!")
			self._declare_winner(dealerWin)
			return dealerWin

		# compare hands to declare winner
		winningPlayer = self._compare_hand_values(self.playerHand, self.dealerHand)
		self._declare_winner(winningPlayer)
		return winningPlayer

	# simulates the player and their actions with game visuals
	def _simulate_player_1_with_visuals(self):
		# the total value of player's cards
		playerSum = self._calculate_sum(self.playerHand)
		# print for game visuals
		print("Player Sum:", playerSum, "Player Hand:", self.playerHand)

		# current bust probability
		bustProb = self._compute_bust_probability(self.playerHand)

		# continue to hit if bust proability is below 50%
		while bustProb < self.confidence:

			self._deal_player_1()

			# update the new sum
			playerSum = self._calculate_sum(self.playerHand)

			# print for game visuals
			print("Player Sum:", playerSum, "Player Hand:", self.playerHand)	

			# update bust probability
			bustProb = self._compute_bust_probability(self.playerHand)

	# simulates the dealer and their actions with game visuals
	def _simulate_player_2_with_visuals(self):
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

	# plays out the game by simulating both players without game visuals
	def simulate_game_no_visuals(self):

		dealerWin = "Dealer"
		playerWin = "Player"

		# first simulate player's decisions with the Markov Chain model
		self._simulate_player_1_no_visuals()

		# if player busts, then dealer wins automatically
		if self._check_bust(self.playerHand):
			return dealerWin
		# if player gets a Blackjack, then player wins right away
		if self._check_blackjack(self.playerHand):
			return	playerWin

		# second simulate the dealer's decisions if player isn't a bust
		self._simulate_player_2_no_visuals()

		# if dealer busts, then player wins automatically
		if self._check_bust(self.dealerHand):
			return playerWin
		# if dealer gets a Blackjack, then dealer wins right away
		if self._check_blackjack(self.playerHand):
			return dealerWin

		# compare hands to declare winner
		winningPlayer = self._compare_hand_values(self.playerHand, self.dealerHand)
		return winningPlayer

	# simulates the player and their actions without game visuals
	def _simulate_player_1_no_visuals(self):

		# current bust probability
		bustProb = self._compute_bust_probability(self.playerHand)

		# continue to hit if bust proability is below 50%
		while bustProb < self.confidence:

			self._deal_player_1()

			# update bust probability
			bustProb = self._compute_bust_probability(self.playerHand)

	# simulates the dealer and their actions without game visuals
	def _simulate_player_2_no_visuals(self):
		# the model assumes this player is the dealer, with actions to Hit until card value is >= 17
		dealerSum = self._calculate_sum(self.dealerHand)

		while dealerSum < 17:

			self._deal_player_2()

			# update the new sum
			dealerSum = self._calculate_sum(self.dealerHand)	

	# simulates a given numer of games and records statistics of the player's wins
	def simulate_multiple_games(self, numGames):

		print("\n********** Begin simulation of", numGames, "games! **********")

		playerWins = 0
		dealerWins = 0
		tieCount = 0

		# simulate the game for the specified number of times
		for episode in range(numGames):

			winningPlayer = self.simulate_game_no_visuals()

			self._reset_game()

			if winningPlayer == "Player":
				playerWins += 1
			elif winningPlayer == "Dealer":
				dealerWins += 1
			else:
				tieCount += 1

		playerWinrate = playerWins / numGames
		dealerWinrate = dealerWins / numGames
		tieRate = tieCount / numGames

		print("\nPlayer winrate:", str(round(playerWinrate * 100, 1)) + "%")
		print("Dealer winrate:", str(round(dealerWinrate * 100, 1)) + "%")
		print("Tie rate:", str(round(tieRate * 100, 1)) + "%\n")

	# simulates the game of Blackjack with varying confidence levels 
	# for drawing statistics for class Math456 - Mathematical Modeling
	def simulate_varying_confidence(self, numGames): 
		for confidence in range(1,10):
			game.set_confidence(confidence/10)
			print("\n********** ********** ********** ********** **********")
			print("********** Simulating player with confidence:", confidence/10, "**********")
			print("Player hits when probability of busting is below:", confidence/10)
			game.simulate_multiple_games(100)
			print("\n\n")


if __name__ == '__main__':

	game = Blackjack()
	
	# play the game once with visuals
	#game.simulate_game_with_visuals()
	
	# simulate multiple games with no visuals
	#game._simulate_multiple_games(100000)

	# simulate multiple games with varying confidence
	game.simulate_varying_confidence(100)

