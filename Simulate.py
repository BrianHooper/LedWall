import pygame
import pygame.freetype
from cv2 import VideoCapture
from Helpers import *

class SimPixel:
    def __init__(self, game, display, location, size):
        self.game = game
        self.display = display
        self.location = location
        self.size = size

    def SetColor(self, color):
        self.game.draw.circle(self.display, color, self.location, self.size)

class Simulator:
    def __init__(self, pixelGrid):
        self.pixelGrid = pixelGrid
        self.pixel_size = int(pixelGrid.config["simulator"]["pixel_diameter"])
        self.pixels = []

    def Initialize(self):
        pygame.init()
        pygame.font.init()

        self.window_width = int(self.pixelGrid.config["simulator"]["window_width"])
        self.window_height = int(self.pixelGrid.config["simulator"]["window_height"])
        self.display = pygame.display.set_mode([self.window_width, self.window_height])
        self.fpsclock = pygame.time.Clock()
        self.font = pygame.freetype.SysFont(None, 24)

        for i in range(1, self.pixelGrid.height + 1):
            row = []
            for j in range(1, self.pixelGrid.width + 1):
                pixel = SimPixel(pygame, self.display, (j * 2 * self.pixel_size, i * 2 * self.pixel_size), self.pixel_size)
                row.append(pixel)
            self.pixels.append(row)

    def Close(self):
        for row in self.pixelGrid.pixels:
            for pixel in row:
                pixel.SetColor((0, 0, 0))
        pygame.display.quit()
        pygame.quit()


    def Run(self, frames, stop_flag):
        self.Initialize()

        while True:

            for fidx, frame in enumerate(frames):
                if stop_flag.value == True:
                    self.Close()
                    return
                self.display.fill(pygame.Color('black'))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                self.font.render_to(self.display, (self.window_width - 100, self.window_height - 50), f"{fidx} of {len(frames)}", (255, 255, 255))

                for PixelColorPair in frame:
                    pixel = PixelColorPair[0]
                    color = PixelColorPair[1]
                    x = pixel.grid_location[0]
                    y = pixel.grid_location[1]
                    self.pixels[x][y].SetColor(color)

                self.fpsclock.tick(30)
                pygame.display.update()

    def Camera(self, stop_flag):
        self.Initialize()
        camera_index = int(self.pixelGrid.config["camera"]["webcam_index"])
        camera = VideoCapture(camera_index)
        while True:
            if stop_flag.value == True:
                self.Close()
                return

            s, img = camera.read()
            if s:
                img = ResizeImage(img, self.pixelGrid)
                frame = GetImageFrame(img, self.pixelGrid)
                for PixelColorPair in frame:
                    pixel = PixelColorPair[0]
                    color = PixelColorPair[1]
                    x = pixel.grid_location[0]
                    y = pixel.grid_location[1]
                    self.pixels[x][y].SetColor(color)

            self.fpsclock.tick(30)
            pygame.display.update()