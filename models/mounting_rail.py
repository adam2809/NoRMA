rail_height = 33
rail_depth = rail_height

clamp_width = 40
clamp_thick = 4
clamp_height = clamp_thick*2 + rail_height
clamp_depth = clamp_thick*2 + rail_depth
bolt_piece_depth = 5.8
bolt_piece_width = 10 

clamp_whole = (cq
  .Workplane('XY')
  .box(clamp_width,clamp_depth,clamp_height)
  .faces('+X').workplane()
  .rect(rail_height,rail_depth)
  .cutThruAll()
)
show_object(clamp_whole)
cont = (clamp_whole
  .faces('>Z').workplane(centerOption='CenterOfMass')
  .pushPoints([
    [(clamp_width-bolt_piece_width/2)/2,0],
    [-(clamp_width-bolt_piece_width/2)/2,0]
  ])
  .rect(bolt_piece_width/2,bolt_piece_depth*2)
)

debug(cont)
