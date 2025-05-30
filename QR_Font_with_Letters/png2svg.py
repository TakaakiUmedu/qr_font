import sys
import PIL.Image
from queue import deque

src = sys.argv[1]
dst = sys.argv[2]

#print(src, dst)

img = PIL.Image.open(src)

w, h = img.size

#print(img.size)

data = []
for y in range(h):
	l = []
	for x in range(w):
		r = img.getpixel((x, y))
		l.append((r == 0))
	data.append(l)

blacks = []
whites = []

layer = [[None] * w for _ in range(h)]

if data[0][0] != False:
	raise Exception("top left is not white")

layer[0][0] = 0
queue = deque([(0, 0)])

while queue:
	x, y = queue.popleft()
	c = data[y][x]
	l = layer[y][x]
	for d, (dx, dy, sx, sy, vx, vy) in enumerate((
			(0, -1, 0, 0, 1, 0),
			(1, 0, 1, 0, 0, 1), 
			(0, 1, 1, 1, -1, 0), 
			(-1, 0, 0, 1, 0, -1), 
		)):
		nx = x + dx
		ny = y + dy
		if nx >= 0 and nx < w and ny >= 0 and ny < h and layer[ny][nx] == None:
			if data[ny][nx] == c:
				layer[ny][nx] = l
				queue.appendleft((nx, ny))
#				add_line(c, d, (x + sx, y + sy), (x + sx + vx, y + sy + vy))
			else:
				layer[ny][nx] = l + 1
				queue.append((nx, ny))
#				add_line(l + 1, d, (x + sx, y + sy), (x + sx + vx, y + sy + vy))

line_table = [{} for _ in range(max(max(l) for l in layer))]

for y in range(h):
	for x in range(w):
		c = data[y][x]
		l = layer[y][x]
		lines = line_table[c]
		for d, (dx, dy, sx, sy, vx, vy) in enumerate((
				(0, -1, 0, 0, 1, 0),
				(1, 0, 1, 0, 0, 1), 
				(0, 1, 1, 1, -1, 0), 
				(-1, 0, 0, 1, 0, -1), 
			)):
			nx = x + dx
			ny = y + dy
			if nx >= 0 and nx < w and ny >= 0 and ny < h and layer[ny][nx] > l:
				p0 = (x + sx, y + sy)
				p1 = (x + sx + vx, y + sy + vy)
				key = (d, p0)
				if key in lines:
					raise Exception
				
				lines[key] = p1

#print(len(line_table))
for lines in line_table:
	while True:
		changed = False
		for key0, p1 in lines.items():
			d, p0 = key0
			key1 = (d, p1)
			if key1 in lines:
				p2 = lines[key1]
				changed = True
				del lines[key1]
				lines[key0] = p2
				break
		
		if not changed:
			break

def dist(p):
	x, y = p
	return min(x, y, w - 1 - x, h - 1 - y)

def output(lines, file):
	while lines:
		
		tmp = []
		for p0, l in lines.items():
			m = min(dist(p0), min(dist(p) for p in l))
			tmp.append((m, p0))
		
		p0 = min(tmp)[1]
		ls = lines[p0]
		p1 = ls.pop()
		if len(ls) == 0:
			del lines[p0]
		print(f"M{p0[0]},{p0[1]}L{p1[0]},{p1[1]}", file = file, end = "", flush = True)

		while True:
			if p1 in lines:
				ls = lines[p1]
				p2 = ls.pop()
				if len(ls) == 0:
					del lines[p1]
				
				print(f"L{p2[0]},{p2[1]}", file = file, end = "", flush = True)
				p1 = p2
			else:
				if p1 != p0:
					print(p1, p0, lines)
					raise Exception()
				break

with open(dst, "w") as svg:
	print('<svg width="29mm" height="29mm" version="1.1" viewBox="0 0 29 29" xmlns="http://www.w3.org/2000/svg"><path d="', end = "", file = svg)
	try:
		for c, lines in enumerate(line_table):
			l = {}
			
			for (d0, p0), p1 in lines.items():
				if c % 2 == 0:
					if p1 in l:
						l[p1].append(p0)
					else:
						l[p1] = [p0]
				else:
					if p0 in l:
						l[p0].append(p1)
					else:
						l[p0] = [p1]
			output(l, svg)
	
	except:
		raise
	finally:
		print('" id="qr-path" fill="#000000" fill-opacity="1" fill-rule="nonzero" stroke="none"/></svg>', end = "", file = svg)
