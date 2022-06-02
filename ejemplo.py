from abaqus import *
from abaqusConstants import *



# functions



def Create_Part_3D_Cylinder(radius,length,thickness,part,model):
    s1 = mdb.models[model].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(radius, 0.0))
    s1.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(radius-thickness, 0.0))
    p = mdb.models[model].Part(name=part, dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p = mdb.models[model].parts[part]
    p.BaseSolidExtrude(sketch=s1, depth=length)
    s1.unsetPrimaryObject()
    p = mdb.models[model].parts[part]
    del mdb.models[model].sketches['__profile__']


def Create_Datum_Plane_by_Principal(type_plane,part,model,offset_plane):
    p = mdb.models[model].parts[part]
    p.DatumPlaneByPrincipalPlane(principalPlane=type_plane, offset=offset_plane)


def Create_Set_All_Cells(model,part,set_name):
    p = mdb.models[model].parts[part]
    c = p.cells[:]
    p.Set(cells=c, name=set_name)


def Create_Material_Data(model,material_name,e11,e22,e33,nu12,nu13,nu23,g12,g13,g23,lts,lcs,tts,tcs,lss,tss):
    mdb.models[model].Material(name=material_name)
    mdb.models[model].materials[material_name].Elastic(type=ENGINEERING_CONSTANTS, table=((e11,e22,e33,nu12,nu13,nu23,g12,g13,g23), ))
    mdb.models[model].materials[material_name].HashinDamageInitiation(table=((lts,lcs,tts,tcs,lss,tss), ))

def Create_Set_Face(x,y,z,model,part,set_name):
    face = ()
    p = mdb.models[model].parts[part]
    f = p.faces
    myFace = f.findAt((x,y,z),)
    face = face + (f[myFace.index:myFace.index+1], )
    p.Set(faces=face, name=set_name)

def Create_Assembly(model,part,instance_name):
    a = mdb.models[model].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[model].parts[part]
    a.Instance(name=instance_name, part=p, dependent=ON)

#-------------------------------------------------------------

def Create_Reference_Point(x,y,z,model,setname):
    a = mdb.models[model].rootAssembly
    myRP = a.ReferencePoint(point=(x, y, z))
    r = a.referencePoints
    myRP_Position = r.findAt((x, y, z),)
    refPoints1=(myRP_Position, )
    a.Set(referencePoints=refPoints1, name=setname)
    return myRP,myRP_Position







# variables

myString = "Buckling_Analysis"


myRadius = 25.0
myThickness = 2.5
myLength = 526.0
myModel = mdb.Model(name=myString)
myPart = "Cylinder"

# material parameters

myE11 = 133000
myE22 = 11500
myE33 = 11500
myNu12 = 0.32
myNu13 = 0.32
myNu23 = 0.37
myG12 = 4800
myG13 = 4800
myG23 = 4200

# hashin damage parameters

myLTS = 1200
myLCS = 972
myTTS = 37
myTCS = 147
myLSS = 71.5
myTSS = 32


# create model

Create_Part_3D_Cylinder(myRadius,myLength,myThickness,myPart,myString)

Create_Datum_Plane_by_Principal(XZPLANE,myPart,myString,0.0)
Create_Datum_Plane_by_Principal(XYPLANE,myPart,myString,myLength/2.0)
Create_Datum_Plane_by_Principal(YZPLANE,myPart,myString,0.0)

Create_Set_All_Cells(myString,myPart,"Cylinder_3D")

Create_Set_Face(myRadius-myThickness/2.0,0.0,myLength,myString,myPart,"Set-RP-2")
Create_Set_Face(myRadius-myThickness/2.0,0.0,0.0,myString,myPart,"Set-RP-1")
Create_Set_Face(myRadius,0.0,myLength/2.0,myString,myPart,"Outer_Surface")

Create_Material_Data(myString,"CFRP",myE11,myE22,myE33,myNu12,myNu13,myNu23,myG12,myG13,myG23,myLTS,myLCS,myTTS,myTCS,myLSS,myTSS)

Create_Assembly(myString,myPart,"Cylinder-1")

myRP1,myRP_Position1 = Create_Reference_Point(0.0,0.0,0.0,myString,"RP-1")
myRP2,myRP_Position2 = Create_Reference_Point(0.0,0.0,myLength,myString,"RP-2")