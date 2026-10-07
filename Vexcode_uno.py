#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()

# Wait for sensor(s) to fully initialize
wait(100, MSEC)

# Generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 

# Initialize random seed 
initializeRandomSeed()
#endregion VEXcode Generated Robot Configuration

# -------------------------------------------------------------
# UNO GAME TRACKER & DECK MANAGER (WITH PLAYER HAND)
# VEX Brain Screen Specs: 5 Rows x 16 Columns
# -------------------------------------------------------------

def create_shuffled_uno_deck():
    colors = ['Red', 'Yellow', 'Green', 'Blue']
    actions = ['Skip', 'Reverse', 'Draw 2']
    deck = []

    for color in colors:
        deck.append(color + " 0")
        for number in range(1, 10):
            deck.append(color + " " + str(number))
            deck.append(color + " " + str(number))
        for action in actions:
            deck.append(color + " " + action)
            deck.append(color + " " + action)
        # Wild cards associated with each individual color
        deck.append(color + " Wild")
        deck.append(color + " Wild Draw 4")

    # Fisher-Yates Shuffle using MicroPython urandom
    for i in range(len(deck) - 1, 0, -1):
        j = urandom.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]

    return deck

# Reusable function to draw a single card from deck
def draw_card(deck):
    if len(deck) > 0:
        return deck.pop(0)
    return None

# Function to deal 7 starting cards into player's hand
def start_game(deck):
    hand = []
    for _ in range(7):
        card = draw_card(deck)
        if card != None:
            hand.append(card)
    return hand

# Function to print player's hand to terminal console
def print_hand_to_console(hand):
    print("=== YOUR HAND (" + str(len(hand)) + " CARDS) ===")
    for index, card in enumerate(hand, 1):
        print("Card " + str(index) + ": " + card)

# Helper function to abbreviate card names for 16-column display
def shorten_card(card):
    parts = card.split(" ")
    color = parts[0][0]  # 'R', 'Y', 'G', 'B'
    val = " ".join(parts[1:])
    
    if val == "Wild Draw 4":
        return color + "+4"
    if val == "Draw 2":
        return color + "+2"
    if val == "Skip":
        return color + "Sk"
    if val == "Reverse":
        return color + "Rv"
    if val == "Wild":
        return color + "W"
    
    return color + val

# Debounced button listener for built-in Brain buttons
def wait_for_button_click():
    while True:
        if brain.buttonLeft.pressing():
            while brain.buttonLeft.pressing():
                wait(20, MSEC)
            return "LEFT"
        elif brain.buttonRight.pressing():
            while brain.buttonRight.pressing():
                wait(20, MSEC)
            return "RIGHT"
        elif brain.buttonCheck.pressing():
            while brain.buttonCheck.pressing():
                wait(20, MSEC)
            return "CHECK"
        wait(20, MSEC)

# Interactive menu to manually choose the active color for Wild cards
def choose_wild_color(wild_type):
    colors = ["Red", "Yellow", "Green", "Blue"]
    idx = 0
    
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("CHOOSE WILD COLOR")
        brain.screen.set_cursor(2, 1)
        brain.screen.print("< " + colors[idx] + " >")
        brain.screen.set_cursor(4, 1)
        brain.screen.print("L/R:Nav CHK:Pick")
        
        btn = wait_for_button_click()
        if btn == "LEFT":
            idx = (idx - 1) % len(colors)
        elif btn == "RIGHT":
            idx = (idx + 1) % len(colors)
        elif btn == "CHECK":
            selected_color = colors[idx]
            break

    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("COLOR CHOSEN:")
    brain.screen.set_cursor(2, 1)
    brain.screen.print("--> " + selected_color + " <--")
    brain.screen.set_cursor(5, 1)
    brain.screen.print("CHK: Continue")
    wait_for_button_click()

    return selected_color + " " + wild_type

# Print player's FULL hand across Rows 2, 3, and 4 (up to 9 cards per page)
def print_hand_to_screen(hand, status_msg=""):
    page = 0
    cards_per_page = 9
    
    while True:
        brain.screen.clear_screen()
        total_cards = len(hand)
        total_pages = (total_cards + cards_per_page - 1) // cards_per_page
        if total_pages == 0:
            total_pages = 1
            
        if total_pages > 1:
            header = "HAND(" + str(total_cards) + ") P" + str(page + 1) + "/" + str(total_pages)
        else:
            header = "HAND (" + str(total_cards) + " cards)"
            
        brain.screen.set_cursor(1, 1)
        brain.screen.print(header[0:16])
        
        start_idx = page * cards_per_page
        end_idx = min(start_idx + cards_per_page, total_cards)
        page_cards = []
        for index in range(start_idx, end_idx):
            page_cards.append(str(index + 1) + ":" + shorten_card(hand[index]))
            
        line1 = ""
        line2 = ""
        line3 = ""
        
        for i in range(len(page_cards)):
            if i < 3:
                line1 = line1 + page_cards[i] + " "
            elif i < 6:
                line2 = line2 + page_cards[i] + " "
            elif i < 9:
                line3 = line3 + page_cards[i] + " "
                
        brain.screen.set_cursor(2, 1)
        brain.screen.print(line1[0:16])
        brain.screen.set_cursor(3, 1)
        brain.screen.print(line2[0:16])
        brain.screen.set_cursor(4, 1)
        brain.screen.print(line3[0:16])
        
        brain.screen.set_cursor(5, 1)
        if total_pages > 1:
            brain.screen.print("L/R:Pg CHK:Done")
        else:
            if status_msg != "":
                brain.screen.print(status_msg[0:16])
            else:
                brain.screen.print("CHK: Continue")
                
        btn = wait_for_button_click()
        if btn == "LEFT" and total_pages > 1:
            page = (page - 1) % total_pages
        elif btn == "RIGHT" and total_pages > 1:
            page = (page + 1) % total_pages
        elif btn == "CHECK":
            break

