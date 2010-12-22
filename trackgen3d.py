# -*- coding: utf-8 -*-
##############################################################
## this module contains a class for generating racing tracks
##############################################################

##          TODO            
## - Conecting the open part under the Street
##

from panda3d.core import * 
from trackgen import Track
from pandac.PandaModules import GeomVertexFormat, Geom, GeomVertexWriter, GeomTristrips, GeomNode
import xml.dom.minidom as dom
from xml.dom.minidom import Document
from direct.directnotify.DirectNotify import DirectNotify

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

class RoadShape(object):
    '''
    describes the shape of the road e.g. |__/\__|
    '''
    def __init__(self, *args, **kwds):
        '''
        '''
        self.points = []
        self.name = "street part"
        self.author = "Rage Tracks Team"
        self.mirrored = True
        
        for arg in args:
            if type(arg) == Vec2:
                self.points.append(arg)
        
        if "name" in kwds.keys():
            self.name = str(kwds["name"])
        
        if "author" in kwds.keys():
            self.author = str(kwds["author"])
        
        if "mirrored" in kwds.keys():
            self.mirrored = bool(kwds["mirrored"])
        
        # if the points should be mirrored, we'll do it
        if self.mirrored:
            self.mirrorPoints()
        self._notify = DirectNotify().newCategory("TrackGen3D")
        self._notify.info("New StreetData-Object created: %s" %(self))
    # -------------------------------------------------------------------------------------

    def addPoint(self, x, y):
        '''
        adds a point to the road
        notice: the points are connected in the same order, they're added
        @param x: (float) x-coordinate
        @param y: (float) y-coordinate
        '''
        self.points.append(Vec2(x,y))
    
    # -------------------------------------------------------------------------------------

    def readFile(self, filename, border=False):
        '''
        reads the shape out of a file
        @param filename: (str) the filename
        '''
        self.points = []
        # open file
        xmlfile = dom.parse(filename)
        
        # create the root element
        xml = xmlfile.getElementsByTagName("xml").item(0)
        self.name = xml.getAttribute("name") # read name and author out of root
        self.author = xml.getAttribute("author")
        
        # check if the points should be mirrored
        mirrored = xml.getAttribute("mirrored")
        if mirrored == "False":
            self.mirrored = False
        else:
            self.mirrored = True
        
        # read out the points
        points = xml.getElementsByTagName("points")
        points = points[0].childNodes

        pointcount = points.length

        for i in xrange(pointcount):
            point = points.item(i)
            if point.nodeType == point.ELEMENT_NODE:
                x = float(point.getAttribute("x"))
                y = float(point.getAttribute("y"))
                self.points.append(Vec2(x, y))
    
        # if the points should be mirrored, we'll do it
        if self.mirrored:
            self.mirrorPoints()

    
    # -------------------------------------------------------------------------------------
    
    def mirrorPoints(self):
        '''
        mirrors the point at y axis
        '''
        pointlist = []
        for point in self.points:
            if point.getX() <= 0:
                pointlist.append(point)
                if point.getX() != 0:
                    pointlist.insert(0,Vec2(point.getX()*-1,point.getY()))
        self.points = pointlist
    
    # -------------------------------------------------------------------------------------
    
    def demirrorPoints(self):
        '''
        mirrors the point at y axis
        '''
        pointlist = []
        for point in self.points:
            if point.getX() <= 0:
                pointlist.append(point)
        self.points = pointlist
    
    # -------------------------------------------------------------------------------------
    
    def writeFile(self, filename):
        '''
        writes the shape into a file
        @param filename: (str) the filename
        '''
        # create the document
        doc = Document()

        # chreate the root element
        xml = doc.createElement("xml")
        
        # the name, author and information if the points are mirrored
        xml.setAttribute("mirrored", str(self.mirrored))
        xml.setAttribute("name", self.name)
        xml.setAttribute("author", self.author)
        doc.appendChild(xml)

        # insert the points
        points = doc.createElement("points")
        
        if self.mirrored:
            self.demirrorPoints()
        
        for point in self.points:
            p = doc.createElement("point")
            p.setAttribute("x", str(point.getX()))
            p.setAttribute("y", str(point.getY()))
            points.appendChild(p)

        xml.appendChild(points)

        # write it into a file
        f = file(filename, "w")
        doc.writexml(f, addindent="   ", newl="\n")
        f.close()
        
        if self.mirrored:
            self.mirrorPoints()
    
        
    # -------------------------------------------------------------------------------------
    
    def __str__(self):
            '''
            returns a string representation e.g. for printing
            '''
            return str(self.points)
        
    # -------------------------------------------------------------------------------------
    
    def __getitem__(self, index):
        '''
        this method is used for indexing like street_data[1]
        '''
        return self.points[index]
    
    # -------------------------------------------------------------------------------------
    
    def __len__(self):
        '''
        returns the count of the points
        '''
        return len(self.points)
    
    # -------------------------------------------------------------------------------------
    
    def getLength(self):
        '''
        returns the count of the points
        '''
        return len(self.points)
    
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

