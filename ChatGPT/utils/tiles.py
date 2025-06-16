import sys

GROUND = "X"
BREAKABLE = "S"
EMPTY = "-"
FULL_QUESTION_BLOCK = "?"
EMPTY_QUESTION_BLOCK = "Q"
ENEMY = "E"
TOP_LEFT_PIPE = "<"
TOP_RIGHT_PIPE = ">"
LEFT_PIPE = "["
RIGHT_PIPE = "]"
COIN = "o"
CANNON_TOP = "B"
CANNON_BOTTOM = "b"

TILES = [GROUND, BREAKABLE, EMPTY, FULL_QUESTION_BLOCK, EMPTY_QUESTION_BLOCK, ENEMY, TOP_LEFT_PIPE, TOP_RIGHT_PIPE, LEFT_PIPE, RIGHT_PIPE, COIN, CANNON_TOP, CANNON_BOTTOM]

def from_int_to_vglc(num):
    if num == 0:
        return "X"
    elif num == 1:
        return "S"
    elif num == 2:
        return "-"
    elif num == 3:
        return "?"
    elif num == 4:
        return "Q"
    elif num == 5:
        return "E"
    elif num == 6:
        return "<"
    elif num == 7:
        return ">"
    elif num == 8:
        return "["
    elif num == 9:
        return "]"
    elif num == 10:
        return "o"
    elif num == 11:
        return "B"
    elif num == 12:
        return "b"
    else:
        print("ERROR: Invalid number. Exiting...")
        sys.exit(1)
        
def from_vglc_to_int(char):
    if char == "X":
        return 0
    elif char == "S":
        return 1
    elif char == "-":
        return 2
    elif char == "?":
        return 3
    elif char == "Q":
        return 4
    elif char == "E":
        return 5
    elif char == "<":
        return 6
    elif char == ">":
        return 7
    elif char == "[":
        return 8
    elif char == "]":
        return 9
    elif char == "o":
        return 10
    elif char == "B":
        return 11
    elif char == "b":
        return 12
    else:
        print("ERROR: Invalid char. Exiting...")
        sys.exit(1)

''' "X" : ["solid","ground"],
    "S" : ["solid","breakable"],
    "-" : ["passable","empty"],
    "?" : ["solid","question block", "full question block"],
    "Q" : ["solid","question block", "empty question block"],
    "E" : ["enemy","damaging","hazard","moving"],
    "<" : ["solid","top-left pipe","pipe"],
    ">" : ["solid","top-right pipe","pipe"],
    "[" : ["solid","left pipe","pipe"],
    "]" : ["solid","right pipe","pipe"],
    "o" : ["coin","collectable","passable"],
    "B" : ["Cannon top","cannon","solid","hazard"],
    "b" : ["Cannon bottom","cannon","solid"]'''
