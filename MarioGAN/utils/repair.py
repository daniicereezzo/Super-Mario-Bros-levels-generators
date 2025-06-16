from .tiles import *
import random
import sys

def repair_level(level):
    if level[-1] == "":
        level = level[:-1]

    height = len(level)
    width = len(level[0])

    no_tube_tiles = TILES[:6] + TILES[10:]

    top_left_pipe_positions = []
    top_right_pipe_positions = []
    left_pipe_positions = []
    right_pipe_positions = []

    for i in range(height):
        for j in range(width):
            if level[i][j] == TOP_LEFT_PIPE:
                if j == width - 1:
                    level[i] = set_character(level[i], j, random.choice(no_tube_tiles))
                else:
                    top_left_pipe_positions.append((j, i))
            elif level[i][j] == TOP_RIGHT_PIPE:
                if j == 0:
                    level[i] = set_character(level[i], j, random.choice(no_tube_tiles))
                else:
                    top_right_pipe_positions.append((j, i))
            elif level[i][j] == LEFT_PIPE:
                if j == width - 1:
                    level[i] = set_character(level[i], j, random.choice(no_tube_tiles))
                else:
                    left_pipe_positions.append((j, i))
            elif level[i][j] == RIGHT_PIPE:
                if j == 0:
                    level[i] = set_character(level[i], j, random.choice(no_tube_tiles))
                else:
                    right_pipe_positions.append((j, i))

    predicted_top_right_pipe_positions = [(x + 1, y) for x, y in top_left_pipe_positions]

    set_top_right_pipe_positions = set(top_right_pipe_positions)
    set_predicted_top_right_pipe_positions = set(predicted_top_right_pipe_positions)

    additions = set_predicted_top_right_pipe_positions - set_top_right_pipe_positions
    deletions = set_top_right_pipe_positions - set_predicted_top_right_pipe_positions

    for addition in additions:
        x, y = addition

        if addition in top_left_pipe_positions:
            top_left_pipe_positions.remove((x - 1, y))
            deletions.add((x - 1, y))
            continue
        if addition in left_pipe_positions:
            top_left_pipe_positions.remove((x - 1, y))
            deletions.add((x - 1, y))
            continue
        
        level[y] = set_character(level[y], x, TOP_RIGHT_PIPE)
    
    for deletion in deletions:
        x, y = deletion
        level[y] = set_character(level[y], x, random.choice(no_tube_tiles))
    
    predicted_right_pipe_positions = [(x + 1, y) for x, y in left_pipe_positions]

    set_right_pipe_positions = set(right_pipe_positions)
    set_predicted_right_pipe_positions = set(predicted_right_pipe_positions)

    additions = set_predicted_right_pipe_positions - set_right_pipe_positions
    deletions = set_right_pipe_positions - set_predicted_right_pipe_positions

    for addition in additions:
        x, y = addition
            
        if addition in top_left_pipe_positions:
            left_pipe_positions.remove((x -1, y))
            deletions.add((x - 1, y))
            continue
        if addition in left_pipe_positions:
            left_pipe_positions.remove((x - 1, y))
            deletions.add((x - 1, y))
            continue
        
        level[y] = set_character(level[y], x, RIGHT_PIPE)

    for deletion in deletions:
        x, y = deletion
        level[y] = set_character(level[y], x, random.choice(no_tube_tiles))

    for left_pipe_position in left_pipe_positions:
        x, y = left_pipe_position

        if y != 0 and y != height-1 and level[y-1][x] != TOP_LEFT_PIPE and level[y-1][x] != LEFT_PIPE and level[y+1][x] != TOP_LEFT_PIPE and level[y+1][x] != LEFT_PIPE:
            level[y] = set_character(level[y], x, TOP_LEFT_PIPE)
            level[y] = set_character(level[y], x+1, TOP_RIGHT_PIPE)
            left_pipe_positions.remove(left_pipe_position)
            top_left_pipe_positions.append(left_pipe_position)
        if y == 0 and level[y+1][x] != TOP_LEFT_PIPE and level[y+1][x] != LEFT_PIPE:
            level[y] = set_character(level[y], x, TOP_LEFT_PIPE)
            level[y] = set_character(level[y], x+1, TOP_RIGHT_PIPE)
            left_pipe_positions.remove(left_pipe_position)
            top_left_pipe_positions.append(left_pipe_position)
        if y == height-1 and level[y-1][x] != TOP_LEFT_PIPE and level[y-1][x] != LEFT_PIPE:
            level[y] = set_character(level[y], x, TOP_LEFT_PIPE)
            level[y] = set_character(level[y], x+1, TOP_RIGHT_PIPE)
            left_pipe_positions.remove(left_pipe_position)
            top_left_pipe_positions.append(left_pipe_position)
    
    for top_left_pipe_position in top_left_pipe_positions:
        x, y = top_left_pipe_position
        if (x, y - 1) in top_left_pipe_positions:
            level[y] = set_character(level[y], x, LEFT_PIPE)
            level[y] = set_character(level[y], x+1, RIGHT_PIPE)
            top_left_pipe_positions.remove(top_left_pipe_position)
            left_pipe_positions.append(top_left_pipe_position)

    for j in range(width):
        top_found = False
        tube_found = False
        first_tube_position = None

        for i in range(height):
            if level[i][j] == TOP_LEFT_PIPE:
                if not top_found and tube_found: # Pipe complete
                    tube_found = False
                    top_found = False
                    first_tube_position = None
                else:                            # New pipe
                    tube_found = False
                    top_found = True
                    first_tube_position = None
            elif level[i][j] == LEFT_PIPE:
                if not tube_found:
                    first_tube_position = (j, i)
                    tube_found = True
            else:
                if tube_found and not top_found:
                    x, y = first_tube_position
                    level[y] = set_character(level[y], x, TOP_LEFT_PIPE)
                    level[y] = set_character(level[y], x+1, TOP_RIGHT_PIPE)
                    top_left_pipe_positions.append(first_tube_position)
                    left_pipe_positions.remove(first_tube_position)
                tube_found = False
                top_found = False
                first_tube_position = None

        if tube_found and not top_found:
            x, y = first_tube_position
            level[y] = set_character(level[y], x, TOP_LEFT_PIPE)
            level[y] = set_character(level[y], x+1, TOP_RIGHT_PIPE)
            top_left_pipe_positions.append(first_tube_position)
            left_pipe_positions.remove(first_tube_position)
        tube_found = False
        top_found = False
        first_tube_position = None

    return "\n".join(level)

def set_character(string, position, character):
    if position < 0 or position >= len(string):
        print("ERROR: position out of range")
        sys.exit(1)

    return string[:position] + character + string[position+1:]