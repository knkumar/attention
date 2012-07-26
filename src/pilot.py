#!/usr/bin/python

# get access to pyepl objects & functions
from pyepl.locals import *
import random
import Image as img
import pygame
import ImageEnhance as Enhance
import ImageChops as ic
import ImageDraw
from drawRectangle import drawRectangle as rectangle
from drawCircle import drawCircle as circle
from gabor import make_gabor as gabor
from Images import Images


def userSpace(stim, bc, orientation, mypc, ):
    ts, b, rt = stim.present(clk=mypc,duration=0,bc=bc)
    response_time = rt[0]-ts[0]
    if b==Key("SPACE"):
        return True
    return False

def drawCanvas(images, video, mypc, posRed, numDist, dist1=None, dist2=None):
    # reset the display to black
    video.clear("black")

    """pos = [[0.35,0.45], [0.35,0.55] , [0.41,0.4] , [0.41,0.6] , [0.47,0.35] , [0.47,0.65] ,
           [0.54,0.65], [0.54,0.35] , [0.61,0.6] , [0.61,0.4] , [0.67,0.55] , [0.67,0.45]]"""


    pos = [[0.8,0.5], [0.76,0.65] , [0.65,0.76] , [0.5,0.8] , [0.35,0.76] , [0.24,0.65] ,
          [0.2,0.5], [0.24,0.35] , [0.35,0.24] , [0.5,0.2] , [0.65,0.24] , [0.76,0.35]]
   
    gabor_switch = [0]*6+[1]*6
    random.shuffle(gabor_switch)

    ret = []
    for i,item in enumerate(pos):
        if i == posRed:
            video.showProportional(Image( images.images["red"][gabor_switch[i]]) , item[0], item[1])
            ret.append("h" if gabor_switch[i] else "v")
            
        elif dist1 and i == dist1:
            video.showProportional(Image( images.distractors["square"][gabor_switch[i]]) , item[0], item[1])
            ret.append("h" if gabor_switch[i] else "v")
            
        elif dist2 and i == dist2:
            video.showProportional(Image( images.distractors["size"][gabor_switch[i]]) , item[0], item[1])
            ret.append("h" if gabor_switch[i] else "v")
            
        else:
            video.showProportional(Image( images.images["green"][gabor_switch[i]]) , item[0], item[1])

    video.updateScreen()
    
    #mypc.delay(1000) 
    # make sure we've finished displaying
    #mypc.wait() 
    
    #0-h, 1-v
    
    return ret


def userInput(stim, bc, mypc, orientation=None ):
    ts, b, rt = stim.present(clk=mypc,duration=0,bc=bc)
    response_time = rt[0]-ts[0]
    if b==Key(orientation):
        result = "Correct.\nPress space for next"
    else:
        result = "Incorrect.\nPress space for next"
    flashStimulus(Text(result), clk=mypc)
    
    return result,response_time

def experiment(distOrder):
    # create an experiment object
    exp = Experiment(resolution=(1024,768))
    # create a VideoTrack object for interfacing with monitor
    video = VideoTrack("video")
    # create a PresentationClock
    mypc = PresentationClock()
    video.clear("black")
    stim = Text("", color="black")
    keyboard = KeyTrack("keyboard")
    bc = ButtonChooser(Key("h"), Key("v"), Key("SPACE"))


    instruct1 = open("instructions.txt","r").read()
    instruct(instruct1,size=0.03, clk=mypc)

    mypc.delay(1000)
    images = Images()
    images.setup()
    random.seed()
    sequence = [val%12 for val in  random.sample(range(len(distOrder)), len(distOrder)) ]
    random.seed()
    dist1_sequence = [val%12 for val in  random.sample(range(len(distOrder)), len(distOrder)) ]
    random.seed()
    dist2_sequence = [val%12 for val in  random.sample(range(len(distOrder)), len(distOrder)) ]
    random.seed()
    random.shuffle(sequence)
    random.seed()
    random.shuffle(dist1_sequence)
    random.seed()
    random.shuffle(dist2_sequence)
    
    
    for i in range(len(distOrder)):

        if distOrder[i] == 0:
            retOrient = drawCanvas(images,video,mypc, sequence[i], distOrder[i])
        if distOrder[i] == 1:
            retOrient = drawCanvas(images,video,mypc, sequence[i], distOrder[i], dist1_sequence[i])
        if distOrder[i] == 2:
            retOrient = drawCanvas(images,video,mypc, sequence[i], distOrder[i],None, dist1_sequence[i])
        if distOrder[i] == 3:
            retOrient = drawCanvas(images,video,mypc, sequence[i], distOrder[i],dist1_sequence[i], dist2_sequence[i])

        result,response_time = userInput(stim, bc, mypc, retOrient[0].lower())
        # busy wait not sure if i need this
        while not userSpace(stim, bc, None, mypc):
            continue
        
    
if __name__ == "__main__":
    # the order is 10 control then interspersed 20 single distractor and 30 double distractor
    dist = [1]*1 + [2]*1 + [3]*3
    random.seed()
    random.shuffle(dist)
    distOrder = [0]*1 + dist
    print distOrder
    experiment(distOrder)
