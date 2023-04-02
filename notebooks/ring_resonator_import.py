from ngsolve import *
from netgen.geom2d import SplineGeometry

geo = SplineGeometry()

xneg  =-0.43
xpos  = 0.43
yneg  =-0.48
ypos  = 0.48
wslab = 0.04
cringx = 0.0
cringy = 0.0
rring = 0.4
gap   = 0.005

pntx = [xneg,xpos]
pnty = [yneg,-rring-gap-wslab,-rring-gap,rring+gap,rring+gap+wslab,ypos]

pts = [geo.AddPoint(xi,yi) for yi in pnty for xi in pntx]

### geometry #######################################################
geo.Append (["line", pts[0], pts[1]], leftdomain=1, rightdomain=0)
geo.Append (["line", pts[1], pts[3]], leftdomain=1, rightdomain=0)
geo.Append (["line", pts[3], pts[2]], leftdomain=1, rightdomain=2)
geo.Append (["line", pts[2], pts[0]], leftdomain=1, rightdomain=0)

geo.Append (["line", pts[3], pts[5]], leftdomain=2, rightdomain=0,bc="normal_wg_rightbottom")
geo.Append (["line", pts[5], pts[4]], leftdomain=2, rightdomain=3)
geo.Append (["line", pts[4], pts[2]], leftdomain=2, rightdomain=0,bc="normal_wg_leftbottom")

geo.Append (["line", pts[5], pts[7]], leftdomain=3, rightdomain=0)
geo.Append (["line", pts[7], pts[6]], leftdomain=3, rightdomain=4)
geo.Append (["line", pts[6], pts[4]], leftdomain=3, rightdomain=0)

geo.Append (["line", pts[7], pts[9]], leftdomain=4, rightdomain=0,bc="normal_wg_righttop")
geo.Append (["line", pts[9], pts[8]], leftdomain=4, rightdomain=5)
geo.Append (["line", pts[8], pts[6]], leftdomain=4, rightdomain=0,bc="normal_wg_lefttop")

geo.Append (["line", pts[9], pts[11]], leftdomain=5, rightdomain=0)
geo.Append (["line", pts[11], pts[10]], leftdomain=5, rightdomain=0)
geo.Append (["line", pts[10], pts[8]], leftdomain=5, rightdomain=0)

geo.AddCircle(c=(cringx,cringy), r=rring, leftdomain=6, rightdomain=3)
geo.AddCircle(c=(cringx,cringy), r=rring-wslab, leftdomain=7, rightdomain=6)

for i in (1,3,5,7):
    geo.SetMaterial(i, "air")
for i in (2,4,6):
    geo.SetMaterial(i, "eps_nine")
data = geo.CreatePML(0.05)
normals = data["normals"]




mesh = Mesh(geo.GenerateMesh(maxh=0.05))

eps_r = {"air" : 1, "eps_nine" : 3**3}

for mat in mesh.GetMaterials():
    if mat.startswith("pml_normal_wg"):
        eps_r[mat] = eps_r["eps_nine"]

for mat in mesh.GetMaterials():
    if mat not in eps_r:
        eps_r[mat] = eps_r["air"]



### Parameters for Source field ##########################################################################
wavelength = 1.542
fcen       = 5/wavelength
df         = 0.1
tpeak      = 1
order = 3

mesh.Curve(order)
fes_facet = FacetFESpace(mesh, order=order+1)
gfsource = GridFunction(fes_facet)

source_cf =  sin( (pi/wslab)*(y-pnty[3]) ) 
gfsource.Set(source_cf,definedon=mesh.Boundaries("normal_wg_lefttop"))


##########################################################################################################

