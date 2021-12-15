# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 19:47:50 2017
@author: lfoul
"""
import copy
import OpenGL.GL as gl

class Section:
    # Constructor
    def __init__(self, parameters = {}) :  
        # Parameters
        # position: position of the wall 
        # width: width of the wall - mandatory
        # height: height of the wall - mandatory
        # thickness: thickness of the wall
        # color: color of the wall        

        # Sets the parameters
        self.parameters = parameters
        
        # Sets the default parameters
        if 'position' not in self.parameters:
            self.parameters['position'] = [0, 0, 0]        
        if 'width' not in self.parameters:
            raise Exception('Parameter "width" required.')   
        if 'height' not in self.parameters:
            raise Exception('Parameter "height" required.')   
        if 'orientation' not in self.parameters:
            self.parameters['orientation'] = 0              
        if 'thickness' not in self.parameters:
            self.parameters['thickness'] = 0.2    
        if 'color' not in self.parameters:
            self.parameters['color'] = [0.5, 0.5, 0.5]       
        if 'edges' not in self.parameters:
            self.parameters['edges'] = False             
            
        # Objects list
        self.objects = []

        # Generates the wall from parameters
        self.generate()   
        
    # Getter
    def getParameter(self, parameterKey):
        return self.parameters[parameterKey]
    
    # Setter
    def setParameter(self, parameterKey, parameterValue):
        self.parameters[parameterKey] = parameterValue
        return self     

    # Defines the vertices and faces 
    def generate(self):
        self.vertices = [ 
                [0, 0, 0 ], 
                [0, 0, self.parameters['height']], 
                [self.parameters['width'], 0, self.parameters['height']],
                [self.parameters['width'], 0, 0],      
                [0,self.parameters["thickness"], 0 ], 
                [0, self.parameters["thickness"], self.parameters['height']], 
                [self.parameters['width'], self.parameters["thickness"], self.parameters['height']],
                [self.parameters['width'], self.parameters["thickness"], 0]
                ]
        self.faces = [
                [0, 3, 2, 1],
                [4,7,6,5],
                [0,4,5,1],
                [3,7,6,2],
                [0,4,7,3],
                [1,5,6,2]
                ]   
  # Checks if the opening can be created for the object x
    def canCreateOpening(self, x):
       return (self.parameters['height']>=x.getParameter('height') + x.getParameter('position')[2] - self.parameters['position'][2]
               and x.getParameter('position')[2]>= self.parameters['position'][2]
               and self.parameters['width']>= x.getParameter('width') + x.getParameter('position')[0] - self.parameters['position'][0]
               and x.getParameter('position')[0] >= self.parameters['position'][0]) 
        
    # Creates the new sections for the object x
    def createNewSections(self, x):
        if self.canCreateOpening(x):
            section = [Section(copy.copy(self.parameters))
                .setParameter('width', x.getParameter('position')[0] - self.getParameter('position')[0]),
                Section(copy.copy(self.parameters))
                .setParameter('height', self.getParameter('height') - x.getParameter('height') - x.getParameter('position')[2] + self.getParameter('position')[2])
                .setParameter('width', x.getParameter('width'))
                .setParameter('position',[x.getParameter('position')[0], self.getParameter('position')[1],x.getParameter('position')[2] + x.getParameter('height')
                ]),
                Section(copy.copy(self.parameters))
                .setParameter('height', x.getParameter('position')[2] -self.getParameter('position')[2])
                .setParameter('width', x.getParameter('width'))
                .setParameter('position', [x.getParameter('position')[0], self.getParameter('position')[1], self.getParameter('position')[2]
                ]),
                Section(copy.copy(self.parameters))
                .setParameter('width', self.getParameter('width') -x.getParameter('width') -x.getParameter('position')[0] +self.getParameter('position')[0])
                .setParameter('position', [x.getParameter('position')[0] + x.getParameter('width'),self.getParameter('position')[1], self.getParameter('position')[2]
                ])
            ]    
            res=[]
            for i in sections:
                print(i.getParameter('width'))
                print(i.getParameter('height'))
                print(i.getParameter('position'))
                if (i.getParameter('width')!= 0.0 and i.getParameter('height')!=0.0):
                    i.generate()
                    res.append(i)
                return res
                
                
            
    # Draws the edges
    def drawEdges(self):
        # A compléter en remplaçant pass par votre code
        gl.glPushMatrix()
        gl.glTranslate(self.parameters['position'][0],self.parameters['position'][1],self.parameters['position'][2])
        gl.glRotate(self.parameters['orientation'],0,0,1)
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE) # on trace les faces : GL_FILL
        for i in self.faces :
            gl.glBegin(gl.GL_QUADS) # TracÃ© dâ€™un quadrilatÃ¨re
            gl.glColor3fv([1,0,0]) # Couleur gris moyen
            for j in i:
                gl.glVertex3fv(self.vertices[j])
            gl.glEnd()
        gl.glPopMatrix()
            
                    
    # Draws the faces
    def draw(self):
        
        if self.parameters['edges']:
            self.drawEdges()

        gl.glPushMatrix()
        gl.glTranslate(self.parameters['position'][0],self.parameters['position'][1],self.parameters['position'][2])
        gl.glRotate(self.parameters['orientation'],0,0,1)
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL) # on trace les faces : GL_FILL
        for i in self.faces :
            gl.glBegin(gl.GL_QUADS) # TracÃ© dâ€™un quadrilatÃ¨re
            gl.glColor3fv(self.parameters['color']) # Couleur gris moyen
            for j in i:
                gl.glVertex3fv(self.vertices[j])
            gl.glEnd()
        gl.glPopMatrix()
