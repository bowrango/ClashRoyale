from typing import List

class Card:
    def __init__(self, name: str, rarity: str, elixir: int, card_type: str, level: int):

        self.name = name
        self.rarity = rarity
        self.elixir = elixir
        self.card_type = card_type
        self.level = level

    def __repr__(self):
        return f"<Card(name={self.name}, rarity={self.rarity}, elixir={self.elixir}, type={self.card_type}, level={self.level})>"

class Deck:
    def __init__(self, player_name: str, player_tag: str):

        self.player_name = player_name
        self.player_tag = player_tag
        self.cards: List[Card] = []

    def add_card(self, card: Card):
        if len(self.cards) < 8:
            self.cards.append(card)
        else:
            raise ValueError("A deck can only contain up to 8 cards.")

    def remove_card(self, card_name: str):
        self.cards = [card for card in self.cards if card.name != card_name]

    def get_average_elixir(self) -> float:
        if not self.cards:
            return 0.0
        return sum(card.elixir for card in self.cards) / len(self.cards)

    def get_cards_by_rarity(self, rarity: str) -> List[Card]:
        return [card for card in self.cards if card.rarity == rarity]

    def __repr__(self):
        return f"<Deck(player={self.player_name}, player_tag={self.player_tag}, cards={self.cards})>"
