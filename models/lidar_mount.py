from cadquery import exporters
lidar_box_width = 50
lidar_box_depth = 50
lidar_box_height = 41
lidar_box_thick = 2.4

rail_mount_ir = 35/2
rail_mount_er = 38.4/2
rail_mount_length = 55

internal_diagonal_holes = 54 
external_diagonal_holes = 59


screw_head_radious = 3.5
screw_hole_radious = 2
cbore_length = 1

rod_length = 94+rail_mount_length/2
rod_thick = 18

gopro_mount_length = 30
gopro_mount_hole_offset = 20
gopro_mount_thick = 6
#screw hole to end of stuff 94

screw_hole = (cq
  .Workplane('XY')
  .cylinder(1000,screw_hole_radious)
)

cbore = (cq
  .Workplane('XY',origin=(0,0,-(rail_mount_er)))
  .cylinder(cbore_length,screw_head_radious,centered=[True,True,False])
)

lidar_attachment = (cq
  .Workplane('XY')
  .box(rail_mount_er+16,rail_mount_length,rail_mount_er*2,centered=[False,True,True])
)

cutoff_bottom = (cq
  .Workplane()
  .box(rail_mount_er*2,rail_mount_length,rail_mount_er,centered=[True,True,False])
)

cutoff_middle = (cq
  .Workplane('ZX')
  .cylinder(rail_mount_length,rail_mount_ir)
)

rail_mount = (cq
  .Workplane('XZ')
  .cylinder(rail_mount_length,rail_mount_er)
) + lidar_attachment - screw_hole - cutoff_bottom -cutoff_middle - cbore
with_holes = (rail_mount
  .faces('>X').workplane(centerOption='CenterOfMass')
  .pushPoints([[-rail_mount_length/3,0],[rail_mount_length/3,0]])
  .hole(3,10)
)

lidar_rod = (cq
  .Workplane('XY')
  .box(rod_length,rod_thick,rod_thick)
  .faces('>X').workplane(centerOption='CenterOfMass')
  .pushPoints([[-(rod_thick-gopro_mount_thick)/2,0],[(rod_thick-gopro_mount_thick)/2,0]])
  .box(gopro_mount_thick,rod_thick,gopro_mount_length,centered=[True,True,False])
  .faces('>Y[1]').workplane(centerOption='CenterOfMass')
  .center((gopro_mount_length/2-gopro_mount_hole_offset),0)
  .hole(3,1000)

  .faces('>Y').workplane()
  .polygon(6,3.03*2)
  .cutBlind(-2)

  .faces('>Y[2]').workplane(centerOption='CenterOfMass')
  .center(-(gopro_mount_length/2-gopro_mount_hole_offset),0)
  .hole(3,1000)
  .faces('>Y').workplane(centerOption='CenterOfMass')
  .center(33,0)
  .pushPoints([[-rail_mount_length/3,0],[rail_mount_length/3,0]])
  .cboreHole(3,6.5,14)
)

cutout_lidar_box = (cq
  .Workplane(origin=(0,0,-(lidar_box_height/2-lidar_box_thick)))
  .cylinder(1000,lidar_box_width/2,centered=[True,True,False])
)

 

lidar_attachment = (cq
  .Workplane(origin=(0,0,-(lidar_box_height+lidar_box_thick)/2))
  .box(lidar_box_width/2+lidar_box_thick+gopro_mount_length,gopro_mount_thick-0.05,rod_thick,centered=[False,True,False])
  .faces('>Y').workplane(centerOption='CenterOfMass')
  .center(-(lidar_box_width/2+lidar_box_thick+gopro_mount_length)/2+(gopro_mount_length-gopro_mount_hole_offset),0)
  .hole(3)
)

lidar_popout = (cq
  .Workplane(origin=(0,0,-(lidar_box_height/2-lidar_box_thick)))
  .cylinder(1000,7)
)

lidar_box = (cq
  .Workplane('XY')
  .cylinder(lidar_box_height+lidar_box_thick,lidar_box_width/2+0.1+lidar_box_thick)
) + lidar_attachment  - cutout_lidar_box -lidar_popout

show_object(lidar_rod)
exporters.export(lidar_box,'stls/lidar_box.stl')
exporters.export(lidar_rod,'stls/lidar_rod.stl')
exporters.export(with_holes,'stls/rail_mount.stl')
#debug(lidar_attachment)
