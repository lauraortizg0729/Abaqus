from abaqus import *
from abaqusConstants import *

import __main__
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior

Beam_h = 40.0 #Beam Height mm
Beam_w = Beam_w*0.5 #Beam width mm 
mesh_size = 2.5 #mesh size mm
Beam_d = 400.0 #Beam length mm
Pressure = 50.0 # Applied Pressure [MPa]
Young_m = 190000 #Young's Modulus [MPa]
Poisson_r = 0.32 #Poisson's ratio

session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
    engineeringFeatures=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
    
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
    
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)

#Create a rectangle using two points
s.rectangle(point1=(-5.0, 5.0), point2=(5.0, -5.0))

#Adjust the two edges of the rectable to desired dimensions
s.ObliqueDimension(vertex1=v[0], vertex2=v[1], textPoint=(-15.8884887695313, 
    -0.332636833190918), value=Beam_h)
s.ObliqueDimension(vertex1=v[1], vertex2=v[2], textPoint=(-0.279197692871094, 
    -17.7970161437988), value=Beam_w)
    
p = mdb.models['Model-1'].Part(name='Beam', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Beam']

#Extrude the sketch "s" over the depth "Beam_d"
p.BaseSolidExtrude(sketch=s, depth=Beam_d)

#Define elastic material    
mdb.models['Model-1'].Material(name='Steel')
mdb.models['Model-1'].materials['Steel'].Elastic(table=((Young_m, Poisson_r), ))

#Define homogeneous solid section 
mdb.models['Model-1'].HomogeneousSolidSection(name='BeamSection', 
    material='Steel', thickness=None)

#Create a set into part level, used for section assignment    
p = mdb.models['Model-1'].parts['Beam']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region = p.Set(cells=cells, name='Beam')
p = mdb.models['Model-1'].parts['Beam']

#Assign the section to a defined "region"
p.SectionAssignment(region=region, sectionName='BeamSection', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
    engineeringFeatures=OFF, mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=ON)
    
#Apply general mesh seed    
p = mdb.models['Model-1'].parts['Beam']
p.seedPart(size=mesh_size, deviationFactor=0.1, minSizeFactor=0.1)

#Generate Mesh
p = mdb.models['Model-1'].parts['Beam']
p.generateMesh()

#Import part into the instance
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['Beam']
a.Instance(name='Beam-1', part=p, dependent=ON)

a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Beam-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#20 ]', ), )
a.Set(faces=faces1, name='BC_Set')

# Create a surface set
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Beam-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#8 ]', ), )
a.Surface(side1Faces=side1Faces1, name='PressSurface')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)

#Create analysis    
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial', 
    timePeriod=1.0, maxNumInc=100, initialInc=1.0, minInc=1e-05, 
    maxInc=1.0, nlgeom=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON, adaptiveMeshConstraints=OFF)

#Define a region using a set    
a = mdb.models['Model-1'].rootAssembly
region = a.surfaces['PressSurface']

#Applied Load
mdb.models['Model-1'].Pressure(name='Load-1', createStepName='Step-1', 
    region=region, distributionType=UNIFORM, field='', magnitude=Pressure, 
    amplitude=UNSET)

#Boundary conditions
a = mdb.models['Model-1'].rootAssembly
region = a.sets['BC_Set']
mdb.models['Model-1'].EncastreBC(name='BC-1', createStepName='Step-1', 
    region=region, localCsys=None)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
    predefinedFields=OFF, connectors=OFF)
    
mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
    numGPUs=0)


