import numpy as np
import sys
import random as rand

suspects = {"M": "Col. Mustard", "P": "Prof. Plum", "G": "Mr. Green", "E": "Mrs. Peacock", "S": "Miss Scarlet", "W": "Mrs. White"}
weapons = {"K": "Knife", "C": "Candlestick", "P": "Pistol", "R": "Rope", "L": "Lead Pipe", "W": "Wrench"}
rooms = {"H": "Hall", "L": "Lounge", "D": "Dining Room", "K": "Kitchen", "B": "Ball Room", "C": "Conservatory", "I": "Billiard Room", "Y": "Library", "S": "Study"}

def get_input(is_valid, message):
    valid_input = input(message)
    if valid_input == "STOP":
        sys.exit()
    while not is_valid(valid_input):
        valid_input = input("Invalid. " + message)
        if valid_input == "STOP":
            sys.exit()
    return valid_input

num_players = int(get_input(lambda input : input.isnumeric(), "Enter the number of players: "))
possible_types = ["S", "W", "R"]
players = []
moves = []
unused_moves = []

def items_for_type(given_type):
    if given_type == "S":
        return suspects.keys()
    elif given_type == "W":
        return weapons.keys()
    elif given_type == "R":
        return rooms.keys()
    
def get_item(type, item):
    if type == "S":
        return suspects[item]
    elif type == "W":
        return weapons[item]
    elif type == "R":
        return rooms[item]

def init_possibilities(possibilities_dict):
    for i in possibilities_dict.keys():
        possibilities_dict[i] = "?"
    return possibilities_dict

def valid_guess(guess):
    if guess == "":
        return True
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

real_s = init_possibilities(suspects.copy())
real_w = init_possibilities(weapons.copy())
real_r = init_possibilities(rooms.copy())
accusation = ["?", "?", "?"]
accuse = False

def check_accusation(possible_items, type_index, type_string, type):
    known = False

    num_possible = 0
    for i in possible_items.keys():
        if possible_items[i] == "?":
            num_possible += 1
            the_possible = i
            might_be_guaranteed = True
            for player in players:
                if type == "S":
                    possible = player.s_possible
                elif type == "W":
                    possible = player.w_possible
                elif type == "R":
                    possible = player.r_possible
                if not possible[i] == "N":
                    might_be_guaranteed = False
            if might_be_guaranteed:
                known = True
                break
    if num_possible == 1:
        known = True

    if known:
        accusation[type_index] = the_possible
        print("We now know that the " + type_string + " is " + get_item(type, the_possible))
        if (not accusation[0] == "?") and (not accusation[1] == "?") and (not accusation[2] == "?"):
            accuse = True

def check_real_s():
    check_accusation(real_s, 0, "SUSPECT", "S")

def check_real_w():
    check_accusation(real_w, 1, "WEAPON", "W")

def check_real_r():
    check_accusation(real_r, 2, "ROOM", "R")

class Move:
    player_possibilities = []
    def __init__(self, player, guess, result):
        self.player = player
        self.s = guess[0]
        self.w = guess[1]
        self.r = guess[2]
        self.process(result)
        self.fully_applied = False

    # Y means the person didn't have it, N means the person did, S/W/R then letter of thing means you were told
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
    
    def apply_move(self):
        applied = True
        for player_i in range(len(self.player_results)):
            result = self.player_results[player_i]
            player = players[player_i]
            if result == "":
                continue
            elif result == "Y":
                player.set_item_false("S", self.s)
                player.set_item_false("W", self.w)
                player.set_item_false("R", self.r)
            elif result == "N":
                s_state = player.s_possible[self.s]
                w_state = player.w_possible[self.w]
                r_state = player.r_possible[self.r]
                if not "Y" in [s_state, w_state, r_state]:
                    num_unknown = 0
                    if s_state == "?":
                        num_unknown += 1
                        the_unknown = ["S", self.s]
                    if w_state == "?":
                        num_unknown += 1
                        the_unknown = ["W", self.w]
                    if r_state == "?":
                        num_unknown += 1
                        the_unknown = ["R", self.r]
                    if num_unknown == 1:
                        player.set_item_true(the_unknown[0], the_unknown[1])
            else:
                player.set_item_true(result[0], result[1])
        self.fully_applied = applied
    
    def is_fully_applied(self):
        return self.fully_applied
    
    def __str__(self):
        return("Guessed: " + suspects[self.s] + " with the " + weapons[self.w] + " in the " + rooms[self.r] + ", Result: " + str(self.player_results))

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
            check_real_s()
        elif type == "W":
            self.w_possible[item] = value
            check_real_w()
        elif type == "R":
            self.r_possible[item] = value
            check_real_r()
        else:
            print("I was somehow given something to change that was not S or W or R. This should be impossible.")

    def set_item_false(self, type, item):
        self.set_item(type, item, "N")

    def set_item_true(self, type, item):
        print("We have discovered that " + suspects[self.get_name()] + " has the card " + get_item(type, item))
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
        players.append(Player(get_input(lambda input : input in suspects.keys(), "Enter the player's name: "), card_num))
    else:
        players.append(Player(get_input(lambda input : input in suspects.keys(), "Enter the player's name: "), cards_from_bool(get_input(lambda input : input in ["Y", "N"], "Does this player have " + str(card_num) + " cards? Y/N: "))))

