import numpy as np
import sys
import random as rand
import time

# Abbreviations as dictionaries, for writing full description
suspects = {"M": "Col. Mustard", "P": "Prof. Plum", "G": "Mr. Green", "E": "Mrs. Peacock", "S": "Miss Scarlett", "W": "Mrs. White"}
weapons = {"K": "Knife", "C": "Candlestick", "P": "Pistol", "R": "Rope", "L": "Lead Pipe", "W": "Wrench"}
rooms = {"H": "Hall", "L": "Lounge", "D": "Dining Room", "K": "Kitchen", "B": "Ballroom", "C": "Conservatory", "I": "Billiard Room", "Y": "Library", "S": "Study"}

def get_input(is_valid, message: str) -> str:
    """Gets input until it is valid, but ends the program if the user enters "STOP"

    Parameters
    ----------
    is_valid
        Lambda expression to check whether the input is valid
    message: str
        Message to be given to the user when getting input

    Returns
    -------
    str
        The validified input
    """

    valid_input = input(message)
    if valid_input == "STOP":
        sys.exit()
    while not is_valid(valid_input):
        valid_input = input("Invalid. " + message)
        if valid_input == "STOP":
            sys.exit()
    return valid_input

def valid_num_players(num: str):
    """Checks if an input number of players is valid
    
    Parameters
    ----------
    num: int
        The input number of players (should be a string from input)

    Returns
    -------
    boolean
        Whether it is a valid number of players
    """

    if not num.isnumeric():
        return False
    if int(num) > 6:
        return False
    if int(num) < 2:
        return False
    return True

num_players = int(get_input(lambda input : valid_num_players(input), "Enter the number of players: "))

# Suspects, weapons, and rooms as types of information
possible_types = ["S", "W", "R"]

# Keeps track of which cards you know (so you know which card to show if necessary)
my_known_cards = [[]] * num_players

players = []
moves = []
unused_moves = []

def items_for_type(given_type: str):
    """Gives abbreviated names for each item of a type

    Parameters
    ----------
    given_type: str ("S" - suspects, "W" - weapons, "R" - rooms)
        Which type of items you would like to get

    Returns
    -------
    list
        A list of abbreviations for each item of the given type
    """

    if given_type == "S":
        return suspects.keys()
    elif given_type == "W":
        return weapons.keys()
    elif given_type == "R":
        return rooms.keys()
    
def get_item(item_type, item):
    """Returns the name of the chosen item

    Parameters
    ----------
    item_type: str ("S", "W", "R")
        The type of item of choice
    item: str
        The first letter of an item of choice of that type
    
    Returns
    -------
    str
        The name of the chosen item
    """

    if item_type == "S":
        return suspects[item]
    elif item_type == "W":
        return weapons[item]
    elif item_type == "R":
        return rooms[item]

def valid_guess(guess: str):
    """Checks whether a guess is valid

    Parameters
    ----------
    guess: str
        The guess that was input

    Returns
    -------
    bool
        Whether the guess is valid (empty or a three-character string of suspects, weapons, rooms)
    """

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

# FIX -- make actually check
def valid_result(result: str):
    """Checks whether the result (response to a guess) is valid

    Parameters
    ----------
    result: str
        The result that was input
    
    Returns
    -------
    bool
        Always True (should be fixed to actually check)
    """

    return True

def init_possibilities(possibilities_dict):
    """Initializes all possibilities to unknown in the input dictionary

    Parameters
    ----------
    possibilities_dict
        The dictionary whose items should be reset to unknown
    
    Returns
    -------
    dict
        The same dictionary that was passed to this method
    """

    for i in possibilities_dict.keys():
        possibilities_dict[i] = "?"
    return possibilities_dict

real_s = init_possibilities(suspects.copy())
real_w = init_possibilities(weapons.copy())
real_r = init_possibilities(rooms.copy())
accusation = ["?", "?", "?"]
accuse = False

# FIX -- it seems like possible_items is useless
def check_accusation(possible_items, type_index, type_string, item_type):
    """This updates a final list of items (suspects, weapons, or rooms). 

    Parameters
    ----------
    possible_items
        A list of final items (real_s, real_w, or real_r)
    type_index
        The index of the type (s = 0, w = 1, r = 2)
    type_string
        A string for the type (SUSPECT, WEAPON, ROOM)
    item_type
        What type of item to check (S, W, R)

    Returns
    -------
    Nothing
    """

    known = False

    num_possible = 0

    print("\nPossible items (" + item_type + ")\n")
    print(possible_items)

    for i in possible_items.keys():
        if possible_items[i] == "?":
            num_possible += 1
            the_possible = i
            might_be_guaranteed = True
            for player in players:
                if item_type == "S":
                    possible = player.s_possible
                elif item_type == "W":
                    possible = player.w_possible
                elif item_type == "R":
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
        print("We now know that the " + type_string + " is " + get_item(item_type, the_possible))
        time.sleep(1)
        if (not accusation[0] == "?") and (not accusation[1] == "?") and (not accusation[2] == "?"):
            global accuse
            accuse = True

