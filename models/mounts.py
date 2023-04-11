from cadquery import exporters
import cadquery as cq


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
caster_rail_mount_gap = rail_mount_width/3

rail_mount_screw_hole_length = 8
rail_mount_screw_hole_r = 8/2
rail_mount_screw_stickout_length = 7
rail_mount_cbore_length = 1

m3_hole_r = 3.1/2
m3_nut_d = 6.3
m3_nut_length = 2.2

def rail_mount(width,gap,to_subtract,mount_count=2,is_vertical_mount=True):
    res = (cq
      .Workplane()
      .box(rail_mount_length,width,width)
    )
    screw_holes_base = (cq
      .Workplane()
      .rect(rail_mount_length/2,width)
      .vertices()
      .box(rail_mount_screw_hole_r*2,rail_mount_screw_stickout_length*2,gap+rail_mount_screw_hole_length*2)
      #.cylinder(gap+rail_mount_screw_hole_length*2,m3_hole_r)
    )

    def get_holes_rect(z_offset=0): 
        return (cq
          .Workplane(origin=(0,0,z_offset))
          .rect(rail_mount_length/2,width+rail_mount_screw_stickout_length*2,forConstruction=True)
          .vertices()
        )

    screw_holes_circle = (
      get_holes_rect()
      .cylinder(gap+rail_mount_screw_hole_length*2,rail_mount_screw_hole_r)
    )

    screw_holes_holes = (
      get_holes_rect()
      .vertices()
      .cylinder(gap+rail_mount_screw_hole_length*2,m3_hole_r)
    )

    screw_holes_hex = (
      get_holes_rect(-(gap/2+rail_mount_screw_hole_length))
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

    dual_mount_y_offset = (rod_width+get_gopro_mount_width(3))/2 if mount_count == 2 else 0

    rotation = 180 if is_vertical_mount else 90
    

    for m in gopro_mount(0):
        m = m.rotate((0,0,1),(0,0,0),rotation)
        res += m.translate((0,-dual_mount_y_offset,width/2))

    if mount_count == 2:
        for m in gopro_mount(0):
            res += m.translate((0,dual_mount_y_offset,width/2))


    (top,bottom) = (res
      .faces('<Z').workplane(offset=-width/2)
      .split(keepBottom=True,keepTop=True)
      .all()
    )
    top -= cq.Workplane().box(1000,1000,gap) + to_subtract
    bottom -= cq.Workplane().box(1000,1000,gap) + to_subtract

    return [top,bottom]




def imu_box():
    pcb_size = [30,35,1.2]
    holes_rect = [23,28]
    holes_radious = 1.5
    port_hole_width = 10
    port_hole_height = 5

    nut_thickness = 2
    nut_r = 3
    nut_head_r = 3
    bolt_shaft_length = 18

    box_thickness = 2.8
    box_height_i = bolt_shaft_length - nut_thickness - box_thickness/2 + 0.1
    box_width_i = pcb_size[0] + 5
    box_depth_i = pcb_size[1] + 5

    box_width = box_width_i + box_thickness*2
    box_depth = box_depth_i + box_thickness*2
    box_height = box_height_i + box_thickness*2

    port_slot = (cq
      .Workplane('XZ',(0,box_depth/2,-(box_height_i-port_hole_height)/2))
      .box(port_hole_width,port_hole_height,box_thickness*3)
    )

    hex_holes = (cq
      .Workplane('XY',(0,0,0))
      .sketch()
      .push([
          (holes_rect[0]/2,holes_rect[1]/2),
          (-holes_rect[0]/2,-holes_rect[1]/2),
          (holes_rect[0]/2,-holes_rect[1]/2),
          (-holes_rect[0]/2,holes_rect[1]/2)
      ])
      .regularPolygon(nut_r+0.1,6)
      .finalize()
      .extrude(nut_thickness+0.1)
    )
    box = (cq
      .Workplane('XY',(0,0,0))
      .box(box_width_i,box_depth_i,box_height_i)        
      .shell(box_thickness)
      .faces('<Z[-2]').workplane()
      .rect(*holes_rect,forConstruction=True)
      .vertices()
      .hole(holes_radious*2+0.1)
      .cut(port_slot)
      .faces("<Z")
      .sketch()
      .push([
          (holes_rect[0]/2,holes_rect[1]/2),
          (-holes_rect[0]/2,-holes_rect[1]/2),
          (holes_rect[0]/2,-holes_rect[1]/2),
          (-holes_rect[0]/2,holes_rect[1]/2)
      ])
      .regularPolygon(3.05,6,90)
      .finalize()
      .cutBlind(nut_thickness+0.1)
      .faces('>Z')
      .rect(*holes_rect,forConstruction=True)
      .vertices()
      .cboreHole(holes_radious*2+0.1,nut_head_r*2+0.1,box_thickness/2)
    )
    (lid, bottom) = box.faces(">Z").workplane(-box_thickness).split(keepTop=True, keepBottom=True).all()  # splits into two solids
    (washers,lid) = (lid
      .faces("<Z").workplane()
      .rect(*holes_rect,forConstruction=True)
      .vertices()
      .cylinder(box_height_i-pcb_size[2], nut_r,centered=[True,True,False])
      .faces("<Z").workplane()
      .rect(*holes_rect,forConstruction=True)
      .vertices()
      .hole(holes_radious*2)
      .faces("<Z[-2]")
      .split(keepTop=True, keepBottom=True).all()  # splits into two solids
    )
    
    for p in gopro_mount(90,2):
        bottom+=p.rotate((0,0,1),(0,0,0),90).translate((0,-(base_height+box_depth/2),-outer_radius*2))
    return [lid,bottom]



def caster_dual_rail_mount():
    return rail_mount(
        rail_mount_width,
        caster_rail_mount_gap,
        cq.Workplane('YZ').cylinder(1000,rail_mount_ir)
    )

rear_rail_mount_height = 30
rear_rail_mount_depth = 30
rear_rail_mount_width_e = 33
rear_rail_mount_gap = rear_rail_mount_width_e/3
def rear_rail_mount():
    return rail_mount(
        rear_rail_mount_width_e,
        rear_rail_mount_gap,
        cq.Workplane('YZ').box(rear_rail_mount_depth,rear_rail_mount_height,1000),
        1,False
    )
#m5x20 - 10
#m3x32 - 10
#m2.5  - 5
show_object(rear_rail_mount())
#show_object(caster_dual_rail_mount())


export = 0
if export == 1:
    exporters.export(rod(),'stls/rod.stl')
    exporters.export(lidar_box(),'stls/lidar_box.stl')
    exporters.export(rail_mount()[0],'stls/rail_mount_top.stl')
    exporters.export(rail_mount()[1],'stls/rail_mount_bottom.stl')
    exporters.export(imu_box()[0],'stls/imu_box_top.stl')
    exporters.export(imu_box()[1],'stls/imu_box_bottom.stl')

