import os
import vtk
import unittest

from pycaster.pycaster import rayCaster

#OPTIONS
cfd = os.path.dirname(os.path.realpath(__file__))
filenameSphereSTL = os.path.join(cfd, "data", "sphere.stl")
filenameSphereHollowSTL = os.path.join(cfd, "data", "sphereHollow.stl")
filenameShapeSSTL = os.path.join(cfd, "data", "shapeS.stl")

class rayCasterTestSTL(unittest.TestCase):
		
	def test_loadSphereSTL(self):
		rT = rayCaster.fromSTL(filenameSphereSTL, scale = 1.0)
		bounds = rT.mesh.GetBounds()
		self.assertEqual(-25, round(bounds[0]))
		
	def test_scaleSphereSTL(self):
		rT = rayCaster.fromSTL(filenameSphereSTL, scale = 1.0)
		rT.scaleMesh(1.0e-3)
		bounds = rT.mesh.GetBounds()
		self.assertEqual(-0.025, round(bounds[0], 3))
		
	def test_loadNscaleSphereSTL(self):
		rT = rayCaster.fromSTL(filenameSphereSTL, scale = 1.0e-3)
		bounds = rT.mesh.GetBounds()
		self.assertEqual(-0.025, round(bounds[0], 3))
		
	def test_castRayOnSphere_noPoints(self):
		rT = rayCaster.fromSTL(filenameSphereSTL, scale = 1.0)
		pointsIntersection = rT.castRay([0.0, 0.0, -25.0], [0.0, 0.0, 25.0])
		self.assertEqual(2, len(pointsIntersection))
		
	def test_castRayOutsideSphere_noPoints(self):
		rT = rayCaster.fromSTL(filenameSphereSTL, scale = 1.0)
		#a warning should occur here
		pointsIntersection = rT.castRay([0.0, 50.0, -25.0], [0.0, 50.0, 25.0])
		self.assertEqual(0, len(pointsIntersection))
		
	def test_castRayOnSphere_Coords(self):
		rT = rayCaster.fromSTL(filenameSphereSTL, scale = 1.0)
		pointsIntersection = rT.castRay([0.0, 0.0, -25.0], [0.0, 0.0, 25.0])
		self.assertEqual(-25.0, round(pointsIntersection[0][2]))
		self.assertEqual(25.0, round(pointsIntersection[1][2]))
		
	def test_castRayOnSphereHollow_noPoints(self):
		rT = rayCaster.fromSTL(filenameSphereHollowSTL, scale = 1.0)
		pointsIntersection = rT.castRay([0.0, 0.0, -25.0], [0.0, 0.0, 25.0])
		self.assertEqual(4, len(pointsIntersection))
		
	def test_castRayOnSphereHollow_Coords(self):
		rT = rayCaster.fromSTL(filenameSphereHollowSTL, scale = 1.0)
		pointsIntersection = rT.castRay([0.0, 0.0, -25.0], [0.0, 0.0, 25.0])
		self.assertEqual(-25.0, round(pointsIntersection[0][2]))
		self.assertEqual(-20.0, round(pointsIntersection[1][2]))
		self.assertEqual(20.0, round(pointsIntersection[2][2]))
		self.assertEqual(25.0, round(pointsIntersection[3][2]))
		
	def test_isPointInside_YES(self):
		rT = rayCaster.fromSTL(filenameSphereSTL, scale = 1.0)
		self.assertEqual(True, rT.isPointInside([0.0, 0.0, 0.0]))
		
	def test_isPointInside_NO(self):
		rT = rayCaster.fromSTL(filenameSphereSTL, scale = 1.0)
		self.assertEqual(False, rT.isPointInside([0.0, 50.0, 0.0]))

