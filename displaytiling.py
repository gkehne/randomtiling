# Gregory Kehne
#
# This file contains the methods that display the 1xn tiling that tiler.py 
# creates. It can display as text output, temporary images, or saved images.


from PIL import Image, ImageDraw


# choose how to display the board:
# displaytype="text" for text output
# displaytype="temp" for a temporary image
# displaytype="filename" for .jpg image output
def disp(board, displaytype):
	dt = displaytype.lower()
	if dt == "text":
		textbrd(board)
	elif dt == "temp":
		picturebrd(board, displaytype, False)
	else:
		picturebrd(board, displaytype, True)
	return


# text board output
def textbrd(b):
	output = ""
	for row in b:
		r1, r2, r3 = [], [], []
		for ele in row:
			if ele == 1:
				r1 = r1 + ["+", "1", "+"]
				r2 = r2 + ["+", "1", "+"]
				r3 = r3 + ["+", "+", "+"]
			if ele == 2:
				r1 = r1 + ["+", "+", "+"]
				r2 = r2 + ["2", "2", "+"]
				r3 = r3 + ["+", "+", "+"]
			if ele == 3:
				r1 = r1 + ["+", "+", "+"]
				r2 = r2 + ["+", "3", "+"]
				r3 = r3 + ["+", "3", "+"]
			if ele == 4:
				r1 = r1 + ["+", "+", "+"]
				r2 = r2 + ["+", "4", "4"]
				r3 = r3 + ["+", "+", "+"]
			if ele == 5:
				r1 = r1 + ["+", "5", "+"]
				r2 = r2 + ["+", "5", "+"]
				r3 = r3 + ["+", "5", "+"]
			if ele == 6:
				r1 = r1 + ["+", "+", "+"]
				r2 = r2 + ["6", "6", "6"]
				r3 = r3 + ["+", "+", "+"]
			if ele == 0:
				r1 = r1 + ["+", "+", "+"]
				r2 = r2 + ["+", "0", "+"]
				r3 = r3 + ["+", "+", "+"]

		r, s, t = "", "", ""
		for n in range(len(r1)):
			r = r + r1[n] + " "
			s = s + r2[n] + " "
			t = t + r3[n] + " "
		output += r + '\n' + s + '\n' + t + '\n'
	print output


# image board output
def picturebrd(b, name, saveit):
	if len(b) == 0:
		print "ERROR: Tried to display an empty board!"
		return

	b = zip(*b)  # transpose b so the picture works

	height = 32 * len(b)
	width = 32 * len(b)

	# new image created
	im = Image.new('RGBA', (height, width), (255, 255, 255, 0))
	draw = ImageDraw.Draw(im)

	color = (0, 0, 0, 0)  # bline color
	w = 1  # width for line

	for i in range(len(b)):
		xZ = 32 * i
		for j in range(len(b[i])):
			yZ = 32 * j
			# standard interior of cell points
			p1 = (xZ + 4, yZ + 4)
			p2 = (xZ + 4, yZ + 28)
			p3 = (xZ + 28, yZ + 28)
			p4 = (xZ + 28, yZ + 4)
			# display cases
			if b[i][j] == 0:
				draw.line([p1, p2], fill=color, width=w)
				draw.line([p2, p3], fill=color, width=w)
				draw.line([p3, p4], fill=color, width=w)
				draw.line([p4, p1], fill=color, width=w)
			if b[i][j] == 1:
				draw.line([(xZ + 4, yZ), p2], fill=color, width=w)
				draw.line([p2, p3], fill=color, width=w)
				draw.line([p3, (xZ + 28, yZ)], fill=color, width=w)
			if b[i][j] == 2:
				draw.line([(xZ, yZ + 28), p3], fill=color, width=w)
				draw.line([p3, p4], fill=color, width=w)
				draw.line([p4, (xZ, yZ + 4)], fill=color, width=w)
			if b[i][j] == 3:
				draw.line([(xZ + 4, yZ + 32), p1], fill=color, width=w)
				draw.line([p4, p1], fill=color, width=w)
				draw.line([p4, (xZ + 28, yZ + 32)], fill=color, width=w)
			if b[i][j] == 4:
				draw.line([(xZ + 32, yZ + 4), p1], fill=color, width=w)
				draw.line([p1, p2], fill=color, width=w)
				draw.line([p2, (xZ + 32, yZ + 28)], fill=color, width=w)
			if b[i][j] == 5:  # vertical?
				draw.line([(xZ, yZ + 4), (xZ + 32, yZ + 4)], fill=color, width=w)
				draw.line([(xZ, yZ + 28), (xZ + 32, yZ + 28)], fill=color, width=w)
			if b[i][j] == 6:  # horizontal?
				draw.line([(xZ + 4, yZ), (xZ + 4, yZ + 32)], fill=color, width=w)
				draw.line([(xZ + 28, yZ), (xZ + 28, yZ + 32)], fill=color, width=w)
	# output choice:
	if not saveit:
		im.show()
	else:
		im.save(name + ".jpg")
	return
