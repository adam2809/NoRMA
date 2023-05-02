To evaluate the odometry provided by the combination of laser\_scan\_matcher and robot\_localization a test was conducted in the robotics lab of the University of Nottingham. A grid made of adhesive tape on the floor was used to provide a consistant point of reference. Three points on the grid were chosen - a starting one (point 0), one 140 cm in front (point 1), one 90 cm to the left (point 2) and red tape was used to mark them to distinguish from the black color of the rest of the grid. A hole in the wheelchairs footrest was used to line up with each point. The wheelchair was first parked on the point 0 and facing point 1. The second step was to drive it to line up with point 1 but turn 90 degrees to the left . This was repeated to reach point 2. Lastly a sharp 180 degree turn was made to come back to point 0. Both angular and linear velocities were kept below 0.3 m/s. This test replicates many conditions which the autonomous system has to be ready for. Those include driving straight (from point 0 to point 1), making a short sharp turn (turning 90 degrees into point 1), a long turn (from point 1 to point 2), sharp long turn (turning when going from point 2 to 0) and microadjustments (when lining up the wheelchair with each point). Tests were conducted three times with the imu support enabled in the laser\_scan\_matcher configuration and three times without. The results presented below are representative of each repeat.

yaw
point | expected | actual
0     | 0        | 359.5
1     | 90       | 89.5 
2     | 180      | 180.5

x
point | expected | actual
0     | 0        | 359.5
1     | 140      | 89.5 
2     | 0        | 180.5

y
point | expected | actual
0     | 0        | 359.5
1     | 0        | 89.5 
2     | 90       | 180.5


The results are similar for both configurations when looking at the y and yaw values but vary signigicantly when considering x. In the test with the IMU there is a significant error introduced on the last sharp 180 degree turn. This suggests an issue with either the quality of the sensor or its calibration as this odometry methodology was originally tested with IMU input \cite{laser\_scan\_matcher\_paper}. Without it the results were more than sufficient to provide the necessary odometry accuracy so the issue was not investigated further. Since the project is being developed with simplicity and cost in mind the IMU will not be mentioned in the final build guide for reasons of parts reduction as the lidar only soluiton is sufficient.
