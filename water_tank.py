# import statements
import random

def get_user_input(question):
    
    """Prompt the user with the given question and process the input. Return the post-processed user input.
        - Remove leading and trailing whitespaces.
        - If the length of the user input after removing leading and trailing whitespaces is 0, reprompt.
        - If the input is a number, cast and return an integer type.
        - If the input is a power card, return the power card as an uppercase string.
        - If the input is any other string, return the string as a lowercase string.
    """
    # Initialize power cards
    power_cards = setup_power_cards()

    # Create loop to continuously prompt the user until valid input is received
    while True:
        # Prompt the user and remove leading/trailing whitespaces
        user = input(question).strip()
        
        # Check if the input is empty
        if not user:
            print('Input can\'t be empty. Please try again.')
            continue
        
        # Check if the input is a number and return it as an integer
        if user.isdigit():
            return int(user)
        # Check if the input is a power card and return it as an uppercase string
        elif user.upper() in power_cards:
            return user.upper()
        # For any other string input, return it as a lowercase string
        else:
            return user.lower()
                        

def setup_water_cards():

    """Create a shuffled list of water cards with the following values and quantities.
    values: [1, 5, 10], quantities: [30, 15, 8]
    Hint: Use the shuffle function from the random module. 
    Return the water cards as a list of integers"""

    # Define the values and quantities of the water cards
    values = [1,5,10]
    quantities = [30, 15, 8]
    
    # Create the list of water cards
    water_cards = []
    for value, quantity in zip(values, quantities):
        water_cards.extend([value] * quantity)
    
    # Shuffle the water cards
    random.shuffle(water_cards)

    # Return the shuffled list of water cards
    return water_cards


def setup_power_cards():
    """Create a shuffled list of power cards with the following values and quantities:
    values: [SOH, DOT, DMT]
    quantities: [10, 2, 3]
    Decription: [Steal half opponent's tank value. If the opponent's tank value is an odd integer, it will truncate the decimal value (Example: ½ of 5 is 2) Hint: You may use the cast to int, Drain opponent's tank, Double my tank's value.]
    
    Hint: Use the shuffle function from the random module. 
    Return the power cards as a list of strings.
    """

    # Define the values and quantities of the power cards
    values = ['SOH', 'DOT', 'DMT']
    quantities = [10, 2, 3]
    
    # Create the list of power cards
    power_cards = []
    for value, quantity in zip(values, quantities):
        power_cards.extend([value] * quantity)
    
    # Shuffle the power cards
    random.shuffle(power_cards)

    # Return the shuffled list of power cards
    return power_cards

def setup_cards():
    """Set up both the water card and power card piles as described in the setup_water_cards and setup_power_cards functions.
    Return a 2-tuple containing the water cards pile and the power cards pile, respectively.(Each pile should be represented by a list.)
    """

    # Set up the water cards and power cards
    water_card = setup_water_cards()
    power_card = setup_power_cards()

    # Return a tuple containing water cards and power cards
    return (water_card, power_card)


def get_card_from_pile(pile, index):
    """Removes the entry at the specified index of the given pile (water or power) and modifies the pile by reference. 
    This function returns the entry at the specified index. HINT: Use the pop function
    """
    # Remove and return the entry at the specified index
    return pile.pop(index)



def arrange_cards(cards_list):
    """Arrange the players cards such that: 
        The first three indices are water cards, sorted in ascending order. 
        The last two indices are power cards, sorted in alphabetical order.
    This function doesn't return anything.
    """
    if not cards_list:
        return
        
    # Separate water cards (integer) and power cards (strings)
    water_card = [card for card in cards_list if isinstance(card, int)]
    power_card = [card for card in cards_list if isinstance(card, str)]
    
    # Sort water cards in ascending order and power cards in alphabetical order
    water_card.sort()
    power_card.sort()

    # Create a list of the hand, ensuring we have enough cards
    water_cards_to_use = water_card[:3] if len(water_card) >= 3 else water_card
    power_cards_to_use = power_card[:2] if len(power_card) >= 2 else power_card
    
    # Update the original cards_list with the sorted water and power cards
    cards_list[:] = water_cards_to_use + power_cards_to_use


