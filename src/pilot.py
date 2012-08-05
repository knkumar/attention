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
#import wave
#import pyaudio
import sys


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
        self.log = LogTrack("session")

    def __del__(self):
        pass

    """def play_buzzer(self):
        # open stream
        chunk = 1024
        wf = wave.open("buzzer.wav",'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format =
                                  p.get_format_from_width(wf.getsampwidth()),
                                  channels = wf.getnchannels(),
                                  rate = wf.getframerate(),
                                  output = True)

        data = wf.readframes(chunk)
        while data != '':
            stream.write(data)
            data = wf.readframes(chunk)
        stream.close()
        p.terminate()
    """

    def userSpace(self):
        ts, b, rt = self.stim.present(clk=self.pc,duration=0,bc=self.bc)
        response_time = rt[0]-ts[0]
        if b==Key("SPACE"):
            return True
        elif b==key("q"):
            return "quit"
        return False

    def userInput(self, orientation=None ):
        ts, b, rt = self.stim.present(clk=self.pc,duration=0,bc=self.bc)
        response_time = rt[0]-ts[0]
        if b==Key(orientation):
            self.video.showCentered(Text("Correct.\nPress space for next"))    
            result = True #correct
        else:
            self.video.showCentered(Text("Incorrect.\nPress space for next"))    
            #self.play_buzzer()
            result = False
        
        return result, response_time



    def baitAndSwitch(self, target, dist_1, dist_2):
        if not dist_1 and not dist_2:
            return target, dist_1, dist_2
        if dist_1:
            dist1 = dist_1[1]
            if target[1] == dist1:
                dist_1[1] = dist1 + random.sample(6,1)
        if dist_2:
            dist2 = dist_2[1]
            if target[1] == dist2:
                dist_2[1] = dist2 + random.sample(6,1)
            if dist1 == dist2:
                dist_2[1] = dist2 + random.sample(6,1) 
        if target[1] == dist1[1] or target[1] == dist2[1] or dist1[1] == dist2[1]:
            return baitAndSwitch(target, dist_1, dist_2)

        return target, dist1, dist2

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
    def drawCanvas(self, target, dist1=None, dist2=None):
        # reset the display to black
        self.video.clear("black")
        self.video.showCentered(Text("+",size=0.2))
        flashStimulus(Text("+",size=0.2), 1000, clk=self.pc)
        self.video.clear("black")
        pos = [[0.8,0.5], [0.76,0.65] , [0.65,0.76] , [0.5,0.8] , [0.35,0.76] , [0.24,0.65] ,
               [0.2,0.5], [0.24,0.35] , [0.35,0.24] , [0.5,0.2] , [0.65,0.24] , [0.76,0.35]]
   
        gabor_switch = [0]*6+[1]*6 #determine whether to keep it horizontal or vertical for the 12 cases
        random.shuffle(gabor_switch)
        ret = {}

        target, dist1, dist2 = self.baitAndSwitch(target, dist1, dist2)

        for i,location in enumerate(pos):
            if i == target[1]:
                self.video.showProportional( Image(self.images.images[target[0]][gabor_switch[i]]) , location[0], location[1])
                ret["red"] = ("h" if gabor_switch[i] else "v", i)
            elif dist1 and i == dist1[1]:
                self.video.showProportional(Image( self.images.images[dist1[0]][gabor_switch[i]]) , location[0], location[1])
                ret["square"] = ("h" if gabor_switch[i] else "v", i)
            elif dist2 and i == dist2[1]:
                self.video.showProportional(Image( self.images.images[dist2[0]][gabor_switch[i]]) , location[0], location[1])
                ret["size"] = ("h" if gabor_switch[i] else "v", i)
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

    def instruct_text(self, target):
        if target == "red":
            return "red circle"
        elif target == "square":
            return "green_square"
        elif target == "size":
            return "large green circle"

    def create_log(self, trials):
        self.log.logMessage("Trial# \t result \t response_time \t target"+ 
                            "\t red orient|red position \t size orient|size position \t square orient|square position")
        for k,v in trials.items():
            trial = "%s"%k
            result = "correct" if v[0] else "Incorrect"
            response_time = "%s"%v[1]
            target = "%s"%v[2]
            pos = ""
            for key,value in v[3].items():
                pos = pos+"%s=%s|%s"%(key,value[0],value[1])+","
            self.log.logMessage("%s,%s,%s,%s,%s"%(trial,result,response_time,target,pos))

    def run(self,distOrder, target, distractors):

        self.log.logMessage("Session Start")
        instruct1 = open("instructions.txt","r").read()    
        instruct(instruct1%self.instruct_text(target),size=0.03, clk=self.pc)
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

            result,response_time = self.userInput(retOrient[target][0].lower())
            trials[i] = [result, response_time, target, retOrient]
            
            ret = self.userSpace()
            if ret == "quit":
                break
        self.create_log(trials)
        self.log.logMessage("Session end")
        
    
if __name__ == "__main__":
    # the order is 10 control then interspersed 20 single distractor and 30 double distractor
    dist = [1]*300 + [2]*300 + [3]*500
    random.seed()
    random.shuffle(dist)
    target = "red"
    distractors = ("square","size")
    distOrder = [0]*20 + dist
    print distOrder
    attexp = attentionExperiment(distOrder)
    attexp.run(distOrder, target, distractors)
