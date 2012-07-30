import Image as im
import ImageDraw as imdraw

def drawCircle(img, color, size=None):
    sizex, sizey = img.size
    draw = imdraw.Draw(img)
    if not size:
        draw.ellipse((2,2,sizex-2,sizex-2),outline=color)
        return img
    else:
        blank_im = im.new('RGBA', (size, size), (0, 0, 0, 0)) # Create a blank image
        sizex = int(2*sizex/3)
        sizey = int(2*sizey/3)
        img = img.resize((sizex,sizey))
        blank_im.paste(img, ( size/6+1, size/6+1) )
        draw = imdraw.Draw(blank_im) # Create a draw object
        draw.ellipse((1, 1, size-1, size-1),outline=color) # Draw a circle
        #draw.ellipse((1,1,size,size), outline=color)
        return blank_im

if __name__ == "__main__":
    drawCircle("green").show()
    drawCircle("red").show()
