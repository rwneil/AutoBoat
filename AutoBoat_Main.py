import AutoBoat_CloudCommunications as CloudCom
import AutoBoat_Navigation as Nav
import ConfigParser
import logging
# import os  # Required when running on windows OS

# set up logging
logger = logging.getLogger(__name__)

# Global Configuration Variables
config_Vehicle_Name = "AutoBoat999"
config_Vehicle_Type = "Boat"
config_api_endpoint = ""  # The connection string to log events to
config_api_key = ""  # The secrete key used to log the events to AWS
config_log_status_wait = 160  # The number of seconds between log events sent to the server
config_log_error_wait = 3  # The number of seconds between error being logged to the server
config_new_heading_wait = 1  # The number of seconds between changing heading (reduces wear on servos)
config_time_turn_360 = 15  # The number of seconds it takes the vehicle to complete a 360 degree turn
config_log_directory = ""  # Holds the directory of the log files
config_kml_file = ""  # Holds the location of the KML waypoint file
config_kml_namespace = ""  # Holds the location of the KML namespace
config_waypoint_file = ""  # Holds the name and location of the active waypoint file
# class VehicleInfo:
#     """ Holds information about the current vehicle"""
#
#     # TODO - We wamt to eventually limit the vehicle types to (boat, UAV, plane, rover)
#     def __init__(self, vehicle_name, vehicle_type):
#         self.vehicle_name = vehicle_name
#         self.vehicle_type = vehicle_type


def config_read(path):
    global config_Vehicle_Name, config_Vehicle_Type
    global config_log_directory
    global config_api_endpoint, config_api_key
    global config_log_status_wait, config_log_error_wait, config_new_heading_wait, config_time_turn_360
    global config_kml_file, config_kml_namespace
    global config_waypoint_file

    try:
        config = ConfigParser.ConfigParser()
        config.read(path)

        config_Vehicle_Name = config.get("VehicleInfo", "VehicleName")
        config_Vehicle_Type = config.get("VehicleInfo", "VehicleType")
        config_log_status_wait = config.getint("WaitTimes", "LogStatusWait")
        config_log_error_wait = config.getint("WaitTimes", "LogErrorWait")
        config_new_heading_wait = config.getint("WaitTimes", "NewHeadingWait")
        config_time_turn_360 = config.getint("WaitTimes", "TimeToTurn360")
        config_log_directory = config.get("LogInfo", "LogDirectory")
        config_api_endpoint = config.get("CloudConnection", "API_EndPoint")
        config_api_key = config.get("CloudConnection", "API_Key")
        config_kml_file = config.get("KmlInfo", "KmlFile")
        config_kml_namespace = config.get("KmlInfo", "NameSpace")
        config_waypoint_file = config.get("WaypointInfo", "WaypointFile")

        logger.debug("Configuration Complete")

    except ConfigParser.Error, err:
        logger.error("Config Parser ERROR : ", err)
        return err


def write_cloud_error_message(message_text, error_code):
    """This function simply takes an error message and writes it to the cloud server"""

    vehicle_position_1 = Nav.VehiclePosition( -122.497885, 37.726946)

    current_cloud_message = CloudCom.CloudMessage('ErrorTest', config_Vehicle_Name, message_text,
                                                  vehicle_position_1.lng, vehicle_position_1.lat, error_code)
    CloudCom.CloudMessage.write_cloud_message(current_cloud_message)


def main():
    logger.info('************ Begin of Run *****************')
    # Load Configurations
    config_path = "/home/pi/Scripts/Python/AutoBoat/AutoBoat_config.ini"
    config_read(config_path)

    logger.debug('Vehicle Name is: %s' % config_Vehicle_Name)

    # Testing the cloud communications

    vehicle_position_1 = Nav.VehiclePosition(-122.497885, 37.726946)

    logger.debug('Vehicle Position is (lng,lat): {0} , {1}'.format(vehicle_position_1.lng, vehicle_position_1.lat))

    current_cloud_message = CloudCom.CloudMessage('Testing', config_Vehicle_Name, "This is a normal log Message",
                                                  vehicle_position_1.lng, vehicle_position_1.lat)

    CloudCom.CloudMessage.write_cloud_message(current_cloud_message)

    write_cloud_error_message("Test Error Message from Main", 9999)

    # Read Waypoints from the KML file and put into csv Waypoint file
    kml_inst = Nav.KmlImport(config_kml_file, config_kml_namespace, config_waypoint_file)
    kml_inst.get_coordinates_from_kml()
    kml_inst.write_coordinates_to_csvfile()
    logger.debug('Waypoint file created at: %s' % config_waypoint_file)

    #
    # TODO - 11/11/19 - THis is where I left off
    #
    #  Seems to be an error below


    waypoint_file_inst = Nav.WaypointList(config_waypoint_file)
    waypoint_file_inst.load_waypoints_to_dict()
    current_waypoint = waypoint_file_inst.get_waypoint_from_dict()
    print(current_waypoint.lng, current_waypoint.lat)


if __name__ == "__main__":
    import logging.config
    logging.config.fileConfig("/home/pi/Scripts/Python/AutoBoat/logging.ini", disable_existing_loggers=False)
    logger = logging.getLogger()
    main()