def deal_cards(water_cards_pile, power_cards_pile):
    """Deals cards to player 1 and player 2. Each player would get 3 water cards and 2 power cards. Then, call the arrange_cards function to arrange the cards.
    When dealing, alternately take off a card from the first entry in the pile.
    
    Return a 2-tuple containing the player 1's hand and player 2's hand, respectively. (Each hand should be represented by a list.)
    """

    player_1 = []
    player_2 = []

    # Deal 3 water cards to each player and reduce the water card pile
    for _ in range(3):
        player_1.append(get_card_from_pile(water_cards_pile, 0))
        player_2.append(get_card_from_pile(water_cards_pile, 0))

    # Deal 2 power cards to each player and reduce the power card pile
    for _ in range(2):
        player_1.append(get_card_from_pile(power_cards_pile, 0))
        player_2.append(get_card_from_pile(power_cards_pile, 0))

    # Arrange cards for both players
    arrange_cards(player_1)
    arrange_cards(player_2)

    return (player_1, player_2)



def apply_overflow(tank_level):
    """If necessary, apply the overflow rule discussed in the “About the Assignment” section of this assignment.
        
        remaining water = maximum fill value - overflow
    
    Return the tank level. If no overflow occurred, this is just the starting tank level.
    """
    # Define the maximum fill value
    maximum_fill_value = 80
    
    # Check if the tank level exceeds the maximum fill value
    if tank_level > maximum_fill_value:
        # Calculate the overflow amount
        overflow = tank_level - maximum_fill_value
        # Return the adjusted tank level after applying overflow
        return maximum_fill_value - overflow
    
    # Return the original tank level if no overflow occurred
    return tank_level


def use_card(player_tank, card_to_use, player_cards, opponent_tank):
    """Get that card from the player's hand, and update the tank level based on the card that was used. This does not include drawing a replacement card, so after using the card, the player_cards size will only be 4 cards. 
    
    Apply overflow if necessary.

    Return a 2-tuple containing the player's tank and the opponent's tank, respectively.
    """
    # Find the index of the card to use and remove it from the player's hand
    card_index = player_cards.index(card_to_use)
    card_value = player_cards.pop(card_index)

    # Check if the card is a water card (integer)
    if isinstance(card_value, int):
        # Add the water card value to the player's tank
        player_tank += card_value
    else:
        # Check if the card is a power card and apply the corresponding effect
        if card_value == 'SOH':
            # Steal half of the opponent's tank value
            value = int(opponent_tank / 2)
            opponent_tank -= value
            player_tank += value
        elif card_value == 'DOT':
            # Drain the opponent's tank
            opponent_tank = 0
        elif card_value == 'DMT':
            # Double the player's tank value
            player_tank *= 2

    # Apply overflow rules if the tank level exceeds 80
    if player_tank > 80:
        player_tank = apply_overflow(player_tank)

    # Return the updated tank levels for both players
    return (player_tank, opponent_tank)


def discard_card(card_to_discard, player_cards, water_cards_pile, power_cards_pile):
    """Discard the given card from the player's hand and return it to the bottom of the
    appropriate pile. (Water cards should go in the water card pile and power cards should go in the power card pile.) The bottom of the pile is the last index in the list.
    
    Same as use_card(), this function does not include drawing a replacement card, so after calling this function, the player_cards size will only be 4 cards.
    
    This function does not return anything.
    """
    # Find the index of the card to discard from the player's hand
    card_index = player_cards.index(card_to_discard)
    card_value = player_cards.pop(card_index)
    
    # Check the card type; if the card is an integer, put it back at the bottom of the water pile
    if isinstance(card_value, int):
        water_cards_pile.append(card_value)
    # If the card is a string, put it back at the bottom of the power pile
    else:
        power_cards_pile.append(card_value)


def filled_tank(tank):
    """Determine if the tank level is between the maximum and minimum fill values (inclusive).
    
    Return a boolean representing whether the tank is filled.
    This will be True if the tank is filled.
    """
    # Define the maximum and minimum fill values
    maximum_value = 80
    minimum_value = 75
    
    # Check if the tank level is within the acceptable range
    if minimum_value <= tank <= maximum_value:
        return True
    
    # Return False if the tank level is outside the acceptable range
    return False


def check_pile(pile, pile_type):
    """Checks if the given pile is empty. If so, call the pile's setup function to replenish the pile. 
    pile_type is a string to determine what type of pile you are checking (“water” or “power”)
    This function does not return anything.
    """
    # Check if pile is empty
    if len(pile) == 0:
        # Check to see if the empty pile is the water pile
        if pile_type.lower() == 'water':
            # Replenish the water pile
            pile.extend(setup_water_cards())
        # Check to see if the empty pile is the power pile
        elif pile_type.lower() == 'power':
            # Replenish the power pile
            pile.extend(setup_power_cards())
        else:
            # Print an error message if the pile type is invalid
            print("Invalid inputs, please enter 'water' or 'power'.")
    