class rayCasterTestPolydata(unittest.TestCase):
	
	def setUp(self):
		readerSTL = vtk.vtkSTLReader() #create a 'vtkSTLReader' object
		readerSTL.SetFileName(filenameSphereSTL) #set the .stl filename in the reader
		readerSTL.Update() #'update' the reader i.e. read the .stl file
		self.polydata = readerSTL.GetOutput()
		
	def test_SphereBounds(self):
		rT = rayCaster(self.polydata)
		bounds = rT.mesh.GetBounds()
		self.assertEqual(-25, round(bounds[0]))
		
	def test_scaleSphere(self):
		rT = rayCaster(self.polydata)
		rT.scaleMesh(1.0e-3)
		bounds = rT.mesh.GetBounds()
		self.assertEqual(-0.025, round(bounds[0], 3))
		
	def test_castRayOnSphere_noPoints(self):
		rT = rayCaster(self.polydata)
		pointsIntersection = rT.castRay([0.0, 0.0, -25.0], [0.0, 0.0, 25.0])
		self.assertEqual(2, len(pointsIntersection))
		
	def test_castRayOutsideSphere_noPoints(self):
		rT = rayCaster(self.polydata)
		#a warning should occur here
		pointsIntersection = rT.castRay([0.0, 50.0, -25.0], [0.0, 50.0, 25.0])
		self.assertEqual(0, len(pointsIntersection))
		
	def test_castRayOnSphere_Coords(self):
		rT = rayCaster(self.polydata)
		pointsIntersection = rT.castRay([0.0, 0.0, -25.0], [0.0, 0.0, 25.0])
		self.assertEqual(-25.0, round(pointsIntersection[0][2]))
		self.assertEqual(25.0, round(pointsIntersection[1][2]))

class rayCasterDistanceSphere(unittest.TestCase):
	
	def setUp(self):
		self.rT = rayCaster.fromSTL(filenameSphereSTL, scale = 1.0)
	
	def test_SrcOutTrgOut(self):
		dist = self.rT.calcDistanceInSolid([0.0, 0.0, -50.0], [0.0, 0.0, 50.0])
		self.assertEqual(50.0, dist)
		
	def test_SrcInTrgIn(self):
		dist = self.rT.calcDistanceInSolid([0.0, 0.0, -20.0], [0.0, 0.0, 20.0])
		self.assertEqual(40.0, dist)
		
	def test_SrcInTrgOut(self):
		dist = self.rT.calcDistanceInSolid([0.0, 0.0, -20.0], [0.0, 0.0, 50.0])
		self.assertEqual(45.0, dist)
		
	def test_SrcOutTrgIn(self):
		dist = self.rT.calcDistanceInSolid([0.0, 0.0, -50.0], [0.0, 0.0, 20.0])
		self.assertEqual(45.0, dist)
	
	def test_SrcOutTrgOutNoInter(self):
		dist = self.rT.calcDistanceInSolid([0.0, 50.0, -50.0], [0.0, 50.0, 50.0])
		self.assertEqual(0.0, dist)

class rayCasterDistanceSphereHollow(unittest.TestCase):
	
	def setUp(self):
		self.rT = rayCaster.fromSTL(filenameSphereHollowSTL, scale = 1.0)
	
	def test_SrcOutTrgOut(self):
		dist = self.rT.calcDistanceInSolid([0.0, 0.0, -50.0], [0.0, 0.0, 50.0])
		self.assertEqual(10.0, dist)
		
	def test_SrcInTrgIn(self):
		dist = self.rT.calcDistanceInSolid([0.0, 0.0, -22.5], [0.0, 0.0, 22.5])
		self.assertEqual(5.0, dist)
		
	def test_SrcInTrgOut(self):
		dist = self.rT.calcDistanceInSolid([0.0, 0.0, -22.5], [0.0, 0.0, 50.0])
		self.assertEqual(7.5, dist)
		
	def test_SrcOutTrgIn(self):
		dist = self.rT.calcDistanceInSolid([0.0, 0.0, -50.0], [0.0, 0.0, 22.5])
		self.assertEqual(7.5, dist)
	
	def test_SrcOutTrgOutNoInter(self):
		dist = self.rT.calcDistanceInSolid([0.0, 0.0, -15.0], [0.0, 0.0, 15.0])
		self.assertEqual(0.0, dist)
		
class rayCasterDistanceShapeS(unittest.TestCase):
	
	def setUp(self):
		self.rT = rayCaster.fromSTL(filenameShapeSSTL, scale = 1.0)
	
	def test_SrcOutTrgOut(self):
		dist = self.rT.calcDistanceInSolid([0.0, -30.0, 0.0], [0.0, 30.0, 0.0])
		self.assertEqual(30.0, dist)
		
	def test_SrcInTrgIn(self):
		dist = self.rT.calcDistanceInSolid([0.0, -15.0, 0.0], [0.0, 15.0, 0.0])
		self.assertEqual(20.0, dist)
		
	def test_SrcInTrgOut(self):
		dist = self.rT.calcDistanceInSolid([0.0, -15.0, 0.0], [0.0, 30.0, 0.0])
		self.assertEqual(25.0, dist)
		
	def test_SrcOutTrgIn(self):
		dist = self.rT.calcDistanceInSolid([0.0, -30.0, 0.0], [0.0, 15.0, 0.0])
		self.assertEqual(25.0, dist)

if __name__ == '__main__':
	unittest.main()