def check_real_s():
    """Checks the final list for suspects."""
    
    if accusation[0] == "?":
        check_accusation(real_s, 0, "SUSPECT", "S")

def check_real_w():
    """Checks the final list for weapons."""

    if accusation[1] == "?":
        check_accusation(real_w, 1, "WEAPON", "W")

def check_real_r():
    """Checks the final list for rooms."""

    if accusation[2] == "?":
        check_accusation(real_r, 2, "ROOM", "R")

def make_accusation():
    """Accuses and ends the program. Call this when the accusation is final."""

    print("Make an accusation. The crime was committed by " + suspects[accusation[0]] + " with the " + weapons[accusation[1]] + " in the " + rooms[accusation[2]] + ".")
    sys.exit()

class Move:
    """Represents what happened in a particular move

    Attributes
    ----------
    player: int
        index of the player who made this move (processed from initially being a str)
    s: str
        suspect that was suggested
    w: str
        weapon that was suggested
    r: str
        room that was suggested
    player_results: list
        list of how each player responded (index i corresponds to players list)
    fully_applied: bool
        whether this move has been fully used
    
    Methods
    -------
    apply_move()
        attempts to fully apply the move, based on current information
    is_fully_applied()
        returns whether the move has been fully applied
    """
    
    # player_possibilities = []
    def __init__(self, player: str, guess: str, result: str):
        """
        Parameters
        ----------
        player: str
            player who made the move (as a single letter)
        guess: str
            the suggestion that was made (three characters, should have already checked validity)
        result: str
            how people responded to the suggestion (Y, N, specific result)
        """

        self.player = player
        self.s = guess[0]
        self.w = guess[1]
        self.r = guess[2]
        self.__process(result)
        self.fully_applied = False

    # Y means the person didn't have it, N means the person did, S/W/R then letter of thing means you were told
    def __process(self, result):
        """Helper method to set the player and player_results correctly in __init__ based on the result

        Parameters
        ----------
        result: str
            the result of the suggestion
        """
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
    
    def apply_move(self):
        """Attempts to fully apply this move, based on currently known information. Updates players
        according to the information gained. 
        """
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
                        applied = False
            else:
                player.set_item_true(result[0], result[1])
                if player_i == 0:
                    my_known_cards[self.player].append(result[0] + result[1])
        self.fully_applied = applied
    
    def is_fully_applied(self):
        return self.fully_applied
    
    def __str__(self):
        return("Guessed: " + suspects[self.s] + " with the " + weapons[self.w] + " in the " + rooms[self.r] + ", Result: " + str(self.player_results))

