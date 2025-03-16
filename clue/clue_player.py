import numpy as np
import sys

suspects = {"M": "Col. Mustard", "P": "Prof. Plum", "G": "Mr. Green", "E": "Mrs. Peacock", "S": "Miss Scarlet", "W": "Mrs. White"}
weapons = {"K": "Knife", "C": "Candlestick", "P": "Pistol", "R": "Rope", "L": "Lead Pipe", "W": "Wrench"}
rooms = {"H": "Hall", "L": "Lounge", "D": "Dining Room", "K": "Kitchen", "B": "Ball Room", "C": "Conservatory", "I": "Billiard Room", "Y": "Library", "S": "Study"}

def get_input(is_valid, message):
    valid_input = input(message)
    if valid_input == "STOP":
        sys.exit()
    while not is_valid(valid_input):
        valid_input = input(message)
        if valid_input == "STOP":
            sys.exit()
    return valid_input

num_players = int(get_input(lambda input : input.isnumeric(), "Enter the number of players: "))
possible_types = ["S", "W", "R"]
players = []
moves = []

def init_possibilities(possibilities_dict):
    for i in possibilities_dict.keys():
        possibilities_dict[i] = "?"
    return possibilities_dict

def valid_guess(guess):
    if not len(guess) == 3:
        return False
    if not guess[0] in suspects.keys():
        return False
    if not guess[1] in weapons.keys():
        return False
    if not guess[2] in rooms.keys():
        return False
    return True

def valid_result(result):
    return True # Fix - make this actually check

class Move:
    player_possibilities = []
    def __init__(self, player, guess, result):
        self.player = player
        self.s = guess[0]
        self.w = guess[1]
        self.r = guess[2]
        self.process(result)

    # Y means the person didn't have it, N means the person didn't, S/W/R then letter of thing means you were told
    def process(self, result):
        for i in range(len(players)):
            if players[i].get_name() == self.player:
                self.player = i
                break
        results = []
        for i in range(len(result)):
            if result[i] in ["Y", "N"]:
                results.append(result[i])
            else:
                results.append(result[i] + result[i + 1])
                break
        self.player_results = ["" for i in range(num_players)]
        for i in range(len(results)):
            self.player_results[(i + self.player + 1) % num_players] = results[i]
        return self
    
    def __str__(self):
        return("Guessed: " + self.s + self.w + self.r + ", Result: " + str(self.player_results))

class Player:
    def __init__(self, name, num_cards):
        self.name = name
        self.num_cards = num_cards
        self.cards_found = 0
        self.s_possible = init_possibilities(suspects.copy())
        self.w_possible = init_possibilities(weapons.copy())
        self.r_possible = init_possibilities(rooms.copy())
    
    def get_name(self):
        return self.name
    
    def get_num_cards(self):
        return self.num_cards
    
    def set_item(self, type, item, value):
        if type == "S":
            self.s_possible[item] = value
        elif type == "W":
            self.w_possible[item] = value
        elif type == "R":
            self.r_possible[item] = value
        else:
            print("I was somehow given something to change that was not S or W or R. This should be impossible.")

    def set_item_false(self, type, item):
        self.set_item(type, item, "N")

    def set_item_true(self, type, item):
        self.set_item(type, item, "Y")
        self.cards_found += 1
        if self.cards_found == self.num_cards:
            self.unknown_are_false()
    
    def unknown_are_false(self):
        for possibilities in [self.s_possible, self.w_possible, self.r_possible]:
            for i in possibilities.keys():
                if possibilities[i] == "?":
                    possibilities[i] = "N"

    def __str__(self):
        return suspects[self.name] + "\nSuspects: " + str(self.s_possible) + "\nWeapons: " + str(self.w_possible) + "\nRooms: " + str(self.r_possible) + "\nDiscovered: " + str(self.cards_found) + " out of " + str(self.num_cards)

card_num = int(18 / num_players)
same_card_num = 18 % num_players == 0
print("I now need to know who all the players are. Please start with me and go to the left.")

def cards_from_bool(input):
    if input == "Y":
        return card_num
    else:
        return card_num + 1

for i in range(num_players):
    if same_card_num:
        players.append(Player(get_input(lambda input : input in suspects.keys(), str(i) + " Enter the player's name: "), card_num))
    else:
        players.append(Player(get_input(lambda input : input in suspects.keys(), str(i) + " Enter the player's name: "), cards_from_bool(get_input(lambda input : input in ["Y", "N"], "Does this player have " + str(card_num) + " cards? Y/N: "))))

def items_for_type(given_type):
    if given_type == "S":
        return suspects.keys()
    elif given_type == "W":
        return weapons.keys()
    elif given_type == "R":
        return rooms.keys()

def valid_my_cards(input):
    if not len(input) == 2 * players[0].get_num_cards():
        return False
    for i in range(players[0].get_num_cards()): # I can have different numbers of cards
        card_type = input[2 * i + 0]
        card_item = input[2 * i + 1]
        if not card_type in possible_types:
            return False
        if not card_item in items_for_type(card_type):
            return False
    return True

my_cards = get_input(lambda input : valid_my_cards(input), "Please enter my cards: ")
for i in range(players[0].get_num_cards()):
    players[0].set_item_true(my_cards[2 * i], my_cards[2 * i + 1])

print(players[0])

while True:
    for i in range(num_players):
        current_guess = get_input(lambda input : valid_guess(input), "Enter the current guess: ")
        moves.append(Move(players[i].get_name(), current_guess, get_input(lambda input : valid_result(input), "Enter the results of the guess: ")))
        print(moves[i])