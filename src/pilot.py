#!/usr/bin/python

from drawCircle import drawCircle as circle
from gabor import make_gabor as gabor
# get access to pyepl objects & functions
from pyepl.locals import *
import random
import Image

gabor_horizontal = Image.fromarray(make_gabor(1000,"horizontal"))
gabor_vertical = Image.fromarray(make_gabor(1000,"vertical"))

# overlay the circle with the gabor patch
def createOverlay(colors):
    images = {}
    for color in colors:
        im = circle(color)
        layer_hor = Image.new('RGBA', im.size, (0,0,0,0))
        layer_hor.paste(gabor_horizontal, im.size)
        layer_ver = Image.new('RGBA', im.size, (0,0,0,0))
        layer_ver.paste(gabor_vertical, im.size)
        images[color]  = [Image.composite(layer_hor,im,layer_hor), Image.composite(layer_ver, im, layer_ver)]
    return images
        
def drawCircles(images):
    # reset the display to black
    video.clear("black")
    pos = ( (0,.5) , (.2,.2) , (.2,.8) , (.4,.4) (.4,.6) , (.6,.8) , (.6,.2) , (.8,.6) , (.8,.4) , (1.0,.5) )
    gabor_switch = random.sample(range(2),len(pos))
    for i,item in enumerate(pos):
        if i == posRed:
            video.showProportional(images["red"][gabor_switch[i]], item[0], item[1])
        else:
            video.showProportional(images["green"][gabor_swtich[i]], item[0], item[1])

    video.updateScreen()
    mypc.delay(3000) 
    # make sure we've finished displaying
    mypc.wait() 

def experiment(num_runs):
    # create an experiment object
    exp = Experiment()
    # create a VideoTrack object for interfacing with monitor
    video = VideoTrack("video")
    # create a PresentationClock
    mypc = PresentationClock()
    images = createOverlay(("red","green"))
    sequence = random.sample(range(10),num_runs)
    for pos in sequence:
        drawCircles(images,video,mypc)
    
if __name__ == "__main__":
    experiment(10)