class Player:
    """Represents all information known about a particular player

    Attributes
    ----------
    name: str
        this player's name (as a single character)
    my_index: int
        the index of this player (used to access in the players list)
    num_cards: int
        how many cards this player has
    cards_found: int
        the number of this player's cards that we know
    fully_known: bool
        whether we know all of the cards for this player
    s_possible: dict
        suspect possibilities (values are Y, N, or ?)
    w_possible: dict
        weapon possibilities (values are Y, N, or ?)
    r_possible: dict
        room possibilities (values are Y, N, or ?)

    Methods
    -------
    get_name()
        returns the name of this player
    get_num_cards()
        returns the number of cards this player has
    set_item_false(item_type, item)
        sets the given item to false (this player doesn't have it)
    set_item_true(item_type, item)
        sets the given item to true (this player has it)
    unknown_are_false()
        sets all unknown cards to being false
    all_are_found()
        returns whether all of this player's cards are discovered
    """
    
    def __init__(self, name: str, index: int, num_cards: int):
        self.name = name
        self.my_index = index
        self.num_cards = num_cards
        self.cards_found = 0
        self.fully_known = False
        self.s_possible = init_possibilities(suspects.copy())
        self.w_possible = init_possibilities(weapons.copy())
        self.r_possible = init_possibilities(rooms.copy())

    def get_item_state(self, item_type, item):
        """Gets the state of an item for a particular player
        
        Parameters
        ----------
        item_type: str
            the type of item to get (S, W, R)
        item: str
            the particular item of that type
        
        Returns
        -------
        str
            the state of the requested item
        """

        if item_type == "S":
            return self.s_possible[item]
        elif item_type == "W":
            return self.w_possible[item]
        elif item_type == "R":
            return self.r_possible[item]
    
    def get_name(self):
        """
        Returns
        -------
        the name of this player
        """

        return self.name
    
    def get_num_cards(self):
        """
        Returns
        -------
        the number of cards this player has
        """
        
        return self.num_cards
    
    # Returns whether setting it would be redundant
    def __set_item(self, item_type, item, value):
        """Sets an item in one of this player's dicts of possibilities

        Parameters
        ----------
        item_type: str
            the type of item (S = suspect, W = weapon, R = room)
        item: str
            the specific item (such as Prof. Plum as P for S or Knife as K for W)
        value: str
            the value to set the item to
        
        Returns
        -------
        bool
            whether setting this value would be redundant
        """

        if item_type == "S":
            if not self.s_possible[item] == "?":
                return True
            self.s_possible[item] = value
            check_real_s()
        elif item_type == "W":
            if not self.w_possible[item] == "?":
                return True
            self.w_possible[item] = value
            check_real_w()
        elif item_type == "R":
            if not self.r_possible[item] == "?":
                return True
            self.r_possible[item] = value
            check_real_r()
        else:
            print("I was somehow given something to change that was not S or W or R. This should be impossible.")
        return False

    def set_item_false(self, item_type, item):
        """Sets the given item to false (the player doesn't have it)

        Parameters
        ----------
        item_type: str
            the type of item (S = suspect, W = weapon, R = room)
        item: str
            the specific item (such as Prof. Plum as P for S or Knife as K for W)

        Returns
        -------
        bool
            whether setting this value would be redundant
        """

        redundant = self.__set_item(item_type, item, "N")
        if not redundant:
            print("We have discovered that " + suspects[self.get_name()] + " does NOT have the card " + get_item(item_type, item))
            time.sleep(1)
            # num_players_without = 0
            # index_may_have = -1
            # for player_i in range(num_players):
            #     if players[player_i].get_item_state(item_type, item) == "N":
            #         num_players_without += 1
            #     else:
            #         index_may_have = player_i
            # if num_players_without == num_players - 1:
            #     players[index_may_have].set

    def set_item_true(self, item_type, item):
        """Sets the given item to true (the player DOES have it)

        Parameters
        ----------
        item_type: str
            the type of item (S = suspect, W = weapon, R = room)
        item: str
            the specific item (such as Prof. Plum as P for S or Knife as K for W)

        Returns
        -------
        bool
            whether setting this value would be redundant
        """

        redundant = self.__set_item(item_type, item, "Y")
        if not redundant:
            players_without_item = list(range(num_players))
            players_without_item.pop(self.my_index)
            for i in players_without_item:
                players[i].set_item_false(item_type, item)
            print("We have discovered that " + suspects[self.get_name()] + " has the card " + get_item(item_type, item))
            time.sleep(1)
            self.cards_found += 1
            if self.cards_found == self.num_cards:
                self.unknown_are_false()
    
    def unknown_are_false(self):
        """Sets all unknown cards to false. Call this when you have discovered all possible cards."""

        for possibilities in [self.s_possible, self.w_possible, self.r_possible]:
            for i in possibilities.keys():
                if possibilities[i] == "?":
                    possibilities[i] = "N"
        self.fully_known = True
    
    def all_are_found(self):
        """
        Returns
        -------
        Whether all cards have been found for this player
        """

        return self.fully_known

    def __str__(self):
        return suspects[self.name] + "\nSuspects: " + str(self.s_possible) + "\nWeapons: " + str(self.w_possible) + "\nRooms: " + str(self.r_possible) + "\nDiscovered: " + str(self.cards_found) + " out of " + str(self.num_cards)

# 6 suspects, 6 weapons, 9 rooms, and 3 of those are the answer (not distributed)
card_num = int(18 / num_players)
same_card_num = 18 % num_players == 0
print("I now need to know who all the players are. Please start with me and go to the left.")

def cards_from_bool(input):
    """Returns a number of cards based on an input answer
    
    Parameters
    ----------
    input: str
        Y or N (whether the number of cards is the default)
    
    Returns
    -------
    int
        the number of cards
    """
    
    if input == "Y":
        return card_num
    else:
        return card_num + 1

