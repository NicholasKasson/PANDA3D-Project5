from direct.showbase.ShowBase import ShowBase
from panda3d.core import Loader, NodePath, Vec3, CollisionNode, CollisionSphere
from direct.task import Task
from CollideObjectBase import *
#---------------------------------------------------------------------MODEL CREATION SCRIPT INIT---------------------------------------------------------------------
def addAdditionalModel(self,ModelFile,scale,CoordX,CoordY,CoordZ,TextureFile,Yaw,Pitch,Rotation):
        new_obj = self.loader.loadModel(ModelFile) 
        new_obj.setScale(scale)
        new_obj.setColorScale(1.0,1.0,1.0,1.0)
        new_obj.reparentTo(self.render)
        new_obj.setPos(CoordX,CoordY,CoordZ)
        new_obj_tex = self.loader.loadTexture(TextureFile)
        new_obj.setTexture(new_obj_tex)
        new_obj.setHpr(Yaw,Pitch,Rotation)
#---------------------------------------------------------------------PLANET INIT---------------------------------------------------------------------
class Planet(SphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Planet, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0,0,0), 1.05)
        # self.modelNode = loader.loadModel(modelPath)
        # self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.modelNode = self.modelNode
#---------------------------------------------------------------------UNIVERSE INIT---------------------------------------------------------------------
class Universe(InverseSphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Universe, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0,0,0), 0.9)
        # self.modelNode = loader.loadModel(modelPath)
        # self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
#---------------------------------------------------------------------DRONE INIT---------------------------------------------------------------------
class Drone(SphereCollideObject):
    droneCount = 0
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Drone, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0,0,0), 2.7)
        # self.modelNode = loader.loadModel(modelPath)
        # self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        # self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
#---------------------------------------------------------------------SPACESTATION INIT---------------------------------------------------------------------
class SpaceStation(CapsuleCollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(SpaceStation, self).__init__(loader, modelPath, parentNode, nodeName, 1, -1, 5, 1, -1, -5, 10)
        # self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)   
#---------------------------------------------------------------------PLAYER INIT---------------------------------------------------------------------
class Player(SphereCollideObject):
    def __init__(self, accept_method, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float, HPRoffset: Vec3):
        super(Player, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0.6,0,5), 4.9)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setHpr(HPRoffset)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.accept = accept_method
        self.taskMgr = taskMgr
        self.render = NodePath()
#---------------------------------------------------------------------MOVEMENT INIT---------------------------------------------------------------------        
    def SetKeyBindings(self):
        self.accept('space', self.UpwardsThrust, [1])
        self.accept('space-up', self.UpwardsThrust, [0])
        self.accept('shift', self.DownwardsThrust, [1])
        self.accept('shift-up', self.DownwardsThrust, [0])
        self.accept('w', self.ForwardsThrust, [1])
        self.accept('w-up', self.ForwardsThrust, [0])
        self.accept('s', self.BackwardsThrust, [1])
        self.accept('s-up', self.BackwardsThrust, [0])
        self.accept('a', self.StrafeLeft, [1])
        self.accept('a-up', self.StrafeLeft, [0])
        self.accept('d', self.StrafeRight, [1])
        self.accept('d-up', self.StrafeRight, [0])
        self.accept('q', self.LeftTurn, [1])
        self.accept('q-up', self.LeftTurn, [0])
        self.accept('e', self.RightTurn, [1])
        self.accept('e-up', self.RightTurn, [0])
        self.accept('z', self.LeftRotate, [1])
        self.accept('z-up', self.LeftRotate, [0])
        self.accept('x', self.RightRotate, [1])
        self.accept('x-up', self.RightRotate, [0])
        self.accept('c', self.ForwardsRoll, [1])
        self.accept('c-up', self.ForwardsRoll, [0])
        self.accept('v', self.BackwardsRoll, [1])
        self.accept('v-up', self.BackwardsRoll, [0])
        
