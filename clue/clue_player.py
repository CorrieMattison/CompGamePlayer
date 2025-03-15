import numpy as np

suspects = {"M": "Col. Mustard", "P": "Prof. Plum", "G": "Mr. Green", "E": "Mrs. Peacock", "S": "Miss Scarlet", "W": "Mrs. White"}
weapons = {"K": "Knife", "C": "Candlestick", "P": "Pistol", "R": "Rope", "L": "Lead Pipe", "W": "Wrench"}
rooms = {"H": "Hall", "L": "Lounge", "D": "Dining Room", "K": "Kitchen", "B": "Ball Room", "C": "Conservatory", "I": "Billiard Room", "Y": "Library", "S": "Study"}

def get_input(is_valid, message):
    valid_input = input(message)
    while not is_valid(valid_input):
        valid_input = input(message)
    return valid_input

class Player:
    def __init__(self, name, num_cards):
        self.num_cards = num_cards
        self.name = name

# str_nums = []
# for i in range(10):
#     str_nums.append(str(i))
# is_number = lambda input : str(input).toCharArray()

num_players = int(get_input(lambda input : input.isnumeric(), "Enter the number of players: "))
card_num = int(18 / num_players)
same_card_num = 18 % num_players == 0
print("I now need to know who all the players are. Please start with me and go to the left.")
players = []

def cards_from_bool(input):
    if input == "Y":
        return card_num
    else:
        return card_num + 1

for i in range(num_players):
    if same_card_num:
        players.append(Player(get_input(lambda input : input in suspects.keys(), "Enter the player's name: "), card_num))
    else:
        players.append(Player(get_input(lambda input : input in suspects.keys(), "Enter the player's name: "), cards_from_bool(get_input(lambda input : input in ["Y", "N"], "Does this player have " + str(card_num) + " cards? Y/N: "))))