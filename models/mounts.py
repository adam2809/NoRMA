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

def gopro_mount(rot_hole,parts=3):
    if parts == 3:
        origin_y = -(gap+thickness)
    else:
        origin_y = -gap + (gap-thickness)/2
    nut_truth = [False,False,True]
    res = []
    for i in range(parts):
        origin = (0,origin_y,0)
        wp = cq.Workplane(origin=origin)
        mount = mount_part(wp,origin,nut_truth[i])
        mount = mount.rotate((0,0,base_height),(0,1,base_height),rot_hole)
        origin_y += gap+thickness
        res.append(mount)
    return res

rod_width = 20
rod_depth = rod_width
rod_height = 180

def rod():
    res = (cq
      .Workplane()
      .box(rod_width,rod_depth,rod_height/2,centered=[True,True,False])
    ) 
    for part in gopro_mount(0):
        part=part.translate((0,0,rod_height/2))
        res+=part
    res+=res.mirror('XY')
    return res



rail_mount_ir = 35/2
rail_mount_er = 38.4/2
rail_mount_length = 55



screw_head_radious = 3.5
screw_hole_radious = 2
cbore_length = 1

lidar_box_width_i = 50.2
lidar_box_height_i = 41
lidar_box_thick = 2.4

lidar_box_width = lidar_box_width_i + lidar_box_thick*2
lidar_box_height = lidar_box_height_i + lidar_box_thick

lidar_box_internal_diagonal_holes = 54 
lidar_box_external_diagonal_holes = 59

m25_head_diameter = 5
m25_hole_diameter = 2.7

def lidar_box():

    res = (cq
      .Workplane()
      .box(lidar_box_width,lidar_box_width,lidar_box_height)
      .faces('>Z')
      .rect(lidar_box_width_i,lidar_box_width_i)
      .cutBlind(-lidar_box_height_i)
    )
    res = (res
      .faces('>Y').workplane()
      .center(0,-lidar_box_height_i/2+lidar_box_thick/2)
      .rect(lidar_box_width_i/2,lidar_box_height_i/2,centered=False)
      .cutBlind(-lidar_box_thick)
    )
    res = (res
      .faces('<Z').workplane(centerOption='CenterOfBoundBox').transformed(rotate=(0,0,45))
      .polygon(4,(lidar_box_external_diagonal_holes+lidar_box_internal_diagonal_holes)/2)
      .vertices()
      .cboreHole(m25_hole_diameter,m25_head_diameter,1)
      
    )

    mount_list = gopro_mount(90)
    for mnt in mount_list:
        mnt = mnt.rotate((0,0,base_height),(1,0,base_height),90)
        res+=mnt.translate((base_height+lidar_box_width/2,0,-(base_height+lidar_box_height)/2+0.15))
    return res

show_object(gopro_mount(0,2))
show_object(gopro_mount(0,3))
