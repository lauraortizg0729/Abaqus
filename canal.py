
#
# Getting Started with Abaqus
#
# Script for forming portion channel example
#
from abaqus import *
from abaqusConstants import *
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
session.journalOptions.setValues(replayGeometry=COORDINATE,
    recoverGeometry=COORDINATE)
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
Mdb()

mdb.models.changeKey(fromName='Model-1', toName='standard')

##
##  Sketch profile of blank
##
s = mdb.models['standard'].ConstrainedSketch(name='__profile__',
    sheetSize=0.25)
g, v, d = s.geometry, s.vertices, s.dimensions
s.sketchOptions.setValues(sheetSize=0.25, gridSpacing=0.005, grid=ON,
    gridFrequency=2, constructionGeometry=ON, dimensionTextHeight=0.005,
    decimalPlaces=3)
s.Line(point1=(-0.05, -0.005), point2=(0.05, -0.005))
s.Line(point1=(0.05, -0.005), point2=(0.05, 0.005))
s.Line(point1=(0.05, 0.005), point2=(-0.05, 0.005))
s.Line(point1=(-0.05, 0.005), point2=(-0.05, -0.005))

s.HorizontalDimension(vertex1=v.findAt((-0.05, 0.005)), vertex2=v.findAt((
    0.05, 0.005)), textPoint=(0.0457058809697628, 0.0127279916778207),
    value=0.1)
s.FixedConstraint(entity=g.findAt((0.0, -0.005)))
s.PerpendicularConstraint(entity1=g.findAt((-0.05, 0.0)), entity2=g.findAt((
    0.0, 0.005)))
s.PerpendicularConstraint(entity1=g.findAt((0.05, 0.0)), entity2=g.findAt((
    0.0, 0.005)))
s.VerticalDimension(vertex1=v.findAt((-0.05, -0.005)), vertex2=v.findAt((
    -0.05, 0.005)), textPoint=(-0.0521911755204201, 0.000539974775165319),
    value=0.001)
p = mdb.models['standard'].Part(name='Blank', dimensionality=TWO_D_PLANAR,
    type=DEFORMABLE_BODY)
p = mdb.models['standard'].parts['Blank']
p.BaseShell(sketch=s)
p = mdb.models['standard'].parts['Blank']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['standard'].sketches['__profile__']
##
##  Sketch profile of punch
##
s0 = mdb.models['standard'].ConstrainedSketch(name='__profile__', sheetSize=0.25)
g, v, d = s0.geometry, s0.vertices, s0.dimensions
s0.sketchOptions.setValues(sheetSize=0.25, gridSpacing=0.005, grid=ON,
    gridFrequency=2, constructionGeometry=ON, dimensionTextHeight=0.005,
    decimalPlaces=3)
s0.Line(point1=(-0.06, 0.0), point2=(0.0, 0.0))
s0.Line(point1=(0.0, 0.0), point2=(0.0, 0.06))
s0.FilletByRadius(radius=0.005, curve1=g.findAt((-0.03, 0.0)), nearPoint1=(
    -0.00207383744418621, 0.000262239947915077), curve2=g.findAt((0.0, 0.03)),
    nearPoint2=(-0.00016310065984726, 0.00246503762900829))
session.viewports['Viewport: 1'].view.fitView()
mdb.models['standard'].ConstrainedSketch(name='Punch', objectToCopy=s0)
p = mdb.models['standard'].Part(name='Punch', dimensionality=TWO_D_PLANAR,
    type=ANALYTIC_RIGID_SURFACE)
p = mdb.models['standard'].parts['Punch']
p.AnalyticRigidSurf2DPlanar(sketch=s0)
p = mdb.models['standard'].parts['Punch']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['standard'].sketches['__profile__']


##  Create material 'Steel'
##
mdb.models['standard'].Material('log')
mdb.models['standard'].materials['log'].Elastic(table=((2.1E11, 0.3), ))
mdb.models['standard'].materials['log'].Plastic(table=((400.E6, 0.0), (
    420.E6, 0.02), (500.E6, 0.2), (600.E6, 0.5)))
##
##  Create and assign solid section to blank
##
mdb.models['standard'].HomogeneousSolidSection(name='BlankSection',
    material='log', thickness=1.0)
