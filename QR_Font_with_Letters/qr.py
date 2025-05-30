import qrcode
import qrcode.image.svg
import PIL
import PIL.ImageFont
import PIL.ImageDraw

size = 27
pos = 17
width = 10
box_size = 1

font = PIL.ImageFont.truetype(r"C:\Users\snowman\Documents\labo\qr\QR Font with Letters\PixelMplus-20130602\PixelMplus10-Regular.ttf", box_size * 10)
#font = PIL.ImageFont.truetype(r"C:\Users\snowman\Documents\labo\qr\QR Font with Letters\PixelMplus-20130602\PixelMplus12-Regular.ttf", 120)
#pos = 15


factory = qrcode.image.svg.SvgPathImage

error_levels = [
	qrcode.constants.ERROR_CORRECT_H,
#	qrcode.constants.ERROR_CORRECT_Q,
#	qrcode.constants.ERROR_CORRECT_M,
#	qrcode.constants.ERROR_CORRECT_L,
]

def make_qr(text):
	results = []
	s = set()
	for l in error_levels:
		qr = qrcode.QRCode(error_correction = l, border = 2, version = 2, box_size = 1) #image_factory=qrcode.image.svg.SvgPathImage, 
		qr.add_data(text)
		qr.make(fit = True)
		img = qr.make_image()
		return img
#		results.append((img.width * img.height, img))
		s.add(img.width * img.height)
	results.sort()
	if len(s) != 1:
		print(results)
	return results[0][1]


def convert(s):
	try:
		u = s.decode("CP932")
		if u.isprintable() and len(u) == 1:
			print(f"{c}: {s}    ", end = "\r")
			png = make_qr(u)
#			if u != "鬱":
#				return
			#with open(f"svg/u{ord(u):04x}.png", "wb") as f:
			#	f.write(svg)
			
			draw = PIL.ImageDraw.Draw(png)
			
			l, t, r, b = draw.multiline_textbbox((0, 0), u, font = font)
			
#			print(l, t, r, b, u, "           ")
			
			w = r - l
			h = b - t
			
			draw.rectangle((size - w - 1, size - h - 1, size, size), fill = 0xffffff, outline = None, width = 0)
			draw.text((size - w - l, size - h - t), u, font = font)
			
#			draw.rectangle(((pos * box_size - box_size, pos * box_size - box_size), (pos * box_size + width * box_size, pos * box_size + width * box_size)), fill = 0xffffff, outline = None, width = 0)
#			draw.text((pos * box_size, pos * box_size), u, font = font)
			
			png.save(f"png/u{ord(u):04x}.png")
#			exit(0)
			return True
	except UnicodeDecodeError:
		pass
	except:
		raise
	

c = 0

if True:
	for a in range(256):
		if convert(int.to_bytes(a)):
			c += 1

#print("鬱".encode("CP932"))
#exit()
for a in range(256):
	for b in range(256):
		if convert(int.to_bytes(a) + int.to_bytes(b)):
			c += 1

