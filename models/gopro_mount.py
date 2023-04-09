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

def mount_part(wp,is_nut):
    res = (wp
      .box(outer_radius*2,thickness,base_height,centered=[True,True,False])
      .faces('+Y').workplane(centerOption='CenterOfMass',offset=-thickness)
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

def gopro_mount(get_wp):
    origin_y = -(gap+thickness)

    mount = (cq
      .Workplane('XY',origin=(0,origin_y,0))
    )
    mount = mount_part(mount,False)
    origin_y += gap+thickness
    show_object(mount)

    mount = (cq
      .Workplane('XY',origin=(0,origin_y,0))
    )
    mount = mount_part(mount,False)
    origin_y += gap+thickness
    show_object(mount)

    mount = (cq
      .Workplane('XY',origin=(0,origin_y,0))
    )
    mount = mount_part(mount,True)
    show_object(mount)
