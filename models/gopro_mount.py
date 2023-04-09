thickness = 3.02
gap = 3.12
hole_r = 5.09/2+0.2
outer_radius = 14.88/2
slot_depth = 15.66
base_height = 15
hole_height = 10

def mount_part(wp):
    return (wp
      .box(outer_radius*2,thickness,base_height,centered=[True,True,False])
      .faces('+Y').workplane(centerOption='CenterOfMass',offset=-thickness)
      .center(0,base_height/2)
      .cylinder(thickness,outer_radius,centered=[True,True,False])
      .faces('+Y').workplane(centerOption='CenterOfBoundBox')
      .center(0,-(base_height+outer_radius)/2+base_height)
      .hole(hole_r)
    )

#mount = (cq
#  .Workplane('XY')
#  .box(outer_radius*2,thickness,base_height,centered=[True,True,False])
#  .faces('+Y').workplane(centerOption='CenterOfMass',offset=-thickness)
#  .center(0,base_height/2)
#  .cylinder(thickness,outer_radius,centered=[True,True,False])
#  .faces('+Y').workplane(centerOption='CenterOfBoundBox')
#  .center(0,-(base_height+outer_radius)/2+base_height)
#  .hole(hole_r)
#)
parts = []
origin_y = -(gap+thickness)

for i in range(3):
    mount = (cq
      .Workplane('XY',origin=(0,origin_y,0))
    )
    mount = mount_part(mount)
    origin_y += gap+thickness
    
    show_object(mount)