#DIRECTIONAL MOVEMENT        
    def ForwardsThrust(self, keyDown):
        if keyDown: 
            self.taskMgr.add(self.ApplyForwardsThrust, 'upwards thrust')
        else: 
            self.taskMgr.remove('upwards thrust')
    def ApplyForwardsThrust(self, task):
        rate = -4
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.up())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont   
    def BackwardsThrust(self, keyDown):
        if keyDown: 
            self.taskMgr.add(self.ApplyBackwardsThrust, 'downwards thrust')
        else: 
            self.taskMgr.remove('downwards thrust')
    def ApplyBackwardsThrust(self, task):
        rate = -4
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.down())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont
    #Forwards works!
    def UpwardsThrust(self, keyDown):
        if keyDown: 
            self.taskMgr.add(self.ApplyUpwardsThrust, 'forwards thrust')
        else: 
            self.taskMgr.remove('forwards thrust')
    def ApplyUpwardsThrust(self, task):
        rate = 4
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont
    def StrafeLeft(self, keyDown):
        if keyDown: 
            self.taskMgr.add(self.ApplyStrafeLeft, 'strafe left')
        else: 
            self.taskMgr.remove('strafe left')
    def ApplyStrafeLeft(self, task):
        rate = 4
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.left())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont 
    def StrafeRight(self, keyDown):
        if keyDown: 
            self.taskMgr.add(self.ApplyStrafeRight, 'strafe right')
        else: 
            self.taskMgr.remove('strafe right')
    def ApplyStrafeRight(self, task):
        rate = 4
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.right())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)      
        return Task.cont
    def DownwardsThrust(self, keyDown):
        if keyDown: 
            self.taskMgr.add(self.ApplyDownwardsThrust, 'backwards thrust')
        else: 
            self.taskMgr.remove('backwards thrust')
    def ApplyDownwardsThrust(self, task):
        rate = 4
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.back())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont    

    #ROTATIONAL
    def LeftTurn(self, keyDown):
        if keyDown: 
            self.taskMgr.add(self.ApplyLeftTurn, 'left-turn')
        else: 
            self.taskMgr.remove('left-turn')
    def ApplyLeftTurn(self, task):
        rate = 1.5
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont
    def RightTurn(self, keyDown):
        if keyDown: 
            self.taskMgr.add(self.ApplyRightTurn, 'right-turn')
        else: 
            self.taskMgr.remove('right-turn')
    def ApplyRightTurn(self, task):
        rate = 1.5
        self.modelNode.setH(self.modelNode.getH() - rate)
        return Task.cont
    def LeftRotate(self, keyDown):
        if keyDown: 
            self.taskMgr.add(self.ApplyLeftRotate, 'left-rotate')
        else: 
            self.taskMgr.remove('left-rotate')
    def ApplyLeftRotate(self, task):
        rate = 1.5
        self.modelNode.setR(self.modelNode.getR() + rate)
        return Task.cont
    def RightRotate(self, keyDown):
        if keyDown: 
            self.taskMgr.add(self.ApplyRightRotate, 'right-rotate')
        else: 
            self.taskMgr.remove('right-rotate')
    def ApplyRightRotate(self, task):
        rate = 1.5
        self.modelNode.setR(self.modelNode.getR() - rate)
        return Task.cont
    def ForwardsRoll(self, keyDown):
        if keyDown: 
            self.taskMgr.add(self.ApplyForwardsRoll, 'forwards-roll')
        else: 
            self.taskMgr.remove('forwards-roll')
    def ApplyForwardsRoll(self, task):
        rate = 1.5
        self.modelNode.setP(self.modelNode.getP() + rate)
        return Task.cont
    def BackwardsRoll(self, keyDown):
        if keyDown: 
            self.taskMgr.add(self.ApplyBackwardsRoll, 'backwards-roll')
        else: 
            self.taskMgr.remove('backwards-roll')
    def ApplyBackwardsRoll(self, task):
        rate = 1.5
        self.modelNode.setP(self.modelNode.getP() - rate)
        return Task.cont