# Initializes the players list (name and number of cards)
for i in range(num_players):
    if same_card_num:
        players.append(Player(get_input(lambda input : input in suspects.keys(), "Enter the player's name: "), i, card_num))
    else:
        players.append(Player(get_input(lambda input : input in suspects.keys(), "Enter the player's name: "), i, cards_from_bool(get_input(lambda input : input in ["Y", "N"], "Does this player have " + str(card_num) + " cards? Y/N: "))))

def valid_my_cards(input):
    """Whether the input is a valid possibility for the computer's cards

    Parameters
    ----------
    input: str
        the input given for the cards
    
    Returns
    -------
    bool
        whether the cards are valid
    """

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

# Sets the cards for the computer
my_cards = get_input(lambda input : valid_my_cards(input), "Please enter my cards: ")
for i in range(players[0].get_num_cards()):
    players[0].set_item_true(my_cards[2 * i], my_cards[2 * i + 1])

print(players[0])

def is_rooms(input):
    """Checks whether a string is rooms

    Parameters
    ----------
    input: str
        the input that was given

    Returns
    -------
    bool
        whether the input is all rooms"""
    for i in range(len(input)):
        if not input[i] in rooms.keys():
            return False
    return True

def rate(item):
    """Rates how much so we would want to ask about this item

    Parameters
    ----------
    item: lambda
        a lambda that takes an index and returns the state of the chosen item for that player

    Returns
    -------
    int
        rating for suggesting this item (-1 = we don't know -> good to ask, 0 = nobody has it, i = this index of player has it)
    """

    all_not = True
    for i in range(num_players):
        if not item(i) == "N":
            all_not = False
        if item(i) == "Y":
            return i
    if all_not:
        # If we know that nobody has it, so therefore it is the item, we rank it the same as if we had it
        return 0
    else:
        return -1

def rate_room(room):
    """Rates how much so we would want to ask about this room

    Parameters
    ----------
    item: lambda
        a lambda that takes an index and returns the state of the chosen room for that player

    Returns
    -------
    int
        rating for suggesting this room (-1 = we don't know -> good to ask, 0 = nobody has it, i = this index of player has it)
    """

    return rate(lambda index : players[index].r_possible[room])

def rate_weapon(weapon):
    """Rates how much so we would want to ask about this weapon

    Parameters
    ----------
    item: lambda
        a lambda that takes an index and returns the state of the chosen weapon for that player

    Returns
    -------
    int
        rating for suggesting this weapon (-1 = we don't know -> good to ask, 0 = nobody has it, i = this index of player has it)
    """

    return rate(lambda index : players[index].w_possible[weapon])

def rate_suspect(suspect):
    """Rates how much so we would want to ask about this suspect

    Parameters
    ----------
    item: lambda
        a lambda that takes an index and returns the state of the chosen suspect for that player

    Returns
    -------
    int
        rating for suggesting this suspect (-1 = we don't know -> good to ask, 0 = nobody has it, i = this index of player has it)
    """

    return rate(lambda index : players[index].s_possible[suspect])

