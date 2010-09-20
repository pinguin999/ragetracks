# _*_ coding: UTF-8 _*_
###################################################################
## this module is the main one, which contains the game class
###################################################################

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import * #Load all PandaModules
import menu3D
import settings
import inputdevice
import player
import splitScreen


# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

class Game(ShowBase):
    '''
    '''
    def __init__(self):
        '''
        '''
        ShowBase.__init__(self)
        base.setFrameRateMeter(True) #Show the Framerate
        base.camNode.setActive(False) #disable default cam 

        # load the settings
        self.settings = settings.Settings()
        self.settings.loadSettings("user/config.ini")

        # initialize the input devices
        self.devices = inputdevice.InputDevices(self.settings.getInputSettings())

        #Initialize needed variables and objects
        self.players = [] #holds the player objects
        self.TRACK_GRIP = 20000.0
        self.FRICTION = 5000
        #self.splitScreen = splitScreen.SplitScreen(0)

        #Initialize Physics (ODE)
        self.world = OdeWorld()
        self.world.setGravity(0, 0, -9.81)
        self.deltaTimeAccumulator = 0.0 #this variable is necessary to track the time for the physics
        self.stepSize = 1.0 / 90.0 # This stepSize makes the simulation run at 60 frames per second

        #Initialize Collisions (ODE)
        self.space = OdeSimpleSpace()
        #Initialize the surface-table, it defines how objects interact with each other
        self.world.initSurfaceTable(1)
        self.world.setSurfaceEntry(0, 0, 1500, 0.0, 0.0, 0.009, 0.00001, 0.0, 0.000002)
        self.space.setAutoCollideWorld(self.world) 
        self.contactgroup = OdeJointGroup()
        self.space.setAutoCollideJointGroup(self.contactgroup)
        
        #set up the collision event
        self.space.setCollisionEvent("ode-collision")
        base.accept("ode-collision", self.onCollision) 

        #Initialize the first player
        self.addPlayer("Tastaturdevice") ##pass the device for the first player (probably the keyboard)

        # try to read the ini-file. If it fails the settings class
        # automatically contains default values
        self.settings = settings.Settings()
        try:
            self.settings.loadSettings("user/config.ini")
        except:
            pass    # so here is nothing to do


        # Add the main menu (though this is only temporary:
        # the menu should me a member-variable, not a local one)
        #m = menu3D.Menu()
        
        #m.addOption("NewGame", self.newGame)
        #m.addOption("AddPlayer", self.addPlayer)

        #Start the Game for testing purpose
        self.newGame()

    # -----------------------------------------------------------------

    def addPlayer(self, device):
        '''
        creates a new player object, initializes it and sorts the cameras on the screen
        '''
        #Create a new player object
        self.players.append(player.Player(len(self.players),self.world, self.space, device, base.makeCamera(base.win,1)))

        #sort the cameras
        #self.splitScreen.reRegion(self.players)

    # -----------------------------------------------------------------

    def removePlayer(self, number):
        '''
        deletes a player object and sorts the cameras on the screem
        '''

        #delete the player
        for player in self.players:
            if player.getNumber() == number:
                self.players.remove(player) ##all objects must be deleted!

        #sort the cameras

    # -----------------------------------------------------------------

    def newGame(self):
        '''
        starts the game or goes to the next menu
        '''

        #Load the Map
        self.map = self.loader.loadModel("data/models/Track01")
        self.map.reparentTo(self.render)
        self.map.setScale(10, 10, 10)
        self.map.setPos(0, 10, -7)

        #add collision with the map
        #OdeTriMeshGeom(self.space, OdeTriMeshData(self.map, True))
        groundGeom = OdePlaneGeom(self.space, Vec4(0, 0, 1, -7))
        groundGeom.setCollideBits(0)
        groundGeom.setCategoryBits(3)

        #Load the Players
        ##probably unnecessary because the players are already initialized at this point

        #Load the Lights
        ambilight = AmbientLight('ambilight')
        ambilight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        render.setLight(render.attachNewNode(ambilight))

        #start the gametask
        taskMgr.add(self.gameTask, "gameTask")



    # -----------------------------------------------------------------
    
    def onCollision(self, entry):
        '''
        Handles Collision-Events
        '''

        geom1 = entry.getGeom1()
        geom2 = entry.getGeom2()
        body1 = entry.getBody1()
        body2 = entry.getBody2()
        
        #Handles the collision-rays from the players
