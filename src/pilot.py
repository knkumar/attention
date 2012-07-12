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
from drawRectangle import drawRectangle as rectangle


class Images:
    def __init__(self):
    self.gabor_hor = img.fromarray( gabor(1000,"horizontal",0.7)).convert("RGB")
    self.fgabor_horizontal = Enhance.Contrast(gabor_hor).enhance(5.4).resize((35,35), img.ANTIALIAS) 
    self.gabor_ver = img.fromarray( gabor(1000,"vertical",0.7)).convert("RGB")
    self.gabor_vertical = Enhance.Contrast(gabor_ver).enhance(5.4).resize((35,35), img.ANTIALIAS)

    def convertPIL(self,im):
        mode = im.mode
        size = im.size
        data = im.tostring()
        return pygame.image.frombuffer(data,size,mode)


    def createDistract(self):
        self.distractors = {}
        
        im_hor = Enhance.Contrast( rectangle(self.gabor_horizontal,"green") ).enhance(0.8)
        draw_hor = ImageDraw.Draw(im_hor)
        im_ver = Enhance.Contrast( rectangle(self.gabor_vertical,"green") ).enhance(0.8)
        self.distractors["square"]  = [self.convertPIL(im_hor), self.convertPIL(im_ver)]
        
        im_hor = Enhance.Contrast( circle(self.gabor_horizontal,size), "green").enhance(0.8).resize((45,45), img.ANTIALIAS)
        draw_hor = ImageDraw.Draw(im_hor)
        im_ver = Enhance.Contrast( circle(self.gabor_vertical,size) , "green").enhance(0.8).resize((45,45), img.ANTIALIAS)
        self.distractors["size"]  = [self.convertPIL(im_hor), self.convertPIL(im_ver)]
        
# overlay the circle with the gabor patch
    def createOverlay(self,colors):
        self.images = {}
        for color in colors:
            im_hor = Enhance.Contrast( circle(self.gabor_horizontal,color) ).enhance(0.8)
            draw_hor = ImageDraw.Draw(im_hor)
            im_ver = Enhance.Contrast( circle(self.gabor_vertical,color) ).enhance(0.8)
            self.images[color]  = [self.convertPIL(im_hor), self.convertPIL(im_ver)]

    def setup(self):
        self.createDistract()
        self.createOverlay(("red","green"))

        

def drawCircles(images, video, mypc, posRed, numDist, dist1, dist2):
    # reset the display to black
    video.clear("black")
    pos = [[0.35,0.45], [0.35,0.55] , [0.41,0.4] , [0.41,0.6] , [0.47,0.35] , [0.47,0.65] ,
           [0.54,0.65], [0.54,0.35] , [0.61,0.6] , [0.61,0.4] , [0.67,0.55] , [0.67,0.45]]

    gabor_switch = [0]*6+[1]*6

    random.shuffle(gabor_switch)

    for i,item in enumerate(pos):
        if i == posRed:
            video.showProportional(Image(images["red"][gabor_switch[i]]) , item[0], item[1])
            orientation = "h" if gabor_switch[i] else "v"
        if i == dist1:
            video.showProportional(Image(images.distractor["square"][gabor_switch[i]]) , item[0], item[1])
            d1Orient = "h" if gabor_switch[i] else "v"
        if i == dist2:
            video.showProportional(Image(images.distractor["size"][gabor_switch[i]]) , item[0], item[1])
            d2Orient = "h" if gabor_switch[i] else "v"

        else:
            video.showProportional(Image(images["green"][gabor_switch[i]]) , item[0], item[1])

    video.updateScreen()
    
    #mypc.delay(1000) 
    # make sure we've finished displaying
    #mypc.wait() 
    
    #0-h, 1-v
    return orientation, d2Orient, d2Orient


def userInput(stim, bc, orientation, mypc, ):
    ts, b, rt = stim.present(clk=mypc,duration=0,bc=bc)
    response_time = rt[0]-ts[0]
    if b==Key(orientation):
        result = "Correct!"
    else:
        result = "Incorrect!"
    flashStimulus(Text(result), clk=mypc)
    
    return result,response_time

def experiment(distOrder):
    # create an experiment object
    exp = Experiment()
    # create a VideoTrack object for interfacing with monitor
    video = VideoTrack("video")
    # create a PresentationClock
    mypc = PresentationClock()

    images = Images()
    images.setup()

    sequence = random.shuffle([1:12] * len(distOrder)/12)
    dist1_sequence = random.shuffle(sequence)
    dist2_sequence = random.shuffle(sequence)
    
    stim = Text("", color="black")
    keyboard = KeyTrack("keyboard")
    bc = ButtonChooser(Key("h"), Key("v"))
    #orientation='H'

    for i in range(len(distOrder)):

        if distOrder[i] == 0:
            tOrient,d1orient,d2orient = drawCircles(images,video,mypc, sequence[i], distOrder[i])
        if distOrder[i] == 1:
            tOrient,d1orient,d2orient = drawCircles(images,video,mypc, sequence[i], distOrder[i], dist1_sequence[i])
        if distOrder[i] == 2:
            tOrient,d1orient, d2Orient = drawCircles(images,video,mypc, sequence[i], distOrder[i],None, dist1_sequence[i])
        if distOrder[i] == 3:
            tOrient,d1orient,d2orient = drawCircles(images,video,mypc, sequence[i], distOrder[i],dist1_sequence[i], dist2_sequence[i])

        result,response_time = userInput(stim,bc,tOrient.lower(),mypc)
        
        
    
if __name__ == "__main__":
    # the order is 10 control then interspersed 20 single distractor and 30 double distractor
    distOrder = [0]*10 + random.shuffle([1]*10 + [2]*10+ [3]*30)
    experiment(distOrder)