class StreetData(RoadShape):
    '''
    '''
    def __init__(self, *args, **kwds):
        RoadShape.__init__(self, *args, **kwds)
        self.border = RoadShape()
    
    # -------------------------------------------------------------------------------------
        
    def readFile(self, filename, border=False):
        '''
        reads the shape out of a file
        @param filename: (str) the filename
        '''
        self.points = []
        # open file
        xmlfile = dom.parse(filename)
        
        # create the root element
        xml = xmlfile.getElementsByTagName("xml").item(0)
        self.name = xml.getAttribute("name") # read name and author out of root
        self.author = xml.getAttribute("author")
        
        # check if the points should be mirrored
        mirrored = xml.getAttribute("mirrored")
        if mirrored == "False":
            self.mirrored = False
        else:
            self.mirrored = True
        
        # read out the points
        points = xml.getElementsByTagName("points")
        points = points[0].childNodes

        pointcount = points.length

        for i in xrange(pointcount):
            point = points.item(i)
            if point.nodeType == point.ELEMENT_NODE:
                x = float(point.getAttribute("x"))
                y = float(point.getAttribute("y"))
                self.points.append(Vec2(x, y))
    
        # if the points should be mirrored, we'll do it
        if self.mirrored:
            self.mirrorPoints()
                
        # read out the border
        border = xml.getElementsByTagName("border")
        border = border[0].childNodes

        bordercount = border.length

        for i in xrange(bordercount):
            point = border.item(i)
            if point.nodeType == point.ELEMENT_NODE:
                x = float(point.getAttribute("x"))
                y = float(point.getAttribute("y"))
                self.border.points.append(Vec2(x, y))

    
    # -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

class Track3d(object):
    '''
    Generate the 3d Mesh out of the StreetData and the 2dTrack
    '''
    def __init__(self, res, x, y, z = 200, player_count=1):
        '''
        '''
        self._notify = DirectNotify().newCategory("TrackGen3D")
        self._notify.info("New Track3D-Object created: %s" %(self))
        #street_data = (Vec2(4.0,4.0), Vec2(10.0,10.0), Vec2(10.0,0.0), Vec2(4.0,0.0), Vec2(0.0,-1.0))
        #street_data = StreetData(Vec2(15.0,1.0), Vec2(15.0,-5.0), Vec2(0.0,-5.0), mirrored=True) #, Vec2(15.0,0.0)
        street_data = StreetData()
        street_data.readFile("data/road/road01.xml")
        
        self.vdata = GeomVertexData('street', GeomVertexFormat.getV3n3c4t2(), Geom.UHStatic) 
        self.bordervdata = GeomVertexData('border', GeomVertexFormat.getV3n3c4t2(), Geom.UHStatic) 
        #self.vdata = GeomVertexData('name', GeomVertexFormat.getV3c4t2(), Geom.UHStatic) 
        
        self.vertex = GeomVertexWriter(self.vdata, 'vertex')
        self.normal = GeomVertexWriter(self.vdata, 'normal')
        self.color = GeomVertexWriter(self.vdata, 'color')
        self.texcoord = GeomVertexWriter(self.vdata, 'texcoord')
        self.prim = GeomTriangles(Geom.UHStatic)
        
        
        m = Track(x, y, z)
        m.generateTestTrack(player_count)