# Step 1: Check Menu to see if robot player is being attacked
def check_attack_status():
    options = ["NONE", "DRAW +2", "DRAW +4"]
    idx = 0
    
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("BEING ATTACKED?")
        brain.screen.set_cursor(2, 1)
        brain.screen.print("< " + options[idx] + " >")
        brain.screen.set_cursor(4, 1)
        brain.screen.print("L/R:Nav CHK:Sel")
        
        btn = wait_for_button_click()
        if btn == "LEFT":
            idx = (idx - 1) % len(options)
        elif btn == "RIGHT":
            idx = (idx + 1) % len(options)
        elif btn == "CHECK":
            return options[idx]

# Step 2: Menu to select top discard card from deck
def select_uno_card_from_deck():
    colors = ["Red", "Yellow", "Green", "Blue", "Wild"]
    color_idx = 0
    
    # Select Color or Wild option directly
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("DISCARD COLOR:")
        brain.screen.set_cursor(2, 1)
        brain.screen.print("< " + colors[color_idx] + " >")
        brain.screen.set_cursor(4, 1)
        brain.screen.print("L/R:Nav CHK:Sel")
        
        btn = wait_for_button_click()
        if btn == "LEFT":
            color_idx = (color_idx - 1) % len(colors)
        elif btn == "RIGHT":
            color_idx = (color_idx + 1) % len(colors)
        elif btn == "CHECK":
            selected_color = colors[color_idx]
            break

    # If Wild chosen, select Wild type then select active color manually
    if selected_color == "Wild":
        wild_options = ["Wild", "Wild Draw 4"]
        w_idx = 0
        while True:
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
            brain.screen.print("WILD CARD TYPE:")
            brain.screen.set_cursor(2, 1)
            brain.screen.print("< " + wild_options[w_idx] + " >")
            brain.screen.set_cursor(4, 1)
            brain.screen.print("L/R:Nav CHK:Sel")
            
            btn = wait_for_button_click()
            if btn == "LEFT":
                w_idx = (w_idx - 1) % len(wild_options)
            elif btn == "RIGHT":
                w_idx = (w_idx + 1) % len(wild_options)
            elif btn == "CHECK":
                return choose_wild_color(wild_options[w_idx])
    else:
        values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "Draw 2"]
        val_idx = 0
        while True:
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)
            brain.screen.print("DISCARD VALUE:")
            brain.screen.set_cursor(2, 1)
            brain.screen.print("< " + values[val_idx] + " >")
            brain.screen.set_cursor(4, 1)
            brain.screen.print("L/R:Nav CHK:Set")
            
            btn = wait_for_button_click()
            if btn == "LEFT":
                val_idx = (val_idx - 1) % len(values)
            elif btn == "RIGHT":
                val_idx = (val_idx + 1) % len(values)
            elif btn == "CHECK":
                return selected_color + " " + values[val_idx]

# Check if a card is valid to play matching top discard
def is_valid_play(card, top_discard):
    card_color = card.split(" ")[0]
    target_color = top_discard.split(" ")[0]

    # If top discard was set by a Wild card, ONLY non-wild cards of the chosen color are allowed
    if "Wild" in top_discard:
        return card_color == target_color and "Wild" not in card

    # Wild cards in hand can be played on standard top discard cards
    if "Wild" in card:
        return True
    
    # Otherwise, card color must strictly match top discard color
    return card_color == target_color