##        for player in self.players:
##            for ray in player.getVehicle().getCollisionRays():
##                if geom1 == ray or geom2 == ray:
##                    force_pos = ray.getPosition()
##                    contact = entry.getContactPoint(0)
##                    force_dir = force_pos - contact
##                    acceleration = (ray.getLength()) - force_dir.length()
##                    stabilizer = (force_dir.length())
##                    print "acc: ", acceleration
##                    print "stab: ", stabilizer
##                    force_dir.normalize()
##                    force1_dir = Vec3(force_dir[0]*acceleration*self.TRACK_GRIP,force_dir[1]*acceleration*self.TRACK_GRIP,force_dir[2]*acceleration*self.TRACK_GRIP)  
##                    #print "force1: ", force_dir
##                    force2_dir = (Vec3(-(force_dir[0]*stabilizer*self.TRACK_GRIP),-(force_dir[1]*stabilizer*self.TRACK_GRIP),-(force_dir[2]*stabilizer*self.TRACK_GRIP))) 
##                    #print "force2: ", force2_dir
##                    player.getVehicle().getPhysicsModel().addForceAtPos(force1_dir, force_pos)
##                    player.getVehicle().getPhysicsModel().addForceAtPos(force2_dir, force_pos)
##                    print "force: ", force1_dir, force2_dir
                    
        for player in self.players:
            for ray in player.getVehicle().getCollisionRays():
                if geom1 == ray or geom2 == ray:
                    force_pos = ray.getPosition()
                    contact = entry.getContactPoint(0)
                    force_dir = force_pos - contact
                    acceleration = ((ray.getLength() / 2)-force_dir.length())
                    acceleration = (acceleration/abs(acceleration))*(acceleration**2)
                    if force_dir.length() < (ray.getLength() / 2):
                        force_dir.normalize()
                        force_dir = Vec3(force_dir[0]*acceleration*self.TRACK_GRIP,force_dir[1]*acceleration*self.TRACK_GRIP,force_dir[2]*acceleration*self.TRACK_GRIP) 
                    else:
                        force_dir.normalize()
                        force_dir = Vec3(force_dir[0]*acceleration*self.TRACK_GRIP,force_dir[1]*acceleration*self.TRACK_GRIP,force_dir[2]*acceleration*self.TRACK_GRIP) 
                    #print force_dir
                    
                    player.getVehicle().getPhysicsModel().addForceAtPos(force_dir, force_pos)
                    #player.getVehicle().getPhysicsModel().setForce(force_dir)
    # -----------------------------------------------------------------
             
    def gameTask(self, task):
        '''
        this task runs once per second if the game is running
        '''
        #calculate the physics
        self.space.autoCollide() # Setup the contact joints

        self.deltaTimeAccumulator += globalClock.getDt()
        while self.deltaTimeAccumulator > self.stepSize:
            # Remove a stepSize from the accumulator until
            # the accumulated time is less than the stepsize
            # Step the simulation
            for player in self.players:                  # refresh player specific things (rays)
                player.doStep()
                #calculate airresistance
                velocity = player.getVehicle().getPhysicsModel().getLinearVel()
                player.getVehicle().getPhysicsModel().addForce(-(Vec3(self.FRICTION * velocity[0],self.FRICTION * velocity[1],self.FRICTION * velocity[2])))      
                #torque = player.getVehicle().getPhysicsModel().getAngularVel()
                #player.getVehicle().getPhysicsModel().addTorque(-(Vec3(self.FRICTION * torque[0],self.FRICTION * torque[1],self.FRICTION * torque[2])))
            self.deltaTimeAccumulator -= self.stepSize
            self.world.quickStep(self.stepSize)
        for player in self.players:                      # set new positions
            player.getVehicle().getModel().setPosQuat(render, player.getVehicle().getPhysicsModel().getPosition(), Quat(player.getVehicle().getPhysicsModel().getQuaternion()))
        self.contactgroup.empty() # Clear the contact joints
        return task.cont
    # -----------------------------------------------------------------

    def menuTask(self, task):
        '''
        this task runs once per second if we are in game menu
        '''
        pass

    # -----------------------------------------------------------------

# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

# this code is only executed if the module is executed and not imported
if __name__ == "__main__":
    game = Game()
    game.run()




