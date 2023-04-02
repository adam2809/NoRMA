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

show_object(bottom)
show_object(lid)
show_object(washers)
