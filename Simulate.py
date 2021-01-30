import pygame

class SimPixel:
    def __init__(self, game, display, location, size):
        self.game = game
        self.display = display
        self.location = location
        self.size = size

    def SetColor(self, color):
        self.game.draw.circle(self.display, color, self.location, self.size)

class Simulator:
    def __init__(self, grid, pixel_size):
        self.grid = grid
        self.pixel_size = pixel_size
        self.pixels = []

    def Initialize(self):
        pygame.init()
        self.display = pygame.display.set_mode([800, 600])
        self.fpsclock = pygame.time.Clock()

        for i in range(1, self.grid.height + 1):
            row = []
            for j in range(1, self.grid.width + 1):
                pixel = SimPixel(pygame, self.display, (j * 2 * self.pixel_size, i * 2 * self.pixel_size), self.pixel_size)
                row.append(pixel)
            self.pixels.append(row)


    def Run(self, frames, fps):
        self.Initialize()
        while True:
            for frame in frames:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()


                for PixelColorPair in frame:
                    pixel = PixelColorPair[0]
                    color = PixelColorPair[1]
                    x = pixel.grid_location[0]
                    y = pixel.grid_location[1]
                    self.pixels[x][y].SetColor(color)

                self.fpsclock.tick(fps)
                pygame.display.update()