#import qrcode
#import qrcode.image.svg
import os
import subprocess

#factory = qrcode.image.svg.SvgPathImage

#error_levels = [
#	qrcode.constants.ERROR_CORRECT_H,
#	qrcode.constants.ERROR_CORRECT_Q,
#	qrcode.constants.ERROR_CORRECT_M,
#	qrcode.constants.ERROR_CORRECT_L,
#]

def make_qr(text):
	results = []
	s = set()
	child = subprocess.Popen(["qrtool-v0.11.8-x86_64-pc-windows-msvc/qrtool.exe", "encode", "-v", "3", "-t", "svg", "--variant", "micro", text], shell = False, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	stdout, stderr = child.communicate()
	if child.returncode != 0:
		print(stderr)
		raise "error"
	img = stdout
	return img

def convert(s):
	try:
		u = s.decode("CP932")
		if u.isprintable() and len(u) == 1:
			print(f"{c}: {s}    ", end = "\r")
			svg = make_qr(u)
			with open(f"svg/u{ord(u):04x}.svg", "wb") as f:
				f.write(svg)
			return True
	except UnicodeDecodeError:
		pass
	except:
		raise
	

c = 0
for a in range(256):
	if convert(int.to_bytes(a, 1, "big")):
		c += 1

for a in range(256):
	for b in range(256):
		if convert(int.to_bytes(a, 1, "big") + int.to_bytes(b, 1, "big")):
			c += 1

