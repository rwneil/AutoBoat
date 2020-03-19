import ConfigParser


def create_config(path):
    config = ConfigParser.ConfigParser()

    config.add_section("VehicleInfo")
    config.set("VehicleInfo", "VehicleName", "AutoBoat003")
    config.set("VehicleInfo", "VehicleType", "Boat")

    config.add_section("WaitTimes")
    config.set("WaitTimes", "LogStatusWait", "180")   # The number of seconds between log events sent to the server
    config.set("WaitTimes", "LogErrorWait", "3")  # THe number of seconds between error being logged to the server
    config.set("WaitTimes", "NewHeadingWait", "3")  # The # of seconds between changing heading (reduces wear on servos)
    config.set("WaitTimes", "TimeToTurn360", "15")  # THe number of seconds it takes to complete a turn

    config.add_section("LogInfo")
    config.set("LogInfo", "LogDirectory", "/home/pi/AutoBoat/log")

    config.add_section("CloudConnection")
    config.set("CloudConnection", "API_EndPoint", "https://999999999.execute-api.us-west-1.amazonaws.com/Production/")
    config.set("CloudConnection", "API_Key", "ThisIsAFakeKey")

    config.add_section("KmlInfo")  # KML files include the waypoints.  These can be created in Google Earth, etc.
    config.set("KmlInfo", "KmlFile", "/home/pi/Scripts/Python/AutoBoat/LakeMerced.kml")
    # config.set("KmlInfo", "KmlFile", "/home/pi/Scripts/Python/AutoBoat/LakeMerced.kml")
    config.set("KmlInfo", "NameSpace", "{http://www.opengis.net/kml/2.2}")

    config.add_section("WaypointInfo")
    config.set("WaypointInfo", "WaypointFile", "/home/pi/AutoBoat/Waypoint.csv")

    with open(path, "w") as config_file:
        config.write(config_file)


if __name__ == '__main__':
    path = "/home/pi/Scripts/Python/AutoBoat/AutoBoat_config.ini"
    create_config(path)