def play(starting_index: int):
    """Method to play a round (starting with player index and going to the player after the computer)

    Parameters
    ----------
    starting_index: int
        the index of the player to start with (typically 0)
    """

    for i in range(starting_index, num_players):
        suggest = True
        if i == 0:
            # Handling if you win.
            if accuse:
                make_accusation()
            possible_rooms = get_input(lambda input : is_rooms(input), "Enter rooms I can go to: ")
            if len(possible_rooms) == 0:
                print("It appears that there is no possible way to suggest. Move to the room that you can get closest to. If there's a tie, choose the position closer to entering a corner room.")
                suggest = False
            else:
                suggestion = [rand.choice(list(suspects.keys())), rand.choice(list(weapons.keys())), rand.choice(possible_rooms)]
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
                # This keeps track of which ones have which rating, making it easier to access.
                organized_ratings = [dict(), dict(), dict()]
                for num_i in range(-1, num_players):
                    for type_i in range(3):
                        organized_ratings[type_i][str(num_i)] = []
                        for key in ratings[type_i].keys():
                            if ratings[type_i][key] == num_i:
                                organized_ratings[type_i][str(num_i)].append(key)
                
                s_known = not accusation[0] == "?"
                w_known = not accusation[1] == "?"
                r_known = not accusation[2] == "?"
                num_known = 0
                if s_known: num_known += 1
                if w_known: num_known += 1
                if r_known: num_known += 1

                # first_all_found = -1
                # for j in range(1, num_players):
                #     if players[j].all_are_found():
                #         first_all_found = j
                #         break

                if num_known == 2:
                    i_not_known = -1
                    if not s_known:
                        i_not_known = 0
                    elif not w_known:
                        i_not_known = 1
                    elif not r_known:
                        i_not_known = 2
                    else:
                        print("Somehow, when two are known, none are NOT known.")
                    options = organized_ratings[i_not_known]["-1"]
                    if not len(options) == 0:
                        chosen = rand.choice(options)
                        for j in range(3):
                            if j == i_not_known:
                                suggestion[j] = chosen
                            else:
                                best_indices = [0, -1]
                                for k in range(1, num_players):
                                    best_indices.append(num_players - k)
                                for k in best_indices:
                                    if not len(organized_ratings[j][str(k)]) == 0:
                                        suggestion[j] = rand.choice(organized_ratings[j][str(k)])
                                        break
                    # FIX -- I think we should add an else

                elif num_known == 1:
                    i_known = -1
                    if not s_known:
                        i_known = 0
                    elif not w_known:
                        i_known = 1
                    elif not r_known:
                        i_known = 2
                    else:
                        print("Somehow, when two are known, none are not known.")
                    for j in range(3):
                        if j == i_known:
                            suggestion[j] = rand.choice([rand.choice(organized_ratings[i_known]["0"]), rand.choice(organized_ratings[i_known]["0"]), rand.choice(organized_ratings[i_known]["0"]), rand.choice(organized_ratings[i_known]["0"]), rand.choice(organized_ratings[i_known]["-1"])])
                        else:
                            best_indices = [-1, 0]
                            for k in range(1, num_players):
                                best_indices.append(num_players - k)
                            for k in best_indices:
                                if not len(organized_ratings[j][str(k)]) == 0:
                                    suggestion[j] = rand.choice(organized_ratings[j][str(k)])
                                    break
                elif num_known == 0:
                    for j in range(3):
                        best_indices = [-1, 0]
                        for k in range(1, num_players):
                            best_indices.append(num_players - k)
                        for k in best_indices:
                            if not len(organized_ratings[j][str(k)]) == 0:
                                suggestion[j] = rand.choice(organized_ratings[j][str(k)])
                                break
                else:
                    print("I should have made an accusation.")
                    make_accusation()

                current_guess = suggestion[0] + suggestion[1] + suggestion[2]
                print("Suggest: " + suspects[suggestion[0]] + " with the " + weapons[suggestion[1]] + " in the " + rooms[suggestion[2]] + ".")

        else:
            current_guess = get_input(lambda input : valid_guess(input), "\nThree characters (suspect, weapon, room)\nEnter the current guess (" + suspects[players[i].get_name()] + "): ")
            if current_guess == "":
                print("I conclude that this player only moved.")
                suggest = False
            else:
                if "S" + current_guess[0] in my_known_cards[i]:
                    print("If asked, show this card: " + suspects[current_guess[0]])
                elif "W" + current_guess[1] in my_known_cards[i]:
                    print("If asked, show this card: " + weapons[current_guess[1]])
                elif "R" + current_guess[2] in my_known_cards[i]:
                    print("If asked, show this card: " + rooms[current_guess[2]])
                else:
                    print("If asked, choose a random card to show.")
        if suggest:
            # Get results of the move and apply move
            result = get_input(lambda input : valid_result(input), "\nY = didn't have, N = had unknown, abbreviation = what they had\nEnter the results of the guess: ")
            new_move = Move(players[i].get_name(), current_guess, result)
            moves.append(new_move)
            new_move.apply_move()
            if not new_move.is_fully_applied():
                unused_moves.append(new_move)
            
            print("\nUnused Moves")
            print(len(unused_moves))
            for j in range(len(unused_moves)): print(str(unused_moves[j]))
            
            # Attempt to apply unused moves.
            for move in unused_moves:
                move.apply_move()
                if move.is_fully_applied():
                    unused_moves.remove(move)
        
            print("\nPlayers")
            for j in range(len(players)): print(players[j])
            print("\n")

            if i == 0:
                can_accuse = True
                for j in range(len(result)):
                    if not result[j] == "Y":
                        can_accuse = False
                        break
                if can_accuse and accuse:
                    make_accusation()

start_i = int(get_input(lambda input : input.isnumeric(), "Index of the starting player (I'm 0): "))

play(start_i)
while True:
    play(0)