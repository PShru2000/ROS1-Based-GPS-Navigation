# ROS1 Based GPS Navigation

## Goal

The goal of this project is to record,publish,and analyze GPS data using GPS Based GNSS puck 

## Overview

This project focuses on acquiring, publishing, and analyzing GPS data using a USB-based GNSS puck in a robotics navigation setting. The objective is to process GPS data from the device, convert latitude and longitude to UTM coordinates, and publish this information via a custom ROS1 message. Additionally, the project includes statistical analysis to assess the accuracy of recorded GPS data and identify potential sources of error.

## Programming Language: Python

## Framework Used : ROS1 Noetic

## Installations

sudo apt update

sudo apt install ros-noetic-ros-base

source /opt/ros/noetic/setup.bash

pip3 install utm bagpy

sudo apt install python3-serial

## Tasks Completed

-**Developed a ROS1 GPS Device Driver**: Implemented a Python script to read, parse, and process NMEA GPGGA sentences over serial communication.

-**Latitude/Longitude to UTM Conversion**: Integrated the utm package to transform raw GPS coordinates into UTM easting and northing values.

-**Custom ROS1 Message Definition**: Created a custom ROS1 msg (gps_msg.msg) file to define nine fields of GPS data, including latitude, longitude, altitude, horizontal dilution of precision (HDOP), and UTM coordinates.

-**ROS1 Publisher Implementation**: Developed a ROS1 node that continuously reads GPS data and publishes messages on the /gps topic.

-**Data Storage in ROS Bag Files**: Collected and stored raw GPS data in .bag files for analysis.

-**Statistical Analysis of GPS Data**: Processed collected data to assess positional accuracy, GPS drift, and error estimation.

## Key Learnings

-**Interfacing with Serial Devices in ROS1**: Understood how to handle real-time data acquisition from external sensors over USB using the pyserial package.

-**Designing Modular ROS Nodes**: Learned how to structure a ROS1 package effectively, ensuring reusability and scalability of the GPS driver.

-**Custom Message Definition in ROS1**: Explored how to define and publish custom messages using msg files for handling structured sensor data.

-**Launch File Configuration for Flexibility**: Understood how to use ROS1 launch files to dynamically handle hardware-specific configurations, such as specifying different serial ports.

-**Error Analysis and Statistical Validation**: Understood the GPS accuracy limitations, the impact of environmental obstructions, and how to evaluate errors using scatter plots, histograms, and numerical error estimation.
-**Working with ROS Bag Files**: Recorded, played back, and extracted GPS data using ROS bag files for offline analysis.


## Data Collection and Storage

GPS data was collected under three different environmental conditions:

1.**Stationary Open Environment** – Clear sky, minimal obstructions.

2.**Stationary Occluded Environment** – Near buildings or trees.

3.**Moving Data Collection** – Walking in a straight line for 200-300 meters.

## Analysis

1. **Stationary Data Analysis**:
   
- Created scatter plots of Northing vs. Easting to observe positional variations.
- Computed error estimates by comparing measured positions with a known reference point.
- Generated histograms to analyze the distribution of GPS positioning errors.
  
2.**Moving Data Analysis**:

- Assessed trajectory accuracy by fitting collected data to an expected straight-line path.
- Plotted altitude vs. time to observe elevation variations.
- Quantified positional deviation and computed an error estimate based on least-squares regression.

## Error Analysis:

-Identified potential GPS error sources, including multipath interference, satellite signal loss, and atmospheric effects.

-Analyzed the impact of environmental obstructions on GPS accuracy.

-Compared HDOP values to observed positioning errors for correlation analysis.

## Sources of Error Encountered

- Wind : Caused slight variations in recorded positions
- Rain : Reduced satellite signal strength , increasing positional drift
- Buildings: Caused multipath interference

## Conclusion

This project successfully demonstrates the implementation of a USB-based GPS puck driver in ROS1, handling real-time GPS data acquisition, processing, and publishing. Through structured data collection, storage, and analysis, critical insights into GPS positioning accuracy and error estimation were obtained. The findings highlight the challenges of real-world GPS data reliability and the importance of sensor fusion for autonomous navigation applications.

