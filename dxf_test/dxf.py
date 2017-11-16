#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 14:48:01 2017

@author: levy
"""

import dxfgrabber

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
 
def drawFunc():
    glClear(GL_COLOR_BUFFER_BIT)
    #glRotatef(1, 0, 1, 0)
    glutWireTeapot(0.5)
    glFlush()
 
glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
glutInitWindowSize(400, 400)
glutCreateWindow("First")
glutDisplayFunc(drawFunc)
#glutIdleFunc(drawFunc)
glutMainLoop()
#dxf = dxfgrabber.readfile("test.dxf")

#for e in dxf.entities:
#    print(e.dxftype,e.layer)
#    if e.dxftype == 'LINE':
#        print (e.start,e.end)
#    if e.dxftype == 'CIRCLE':
#        print (e.center,e.radius)
#    if e.dxftype == 'ARC':
#        print (e.center,e.radius,e.start_angle,e.end_angle)
#    if e.dxftype == 'POLYLINE':
#        print (e.points)
#for b in dxf.blocks:
#    print(b.name)