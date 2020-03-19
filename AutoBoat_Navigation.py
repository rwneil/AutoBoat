import datetime
import xml.etree.ElementTree as ETree
import csv
from io import StringIO
from collections import OrderedDict
from geographiclib.geodesic import Geodesic
import logging
logger = logging.getLogger(__name__)


class VehiclePosition:
    # Holds the current and previous locations of the vehicle
    #  TODO - Confirm how much history to keep in the VehiclePosition class
    def __init__(self, lng, lat, altitude=0, heading=0, speed=0):
        self.position_time = str(datetime.datetime.now())
        self.lng = lng
        self.lat = lat
        self.altitude = altitude
        self.heading = heading
        self.speed = speed


class KmlImport:

    # TODO confirm if KML file is new or not

    def __init__(self, kml_file, namespace, waypoint_file):
        self.kml_file = kml_file
        self.namespace = namespace
        self.waypoint_file = waypoint_file

        if not isinstance(self.kml_file, str):
            raise ValueError("KML File must be a string")
        if not isinstance(self.namespace, str):
            raise ValueError("namsspace must be a string")
        if not isinstance(self.waypoint_file, str):
            raise ValueError("waypoint_file must be a string")

        self.fieldnames = 'lng,lat,alt'

        self.coordinates = ''

    def get_coordinates_from_kml(self):
        # This method gets the coordinates section from the KML file and loads it to the coordinates string
        logger.debug('Begin KMLImport.get_coordinate_list_from_kml()')
        kml_tree = ETree.parse(self.kml_file)
        # Get the coordinates from KMO file and load into string (coordinates)
        for pm in kml_tree.iterfind('.//{0}Placemark'.format(self.namespace)):
            for ls in pm.iterfind('{0}LineString/{0}coordinates'.format(self.namespace)):
                self.coordinates = ls.text.strip().replace(' ', '\n')

    def write_coordinates_to_csvfile(self):
        # This method creates a csv waypoints file from the coordinates in the KML file
        logging.debug('writing waypoint file: %s' % self.waypoint_file)
        with open(self.waypoint_file, 'w+') as f:
            f.write(self.fieldnames)
            f.write('\n')
            f.write(self.coordinates)


class WaypointList:
    def __init__(self, waypoint_file):
        self.waypoint_file = waypoint_file

        if not isinstance(self.waypoint_file, str):
            raise ValueError("waypoint_file must be a string")

        # self.ordered_fieldnames = OrderedDict([('lng', None), ('lat', None), ('alt', None)])
        self.waypoint_dict = []

    def load_waypoints_to_dict(self):
        # This method loads the waypoints from the csv file to a dictionary
        with open(self.waypoint_file, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            headers = next(reader)
            for row in reader:
                self.waypoint_dict.append(OrderedDict(zip( headers, row)))

    def get_waypoint_from_dict(self):
        local_waypoint = WayPoint(elf.waypoint_dict[0]['lng'], self.waypoint_dict[0]['lat'])
        return local_waypoint


class WayPoint:
    """ Holds the planned (and previous) way points for the vehicle """

    #       The valid range of latitude in degrees is -90 and +90 for the southern and northern hemisphere
    #       respectively. longitude is in the range -180 and +180 specifying coordinates west and east of the Prime
    #       Meridian, respectively.

    # TODO remove reached waypoints from file

    def __init__(self, lng, lat):
        self.lng = round(float(lng), 5)
        self.lat = round(float(lat), 5)
        if isinstance(self.lng, str):
            raise ValueError("longitude must be numeric between -180 and +180")
        if isinstance(self.lat, str):
            raise ValueError("Latitude must be numeric between -90 and +90")
        if self.lng < -180:
            raise ValueError("Longitude must be between-180 and +180 specifying coordinates west and east of the "
                             "Prime Meridian,.")
        if self.lng > 180:
            raise ValueError("Longitude must be between -180 and +180 specifying coordinates west and east of the "
                             "Prime Meridian,.")
        if self.lat < -90:
            raise ValueError("Latitude must be between -90 and +90 for he southern and northern hemisphere "
                             "respectively.")
        if self.lat > 90:
            raise ValueError("Latitude must be between -90 and +90 for he southern and northern hemisphere "
                             "respectively.")


"""                for column, value in row.iteritems():
                    self.waypoint_dict.setdefault(column, []).append(value)"""

"""        for row in self.waypoint_dict:
            print('wp: ', row)"""

"""        reader = csv.DictReader(coordinates, self.fieldnames)
        for row in reader:
            for field in self.fieldnames:
                self.waypoint_dict[field].append((row[field]))
            logger.debug('In KMLImport.parse_csv_text_to_dict()')
            return self"""

"""    def parse_csv_text_to_dict(self, csv_text):
        d = defaultdict(list)
        reader = csv.DictReader(csv_text, self.fieldnames)
        return dict(d)"""

# Convert coordinate string to waypoint dictionary
"""       reader = csv.DictReader(StringIO(unicode(self.coordinates, 'utf-8')), fieldnames=self.ordered_fieldnames)
        self.waypoint_dict = reader
        for row in self.waypoint_dict:
            print('wp: ', row)
            # print(self.waypoint_dict['lat'])
        return self"""