##        m.generateTrack(player_count)
        #m.genStart(5)
        ##res = 20
        self.track_points = m.getInterpolatedPoints(res)
        #track_points = (Vec3(-5, 0, 0), Vec3(-5, 10, 0), Vec3(-5, 20, 0), Vec3(-5, 30, 0), Vec3(-5, 40, 0), Vec3(-5, 43, 0), Vec3(-5, 53, 0), Vec3(-5, 63, 0))
        #print "Imput Centers:", track_points
        self.varthickness = []  #Generate the Vector for thickness of the road
        
        for i in range(len(self.track_points)-1):
            if i == 0:
##                self.varthickness.append(self.calcTheVector(track_points[len(track_points)-1],track_points[i],track_points[i+1])) #Wieder benutzen wenn wir einen geschlossenen Kreis haben
                self.varthickness.append(self.calcTheVector(self.track_points[i],self.track_points[i],self.track_points[i+1]))
                continue
            self.varthickness.append(self.calcTheVector(self.track_points[i-1],self.track_points[i],self.track_points[i+1]))
##        self.varthickness.append(self.calcTheVector(track_points[len(track_points)-2],track_points[len(track_points)-1],track_points[0])) #Wieder benutzen wenn wir einen geschlossenen Kreis haben
        self.varthickness.append(self.calcTheVector(self.track_points[len(self.track_points)-2],self.track_points[len(self.track_points)-1],self.track_points[len(self.track_points)-1]))  
        
        #Normalizing the Vector
        for i in self.varthickness:
            i.normalize()
            
        for i in range(len(self.varthickness)):
            if self.varthickness[i-1].almostEqual(self.varthickness[i], 0.3):
                pass
            else:
                print self.varthickness[i-1], self.varthickness[i]
        #Creating the Vertex
        ##self.creatingVertex(track_points, street_data)
        self.createVertices(self.track_points, street_data)
        #Connect the Vertex
        self.connectVertices(street_data)
        #?Show the Mesh
        #self.CreateMesh(self.vdata, self.prim)
        ##Debugprint
        #print "Thickness Vectors:", self.varthickness

# -------------------------------------------------------------------------------------

    def calcTheVector(self, pre, now, past):
        vector1 = (pre[0] - now[0], pre[1] - now[1])
        vector2 = (now[0] - past[0], now[1] - past[1]) 
        high = pre[2] - past[2]
        return Vec3(((vector1[1] + vector2[1])/2.0),((vector1[0] + vector2[0])/2.0), high)

# -------------------------------------------------------------------------------------

    def getVarthickness(self):
        return self.varthickness
    
# -------------------------------------------------------------------------------------

    def setTrackPoints(self, track_points):
        '''
        '''
        self.track_points = track_points
        
    def getTrackPoints(self):
        '''
        '''
        return self.track_points
        
    trackpoints = property(fget = getTrackPoints, fset = setTrackPoints)
    
