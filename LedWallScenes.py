import cv2
from cv2 import VideoCapture
from Helpers import *
import random
from DefinedColors import *

BLACK = (0, 0, 0)

def ColorWall(pixelGrid):
    frames = []
    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
        (0, 255, 255),
        (255, 255, 255),
    ]
    for color in colors:
        for ii in range(3):
            frame = []
            for row in pixelGrid.pixels:
                for pixel in row:
                    frame.append([pixel, color])
            frames.append(frame)

    return frames

def ColorWheel(pixelGrid):
    indices = [[0 for i in range(pixelGrid.width)] for j in range(pixelGrid.height)]
    count = 0
    for ridx, row in enumerate(indices):
        for cidx, pixel in enumerate(row):
            indices[ridx][cidx] = count
            count += 1
            if count > 255:
                count = 0

    frames = []
    for i in range(0, 255):
        frame = []
        for ridx, row in enumerate(pixelGrid.pixels):
            for cidx, pixel in enumerate(row):
                color_index = indices[ridx][cidx]
                color = Wheel(color_insdex)
                color_index += 1
                if color_index > 255:
                    color_index = 0
                indices[ridx][cidx] = color_index
                frame.append([pixel, color])
        frames.append(frame)
    return frames


def DisplayImage(pixelGrid, image_path, frames_duration=30):
    img = LoadImage(image_path, pixelGrid)
    frame = GetImageFrame(img, pixelGrid)
    frames = [frame for x in range(frames_duration)]
    return frames

def PlayVideo(pixelGrid, video_path):
    camera = VideoCapture(video_path)
    frames = []
    s = True
    while s:
        s, img = camera.read()
        if s:
            img = ResizeImage(img, pixelGrid)
            frame = GetImageFrame(img, pixelGrid)
        frames.append(frame)
    return frames

def Blank(pixelGrid):
    frame = []
    for ridx, row in enumerate(pixelGrid.pixels):
        for cidx, pixel in enumerate(row):
            color = (0, 0, 0)
            frame.append([pixel, color])
    return frame

class FallingPixel:
    def __init__(self, ridx, cidx, color_palette, color=None):
        self.ridx = ridx
        self.cidx = cidx
        if color is None:
            self.color = color_palette[random.randrange(len(color_palette))]
        else:
            self.color = color

    def Reduce(self):
        red = self.color[0] - 50
        green = self.color[1] - 50
        blue = self.color[2] - 50
        if red < 0:
            red = 0
        if blue < 0:
            blue = 0
        if green < 0:
            green = 0
        self.color = (red, green, blue)
        if red == 0 and green == 0 and blue == 0:
            return False
        else:
            return True


def Waterfall(pixelGrid, color_palette=PASTEL):
    frames = []

    possible_cidxs = list(range(0, pixelGrid.width))
    falling_pixels = [
        FallingPixel(0, possible_cidxs.pop(random.randrange(len(possible_cidxs))), color_palette)
    ]
    total_fallen = 1
    while len(falling_pixels) > 0 and total_fallen < 50:
        chance = random.randrange(5)
        if chance == 3:
            total_fallen += 1
            falling_pixels.append(FallingPixel(0, possible_cidxs.pop(random.randrange(len(possible_cidxs))), color_palette))

        frame = Blank(pixelGrid)
        for falling_pixel in falling_pixels:
            for pxidx, pixel in enumerate(frame):
                grid_location = pixel[0].grid_location
                pridx = grid_location[0]
                pcidx = grid_location[1]

                if falling_pixel.ridx == pridx and falling_pixel.cidx == pcidx:
                    frame[pxidx][1] = falling_pixel.color
        extra_pixels = []
        for falling_pixel in falling_pixels:
            if falling_pixel.ridx == 0:
                extra_pixel = FallingPixel(0, falling_pixel.cidx, color_palette, falling_pixel.color)
                if extra_pixel.Reduce():                    
                    extra_pixels.append(extra_pixel)
            if falling_pixel.ridx == 10:
                possible_cidxs.append(falling_pixel.cidx)
            falling_pixel.ridx += 1

        falling_pixels += extra_pixels
        falling_pixels = [x for x in falling_pixels if falling_pixel.ridx < pixelGrid.height]
        frames += [frame for x in range(3)]

    return frames

class FadeInPixel:
    def __init__(self, color_palette):
        self.color = (0, 0, 0)
        self.goal_color = PASTEL[random.randrange(len(PASTEL))]
        self.started = False
        self.finished = False

    def Increase(self):
        if self.finished:
            return False
        red = self.color[0] + 3
        green = self.color[1] + 3
        blue = self.color[2] + 3

        goal_red = self.goal_color[0]
        goal_green = self.goal_color[1]
        goal_blue = self.goal_color[2]
        if red > goal_red:
            red = goal_red
        if blue > goal_blue:
            blue = goal_blue
        if green > goal_green:
            green = goal_green
        self.color = (red, green, blue)
        if red == goal_red and green == goal_green and blue == goal_blue:
            self.finished = True
            return True
        else:
            return False

def RandomFadeIn(pixelGrid, color_palette=PASTEL):
    frames = []

    frame = []
    total_pixels = pixelGrid.width * pixelGrid.height
    finished_pixels = 0
    random_threshold = total_pixels // 10
    for ridx, row in enumerate(pixelGrid.pixels):
        for cidx, pixel in enumerate(row):
            frame.append([pixel, (0, 0, 0), FadeInPixel(color_palette)])
    frames.append(frame)
    while finished_pixels < total_pixels:
        frame  = []
        chance_count = 0
        for previous_pixel in frames[-1]:
                fadeinpixel = previous_pixel[2]
                if fadeinpixel.finished:
                    frame.append(previous_pixel)
                elif fadeinpixel.started:
                    if fadeinpixel.Increase():
                        finished_pixels += 1
                    frame.append([previous_pixel[0], fadeinpixel.color, previous_pixel[2]])
                else:
                    chance = int(100 * float(total_pixels - finished_pixels) / float(total_pixels))
                    if chance == 0:
                        chance = 1
                    choice = random.randrange(chance)
                    if choice == 0:
                        fadeinpixel.started = True
                    frame.append([previous_pixel[0], fadeinpixel.color, fadeinpixel])
        frames += [frame for x in range(3)]
    return frames