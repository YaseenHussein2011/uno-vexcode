#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
motor_1 = Motor(Ports.PORT1, False)
motor_5 = Motor(Ports.PORT5, True)

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

# Create events
FWD = Event()
RT = Event()
LT = Event()

# Functions
def motor_1_move_forward():
    motor_1.spin_for(FORWARD, 425, DEGREES)

def motor_5_move_forward():
    motor_5.spin_for(FORWARD, 425, DEGREES)

def motor_1_turn_right():
    motor_1.spin_for(FORWARD, 220, DEGREES)

def motor_5_turn_right():
    motor_5.spin_for(REVERSE, 220, DEGREES)

def motor_1_turn_left():
    motor_1.spin_for(REVERSE, 220, DEGREES)

def motor_5_turn_left():
    motor_5.spin_for(FORWARD, 220, DEGREES)

# Register event callbacks
FWD(motor_1_move_forward)
FWD(motor_5_move_forward)
RT(motor_1_turn_right)
RT(motor_5_turn_right)
LT(motor_1_turn_left)
LT(motor_5_turn_left)
wait(15, MSEC)

def when_started():
    FWD.broadcast_and_wait()
    LT.broadcast_and_wait()
    FWD.broadcast_and_wait()
    RT.broadcast_and_wait()

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

    for _ in range(4):
        deck.append("Wild")
        deck.append("Wild Draw 4")

    # Fisher-Yates Shuffle
    for i in range(len(deck) - 1, 0, -1):
        j = urandom.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]

    return deck

def draw_card(deck):
    if len(deck) > 0:
        return deck.pop(0)
    return None

def start_game(deck):
    hand = []
    for _ in range(7):
        card = draw_card(deck)
        if card != None:
            hand.append(card)
    return hand

def print_hand_to_console(hand):
    print("=== STARTING HAND ===")
    for index, card in enumerate(hand, 1):
        print("Card " + str(index) + ": " + card)

# Helper function to abbreviate card names to fit 16 columns
def shorten_card(card):
    if card == "Wild":
        return "W"
    if card == "Wild Draw 4":
        return "W+4"
    
    parts = card.split(" ")
    color = parts[0][0]  # 'R', 'Y', 'G', 'B'
    
    if len(parts) == 3:
        return color + "+2"
    if parts[1] == "Skip":
        return color + "Sk"
    if parts[1] == "Reverse":
        return color + "Rv"
    
    return color + parts[1]

# Display all 7 cards fitting into 5 rows x 16 columns
def print_hand_to_screen(hand):
    brain.screen.clear_screen()
    
    short_cards = []
    for index, card in enumerate(hand, 1):
        short_cards.append(str(index) + ":" + shorten_card(card))
        
    # Row 1: Header (15 chars)
    brain.screen.set_cursor(1, 1)
    brain.screen.print("--- MY HAND ---")
    
    # Row 2: Cards 1, 2, 3 (Max ~15 chars)
    line1 = short_cards[0] + " " + short_cards[1] + " " + short_cards[2]
    brain.screen.set_cursor(2, 1)
    brain.screen.print(line1[0:16])
    
    # Row 3: Cards 4, 5 (Max ~12 chars)
    line2 = short_cards[3] + " " + short_cards[4]
    brain.screen.set_cursor(3, 1)
    brain.screen.print(line2[0:16])
    
    # Row 4: Cards 6, 7 (Max ~12 chars)
    line3 = short_cards[5] + " " + short_cards[6]
    brain.screen.set_cursor(4, 1)
    brain.screen.print(line3[0:16])
    
    # Row 5: Remaining Deck Status (15 chars)
    brain.screen.set_cursor(5, 1)
    brain.screen.print("Deck: " + str(len(uno_deck)) + " cards")

# Run motor sequence


# Generate deck, start game, and print outputs
uno_deck = create_shuffled_uno_deck()
player_hand = start_game(uno_deck)

print_hand_to_console(player_hand)
print_hand_to_screen(player_hand)