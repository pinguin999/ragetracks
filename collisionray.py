# _*_ coding: UTF-8 _*_
###################################################################
## this module represents a collision ray
###################################################################

from pandac.PandaModules import * #Load all PandaModules
from wiregeom import WireGeom

class CollisionRay(object):
    '''
    '''
    def __init__(self, position, direction, ode_space, length = 1.0, parent = None ,debug = False, collide_bits = 2, category_bits = 0 ):
        '''
        '''
        self.ode_space = ode_space
        self.parent = parent #the collision_model
        self.position = position #Vec3()
        self.direction = direction #Vec3()
        self.ray = OdeRayGeom(self.ode_space, length)
        self.debug = debug
        
        self.ray.setCollideBits(collide_bits)
        self.ray.setCategoryBits(category_bits)       
        
        if self.debug:
            self.drawray = WireGeom().generate ('ray', length=length)
            self.drawray.reparentTo(render)
            self.drawray.setPos (self.position[0] + self.parent.getPosition()[0], 
                            self.position[1]  + self.parent.getPosition()[1], 
                            self.position[2] + self.parent.getPosition()[2])
            
            relative_vec = self.parent.getRotation().xform(self.direction)
            self.drawray.setHpr (Quat(0.0, relative_vec[2], relative_vec[1], relative_vec[0],).getHpr())
        
    # ---------------------------------------------------------
    
    def doStep(self):
        '''
        Calculates the new position of the ray, relative to the collision-model, 
        needs to be executed everytime ode.quickStep gets executed
        '''
        
        ##the calculation of the position seems to be broken
        relative_vec = self.parent.getRotation().xform(self.direction)
        self.ray.set(self.parent.getPosition() + self.position, 
                    relative_vec)
        
        if self.debug:
            self.drawray.setPos (self.position[0] + self.parent.getPosition()[0], 
                            self.position[1]  + self.parent.getPosition()[1], 
                            self.position[2] + self.parent.getPosition()[2])
            
            self.drawray.setHpr (Quat(0.0, relative_vec[2], relative_vec[1], relative_vec[0],).getHpr())

        
    # ---------------------------------------------------------
    
    def getRay(self):
        return self.ray