#!/usr/bin/python

from drawCircle import drawCircle as circle
from gabor import make_gabor as gabor
# get access to pyepl objects & functions
from pyepl.locals import *
import random
import Image as img
import pygame
import ImageEnhance as Enhance
import ImageChops as ic
import ImageDraw
from drawRectangle import drawRectagle as rectangle

gabor_hor = img.fromarray( gabor(1000,"horizontal",0.7)).convert("RGB")
gabor_horizontal = Enhance.Contrast(gabor_hor).enhance(5.4).resize((35,35), img.ANTIALIAS) 
gabor_ver = img.fromarray( gabor(1000,"vertical",0.7)).convert("RGB")
gabor_vertical = Enhance.Contrast(gabor_ver).enhance(5.4).resize((35,35), img.ANTIALIAS)

def createDistract(colors):
    distractors = {}
    im_hor = Enhance.Contrast( rectangle(gabor_horizontal,"green") ).enhance(0.8)
    draw_hor = ImageDraw.Draw(im_hor)
    im_ver = Enhance.Contrast( rectangle(gabor_vertical,"green") ).enhance(0.8)
    distractors["square"]  = [convertPIL(im_hor), convertPIL(im_ver)]
    im_hor = Enhance.Contrast( circle(gabor_horizontal,color) ).enhance(0.8).resize((45,45), img.ANTIALIAS)
    draw_hor = ImageDraw.Draw(im_hor)
    im_ver = Enhance.Contrast( circle(gabor_vertical,color) ).enhance(0.8).resize((45,45), img.ANTIALIAS)
    distractors["size"]  = [convertPIL(im_hor), convertPIL(im_ver)]
    return distractors
        
# overlay the circle with the gabor patch
def createOverlay(colors):
    images = {}
    for color in colors:
        im_hor = Enhance.Contrast( circle(gabor_horizontal,color) ).enhance(0.8)
        draw_hor = ImageDraw.Draw(im_hor)
        im_ver = Enhance.Contrast( circle(gabor_vertical,color) ).enhance(0.8)
        images[color]  = [convertPIL(im_hor), convertPIL(im_ver)]
    return images
        
def convertPIL(im):
    mode = im.mode
    size = im.size
    data = im.tostring()
    return pygame.image.frombuffer(data,size,mode)

def drawCircles(images, video, mypc, posRed):
    # reset the display to black
    video.clear("black")
    pos = [[0.35,0.45], [0.35,0.55] , [0.41,0.4] , [0.41,0.6] , [0.47,0.35] , [0.47,0.65] ,
           [0.54,0.65], [0.54,0.35] , [0.61,0.6] , [0.61,0.4] , [0.67,0.55] , [0.67,0.45]]
    gabor_switch = [0]*6+[1]*6
    random.shuffle(gabor_switch)
    print images
    for i,item in enumerate(pos):
        if i == posRed:
            video.showProportional(Image(images["red"][gabor_switch[i]]) , item[0], item[1])
            orientation=gabor_switch[i]
        else:
            video.showProportional(Image(images["green"][gabor_switch[i]]) , item[0], item[1])

    video.updateScreen()
    
    #mypc.delay(1000) 
    # make sure we've finished displaying
    #mypc.wait() 
    
    #0-h, 1-v
    return orientation


def userInput(stim,bc,patchOrientation):
    ts, b, rt = stim.present(clk=mypc,duration=0,bc=bc)
    response_time = rt[0]-ts[0]
    if b==Key(patchOrientation):
        result = "Correct!"
    else:
        result = "Incorrect!"
    flashStimulus(Text(result), clk=mypc)
    
    return result,response_time

def experiment(num_runs):
    # create an experiment object
    exp = Experiment()
    # create a VideoTrack object for interfacing with monitor
    video = VideoTrack("video")
    # create a PresentationClock
    mypc = PresentationClock()
    images = createOverlay(("red","green"))
    sequence = random.sample(range(12),num_runs)
    
    stim = Text("", color="black")
    keyboard = KeyTrack("keyboard")
    bc = ButtonChooser(Key("H"), Key("V"))
    #orientation='H'
    for pos in sequence:
        patchOrientation=drawCircles(images,video,mypc, pos)
        result,response_time=userInput(stim,bc,patchOrientation)
        
        
    
if __name__ == "__main__":
    experiment(10)
