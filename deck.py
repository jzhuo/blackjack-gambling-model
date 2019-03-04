import math
import random


class Deck():
	"""
	Deck class is used to store the cards of a deck
	"""

	def __init__(self, decks):
		self.cards = None
		self.numDecks = decks
		self.reset_deck()

	# creates a new deck and resets the deck
	def reset_deck(self):
		
		'''
		Numerical values mean themselves but
		1 is A,
		11 is J,
		12 is Q,
		13 is K
		'''
		cardRanks = ["A"] + [str(cardRank) for cardRank in range(2, 11)] + ["J", "Q", "K"]

		newCards = []

		# uses the specified number of decks, 5 decks are used in blackjack
		for deckCount in range(self.numDecks):
			for cardRank in cardRanks:
				for cardSuit in range(4):
					newCards.append(cardRank)

		# shuffling the deck three times for good measures
		for shuffleCount in range(3):
			random.shuffle(newCards)

		self.cards = newCards

	# returns the stored deck
	def get_cards(self):
		return self.cards

	# deals a randomly selected card from the deck
	def deal_card(self):

		if len(self.cards) == 0:
			return None

		# random number inclusive for both lower and upper bounds
		selectedCardIndex = random.randint(0, len(self.cards)-1)

		selectedCard = self.cards[selectedCardIndex]

		# remove the card at the index
		self.cards.pop(selectedCardIndex)

		return selectedCard


if __name__ == '__main__':
	deck = Deck()
	print(deck.deal_card())