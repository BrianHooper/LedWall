import cv2

def load_image(image_path, pixelGrid):
    img = cv2.imread(image_path)
    return resize_image(img, pixelGrid)

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