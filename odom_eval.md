To evaluate the odometry provided by the combination of laser\_scan\_matcher and robot\_localization packages a test was conducted in the robotics lab of the University of Nottingham. A grid made of adhesive tape on the floor was used to provide a consistant point of reference. Three points on the grid were chosen - a starting one (point 0), one 140 cm in front (point 1), one 90 cm to the left (point 2) and red tape was used to mark them to distinguish from the black color of the rest of the grid. A hole in the wheelchairs footrest was used to line up with each point. The wheelchair was first parked on the point 0 and facing point 1. The second step was to drive it to line up with point 1 but turn 90 degrees to the left . This was repeated to reach point 2. Lastly a sharp 180 degree turn was made to come back to point 0. Both angular and linear velocities were kept below 0.3 m/s. This test replicates many conditions which the autonomous system has to be ready for. Those include driving straight (from point 0 to point 1), making a short sharp turn (turning 90 degrees into point 1), a long turn (from point 1 to point 2), sharp long turn (turning when going from point 2 to 0) and microadjustments (when lining up the wheelchair with each point). Tests were conducted three times with the imu support enabled in the laser\_scan\_matcher configuration and three times without. The expected x and y values had to be shifted from the position of the grid points approperiately since the odometry is measuring the position of the middle point of the wheel axle while the 'crosshair' used to align with the points is offset by 45cm to the front.

no imu \/
yaw
point | expected | actual
0     | 0        | 359.5 , 354.6 , 355.0
1     | 90       | 89.5  , 86.9  , 88.2
2     | 180      | 180.5 , 177.6 , 178.9

x
point | expected | actual
0     | 0        | -0.36 , -0.18 , 0.02
1     | 1.95     | 1.81  , 1.76  , 1.73
2     | 0.90     | 0.81  , 0.82  , 0.79

y
point | expected | actual
0     | 0        | 0.06  , 0.12  , 0.09
1     | -0.45    | -0.30 , -0.33 , -0.34
2     | 0.9      | 1.06  , 1.05  , 1.01


yes imu \/
yaw
point | expected | actual
0     | 0        | 357.4 , 356.4 , 357.9
1     | 90       | 88.4  , 90.8  , 89.47       
2     | 180      | 179.8 , 180.4 , 180.5            

x
point | expected | actual
0     | 0        | -1.99 , -0.83 , -0.14            
1     | 1.95     | 1.81  , 1.77  , 1.76      
2     | 0.90     | 0.80  , 0.78  , 0.79          

y
point | expected | actual
0     | 0        | -0.3  , 0.02  , 0.07           
1     | -0.45    | -0.31 , -0.32 , -0.34      
2     | 0.9      | 1.07  , 1.02  , 1.00         


The error on return to the starting point on the x axis can be attributed to the keyframes mechanism of the odometry package. It prevents any drift introduced by not completely consistant scans when stationary by only starting to calculate odometry after it detects some amount of movement. In the case of this test it was set to 0.1 meters which explains the final error of around -0.3 as the wheelchair started from stationary three times. The results are similar for both configurations when looking at the y and yaw values but vary signigicantly when considering x. In the test with the IMU there is a significant error introduced on the last sharp 180 degree turn. This suggests an issue with either the quality of the sensor or its calibration as this odometry methodology was originally tested with IMU input \cite{laser\_scan\_matcher\_paper}. Without it the results were more than sufficient to provide the necessary odometry accuracy so the issue was not investigated further. Since the project is being developed with simplicity and cost in mind the IMU will not be mentioned in the final build guide for reasons of parts reduction.
