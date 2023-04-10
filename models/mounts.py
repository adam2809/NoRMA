from cadquery import exporters

thickness = 3.02
gap = 3.12
hole_r = 5.09/2+0.2
outer_radius = 14.88/2
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
        origin_y = -(gap+thickness)/2
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

def get_gopro_mount_width(parts):
    return thickness*(parts-1) + gap*parts

rod_width = 20
rod_depth = rod_width
rod_height = 180
rod_taper_offset = 30
dual_mount_y_offset = (rod_width+get_gopro_mount_width(3))/2
def rod():
    res = (cq
      .Workplane()
      .box(rod_width,rod_depth,rod_height,centered=[True,True,False])
    ) 
    res = (res
      .faces('<Z').workplane(offset=-rod_height+rod_taper_offset)
      .rect(rod_width,rod_width)
      .workplane(offset=-rod_height-(-rod_height+rod_taper_offset))
      .rect(rod_width,get_gopro_mount_width(3)*2+rod_width)
      .loft(combine=True)
    )

    for part in gopro_mount(0,2):
        part=part.translate((0,dual_mount_y_offset,rod_height))
        res+=part
    for part in gopro_mount(0,2):
        part=part.translate((0,-dual_mount_y_offset,rod_height))
        res+=part
    for part in gopro_mount(180,2):
        part=part.translate((0,0,-base_height*2))
        part = part.rotate((0,0,1),(0,0,0),90)
        res+=part
    return res




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

rail_mount_ir = 35.5/2
rail_mount_width = rod_width+2*get_gopro_mount_width(3)
rail_mount_length = 55
rail_mount_gap = rail_mount_width/3

rail_mount_screw_hole_length = 8
rail_mount_screw_hole_r = 8/2
rail_mount_screw_stickout_length = 7
rail_mount_cbore_length = 1

m3_hole_r = 3.1/2
m3_nut_d = 6.3
m3_nut_length = 2.2

def rail_mount():
    res = (cq
      .Workplane()
      .box(rail_mount_length,rail_mount_width,rail_mount_width)
    )
    screw_holes_base = (cq
      .Workplane()
      .rect(rail_mount_length/2,rail_mount_width)
      .vertices()
      .box(rail_mount_screw_hole_r*2,rail_mount_screw_stickout_length*2,rail_mount_gap+rail_mount_screw_hole_length*2)
      #.cylinder(rail_mount_gap+rail_mount_screw_hole_length*2,m3_hole_r)
    )

    def get_holes_rect(z_offset=0): 
        return (cq
          .Workplane(origin=(0,0,z_offset))
          .rect(rail_mount_length/2,rail_mount_width+rail_mount_screw_stickout_length*2,forConstruction=True)
          .vertices()
        )

    screw_holes_circle = (
      get_holes_rect()
      .cylinder(rail_mount_gap+rail_mount_screw_hole_length*2,rail_mount_screw_hole_r)
    )

    screw_holes_holes = (
      get_holes_rect()
      .vertices()
      .cylinder(rail_mount_gap+rail_mount_screw_hole_length*2,m3_hole_r)
    )

    screw_holes_hex = (
      get_holes_rect(-(rail_mount_gap/2+rail_mount_screw_hole_length))
      .vertices()
      .polygon(6,m3_nut_d)
      .extrude(m3_nut_length)
    )
    
    res += (
       screw_holes_base
      +screw_holes_circle
      -screw_holes_holes
      -screw_holes_hex
      
    )
    for m in gopro_mount(0):
        res += m.translate((0,dual_mount_y_offset,rail_mount_width/2))

    for m in gopro_mount(0):
        m = m.rotate((0,0,1),(0,0,0),180)
        res += m.translate((0,-dual_mount_y_offset,rail_mount_width/2))

    (top,bottom) = (res
      .faces('<Z').workplane(offset=-rail_mount_width/2)
      .split(keepBottom=True,keepTop=True)
      .all()
    )
    top -= cq.Workplane().box(1000,1000,rail_mount_gap) + cq.Workplane('YZ').cylinder(1000,rail_mount_ir)
    bottom -= cq.Workplane().box(1000,1000,rail_mount_gap) + cq.Workplane('YZ').cylinder(1000,rail_mount_ir)

    return [top,bottom]
res = (cq
  .Workplane()
  .rect(0.75,1.5)
  .workplane(offset=3.0)
  .rect(0.75, 0.5)
  .loft(combine=True)
)
show_object(rail_mount())

export = 1
if export == 1:
    exporters.export(rod(),'stls/rod.stl')
    exporters.export(lidar_box(),'stls/lidar_box.stl')
    exporters.export(rail_mount()[0],'stls/rail_mount_top.stl')
    exporters.export(rail_mount()[1],'stls/rail_mount_bottom.stl')