def human_play(human_tank, human_cards, water_cards_pile, power_cards_pile, opponent_tank):
    """
    Function to handle the human player's turn.
    - Show the human player's water level and then the computer player's water level.
    - Show the human player their hand and ask them if they want to use or discard a card. If the human player enters an invalid answer, reprompt until a valid answer is entered.
    - Carry out the human's turn based on the action they have chosen (based on user input). 
    Be sure to use the get_user_input function.
    - Print the card the human player uses or discards. If the human player enters a card to use or discard which is not in their hand, reprompt until a valid card is entered.
    - Remember to handle potential overflows.
    - Once the human has used or discarded a card, draw a new card of the same type they just used/discarded.
    - Make sure that the human's hand is still properly arranged after adding the new card.
    - Return a 2-tuple containing the human's tank level and the computer's tank level, respectively.
    """

    # Print the current tank levels and the human's cards
    print("Your water level is at: {}. \nComputer's water level is at: {}. \nYour cards are: {}\n".format(human_tank, opponent_tank, human_cards))
    
    while True:
        # Ask the human player if they want to use or discard a card
        try:
            action = str(get_user_input('Would you like to "use" or "discard" a card? u/d: ').lower())
            if action not in ["u", "d"]:
                print('Invalid action. Please enter "u" or "d".')
                continue
        except:
            print('Invalid action. Please enter "u" or "d".')
            continue
            
        # Ask the human player which card they want to use or discard
        card = get_user_input('\nWhich card would you like to use or discard? ')
        if card in human_cards:
            # Check and use if play want to use a card
            if action == "u":
                print('Card used: {}\n'.format(card))
                # Use the selected card and update the tank levels
                human_tank, opponent_tank = use_card(human_tank, card, human_cards, opponent_tank)
                
                if human_tank > 80:
                    # Apply overflow rules if the tank level exceeds 80
                    human_tank = apply_overflow(human_tank)
            else:
                # Discard the selected card
                print('Card discarded: {}\n'.format(card))
                discard_card(card, human_cards, water_cards_pile, power_cards_pile)
            
            # Draw a new card of the same type
            if isinstance(card, int):
                new_card = get_card_from_pile(water_cards_pile, 0)
            else:
                new_card = get_card_from_pile(power_cards_pile, 0)
            
            # Add the new card to the human's hand
            human_cards.append(new_card)
            # Arrange the human's cards
            arrange_cards(human_cards)
            break
        else:
            print('\nInvalid entry, please choose a card from your hand.\n')
    
    # Print the updated tank levels after the turn
    print("Your water level is now at: {}. \nComputer's water level is now at: {}. \nYour cards are now: {}\n".format(human_tank, opponent_tank, human_cards))

    return (human_tank, opponent_tank)


