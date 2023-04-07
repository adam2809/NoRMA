#include "std_msgs/String.h"

#include "ros/ros.h"
#include "std_msgs/Float32MultiArray.h"
#include "sensor_msgs/LaserScan.h"
#include "sensor_msgs/PointCloud2.h"
#include "sensor_msgs/point_cloud2_iterator.h"
#include "laser_geometry/laser_geometry.h"
#include <tf/transform_listener.h>
#include <pcl_ros/point_cloud.h>



int main(int argc, char **argv)
{
    ros::init(argc, argv, "scan_merger");
    ros::NodeHandle n;

    std::string frame_id_;
    ros::Publisher cloud_pub_;
    tf::TransformListener tfListener_;
    laser_geometry::LaserProjection projector_;


    cloud_pub_ = n.advertise<sensor_msgs::PointCloud2>("cloud", 10);
    ros::Duration duration = ros::Duration(10.0);
    ros::Rate loop_rate(duration);

    while (ros::ok())
    {

        boost::shared_ptr<sensor_msgs::LaserScan const> scan_ptr;
        sensor_msgs::PointCloud2 cloud_rear;
        sensor_msgs::PointCloud2 cloud_front;
        sensor_msgs::PointCloud2 cloud_merged;

        scan_ptr = ros::topic::waitForMessage<sensor_msgs::LaserScan>("/scan_laser_rear", ros::Duration(1));
        projector_.transformLaserScanToPointCloud("base_link", *scan_ptr, cloud_rear, tfListener_);

        if (scan_ptr == NULL)
            ROS_WARN("No laser messages received from the rear");

        scan_ptr = ros::topic::waitForMessage<sensor_msgs::LaserScan>("/scan_laser_front", ros::Duration(1));
        projector_.transformLaserScanToPointCloud("base_link", *scan_ptr, cloud_front, tfListener_);

        if (scan_ptr == NULL)
            ROS_WARN("No laser messages received from the front");

        pcl::concatenatePointCloud(cloud_rear, cloud_front, cloud_merged);
        cloud_merged.fields[3].name = "intensity";
        cloud_merged.header.frame_id = "base_link";
        cloud_pub_.publish(cloud_merged);

        ros::spinOnce();

        loop_rate.sleep();
    }
}