# -------------------------------------------------------------------------------------

    def createVertices(self, track_points, street_data):
        '''
        '''
        texcoordinates =[]
        bordertexcoordinates =[]
        street_data_length = len(street_data)
        
        for i in xrange(street_data_length):
            texcoordinates.append((i+1.0)/street_data_length)
        
        for i in xrange(len(street_data.border)):
            bordertexcoordinates.append((i+1.0)/street_data_length)
            
        print "\n\n\n#-#-#-#-#-#-#-##-#-#-#-#-#-#####################-#-#-#-\n\n"
        
        last_normal = Vec3(0,0,1)
        last_vec = Vec3(0,1,0)
        for i in xrange(len(track_points)):
            if i == 0:
                vec = track_points[0]-track_points[1]
            elif i+1 == len(track_points):
                vec = track_points[i-1]-track_points[0]
            else:
                vec = track_points[i-1]-track_points[i+1]
                
            
            # calculate here the direction out of the street vector and the last normal
            last_normal.normalize()
            vec.normalize()
            mat = Mat3()

            mat.setRotateMat(-90, last_normal) # turn the direction around the last_normal
            turned_vec = mat.xform(vec)
            
            turned_vec.normalize()
            last_normal = turned_vec.cross(vec) # calculate the new normal
            
            turned_vec.normalize()
            
            j = 0    
            for shapedot in street_data:
                # this is like a layer in 3d [Ebenengleichung] 
                # vec = vec + vec*scalar + vec*scalar
                # this is used to transform the 2d-Streetshape to 3d
                point = track_points[i] + (turned_vec*shapedot[0]) + (last_normal*shapedot[1])
                
                self.vertex.addData3f(point[0], point[1], point[2])
                self.normal.addData3f(0, 0, 1) #KA how to calc
                ##self.texcoord.addData2f(texcoordinates[j], (i%2)) #
                self.texcoord.addData2f(texcoordinates[j], (i%2)) #
                j += 1
            

##        #####
##        #####
##        
##        texcoordinates =[]
##        street_data_length = len(street_data)
##        for i in xrange(street_data_length):
##            texcoordinates.append((i+1.0)/street_data_length)
##            
##        for i in xrange (len(track_points)):
##            if i+1 == len(track_points):
##                vec = track_points[i-1]-track_points[0]
##            else:
##                vec = track_points[i-1]-track_points[i+1]
##                
##            normal = self.varthickness[i].cross(vec)
##            normal.normalize()
##                
##            j = 0
##            for shapedot in street_data:
##                # this is like a layer in 3d [Ebenengleichung] 
##                # vec = vec + vec*scalar + vec*scalar
##                # this is used to transform the 2d-Streetshape to 3d
##                point = track_points[i] + (self.varthickness[i]*shapedot[0]) + (normal*shapedot[1])
##                
##                ##self.vertex.addData3f((track_points[i][0] + (self.varthickness[i][0]*street_data[j][0]), track_points[i][1] + (self.varthickness[i][1]*street_data[j][0]), track_points[i][2] + (self.varthickness[i][2]+street_data[j][1])))
##                
##                self.vertex.addData3f(point[0], point[1], point[2])
##                ##self.normal.addData3f(0, 0, 1) #KA how to calc
##                self.texcoord.addData2f(texcoordinates[j], (i%2))
##                j += 1
        
### -------------------------------------------------------------------------------------
##
##    def creatingVertex(self, track_points, street_data):
##        #Math: self.varthickness are the midd points
##        #for every Street Point create one Vertex by x*varthickness+Center and high+Center
##        colors = ((255,255,255,255),(255,255,0,1),(255,0,0,1),(0,0,0,1),(0,255,0,1))
##        texcoordinates =[]
##        street_data_length = len(street_data)
##        for i in range(street_data_length):
##            texcoordinates.append((i+1.0)/street_data_length)
##        for i in range (len(track_points)):
##            for j in range (street_data_length): ###WARUM war hier -2!!!!!!!!!!!!!! wenn man den end und start punkt nicht hat ;)
##                    self.vertex.addData3f((track_points[i][0] + (self.varthickness[i][0]*street_data[j][0]), track_points[i][1] + (self.varthickness[i][1]*street_data[j][0]), track_points[i][2] + (self.varthickness[i][2]+street_data[j][1])))
##                    self.normal.addData3f(0, 0, 1) #KA how to calc
##                    #self.color.addData4f(colors[j])
##                    self.texcoord.addData2f(texcoordinates[j], (i%2)) #
####                track_points[i][0] + (self.varthickness[i][0]*street_data[j][0])   #x
####                track_points[i][1] + (self.varthickness[i][1]*street_data[j][0])   #y
####                track_points[i][2] + (self.varthickness[i][2]+street_data[j][1])   #z