def computer_play(computer_tank, computer_cards, water_cards_pile, power_cards_pile, opponent_tank):
    """
    This function handles the computer's turn.
    - The computer's strategy should consider all of its cards when playing.
    - The computer should not “cheat.” They should not be able to see any cards from the human's hand, the water card pile, or power card pile.
    - This function should carry out the computer's turn based on the action that the computer chooses.
    - Remember to handle potential overflows.
    - Print the card the computer player uses or discards.
    - Once the computer has used or discarded a card, give them a new card of the same type they just used/discarded.
    - Make sure that the computer's hand is still properly arranged after adding the new card.
    - Return a 2-tuple containing the computer's tank level and the human's tank level, respectively.
    """

    best_card = None

    # Print the current tank levels
    print("Computer's water level is at: {}. \nYour water level is at: {}\n".format(computer_tank, opponent_tank))

    # Check if the computer can win with a power card
    for card in computer_cards:
        if card == 'DMT' and computer_tank * 2 >= 75:
            best_card = card
            break
    
    # Check if the computer can win with a water card
    for card in computer_cards:
        if isinstance(card, int):
            if card + computer_tank >= 75:
                best_card = card
                break

    # Check if the opponent is close to winning and the computer has special cards to use
    if best_card is None and 36 <= opponent_tank <= 75:
        for card in computer_cards:
            if card == 'SOH' or card == 'DOT':
                best_card = card
                break
    
    # Check if the opponent tank is between 10 and 30 computer have two SOH cards.
    soh_counter = 0
    for card in computer_cards:
        if card == 'SOH':
            soh_counter += 1
        if soh_counter == 2 and 10 <= opponent_tank <= 30:
            best_card = card
            break
    
    # Check if the opponent tank is between 10 and 30 computer have two DMT cards.
    dmt_counter = 0
    for card in computer_cards:
        if card == 'DMT':
            dmt_counter += 1
        if dmt_counter == 2 and 10 <= opponent_tank <= 50:
            best_card = card
            break

    # Check if the opponent tank is between 10 and 30 computer have two DMT cards.
    dmt_counter = 0
    for card in computer_cards:
        if card == 'DOT':
            dmt_counter += 1
        if dmt_counter == 2 and 10 <= opponent_tank <= 50:
            best_card = card
            break

    # If no special card was chosen, iterate through the computer's cards to find the best water card to play
    if best_card is None:
        for card in computer_cards:
            if isinstance(card, int):  # Check if the card is a water card
                potential_tank = computer_tank + card
                if 75 <= potential_tank <= 80:
                    best_card = card
                    break
                if best_card is None or (card > best_card and potential_tank <= 80):
                    best_card = card

    # If no valid card is found, discard the first card
    if best_card is None:
        best_card = computer_cards[0]

    if isinstance(best_card, int):
        # Use the best water card and update the tank level
        computer_tank += best_card
        if computer_tank > 80:
            computer_tank = apply_overflow(computer_tank)
        new_card = get_card_from_pile(water_cards_pile, 0)
    else:
        # Use the best power card and update the tank levels accordingly
        if best_card == 'SOH':
            value = int(opponent_tank / 2)
            computer_tank += value
            opponent_tank -= value
        elif best_card == 'DOT':
            opponent_tank = 0
        elif best_card == 'DMT':
            computer_tank *= 2
            if computer_tank > 80:
                computer_tank = apply_overflow(computer_tank)
        new_card = get_card_from_pile(power_cards_pile, 0)

    # Print the card the computer is playing
    print(f"Computer playing with card: {best_card}")

    # Remove the used card from the computer's hand
    computer_cards.remove(best_card)

    # Add the new card to the computer's hand
    computer_cards.append(new_card)
    arrange_cards(computer_cards)

    # Print the updated tank levels after the turn
    print("Computer's water level is now at: {}. \nYour water level is now at: {}. \n".format(computer_tank, opponent_tank))

    return (computer_tank, opponent_tank)


def main():
    """
    Main function to run the water tank game.
    Initializes the game, deals cards, and manages turns between human and computer players.
    """
    # print game instructions
    print("\nWater Tank is a competitive card game played between two players. The players will be a human player and a computer player. Each player starts with an empty water tank, which they need to fill. The goal is to be the first player to fill their tank. A tank is filled if it reaches the value of 75 to 80 units (inclusive). There are two types of cards: water cards and power cards. There will be a pile for each type of card (one pile for water and one pile for power). Each water card has a value that represents the amount of water that it contributes to the tank. When a water card is played, that player adds the specified amount of water to their tank. \n\nPower cards allow players to perform special actions:\n \t● SOH (Steal Opponent’s Half): Take half the water in your opponent’s tank and add it to your own\n \t● DOT (Drain Opponent’s Tank): Empty your opponent’s tank completely\n \t● DMT (Double My Tank): Double the current value of your own tank.\n\nIf a player’s water level exceeds their tank’s maximum fill value, an overflow happens. In the case of an overflow, extra water sloshes out of the tank. The amount of water that remains in the tank is determined by a formula: remaining water = maximum fill value - overflow.\n")

    # Initialize Tanks
    human_tank = 0
    computer_tank = 0

    try:
        # Set up the water and power card piles
        water_cards_pile, power_cards_pile = setup_cards()
        
        # Deal cards to both players
        human_cards, computer_cards = deal_cards(water_cards_pile, power_cards_pile)
        
        # Randomly decide who goes first
        player = random.randint(0, 1)
        if player == 0:
            print("\nHuman player goes first.")
        else:
            print('\nComputer goes first.')

        # Main game loop
        while True:
            if player == 0:
                print("=== Human Player's turn ===")
                # Human player's turn
                human_tank, computer_tank = human_play(human_tank, human_cards, water_cards_pile, power_cards_pile, computer_tank)
                # Check if the human player has won
                if filled_tank(human_tank):
                    print("Human player wins!\n")
                    break
            else:
                print("=== Computer Player's turn ===")
                # Computer player's turn
                computer_tank, human_tank = computer_play(computer_tank, computer_cards, water_cards_pile, power_cards_pile, human_tank)
                # Check if the computer player has won
                if filled_tank(computer_tank):
                    print("Computer player wins!\n")
                    break
            
            # Switch turns
            player = 1 - player
            
            # Check and replenish piles if necessary
            check_pile(water_cards_pile, 'water')
            check_pile(power_cards_pile, 'power')

    except Exception as e:
        # Handle any unexpected errors
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()