# Step 3: Menu allowing player to PLAY a card from THEIR HAND or DRAW from deck
def process_player_turn(hand, deck, top_discard, new_cards_counter):
    playable_indices = []
    for idx, card in enumerate(hand):
        if is_valid_play(card, top_discard):
            playable_indices.append(idx)

    actions = ["PLAY CARD", "DRAW CARD"]
    action_idx = 0 if len(playable_indices) > 0 else 1

    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("TOP: " + shorten_card(top_discard))
        brain.screen.set_cursor(2, 1)
        brain.screen.print("< " + actions[action_idx] + " >")
        brain.screen.set_cursor(3, 1)
        brain.screen.print("Valid in Hand:" + str(len(playable_indices)))
        brain.screen.set_cursor(5, 1)
        brain.screen.print("L/R:Nav CHK:Sel")

        btn = wait_for_button_click()
        if btn == "LEFT" or btn == "RIGHT":
            action_idx = (action_idx + 1) % len(actions)
        elif btn == "CHECK":
            selected_action = actions[action_idx]

            # Play a card directly from the player's hand
            if selected_action == "PLAY CARD":
                if len(playable_indices) == 0:
                    brain.screen.clear_screen()
                    brain.screen.set_cursor(2, 1)
                    brain.screen.print("NO VALID CARDS!")
                    brain.screen.set_cursor(4, 1)
                    brain.screen.print("CHK: Must Draw")
                    wait_for_button_click()
                    action_idx = 1
                else:
                    card_pos = 0
                    while True:
                        c_idx = playable_indices[card_pos]
                        c_card = hand[c_idx]

                        brain.screen.clear_screen()
                        brain.screen.set_cursor(1, 1)
                        brain.screen.print("TOP: " + shorten_card(top_discard))
                        brain.screen.set_cursor(2, 1)
                        brain.screen.print("HAND: " + shorten_card(c_card))
                        brain.screen.set_cursor(4, 1)
                        brain.screen.print("L/R:Nav CHK:Play")

                        c_btn = wait_for_button_click()
                        if c_btn == "LEFT":
                            card_pos = (card_pos - 1) % len(playable_indices)
                        elif c_btn == "RIGHT":
                            card_pos = (card_pos + 1) % len(playable_indices)
                        elif c_btn == "CHECK":
                            played_card = hand.pop(c_idx)
                            
                            # Prompt player to manually select color when playing a Wild card from hand
                            if "Wild" in played_card:
                                wild_type = "Wild Draw 4" if "Wild Draw 4" in played_card else "Wild"
                                played_card = choose_wild_color(wild_type)
                                
                            print("Played Card from Hand: " + played_card)
                            return played_card

            # Draw a card into the player's hand
            if selected_action == "DRAW CARD":
                drawn_card = draw_card(deck)
                if drawn_card != None:
                    hand.append(drawn_card)
                    new_cards_counter[0] += 1
                    print("Drawn Card into Hand: " + drawn_card)
                    
                    if new_cards_counter[0] >= 2:
                        print("=== HAND UPDATED (2+ NEW CARDS) ===")
                        print_hand_to_screen(hand, "CHK: Continue")
                else:
                    brain.screen.clear_screen()
                    brain.screen.set_cursor(2, 1)
                    brain.screen.print("DECK EMPTY!")
                    wait(1500, MSEC)
                    
                return top_discard

# Main Program Execution Loop
def main_game_loop():
    uno_deck = create_shuffled_uno_deck()
    player_hand = start_game(uno_deck)
    new_cards_counter = [0]
    top_discard = "Red 0"
    
    while True:
        # Check Win Condition
        if len(player_hand) == 0:
            brain.screen.clear_screen()
            brain.screen.set_cursor(2, 1)
            brain.screen.print("YOU WIN UNO!")
            break

        # Display full hand on screen before starting each turn (press CHECK to proceed)
        print_hand_to_console(player_hand)
        print_hand_to_screen(player_hand, "CHK: Start Turn")

        # STEP 1: Check if robot player is being attacked (+2 or +4)
        attack_type = check_attack_status()
        
        if attack_type == "DRAW +2":
            print("Robot attacked with +2! Forcing 2 card draws...")
            for _ in range(2):
                c = draw_card(uno_deck)
                if c != None:
                    player_hand.append(c)
                    new_cards_counter[0] += 1
                    print("Attacked Draw: " + c)
            
            print_hand_to_console(player_hand)
            print_hand_to_screen(player_hand, "+2 Drawn CHK:End")

        elif attack_type == "DRAW +4":
            print("Robot attacked with +4! Forcing 4 card draws...")
            for _ in range(4):
                c = draw_card(uno_deck)
                if c != None:
                    player_hand.append(c)
                    new_cards_counter[0] += 1
                    print("Attacked Draw: " + c)
            
            print_hand_to_console(player_hand)
            print_hand_to_screen(player_hand, "+4 Drawn CHK:End")

        else:
            # STEP 2: If NOT attacked ("NONE"), select top discard card set by previous player
            top_discard = select_uno_card_from_deck()
            print("Current Discard Top: " + top_discard)
            
            # STEP 3: Process turn (PLAY card from hand or DRAW card into hand)
            top_discard = process_player_turn(player_hand, uno_deck, top_discard, new_cards_counter)
            print_hand_to_console(player_hand)

        wait(300, MSEC)

# Start UNO Game
main_game_loop()