#
# Getting Started with Abaqus
#
# Script for springback portion of channel example
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

a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
openMdb('Channel.cae')
a = mdb.models['explicit'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)

##
##  Springback analysis model
##

mdb.Model(name='import', objectToCopy=mdb.models['explicit'])

a = mdb.models['import'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)

a.deleteFeatures(('Punch-1', 'Holder-1', 'Die-1', ))
del mdb.models['import'].rootAssembly.sets['RefDie']
del mdb.models['import'].rootAssembly.sets['RefHolder']
del mdb.models['import'].rootAssembly.sets['RefPunch']
del mdb.models['import'].rootAssembly.surfaces['BlankBot']
del mdb.models['import'].rootAssembly.surfaces['BlankTop']
del mdb.models['import'].rootAssembly.surfaces['DieSurf']
del mdb.models['import'].rootAssembly.surfaces['HolderSurf']
del mdb.models['import'].rootAssembly.surfaces['PunchSurf']
mdb.models['import'].interactions.delete(
    ('Die-Blank', 'Holder-Blank', 'Punch-Blank', ))
del mdb.models['import'].interactionProperties['Fric']
del mdb.models['import'].interactionProperties['NoFric']
del mdb.models['import'].steps['Move punch']
del mdb.models['import'].steps['Holder force']

region = a.sets['Center']
mdb.models['import'].XsymmBC(name='BC-1', createStepName='Initial',
    region=region)

a = mdb.models['import'].rootAssembly
n1 = a.instances['Blank-1'].nodes
nodes1 = n1[2:3]
a.Set(nodes=nodes1, name='MidLeft')

region = a.sets['MidLeft']
mdb.models['import'].VelocityBC(name='BC-2', createStepName='Initial',
    region=region, v1=UNSET, v2=SET, vr3=UNSET, amplitude=UNSET,
    distributionType=UNIFORM, localCsys=None)

mdb.models['import'].StaticStep(name='springback', previous='Initial',
    initialInc=0.1, nlgeom=ON, stabilizationMagnitude=0.0002,
    stabilizationMethod=DISSIPATED_ENERGY_FRACTION, adaptiveDampingRatio=0.0)

instances=(a.instances['Blank-1'], )
mdb.models['import'].InitialState(updateReferenceConfiguration=OFF,
    fileName='expChannel', endStep=LAST_STEP, endIncrement=STEP_END,
    name='Field-1', createStepName='Initial', instances=instances)

mdb.Job(name='springback', model='import',
    description='Analysis of the forming of a channel-springback')

a = mdb.models['import'].rootAssembly
a.regenerate()

mdb.save()