pcb_size = [30,35,1.2]
holes_rect = [23,28]
holes_radious = 1.5
port_width = 8
port_height = 4


prongs_stickout = 5
prongs_length = pcb_size[2] + prongs_stickout
prongs_radious = holes_radious*2 - 0.1

box_thickness = 1.2
box_height = prongs_length + box_thickness

socket_length = box_height - pcb_size[2] - box_thickness
socket_radious = holes_radious + 1.25
socket_bore_radious = holes_radious

box_width = box_thickness*2 + holes_rect[0] + socket_radious*4 + 1.5
box_depth = box_thickness*2 + holes_rect[1] + socket_radious*4 + 1.5

port_slot = (cq
  .Workplane('XZ',(0,box_depth/2,0))
  .box(port_width,box_height-pcb_size[2],box_thickness*3)
)
bottom = (cq
  .Workplane('XY')
  .box(box_width,box_depth,box_height-box_thickness)        
  .faces('+Z')
  .shell(box_thickness)
  .faces('<Z[-2]').workplane()
  .rect(*holes_rect,forConstruction=True)
  .vertices()
  .cylinder(prongs_length,prongs_radious,centered=[True,True,False])
)
cont = (bottom
  .cut(port_slot)
)
show_object(cont)
 #.faces('>Z').workplane()
 #.rect(box_width - box_thickness*2,box_depth - box_thickness*2)
 #.extrude(-box_height+box_thickness,'cut')
