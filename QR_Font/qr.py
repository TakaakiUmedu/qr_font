import qrcode
import qrcode.image.svg

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
		qr = qrcode.QRCode(error_correction = l, image_factory=qrcode.image.svg.SvgPathImage, border = 2)
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
			svg = make_qr(u)
			with open(f"svg/u{ord(u):04x}.svg", "wb") as f:
				f.write(svg.to_string())
			return True
	except UnicodeDecodeError:
		pass
	except:
		raise
	

c = 0
for a in range(256):
	if convert(int.to_bytes(a)):
		c += 1

for a in range(256):
	for b in range(256):
		if convert(int.to_bytes(a) + int.to_bytes(b)):
			c += 1

