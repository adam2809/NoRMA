thickness = 3.02
gap = 3.12
hole_r = 5.09/2+0.2
outer_radius = 14.88/2
slot_depth = 15.66
base_height = 15
hole_height = 10
nut_diameter = 9
nut_thickness = 4
nut_holder_r = (nut_diameter + 2.4)/2

def mount_part(wp,origin,is_nut):
    res = (wp
      .box(outer_radius*2,thickness,base_height,centered=[True,True,False])
      .faces('>Y').workplane(centerOption='CenterOfMass',offset=-thickness)
      .center(0,base_height/2)
      .cylinder(thickness,outer_radius,centered=[True,True,False])
      .faces('>Y').workplane(centerOption='CenterOfBoundBox')
      .center(0,-(base_height+outer_radius)/2+base_height)
    )
    if is_nut:
      res = (res
        .cylinder(nut_thickness,nut_holder_r)
        .faces('>Y').workplane(centerOption='CenterOfBoundBox')
        .polygon(6,nut_diameter)
        .cutBlind(-nut_thickness)
        .faces('>Y').workplane(centerOption='CenterOfBoundBox')
        .hole(hole_r*2)
      )
    else:
      res = res.hole(hole_r*2)

    res = res
    return res

def gopro_mount(origin_x):
    origin_y = -(gap+thickness)
    nut_truth = [False,False,True]
    res = []
    for i in range(3):
        origin = (origin_x,origin_y,0)
        wp = cq.Workplane(origin=origin)
        mount = mount_part(wp,origin,nut_truth[i])
        origin_y += gap+thickness
        res.append(mount)#.rotateAboutCenter((0,1,0),180)
    return res