def valid_my_cards(input):
    if not len(input) == 2 * players[0].get_num_cards():
        return False
    for i in range(players[0].get_num_cards()):
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

def is_rooms(input):
    for i in range(len(input)):
        if not input[i] in rooms.keys():
            return False
    return True

def rate_room(room):
    for i in range(num_players):
        if players[i].r_possible[room] == "Y":
            return i
    return -1

def rate_weapon(weapon):
    for i in range(num_players):
        if players[i].w_possible[weapon] == "Y":
            return i
    return -1

def rate_suspect(suspect):
    for i in range(num_players):
        if players[i].s_possible[suspect] == "Y":
            return i
    return -1

def play(starting_index):
    for i in range(starting_index, num_players):
        suggest = True
        if i == 0:
            # Handling if you win.
            if accuse:
                print("Make an accusation. The crime was committed by " + accusation[0] + " with the " + accusation[1] + " in the " + accusation[2] + ".")
                sys.exit()
            
            possible_rooms = get_input(lambda input : is_rooms(input), "Enter rooms I can go to: ")
            if len(possible_rooms) == 0:
                print("It appears that there is no possible way to suggest. Move to the room that you can get closest to. If there's a tie, choose the position closer to entering a corner room.")
                suggest = False
            else:
                # Rooms not known by the next player(s). If it were known by index 1, we wouldn't learn anything.
                room_ratings = dict()
                for j in range(len(possible_rooms)):
                    room_ratings[possible_rooms[j]] = rate_room(possible_rooms[j])
                
                # Same for weapons
                weapon_ratings = dict()
                for weapon in weapons.keys():
                    weapon_ratings[weapon] = rate_weapon(weapon)

                # And suspects
                suspect_ratings = dict()
                for suspect in suspects.keys():
                    suspect_ratings[suspect] = rate_suspect(suspect)

                ratings = [suspect_ratings, weapon_ratings, room_ratings]

                # Now, for all three, we will make a dictionary of lists, from -1 to the number of players
                organized_ratings = [dict(), dict(), dict()]
                for num_i in range(-1, num_players):
                    for type_i in range(3):
                        organized_ratings[type_i][str(num_i)] = []
                        for key in ratings[type_i].keys():
                            if ratings[type_i][key] == num_i:
                                organized_ratings[type_i][str(num_i)].append(key)
                print(organized_ratings)

                current_guess = "WRL" # FIX, THIS IS JUST SO IT DOESN'T BREAK

        else:
            current_guess = get_input(lambda input : valid_guess(input), "Enter the current guess (" + suspects[players[i].get_name()] + "): ")
            if current_guess == "":
                suggest = False
        if suggest:
            new_move = Move(players[i].get_name(), current_guess, get_input(lambda input : valid_result(input), "Enter the results of the guess: "))
            moves.append(new_move)
            new_move.apply_move()
            if not new_move.is_fully_applied():
                unused_moves.append(new_move)
            for j in range(len(unused_moves)): print("\n" + str(unused_moves[i]))
            for move in unused_moves:
                move.apply_move()
                if move.is_fully_applied():
                    unused_moves.remove(move)
            for j in range(len(players)): print(players[i])

start_i = int(get_input(lambda input : input.isnumeric(), "Index of the starting player (I'm 0): "))

play(start_i)
while True:
    play(0)