import cv2
from cv2 import VideoCapture

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

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)

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
                color = wheel(color_index)
                color_index += 1
                if color_index > 255:
                    color_index = 0
                indices[ridx][cidx] = color_index
                frame.append([pixel, color])
        frames.append(frame)

    return frames

def load_image(image_path, pixelGrid):
    img = cv2.imread(image_path)
    return resize_image(img, pixelGrid)

def resize_image(img, pixelGrid):    
    x = pixelGrid.width
    y = pixelGrid.height
    resized_image = cv2.resize(img, (x, y))
    return resized_image

def fix_color(img):
    for ridx, row in enumerate(img):
        for cidx, color in enumerate(row):
            color = [color[2], color[1], color[0]]
            img[ridx][cidx] = color
    return img

def DisplayImage(pixelGrid, image_path, frames_duration=30):
    img = load_image(image_path, pixelGrid)

    frame = []
    for ridx, row in enumerate(pixelGrid.pixels):
        for cidx, pixel in enumerate(row):
            color = img[ridx][cidx]
            color = (color[2], color[1], color[0])
            frame.append([pixel, color])
    frames = [frame for x in range(frames_duration)]

    return frames

def PlayVideo(pixelGrid, video_path):
    cam = VideoCapture(video_path)

    frames = []
    s = True
    while s:
        frame = []
        s, img = cam.read()
        if not s:
            break
        img = resize_image(img, pixelGrid)
        for ridx, row in enumerate(pixelGrid.pixels):
            for cidx, pixel in enumerate(row):
                if ridx >= len(img) or cidx >= len(img[0]):
                    continue
                color = img[ridx][cidx]
                color = (color[2], color[1], color[0])
                frame.append([pixel, color])
        frames.append(frame)

    return frames

def Blank(pixelGrid):
    frame = []
    for ridx, row in enumerate(pixelGrid.pixels):
        for cidx, pixel in enumerate(row):
            color = (0, 0, 0)
            frame.append([pixel, color])
    return frame