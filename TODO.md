### Software

- measure dimenstions and find values for TF transforms:
  - can be derived from urdf [tutorial](https://articulatedrobotics.xyz/ready-for-ros-6-tf/)
- measure parameters for Shared-DWA:
  - footprint (input in shared-dwa repo rtcus_shared_dwa/launch/shared_dwa_demo.launch:14)
  - kinedynamic values (input in shared-dwa repo rtcus_shared_dwa/launch/shared_dwa_demo.launch:12)
    - linear_forward_speed_limit
    - linear_backwards_speed_limit
    - linear_acceleration_limit
    - linear_brake_limit
    - angular_speed_limit
    - angular_acceleration_limit
    - for measuring linear values use accelerometer and for angular use gyroscope maybe use https://github.com/Wojtek120/IMU-velocity-and-displacement-measurements for greater accuracy
  - clearence parameters (input in shared-dwa repo rtcus_shared_dwa/launch/shared_dwa_demo.launch:12) the ones provided in rtcus_shared_dwa/config/clearance_parameters/shared_control_wheelchair.yaml

- interface sonar data with Shared-DWA (edit the default file rtcus_shared_dwa/config/shared_dwa_default_config.yaml)
- make lights react to joystick position and Shared-DWA output

- develop simulator:
  - simplify by just having a box on two wheels with roughly the same dimensions as the robot 
  - add sonar sensors example [how to add them](https://answers.ros.org/question/260131/adding-ultrasonic-sensor-to-the-robot/)
### Hardware
- research integration of many sonar sensors with ros
- develop sonar sensor holders and their attachmments
- rgb led ring with underglow
- speakers and theier sound
