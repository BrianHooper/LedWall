import Simulate
import LedWallScenes as Scenes
from Helpers import *
import threading
import time
import platform
import configparser

IS_PI = "arm" in platform.machine().lower()

def GetController(num_pixels):
    print(f"Loading config for platform {platform.machine()}")
    if IS_PI:
        import board
        import neopixel
        PIXEL_PIN = board.D18
        ORDER = neopixel.GRB
        controller = neopixel.NeoPixel(PIXEL_PIN, num_pixels, brightness=0.8, auto_write=False, pixel_order=ORDER)
        return controller
    else:
        return None


class Pixel:
    def __init__(self, strand_location, grid_location, controller):
        self.strand_location = strand_location
        self.grid_location = grid_location
        self.controller = controller

    def SetColor(self, color):
        if self.controller is not None:
            self.controller[self.strand_location] = color

class Grid:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.num_blocks_wide = int(self.config["grid"]["num_blocks_wide"])
        self.num_blocks_tall = int(self.config["grid"]["num_blocks_tall"])
        self.block_width = int(self.config["grid"]["block_pixels_wide"])
        self.block_height = int(self.config["grid"]["block_pixels_tall"])
        self.width = self.num_blocks_wide * self.block_width
        self.height = self.num_blocks_tall * self.block_height
        self.Initalize()

    def Initalize(self):
        total_pixels = self.width * self.height
        self.controller = GetController(total_pixels)
        self.pixels = [[-1 for x in range(0, self.width)] for y in range(0, self.height)]

        count = 0
        for ridx in range(0, self.num_blocks_tall):
            for cidx in range(0, self.num_blocks_wide):
                for bridx in range(self.block_height * ridx, self.block_height * (ridx + 1)):
                    for bcidx in range(self.block_width * cidx, self.block_width * (cidx + 1)):
                        self.pixels[bridx][bcidx] = Pixel(count, (bridx,bcidx), self.controller)
                        count += 1

    def PrintGrid(self):
        for ridx, row in enumerate(self.pixels):
            for cidx, pixel in enumerate(row):
                print(f"({ridx},{cidx}): {pixel.strand_location}", end="\t")
            print("")

    def Display(self, frames, fps=30, endless=False):
        self.controller.show()
        milliseconds_per_frame = float(fps) / 1000.0
        while True:
            for frame in frames:
                for PixelColorPair in frame:
                    pixel = PixelColorPair[0]
                    color = PixelColorPair[1]
                    pixel.SetColor(color)
                self.controller.show()
                time.sleep(milliseconds_per_frame)
            if not endless:
                break

    def Camera(self):
        self.Initialize()
        camera_index = int(self.config["camera"]["webcam_index"])
        camera = VideoCapture(camera_index)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            s, img = camera.read()
            if s:
                img = ResizeImage(img, self.pixels)
                frame = GetImageFrame(img, self.pixels)
                for PixelColorPair in frame:
                    pixel = PixelColorPair[0]
                    color = PixelColorPair[1]
                    pixel.SetColor(color)


if __name__ == "__main__":
    pixelGrid = Grid()
    simulator = Simulate.Simulator(pixelGrid)

    # wall = Scenes.ColorWall(pixelGrid)
    # wheel = Scenes.ColorWheel(pixelGrid)
    # image = Scenes.DisplayImage(pixelGrid, "")
    # video = Scenes.PlayVideo(pixelGrid, "")
    # scene = Scenes.RandomFadeIn(pixelGrid)

    # if IS_PI:
    #     pixelGrid.Display(wheel, 30, True)
    # else:
    #     simulator.Run(scene)

    # worker_thread = threading.Thread(target=simulator.Camera, args=(False,))
    # worker_thread.start()