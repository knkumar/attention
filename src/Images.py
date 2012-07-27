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

class Images:
    def __init__(self):
        self.createGabor()
        self.images = {}

    def createGabor(self, size=(50,50)):
        gabor_hor = img.fromarray( gabor(1000,"horizontal",0.7)).convert("RGB")
        self.gabor_horizontal = Enhance.Contrast(gabor_hor).enhance(1.2).resize(size, img.ANTIALIAS) 
        gabor_ver = img.fromarray( gabor(1000,"vertical",0.7)).convert("RGB")
        self.gabor_vertical = Enhance.Contrast(gabor_ver).enhance(1.2).resize(size, img.ANTIALIAS)

        
    def convertPIL(self,im):
        mode = im.mode
        size = im.size
        data = im.tostring()
        return pygame.image.frombuffer(data,size,mode)


    def createDistract(self):
        self.createGabor()
        im_hor = Enhance.Contrast( rectangle(self.gabor_horizontal,"green") ).enhance(1.2)
        im_ver = Enhance.Contrast( rectangle(self.gabor_vertical,"green") ).enhance(1.2)
        self.images["square"]  = [self.convertPIL(im_hor), self.convertPIL(im_ver)]

        self.createGabor((100,100))
        im_hors = Enhance.Contrast( circle(self.gabor_horizontal,"green") ).enhance(1.2).resize((100,100), img.ANTIALIAS)
        im_vers = Enhance.Contrast( circle(self.gabor_vertical,"green") ).enhance(1.2).resize((100,100), img.ANTIALIAS)
        self.images["size"]  = [self.convertPIL(im_hors), self.convertPIL(im_vers)]
        
# overlay the circle with the gabor patch
    def createOverlay(self,colors):
        for color in colors:
            self.createGabor()
            img_hor = Enhance.Contrast( circle(self.gabor_horizontal,color) ).enhance(0.7)
            img_ver = Enhance.Contrast( circle(self.gabor_vertical,color) ).enhance(0.7)
            self.images[color]  = [self.convertPIL(img_hor), self.convertPIL(img_ver)]

    def setup(self):
        self.createOverlay(("red","green"))
        self.createDistract()

