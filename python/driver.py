#!/usr/bin/env python3
# -- coding: utf-8 --

import rospy
import serial
import utm
from gps_driver.msg import gps_msg
from std_msgs.msg import Header
import argparse
import sys

def parse_gpgga(data):
    """
    Parse the GPGGA string into individual GPS components.
    """
    fields = data.split(',')
    if len(fields) < 15:
        rospy.logerr("Incomplete GPGGA string.")
        return None

    try:
        utc_time = float(fields[1]) if fields[1] else 0.0
        lat_raw = fields[2] if fields[2] else '0'
        lat_dir = fields[3]
        lon_raw = fields[4] if fields[4] else '0'
        lon_dir = fields[5]
        altitude = float(fields[9]) if fields[9] else 0.0
        hdop = float(fields[8]) if fields[8] else 0.0

        return utc_time, lat_raw, lat_dir, lon_raw, lon_dir, altitude, hdop
    except Exception as e:
        rospy.logerr(f"Error parsing GPGGA string: {e}")
        return None

def convert_to_utm(lat_raw, lat_dir, lon_raw, lon_dir):
    """
    Convert raw latitude and longitude values to UTM coordinates.
    """
    latitude = float(lat_raw[:2]) + float(lat_raw[2:]) / 60
    if lat_dir == 'S':
        latitude = -latitude

    longitude = float(lon_raw[:3]) + float(lon_raw[3:]) / 60
    if lon_dir == 'W':
        longitude = -longitude

    easting, northing, zone_number, zone_letter = utm.from_latlon(latitude, longitude)
    return latitude, longitude, easting, northing, zone_number, zone_letter

def create_gps_msg(parsed_data, utm_data, utc_time):
    """
    Populate the gps_msg with parsed and converted data.
    """
    msg = gps_msg()
    msg.header = Header(stamp=rospy.Time.from_sec(utc_time), frame_id="GPS1_FRAME")
    msg.Latitude, msg.Longitude = utm_data[:2]
    msg.UTM_easting, msg.UTM_northing = utm_data[2:4]
    msg.Altitude = parsed_data[5]
    msg.HDOP = parsed_data[6]
    msg.Zone = str(utm_data[4])
    msg.Letter = utm_data[5]
    return msg

def main():
    """
    Main function to initialize ROS node, read serial data, and publish GPS messages.
    """
    rospy.init_node('gps_driver', anonymous=True)
    pub = rospy.Publisher('/gps', gps_msg, queue_size=10)

    # Parse command-line arguments for serial port
    argv = rospy.myargv(argv=sys.argv)
    parser = argparse.ArgumentParser(description="GPS Driver")
    parser.add_argument('--port', type=str, required=True, help="Serial port for GPS device (e.g., /dev/ttyUSB0)")
    args = parser.parse_args(argv[1:]) 

    # Open serial port
    try:
        ser = serial.Serial(args.port, baudrate=4800, timeout=1)
        rospy.loginfo(f"Connected to GPS device on {args.port}")
    except serial.SerialException as e:
        rospy.logfatal(f"Failed to open serial port: {e}")
        return

    rate = rospy.Rate(10)  # Publish at 10 Hz

    while not rospy.is_shutdown():
        try:
            # Read a line from the serial port
            raw_data = ser.readline().decode('utf-8').strip()
            if raw_data.startswith("$GPGGA"):
                rospy.loginfo(f"Received: {raw_data}")
                parsed_data = parse_gpgga(raw_data)
                if parsed_data:
                    utm_data = convert_to_utm(*parsed_data[1:5])
                    msg = create_gps_msg(parsed_data, utm_data, parsed_data[0])
                    pub.publish(msg)
                    rospy.loginfo(f"Published: {msg}")

            rate.sleep()
        except Exception as e:
            rospy.logerr(f"Error reading or publishing data: {e}")

    # Close the serial port on shutdown
    if ser and ser.is_open:
        ser.close()
        rospy.loginfo("Serial connection closed.")

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

