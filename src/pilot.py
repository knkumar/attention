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


class attentionExperiment:

    def __init__(self, distOrder):
        # create an experiment object
        self.exp = Experiment(resolution=(1024,768))
        self.video = VideoTrack("video")
        self.pc = PresentationClock()
        self.video.clear("black")
        self.stim = Text("", color="black")
        self.keyboard = KeyTrack("keyboard")
        self.bc = ButtonChooser(Key("h"), Key("v"), Key("SPACE"))
        self.images = Images()
        self.images.setup()
        self.generate_sequences(12, len(distOrder))


    def userSpace(self):
        ts, b, rt = self.stim.present(clk=self.pc,duration=0,bc=self.bc)
        response_time = rt[0]-ts[0]
        if b==Key("SPACE"):
            return True
        return False

    def userInput(self, orientation=None ):
        ts, b, rt = self.stim.present(clk=self.pc,duration=0,bc=self.bc)
        response_time = rt[0]-ts[0]
        if b==Key(orientation):
            self.video.showCentered(Text("Correct.\nPress space for next"))    
            result = True #correct
        else:
            self.video.showCentered(Text("Incorrect.\nPress space for next"))    
            result = False
        
        return result, response_time


    """
    Draw the canvas for the trial
    @input: 
    images dictionary - contains the images, 
    video - the video track to write, 
    pc - the presentation clock
    posRed - the position of the red circle
    numDist - the number of distractors
    dist1 - the first distractor position, if no distractor then None
    dist2 - the second distractor position, if no distractor then None
    @output: 
    A tuple containing the gabor patch orientation for the target and distractor
    """
    def drawCanvas(self, posRed, dist1=None, dist2=None):
        # reset the display to black
        self.video.clear("black")
        
        pos = [[0.8,0.5], [0.76,0.65] , [0.65,0.76] , [0.5,0.8] , [0.35,0.76] , [0.24,0.65] ,
               [0.2,0.5], [0.24,0.35] , [0.35,0.24] , [0.5,0.2] , [0.65,0.24] , [0.76,0.35]]
   
        gabor_switch = [0]*6+[1]*6 #determine whether to keep it horizontal or vertical for the 12 cases
        random.shuffle(gabor_switch)
        ret = {}

        for i,location in enumerate(pos):
            if i == posRed[1]:
                self.video.showProportional( Image(self.images.images[posRed[0]][gabor_switch[i]]) , location[0], location[1])
                ret["red"] = "h" if gabor_switch[i] else "v"
            elif dist1 and i == dist1[1]:
                self.video.showProportional(Image( self.images.images[dist1[0]][gabor_switch[i]]) , location[0], location[1])
                ret["square"] = "h" if gabor_switch[i] else "v"
            elif dist2 and i == dist2[1]:
                self.video.showProportional(Image( self.images.images[dist2[0]][gabor_switch[i]]) , location[0], location[1])
                ret["size"] = "h" if gabor_switch[i] else "v"
            else:
                self.video.showProportional(Image( self.images.images["green"][gabor_switch[i]]) , location[0], location[1])

        self.video.updateScreen()       
        return ret

    def randomize(self, sequence):
        random.seed()
        random.shuffle(sequence)
        return sequence


    def generate_sequences(self,num, distLength):
        random.seed()
        sequence = [val%num for val in  random.sample(range(distLength), distLength) ]
        dist1_sequence = [val%num for val in  random.sample(range(distLength), distLength) ]
        dist2_sequence = [val%num for val in  random.sample(range(distLength), distLength) ]
        self.sequence = self.randomize(sequence)
        self.dist1_sequence = self.randomize(dist1_sequence)
        self.dist2_sequence = self.randomize(dist2_sequence)

    def run(self,distOrder, target, distractors):
 

        instruct1 = open("instructions.txt","r").read()
        instruct(instruct1,size=0.03, clk=self.pc)

        #self.pc.delay(10000)
        trials = {}

        for i in range(len(distOrder)):

            if distOrder[i] == 0:
                #target only
                retOrient = self.drawCanvas((target,self.sequence[i]))
            if distOrder[i] == 1:
                #target + first distractor
                retOrient = self.drawCanvas((target,self.sequence[i]), (distractors[0],self.dist1_sequence[i]) )
            if distOrder[i] == 2:
                #target + second distractor
                retOrient = self.drawCanvas((target,self.sequence[i]), None, (distractors[1],self.dist1_sequence[i]) )
            if distOrder[i] == 3:
                #target + both distractor
                retOrient = self.drawCanvas((target,self.sequence[i]), (distractors[0],self.dist1_sequence[i]), (distractors[1],self.dist2_sequence[i]) )

            result,response_time = self.userInput(retOrient["red"].lower())
            trials[i] = [result, response_time]
            self.userSpace()
    
        
    
if __name__ == "__main__":
    # the order is 10 control then interspersed 20 single distractor and 30 double distractor
    dist = [1]*1 + [2]*1 + [3]*3
    random.seed()
    random.shuffle(dist)
    target = "red"
    distractors = ("square","size")
    distOrder = [0]*1 + dist
    print distOrder
    attexp = attentionExperiment(distOrder)
    attexp.run(distOrder, target, distractors)
