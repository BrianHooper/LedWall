# num_blocks_wide = 5
# num_blocks_tall = 4
# block_pixels_wide = 7
# block_pixels_tall = 7

import Simulate
import LedWallScenes as Scenes

class Pixel:
    def __init__(self, strand_location, grid_location, neopixels):
        self.strand_location = strand_location
        self.grid_location = grid_location
        self.neopixels = neopixels

    def SetColor(self, color):
        self.neopixels[self.strand_location] = color

class Grid:
    def __init__(self, num_blocks_wide, num_blocks_tall, block_width, block_height):
        self.neopixels = None
        self.num_blocks_wide = num_blocks_wide
        self.num_blocks_tall = num_blocks_tall
        self.block_width = block_width
        self.block_height = block_height
        self.width = num_blocks_wide * block_pixels_wide
        self.height = num_blocks_tall * block_pixels_tall
        self.Initalize()

    def Initalize(self):
        total_rows_high = num_blocks_tall * block_pixels_tall
        total_cols_wide = num_blocks_wide * block_pixels_wide

        self.pixels = [[-1 for x in range(0, self.width)] for y in range(0, self.height)]

        count = 0
        for ridx in range(0, self.num_blocks_tall):
            for cidx in range(0, self.num_blocks_wide):
                for bridx in range(self.block_height * ridx, self.block_height * (ridx + 1)):
                    for bcidx in range(self.block_width * cidx, self.block_width * (cidx + 1)):
                        self.pixels[bridx][bcidx] = Pixel(count, (bridx,bcidx), self.neopixels)
                        count += 1

    def PrintGrid(self):
        for ridx, row in enumerate(self.pixels):
            for cidx, pixel in enumerate(row):
                print(f"({ridx},{cidx}): {pixel.strand_location}", end="\t")
            print("")

    def Display(self, frames, fps=30):
        milliseconds_per_frame = 1000 / 30
        for frame in frames:
            for PixelColorPair in frame:
                pixel = PixelColorPair[0]
                color = PixelColorPair[1]
                pixels.SetColor(color)

if __name__ == "__main__":
    num_blocks_wide = 5
    num_blocks_tall = 4
    block_pixels_wide = 7
    block_pixels_tall = 7

    pixelGrid = Grid(num_blocks_wide, num_blocks_tall, block_pixels_wide, block_pixels_tall)
    simulator = Simulate.Simulator(pixelGrid, 2)

    wall = Scenes.ColorWall(pixelGrid)
    wheel = Scenes.ColorWheel(pixelGrid)
    # image = Scenes.DisplayImage(pixelGrid, "")
    # video = Scenes.PlayVideo(pixelGrid, "")
    simulator.Run(wheel, 30)