p = mdb.models['standard'].parts['Blank']
f = p.faces
faces = f.findAt(((-0.016667, -0.004667, 0.0), ))
region = regionToolset.Region(faces=faces)
p = mdb.models['standard'].parts['Blank']
p.SectionAssignment(region=region, sectionName='BlankSection', offset=0.0)
##
##  Define datum coordinate system
##
p = mdb.models['standard'].parts['Blank']
p.DatumCsysByDefault(coordSysType=CARTESIAN)
##
##  Assign material orientation to blank
##
p = mdb.models['standard'].parts['Blank']
f = p.faces
faces = f.findAt(((-0.016667, -0.004667, 0.0), ))
region = regionToolset.Region(faces=faces)
datum = p.datums[3]
p.MaterialOrientation(region=region, localCsys=datum)

a = mdb.models['standard'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
##
##  Set coordinate system (done by default)
##
a = mdb.models['standard'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
##
##  Instance the blank
##
p = mdb.models['standard'].parts['Blank']
a.Instance(name='Blank-1', part=p, dependent=ON)
a = mdb.models['standard'].rootAssembly
##
##  Instance the punch
##
p = mdb.models['standard'].parts['Punch']
a.Instance(name='Punch-1', part=p, dependent=ON)
##
##  Translate the punch
##
a = mdb.models['standard'].rootAssembly
p = a.instances['Punch-1']
p.translate(vector=(0.116, 0.0, 0.0))
##
##   Edge to edge constraints between punch and blank
##
e11 = a.instances['Punch-1'].edges
e12 = a.instances['Blank-1'].edges
a.EdgeToEdge(movableAxis=e11.findAt(coordinates=(0.06975, 0.0, 0.0)),
    fixedAxis=e12.findAt(coordinates=(0.025, -0.004, 0.0)), flip=ON,
    clearance=0.0)
session.viewports['Viewport: 1'].view.fitView()
e11 = a.instances['Punch-1'].edges
e12 = a.instances['Blank-1'].edges
a.EdgeToEdge(movableAxis=e11.findAt(coordinates=(0.116, 0.01575, 0.0)),
    fixedAxis=e12.findAt(coordinates=(-0.05, -0.00425, 0.0)), flip=ON,
    clearance=-0.05)
##
##  Instance the holder
##
p = mdb.models['standard'].parts['Holder']
a.Instance(name='Holder-1', part=p, dependent=ON)
p = a.instances['Holder-1']
p.translate(vector=(0.056, 0.0, 0.0))
session.viewports['Viewport: 1'].view.fitView()
##
##   Edge to edge constraints between holder and punch
##
e11 = a.instances['Holder-1'].edges
e12 = a.instances['Punch-1'].edges
a.EdgeToEdge(movableAxis=e11.findAt(coordinates=(0.056, 0.01875, 0.0)),
    fixedAxis=e12.findAt(coordinates=(0.0, 0.01575, 0.0)), flip=OFF,
    clearance=0.001)

e11 = a.instances['Holder-1'].edges
e12 = a.instances['Blank-1'].edges
a.EdgeToEdge(movableAxis=e11.findAt(coordinates=(0.04725, 0.0, 0.0)),
    fixedAxis=e12.findAt(coordinates=(0.025, -0.004, 0.0)), flip=OFF,
    clearance=0.0)
##
##  Instance the die
##
p = mdb.models['standard'].parts['Die']
a.Instance(name='Die-1', part=p, dependent=ON)
p = a.instances['Die-1']
p.translate(vector=(0.067, 0.0, 0.0))
session.viewports['Viewport: 1'].view.fitView()
##
##   Edge to edge constraints between die and blank (horizontal)
##
e11 = a.instances['Die-1'].edges
e12 = a.instances['Blank-1'].edges
a.EdgeToEdge(movableAxis=e11.findAt(coordinates=(0.067, -0.01875, 0.0)),
    fixedAxis=e12.findAt(coordinates=(-0.05, -0.00425, 0.0)), flip=OFF,
    clearance=-0.051)

e11 = a.instances['Die-1'].edges
e12 = a.instances['Blank-1'].edges
a.EdgeToEdge(movableAxis=e11.findAt(coordinates=(0.04725, 0.0, 0.0)),
    fixedAxis=e12.findAt(coordinates=(-0.025, -0.005, 0.0)), flip=ON,
    clearance=0.0)

p = a.instances['Blank-1']
p.translate(vector=(0.0, 0.009, 0.0))

a = mdb.models['standard'].rootAssembly
a.regenerate()

#
#   Create geometry set RefPunch
#
a = mdb.models['standard'].rootAssembly
r1 = a.instances['Punch-1'].referencePoints
refPoints1 = (r1[2], )
a.Set(referencePoints=refPoints1, name='RefPunch')
#
#   Create geometry set RefHolder
#
a = mdb.models['standard'].rootAssembly
r1 = a.instances['Holder-1'].referencePoints
refPoints1 = (r1[2], )
a.Set(referencePoints=refPoints1, name='RefHolder')
#
#   Create geometry set RefDie
#
a = mdb.models['standard'].rootAssembly
r1 = a.instances['Die-1'].referencePoints
refPoints1 = (r1[2], )
a.Set(referencePoints=refPoints1, name='RefDie')
#
#   Reset view
#
session.viewports['Viewport: 1'].view.setValues(width=0.0066561,
    height=0.0042551, cameraPosition=(-0.048954, 0.0037356, 0.34938),
    cameraTarget=(-0.048954, 0.0037356, 0))
#
#   Create geometry set Center
#
a = mdb.models['standard'].rootAssembly
e = a.instances['Blank-1'].edges
edges = e.findAt(((-0.05, 0.00475, 0.0), ))
a.Set(edges=edges, name='Center')
#
#   Create surface BlankTop
#
a = mdb.models['standard'].rootAssembly
e1 = a.instances['Blank-1'].edges
a.Surface(name='BlankTop', side1Edges=e1.findAt(((0.025, 0.005, 0.0), ), ))
#
#   Create surface BlankBot
#
a = mdb.models['standard'].rootAssembly
e1 = a.instances['Blank-1'].edges
a.Surface(name='BlankBot', side1Edges=e1.findAt(((-0.025, 0.004, 0.0), ), ))

session.viewports['Viewport: 1'].view.fitView()
#
#   Create surface PunchSurf
#
s = a.instances['Punch-1'].edges
side2Edges1 = s.findAt(((0.0, 0.02375, 0.0), ))
a.Surface(side2Edges=side2Edges1, name='PunchSurf')
#
#   Create surface HolderSurf
#
s = a.instances['Holder-1'].edges
side1Edges = s.findAt(((0.001, 0.02375, 0.0), ))
a.Surface(side1Edges=side1Edges, name='HolderSurf')

#
#   Create surface DieSurf
#
s = a.instances['Die-1'].edges
side2Edges = s.findAt(((0.001, -0.01475, 0.0), ))
a.Surface(side2Edges=side2Edges, name='DieSurf')

##
##  Create two static general steps
##
mdb.models['standard'].StaticStep(name='Holder force',
    previous='Initial',
    description='Apply holder force', timePeriod=1,
    adiabatic=OFF, maxNumInc=100, stabilization=None,
    timeIncrementationMethod=AUTOMATIC,
    initialInc=0.05, minInc=1e-05, maxInc=1, matrixSolver=SOLVER_DEFAULT,
    amplitude=RAMP, extrapolation=LINEAR, nlgeom=ON)
mdb.models['standard'].StaticStep(name='Move punch',
    previous='Holder force',
    description='Apply punch stroke', timePeriod=1,
    adiabatic=OFF, maxNumInc=1000, stabilization=None,
    timeIncrementationMethod=AUTOMATIC,
    initialInc=0.05, minInc=1e-05, maxInc=1, matrixSolver=SOLVER_DEFAULT,
    amplitude=RAMP, extrapolation=LINEAR)
##
##  Modify output requests
##
mdb.models['standard'].fieldOutputRequests['F-Output-1'].setValues(
    variables=PRESELECT, frequency=20)

regionDef=a.sets['RefPunch']
mdb.models['standard'].HistoryOutputRequest(name='H-Output-2',
    createStepName='Holder force',
    variables=('RF2', 'U2'),
    region=regionDef)
##
##  Create degree of freedom monitor
##
mdb.models['standard'].steps['Holder force'].Monitor(dof=2,
    node=regionDef, frequency=1)
mdb.models['standard'].steps['Move punch'].Monitor(dof=2,
    node=regionDef, frequency=1)
##
##  Print diagnostic data for contact
##
mdb.models['standard'].steps['Holder force'].DiagnosticPrint(frequency=1,
    contact=ON, plasticity=OFF, residual=ON, solve=OFF)
mdb.models['standard'].steps['Move punch'].DiagnosticPrint(frequency=1,
    contact=ON, plasticity=OFF, residual=ON, solve=OFF)
##
##  Reset view
##
session.viewports['Viewport: 1'].view.setValues(width=0.025757,
    height=0.016466, cameraPosition=(-0.04834, 0.0033255, 0.34366),
    cameraTarget=(-0.04834, 0.0033255, 0))

session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON)
session.viewports['Viewport: 1'].view.fitView()
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
##
##  Create contact property 'Fric'
##
mdb.models['standard'].ContactProperty('Fric')
mdb.models['standard'].interactionProperties['Fric'].TangentialBehavior(
    formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF,
    pressureDependency=OFF, temperatureDependency=OFF, dependencies=0,
    table=((0.1, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION,
    fraction=0.005, elasticSlipStiffness=None)
##
##  Create contact property 'NoFric'
##
mdb.models['standard'].ContactProperty('NoFric')
mdb.models['standard'].interactionProperties['NoFric'].TangentialBehavior(
    formulation=FRICTIONLESS)
##
##  Create contact interaction 'Punch-Blank'
##
region1=a.surfaces['PunchSurf']
region2=a.surfaces['BlankTop']
mdb.models['standard'].SurfaceToSurfaceContactStd(name='Punch-Blank',
    createStepName='Initial', master=region1, slave=region2,
    sliding=FINITE, interactionProperty='NoFric')
##
##  Create contact interaction 'Holder-Blank'
##
region1=a.surfaces['HolderSurf']
region2=a.surfaces['BlankTop']
mdb.models['standard'].SurfaceToSurfaceContactStd(name='Holder-Blank',
    createStepName='Initial', master=region1, slave=region2,
    sliding=FINITE, interactionProperty='Fric')
##
##  Create contact interaction 'Die-Blank'
##
region1=a.surfaces['DieSurf']
region2=a.surfaces['BlankBot']
mdb.models['standard'].SurfaceToSurfaceContactStd(name='Die-Blank',
    createStepName='Initial', master=region1, slave=region2,
    sliding=FINITE, interactionProperty='Fric')

mdb.models['standard'].StdContactControl(name='stabilize',
    automaticTolerances=OFF,
    stabilizeChoice=AUTOMATIC,
    dampFactor=0.001)
mdb.models['standard'].interactions['Punch-Blank'].setValuesInStep(
    stepName='Move punch', contactControls='stabilize')
##
##
session.viewports['Viewport: 1'].view.fitView()
##
##  Create BCs in step "Establish contact"
##
region = a.sets['Center']
mdb.models['standard'].XsymmBC(name='CenterBC',
    createStepName='Holder force', region=region)
region = a.sets['RefDie']
mdb.models['standard'].DisplacementBC(name='RefDieBC',
    createStepName='Holder force', region=region,
    u1=0.0, u2=0.0, ur3=0.0)
region = a.sets['RefHolder']
mdb.models['standard'].DisplacementBC(name='RefHolderBC',
    createStepName='Holder force', region=region,
    u1=0.0, ur3=0.0)
region = a.sets['RefPunch']
mdb.models['standard'].DisplacementBC(name='RefPunchBC',
    createStepName='Holder force', region=region,
    u1=0.0, u2=0.0, ur3=0.0)
##
##  Add holder force
##
region = a.sets['RefHolder']
mdb.models['standard'].ConcentratedForce(name='RefHolderForce',
    createStepName='Holder force', region=region, cf2=-440000.0)
##
##  Push punch down in step  "Move punch"
##
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Move punch')
mdb.models['standard'].boundaryConditions['RefPunchBC'].setValuesInStep(
    stepName='Move punch', u2=-0.03)

session.viewports['Viewport: 1'].view.fitView()
##
##  Assign edge seeds
##
p = mdb.models['standard'].parts['Blank']
e = p.edges
pickedEdges = e.findAt(((-0.025, -0.005, 0.0), ), ((0.025, -0.004, 0.0), ))
p.seedEdgeByNumber(edges=pickedEdges, number=100)
pickedEdges = e.findAt(((-0.05, -0.00425, 0.0), ), ((0.05, -0.00475, 0.0), ))
p.seedEdgeByNumber(edges=pickedEdges, number=4)
##
##  Assign element type
##
elemType1 = mesh.ElemType(elemCode=CPE4R, elemLibrary=STANDARD,
    secondOrderAccuracy=OFF, hourglassControl=ENHANCED, distortionControl=OFF)
elemType2 = mesh.ElemType(elemCode=CPE3, elemLibrary=STANDARD)
f = p.faces
faces = f
pickedRegions =(faces, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
##
##  Use structured meshing
##
f = p.faces
pickedRegions = f
p.setMeshControls(regions=pickedRegions, technique=STRUCTURED)
##
##  Generate mesh
##
p.generateMesh()
session.viewports['Viewport: 1'].assemblyDisplay.geometryOptions.setValues(
    geometryEdgesInShaded=OFF, datumPoints=OFF, datumAxes=OFF, datumPlanes=OFF,
    datumCoordSystems=OFF)

session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=OFF)
##
##  Create job
##
mdb.Job(name='Channel', model='standard',
    description='Analysis of the forming of a channel-static')
##
##  Save model database
##
mdb.saveAs('Channel')
##

##
##  Create explicit dynamics model
##
mdb.Model(name='explicit', objectToCopy=mdb.models['standard'])
#: The model "explicit" has been created.

p = mdb.models['explicit'].parts['Blank']
session.viewports['Viewport: 1'].setValues(displayedObject=p)

##
##  add density
##
mdb.models['explicit'].materials['log'].Density(table=((7800.0, ), ))

p = mdb.models['explicit'].parts['Holder']
session.viewports['Viewport: 1'].setValues(displayedObject=p)

##
##  add point mass to holder
##
r = p.referencePoints
refPoints=(r[2], )
region = regionToolset.Region(referencePoints=refPoints)
mdb.models['explicit'].parts['Holder'].engineeringFeatures.PointMassInertia(
    name='mass', region=region, mass=0.1, alpha=0.0,
    composite=0.0)

a = mdb.models['explicit'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)

##
##  delete all but first step
##
del mdb.models['explicit'].steps['Move punch']

##
##  define set containing blank
##
f1 = a.instances['Blank-1'].faces
faces1 = f1
a.Set(faces=faces1, name='blank')

##
##  replace the remaining static step with an explicit dynamics step
##
mdb.models['explicit'].ExplicitDynamicsStep(name='Holder force',
    previous='Initial', maintainAttributes=True, timePeriod=0.0001)

##
##  create a second explicit dynamics step
##
mdb.models['explicit'].ExplicitDynamicsStep(name='Move punch',
    previous='Holder force', timePeriod=0.007,
    description='Apply punch stroke')

##
##  define mass scaling
##
regionDef=mdb.models['explicit'].rootAssembly.sets['blank']
mdb.models['explicit'].steps['Holder force'].setValues(massScaling=((
    SEMI_AUTOMATIC, regionDef, AT_BEGINNING, 5.0, 0.0, None, 0, 0, 0.0,
    0.0, 0, None), ))

##
##  request RF2, U2 history output for punch reference point
##
regionDef=mdb.models['explicit'].rootAssembly.sets['RefPunch']
mdb.models['explicit'].HistoryOutputRequest(name='H-Output-2',
    createStepName='Holder force', variables=('U2', 'RF2'),
    region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE,
    filter=ANTIALIASING)

##
##  define smooth step amplitude curves
##
mdb.models['explicit'].SmoothStepAmplitude(name='smooth1', timeSpan=STEP,
    data=((0.0, 0.0), (0.0001, 1.0)))
mdb.models['explicit'].SmoothStepAmplitude(name='smooth2', timeSpan=STEP,
    data=((0.0, 0.0), (0.007, 1.0)))
##
##  use smooth step amplitude for holder force
##
mdb.models['explicit'].loads['RefHolderForce'].setValues(amplitude='smooth1')

##
##  use smooth step amplitude for punch bc
##
mdb.models['explicit'].boundaryConditions['RefPunchBC'].setValuesInStep(
    stepName='Move punch', u2=-0.030, amplitude='smooth2')

elemType1 = mesh.ElemType(elemCode=CPE4R, elemLibrary=EXPLICIT,
    secondOrderAccuracy=OFF, hourglassControl=ENHANCED, distortionControl=OFF)
elemType2 = mesh.ElemType(elemCode=CPE3, elemLibrary=EXPLICIT)

p = mdb.models['explicit'].parts['Blank']
f = p.faces
faces = f
pickedRegions =(faces, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))

a.regenerate()
p.generateMesh()

##
##  create job
##
mdb.Job(name='expChannel', model='explicit',
    description='Analysis of the forming of a channel-quasistatic')

a = mdb.models['standard'].rootAssembly
a.regenerate()
a = mdb.models['explicit'].rootAssembly
a.regenerate()

mdb.save()


