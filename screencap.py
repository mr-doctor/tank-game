import ctypes
import struct
import numpy as np

# enums used by gdi32 and user32
SM_CXSCREEN = 0
SM_CYSCREEN = 1
SRCCOPY = 0xCC0020
DIB_RGB_COLORS = 0x00

sceen_width = ctypes.windll.user32.GetSystemMetrics(SM_CXSCREEN)
screen_height = ctypes.windll.user32.GetSystemMetrics(SM_CYSCREEN)

# objects used for all screen grabbing
# use EnumDisplayMonitors for non-primary monitor
srcdc = ctypes.windll.user32.GetWindowDC(0)
memdc = ctypes.windll.gdi32.CreateCompatibleDC(srcdc)

# access to python's PyMemoryView_FromMemory
PyBUF_READ = 0x100
buf_from_mem = ctypes.pythonapi.PyMemoryView_FromMemory
buf_from_mem.restype = ctypes.py_object
buf_from_mem.argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.c_int)


def get_screen(left, top, width, height):
	cwidth = int(np.ceil(width / 4) * 4)
	bmp = ctypes.windll.gdi32.CreateCompatibleBitmap(srcdc, cwidth, height)
	ctypes.windll.gdi32.SelectObject(memdc, bmp)
	c_bmp_header = ctypes.create_string_buffer(struct.pack('LHHHH', struct.calcsize('LHHHH'), cwidth, height, 1, 24))

	ctypes.windll.gdi32.BitBlt(memdc, 0, 0, cwidth, height, srcdc, left, top, SRCCOPY)

	c_bits = ctypes.create_string_buffer(height * cwidth * 3)
	got_bits = ctypes.windll.gdi32.GetDIBits(memdc, bmp, 0, height, c_bits, c_bmp_header, DIB_RGB_COLORS)

	# copy out data using PyMemoryView_FromMemory then copying the data
	buf = buf_from_mem(c_bits, height * cwidth * 3, PyBUF_READ)
	img = np.ndarray((height, cwidth, 3), np.uint8, buf, order='C').copy()
	img = np.flipud(img)

	ctypes.windll.gdi32.DeleteObject(bmp)

	return img


if __name__ == '__main__':
	screen = get_screen(0, 0, 1920, 1080)
	np.savez('./screen', screen)