#!/usr/bin/python

# get access to pyepl objects & functions
from pyepl.locals import *
import random
from Images import Images
from config import *

class attentionExperiment:

    def __init__(self):
        # create an experiment object
        self.exp = Experiment(resolution=(1024,768))
        self.video = VideoTrack("video")
        self.pc = PresentationClock()
        self.video.clear("black")
        self.stim = Text("", color="black")
        self.keyboard = KeyTrack("keyboard")
        self.bc = ButtonChooser(Key("a"), Key("l"), Key("SPACE"), Key("q"))
        self.images = Images()
        self.images.setup()
        self.log = LogTrack("session")

    def __del__(self):
        pass

    def userSpace(self):
        ts, b, rt = self.stim.present(clk=self.pc,duration=0,bc=self.bc)
        if b==Key("SPACE"):
            return True
        elif b==Key("q"):
            return "quit"
        else:
            return self.userSpace()

    def userInput(self, orientation=None ):
        ts, b, rt = self.stim.present(clk=self.pc,duration=0,bc=self.bc)
        response_time = rt[0]-ts[0]
        self.video.clear("black")
        if b==Key(orientation):
            self.video.showCentered(Text("Correct.\nPress space for next"))    
            result = True #correct
        else:
            self.video.showCentered(Text("Incorrect.\nPress space for next"))    
            #self.play_buzzer()
            result = False        
        return result, response_time

    def baitAndSwitch(self, target, dist_1, dist_2):
        random.seed()
        position = range(12)
        if target:
            target.append( random.sample(position,1)[0])
            position.remove(target[1])
        if dist_1:
            dist_1.append( random.sample(position,1)[0] )
            position.remove(dist_1[1])
        if dist_2:
            dist_2.append( random.sample(position,1)[0] )
        return target, dist_1, dist_2

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
    def drawCanvas(self, obj):
        target, dist1, dist2 = obj["target"],obj["dist1"],obj["dist2"]
        # reset the display to black
        self.video.clear("black")
        self.video.showCentered(Text("+"))
        flashStimulus(Text("+",size=0.01), 1500, clk=self.pc)
        self.video.clear("black")
        self.video.showCentered(Text("+"))            
        pos = [[0.8,0.5], [0.76,0.65] , [0.65,0.76] , [0.5,0.8] , [0.35,0.76] , [0.24,0.65] ,
               [0.2,0.5], [0.24,0.35] , [0.35,0.24] , [0.5,0.2] , [0.65,0.24] , [0.76,0.35]]
   
        gabor_switch = [0]*6+[1]*6 #determine whether to keep it horizontal or vertical for the 12 cases
        random.shuffle(gabor_switch)
        ret = {"red":None, "square":None, "size":None}
        target, dist1, dist2 = self.baitAndSwitch(target, dist1, dist2)
        print target, dist1, dist2
        
        for i,location in enumerate(pos):
            if target[0] and i == target[1]:
                self.video.showProportional( Image(self.images.images[target[0]][gabor_switch[i]]) , location[0], location[1])
                ret[target[0]] = ("a" if gabor_switch[i] else "l", i)
            elif dist1 and i == dist1[1]:
                self.video.showProportional(Image( self.images.images[dist1[0]][gabor_switch[i]]) , location[0], location[1])
                ret[dist1[0]] = ("a" if gabor_switch[i] else "l", i)
            elif dist2 and i == dist2[1]:
                self.video.showProportional(Image( self.images.images[dist2[0]][gabor_switch[i]]) , location[0], location[1])
                ret[dist2[0]] = ("a" if gabor_switch[i] else "l", i)
            else:
                self.video.showProportional(Image( self.images.images["green"][gabor_switch[i]]) , location[0], location[1])

        self.video.updateScreen()       
        return ret

    def instruct_text(self, target):
        if target == "red":
            return "red circle"
        elif target == "square":
            return "green_square"
        elif target == "size":
            return "large green circle"

    def create_log(self, trials):
        self.log.logMessage("Trial# \t result \t response_time \t target \t square \t red \t size \t #Dist \t presence")
        for k,v in trials.items():
            trial = "%s"%k
            result = "correct" if v[0] else "Incorrect"
            response_time = "%s"%v[1]
            target = "%s"%v[2]
            pos = ""
            count=0
            tFlag = False
            for key,value in v[3].items():
                if value:
                    pos = pos+"%s=%s|%s"%(key,value[0],value[1])+","
                    count=count+1
                    if key == target:
                        tFlag = True
                else:
                    pos = pos+","
            if tFlag:
                self.log.logMessage("%s,%s,%s,%s,%s%s,%s"%(trial,result,response_time,target,pos,count-1,tFlag))
            else:
                self.log.logMessage("%s,%s,%s,%s,%s%s,%s"%(trial,result,response_time,target,pos,count,tFlag))

    def run(self,distOrder, target, distractors):
        self.log.logMessage("Session Start")
        instruct1 = open("instructions.txt","r").read()    
        instruct(instruct1%self.instruct_text(target),size=0.03, clk=self.pc)
        #self.pc.delay(10000)
        trials = {}
        paramsDict = {0: {"target":[target], "dist1":None, "dist2":None},
                      1: {"target":[target], "dist1":[distractors[0]], "dist2":None},
                      2: {"target":[target], "dist1":[distractors[1]], "dist2":None},
                      3: {"target":[target], "dist1":[distractors[0]], "dist2":[distractors[0]]},
                      4: {"target":[None], "dist1":None, "dist2":None},
                      5: {"target":[None], "dist1":[distractors[0]], "dist2":None},
                      6: {"target":[None], "dist1":[distractors[1]], "dist2":None},
                      7: {"target":[None], "dist1":[distractors[0]], "dist2":[distractors[1]]}
                      }
        for i in range(len(distOrder)):
            #params are populated from paramDict
            retOrient = self.drawCanvas( paramsDict[distOrder[i]] )
            if EXP == 'gabor':
                result,response_time = self.userInput(retOrient[target][0].lower())
            else:
                if distOrder[i] >= 4:
                    result,response_time = self.userInput('a'.lower())
                else:
                    result,response_time = self.userInput('l'.lower())
            trials[i] = [result, response_time, target, retOrient]
            ret = self.userSpace()
            if ret == "quit":
                break
        self.create_log(trials)
        self.log.logMessage("Session end")
        
def doRun(distOrder):
    attexp = attentionExperiment()
    attexp.run(distOrder, TARGET, ITEMS)

if __name__ == "__main__":
    # the order is 10 control then interspersed 20 single distractor and 30 double distractor
    if EXP == 'gabor':
        dist = [0]*230 + [1]*250 + [2]*250 + [3]*750
        random.seed()
        random.shuffle(dist)
        distOrder = [0]*20 + dist
    else:
        dist = [0]*115 + [1]*125 + [2]*125 + [3]*375 + [4]*115 + [5]*125 + [6]*125 + [7]*375
        random.seed()
        random.shuffle(dist)
        distStart = dist[0]*10 + dist[4]*10
        random.shuffle(distStart)
        distOrder = distStart + dist
    doRun(distOrder)