# -------------------------------------------------------------------------------------

    def connectVertices(self, street_data):
        #param j = len(street_Data)
        j = len(street_data)
        for i in xrange (self.vdata.getNumRows()-(j)): #-j??????  oder +-1
            if (i+1) % j != 0:
                self.prim.addVertex(i)
                self.prim.addVertex(i+1)
                self.prim.addVertex(i+j+1)
                self.prim.closePrimitive()
                
                self.prim.addVertex(i)
                self.prim.addVertex(i+j+1)
                self.prim.addVertex(i+j)
                self.prim.closePrimitive()
            else: # close mesh's bottom side
                
                self.prim.addVertex(i+1-j)
                self.prim.addVertex(i+1)
                self.prim.addVertex(i)
                self.prim.closePrimitive()
                
                self.prim.addVertex(i)
                self.prim.addVertex(i+1)
                self.prim.addVertex(i+j)
                self.prim.closePrimitive()
                
        # close start and end
        k = self.vdata.getNumRows()-j
        for i in xrange (j):
            if (i+1) % j != 0:
                self.prim.addVertex(i)
                self.prim.addVertex(i+k+1)
                self.prim.addVertex(i+1)                
                self.prim.closePrimitive()
                
                self.prim.addVertex(i)
                self.prim.addVertex(i+k)
                self.prim.addVertex(i+k+1)
                self.prim.closePrimitive()
                
            else: # close mesh's bottom side
                self.prim.addVertex(i)
                self.prim.addVertex(i+k-j+1)
                self.prim.addVertex(i-j+1)                
                self.prim.closePrimitive()
                
                self.prim.addVertex(i)
                self.prim.addVertex(i+k)
                self.prim.addVertex(i+k-j+1)
                self.prim.closePrimitive()

# -------------------------------------------------------------------------------------
    
##    def connectVertex(self, i, j):
##        '''
##        '''
##        if (i+1) % j != 0:
##            self.prim.addVertex(i)
##            self.prim.addVertex(i+1)
##            self.prim.addVertex(i+j+1)
##            self.prim.closePrimitive()
##            
##            self.prim.addVertex(i)
##            self.prim.addVertex(i+j+1)
##            self.prim.addVertex(i+j)
##            self.prim.closePrimitive()
##        else: # close mesh's bottom side
##            
##            self.prim.addVertex(i+1-j)
##            self.prim.addVertex(i+1)
##            self.prim.addVertex(i)
##            self.prim.closePrimitive()
##            
##            self.prim.addVertex(i)
##            self.prim.addVertex(i+1)
##            self.prim.addVertex(i+j)
##            self.prim.closePrimitive()

# -------------------------------------------------------------------------------------


    def createMesh(self):
        geom = Geom(self.vdata)
        geom.addPrimitive(self.prim)
        
        node = GeomNode('street')
        node.addGeom(geom)
        
        #nodePath = self.render.attachNewNode(node)
        return node
    
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

if __name__ == "__main__":
    #import main
    #Track3d(200,800,600)
    #Test
    import trackgentest
##    tuple1 = ((1.0,1.0,0.0),(1.0,4.0,0.0),(1.0,10.0,0.0))
##    tuple2 = ((-2.0, -3.0, 0.0),(1.0, -5.0, 0.0),(4.0, -4.0, 0.0),(6.0, 0.0, 0.0),(3.0, 4.0, 0.0),(-2.0, 6.0, 0.0),(-7.0, 3.0, 0.0),(-8.0, -2.0, 0.0))
##    tuple3 = ((10.0,10.0,0.0),(10.0,-10.0,0.0),(-10.0,-10.0,0.0),(-10.0,10.0,0.0))
##
##
##
##    Track3d(100, 800, 600, 50)


  
