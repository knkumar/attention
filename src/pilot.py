#!/usr/bin/python

from drawCircle import drawCircle as circle
from gabor import make_gabor as gabor
# get access to pyepl objects & functions
from pyepl.locals import *
import random
import Image as img
import pygame

gabor_horizontal = img.fromarray(gabor(1000,"horizontal"))
gabor_vertical = img.fromarray(gabor(1000,"vertical"))
gabor_horizontal.show()
gabor_vertical.show()

# overlay the circle with the gabor patch
def createOverlay(colors):
    images = {}
    for color in colors:
        im = circle(color)
        layer_hor = img.new('RGBA', im.size, (0,0,0,0))
        layer_hor.paste(gabor_horizontal, im.size)
        layer_ver = img.new('RGBA', im.size, (0,0,0,0))
        layer_ver.paste(gabor_vertical, im.size)
        images[color]  = [convertPIL(img.composite(layer_hor,im,layer_hor)), convertPIL(img.composite(layer_ver, im, layer_ver))]
    return images
        
def convertPIL(im):
    mode = im.mode
    size = im.size
    data = im.tostring()
    return pygame.image.frombuffer(data,size,mode)

def drawCircles(images, video, mypc, posRed):
    # reset the display to black
    video.clear("black")
    pos = [[0.0,0.5], [0.2,0.2] , [0.2,0.8] , [0.4,0.4] , [0.4,0.6] , [0.6,0.8] , [0.6,0.2] , [0.8,0.6] , [0.8,0.4] , [1.0,0.5] , [0.5,0], [0.5,1.0]]
    gabor_switch = [0]*6+[1]*6
    random.shuffle(gabor_switch)
    print images
    for i,item in enumerate(pos):
        if i == posRed:
            video.showProportional(Image(images["red"][gabor_switch[i]]) , item[0], item[1])
        else:
            video.showProportional(Image(images["green"][gabor_switch[i]]) , item[0], item[1])

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
    sequence = random.sample(range(12),num_runs)
    for pos in sequence:
        drawCircles(images,video,mypc, pos)
    
if __name__ == "__main__":
    experiment(10)
