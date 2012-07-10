import Image as im
import ImageDraw as imdraw

def drawCircle(img, color):
    sizex, sizey = img.size
    draw = imdraw.Draw(img)
    draw.ellipse((2,2,sizex-2,sizex-2),outline=color)
    return img

if __name__ == "__main__":
    drawCircle("green").show()
    drawCircle("red").show()
