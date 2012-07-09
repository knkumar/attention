import Image as im
import ImageDraw as imdraw

def drawCircle(color, size=100):
    img = im.new("RGBA",(size,size))
    draw = imdraw.Draw(img)
    draw.ellipse((0,0,size-1,size-1),outline=color)
    return img

if __name__ == "__main__":
    drawCircle("green").show()
    drawCircle("red").show()
