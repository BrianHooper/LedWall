import cv2
import pickle

def LoadImage(image_path, pixelGrid):
    img = cv2.imread(image_path)
    return ResizeImage(img, pixelGrid)

def ResizeImage(img, pixelGrid):    
    x = pixelGrid.width
    y = pixelGrid.height
    resized_image = cv2.resize(img, (x, y))
    return resized_image

def GetImageFrame(img, pixelGrid):
    frame = []
    for ridx, row in enumerate(pixelGrid.pixels):
        for cidx, pixel in enumerate(row):
            color = img[ridx][cidx]
            color = (color[2], color[1], color[0])
            frame.append([pixel, color])
    return frame

def Wheel(pos):
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

def WriteFrames(filename, frames):
    with open(filename, 'wb') as outfile:
        pickle.dump(frames, outfile)

def ReadFrames(filename):
    with open(filename, 'rb') as infile:
        return pickle.load(infile)