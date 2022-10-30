import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage.metrics import structural_similarity
from skimage.metrics import mean_squared_error

image_file = sys.argv[1]
game = plt.imread(image_file)

empty = plt.imread('images/empty-board.png')

def as_tiled(image):
    without_border = image[18:18+42*15, 18:18+42*15]
    tiled = without_border.reshape(15, 42, 15, 42, 4)
    tiled = np.moveaxis(tiled, 2, 0)
    return tiled

empty_as_tiled = as_tiled(empty)
game_as_tiled = as_tiled(game)

#CAUTION, we are using a strange column, row indexing (so as to have A1, A3... first column then row)
#tile1 = game_as_tiled[2][2]

# Load known images of letters into a dictionary
letter_images = {}
for i in range(26):
    ltr = chr(ord('A') + i)
    letter_images[ltr] = plt.imread(f'images/{ltr}.png')
    letter_images[ltr.lower()] = plt.imread(f'images/{ltr}_blank.png')

scrabble_text = np.zeros((15, 15), dtype='U1')

for row in range(15):
    for col in range(15):
        sim = structural_similarity(empty_as_tiled[col][row], game_as_tiled[col][row], win_size=3)
        if sim > 0.90:
            scrabble_text[row][col] = ' '
        else:
            tile = game_as_tiled[col][row]
            dist_letters = [ (mean_squared_error(tile, letter_images[ltr]), ltr) for ltr in letter_images.keys()]
            # In case the empirically found threshold is wrong... We compare with the tile in the empty board along with letters
            dist_letters.append((mean_squared_error(tile, empty_as_tiled[col][row]), ' '))
            probab_letter = min(dist_letters)[1]
            scrabble_text[row][col] = probab_letter

for row in range(15):
    for col in range(15):
        print(scrabble_text[row][col], end='')
    print('')

print('\n')

for col in range(15):
    for row in range(15):
        print(scrabble_text[row][col], end='')
    print('')
