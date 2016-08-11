# Gregory Kehne
#
# This program generates a square window of fixed size into a planar tiling
# of 1x2 blocks that is randomly generated. It works by adding block positions
# that are randomly chosen from the frontier of possiblities on a diagonal
# that sweeps from one corner to the opposite corner. 

import displaytiling
import random

# length of tile. This works for tile=2, tile>=3 is increasingly unreliable.
tilesize = 2


# initializes an empty bxb matrix
def initboard(b):
	board = []
	for i in range(b):
		board.append([])
		for j in range(b):
			board[i].append(0)
	return board


# this adds a tile to board at spot r, c in direction s
def fill(board, r, c, s):
	b = len(board)
	# x, y, z are beginning, middle, and end squares for a tile
	if s == "u":
		x, y, z = 1, 6, 3
	if s == "d":
		x, y, z = 3, 6, 1
	if s == "r":
		x, y, z = 4, 5, 2
	if s == "l":
		x, y, z = 2, 5, 4
	u, v = 0, 0

	for i in range(tilesize):
		if 0 <= r + u and r + u < b and 0 <= c + v and c + v < b:
			if i == 0:
				board[r + u][c + v] = x
			if i == tilesize - 1:
				board[r + u][c + v] = z
			if i > 0 and i < tilesize - 1:
				board[r + u][c + v] = y
		# update the relevant direction for the loop
		if s == "d":
			u = u + 1
		if s == "u":
			u = u - 1
		if s == "l":
			v = v - 1
		if s == "r":
			v = v + 1


# checks to see if a tile can be placed on board at r, c in direction s
def checkdir(board, r, c, s):
	b = len(board)
	x, y = 0, 0
	boo = True
	for i in range(tilesize):
		# if its inside the box
		if 0 <= r + x and r + x < b and 0 <= c + y and c + y < b:
			if board[r + x][c + y] != 0:
				boo = False
		# update the relevant direction
		if s == "d":
			x = x + 1
		if s == "u":
			x = x - 1
		if s == "l":
			y = y - 1
		if s == "r":
			y = y + 1
	return boo


# Check to see if the board has 'contradictions' (unfillable spaces) in it
# or not. Possible problems for tile>2
def check(board):
	b = len(board)
	for r in range(b):
		for c in range(b):
			if board[r][c] == 0 and not (checkdir(board, r, c, "u") or
											checkdir(board, r, c, "d") or
											checkdir(board, r, c, "l") or
											checkdir(board, r, c, "r")):
				return False
	return True


# Creates a list of potential next moves to choose randomly from.
def findSpots(board):
	b = len(board)
	# array of potential next moves
	spots = []
	marker = False
	# scan diagonal for next moves
	for rc in range(2 * b):
		if marker:
			continue
		for i in range(b):
			if (rc - i < b and
				board[i][rc - i] == 0 and
				neighbors(board, i, rc - i) == 2):
				if checkdir(board, i, rc - i, "u"):
					spots.append([i, rc - i, "u"])
					if not marker:
						marker = True
				if checkdir(board, i, rc - i, "d"):
					spots.append([i, rc - i, "d"])
					if not marker:
						marker = True
				if checkdir(board, i, rc - i, "l"):
					spots.append([i, rc - i, "l"])
					if not marker:
						marker = True
				if checkdir(board, i, rc - i, "r"):
					spots.append([i, rc - i, "r"])
					if not marker:
						marker = True
	# If no 'corners' (2-neighbors), then choose from ones
	if len(spots) == 0:
		for r in range(b):
			for c in range(b):
				if board[r][c] == 0 and neighbors(board, r, c) == 1:
					if checkdir(board, r, c, "u"):
						spots.append([r, c, "u"])
					if checkdir(board, r, c, "d"):
						spots.append([r, c, "d"])
					if checkdir(board, r, c, "l"):
						spots.append([r, c, "l"])
					if checkdir(board, r, c, "r"):
						spots.append([r, c, "r"])

	return spots


# returns the number of tiled entries directly adjacent to the square
# at r, c in board
def neighbors(board, r, c):
	b = len(board)
	count = 0
	if 0 <= r and r < b and 0 <= c + 1 and c + 1 < b:
		if board[r][c + 1] != 0:
			count = count + 1
	if 0 <= r and r < b and 0 <= c - 1 and c - 1 < b:
		if board[r][c - 1] != 0:
			count = count + 1
	if 0 <= r + 1 and r + 1 < b and 0 <= c and c < b:
		if board[r + 1][c] != 0:
			count = count + 1
	if 0 <= r - 1 and r - 1 < b and 0 <= c and c < b:
		if board[r - 1][c] != 0:
			count = count + 1
	return count


# fills in all tiles that follow deterministcally (3 neighbors on a square)
def fillBoard(board):
	b = len(board)
	runitback = True  # this fills until there are no more fillable spots
	while runitback:
		runitback = False
		for r in range(b):
			for c in range(b):
				if board[r][c] == 0 and neighbors(board, r, c) == 3:
					if checkdir(board, r, c, "u"):
						fill(board, r, c, "u")
						runitback = True
					if checkdir(board, r, c, "d"):
						fill(board, r, c, "d")
						runitback = True
					if checkdir(board, r, c, "l"):
						fill(board, r, c, "l")
						runitback = True
					if checkdir(board, r, c, "r"):
						fill(board, r, c, "r")
						runitback = True


# checks if the board has been fully tiled (returns True if NOT fully tiled)
def notfull(board):
	b = len(board)
	for r in range(b):
		for c in range(b):
			if board[r][c] == 0:
				return True
	return False


# This is the main section of the program. It constructs the board, while
# it's not full or stuck it iterates through finding all options on the
# diagonal and choosing randomly between them. Finally it prints it out in
# progress (optional) and prints it out at the end
#
# b=dimension of square board to be randomly tiled with 1x2 tiles
# displaytype="text" for text output, ="temp" for a temporary picture, and
# ="filename" (no extension) for saved picture
def tile(b, displaytype):
	board = initboard(b)
	fill(board, 0, 0, "r")
	n = 0
	while check(board) and notfull(board):
		n = n + 1
		fillBoard(board)
		l = findSpots(board)
		if len(l) == 0:
			print "NO POSSIBLE TILING OPTIONS?!?!"
			displaytiling.disp(board)
			continue
		else:
			r = random.randint(0, len(l) - 1)
			m = l[r]
			fill(board, m[0], m[1], m[2])
	displaytiling.disp(board, displaytype)

# Default behavior: a 20x20 tiling of 1x2 blocks, displayed as a temporary image.
if __name__ == '__main__':
	tile(20, "temp")
