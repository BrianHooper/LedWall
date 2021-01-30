import board
import neopixel
PIXEL_PIN = board.D18
ORDER = neopixel.GRB
total_pixels = 50
pixels = neopixel.NeoPixel(PIXEL_PIN, total_pixels, brightness=0.8, auto_write=False, pixel_order=ORDER)
pixels.fill((0,0,0))
pixels.show()
