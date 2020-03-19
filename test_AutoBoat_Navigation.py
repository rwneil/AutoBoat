from unittest import TestCase
import AutoBoat_Navigation as Nav


class TestWayPoint(TestCase):
    """
       The valid range of latitude in degrees is -90 and +90 for the southern and northern hemisphere
       respectively. Longitude is in the range -180 and +180 specifying coordinates west and east of the Prime
       Meridian, respectively.
    """

    def test___init__valid(self):
        # Valid Tests
        wp_1 = Nav.WayPoint(20, 10)
        assert wp_1.lng == 20
        assert wp_1.lat == 10
        wp_2 = Nav.WayPoint(-20, -10)
        assert wp_2.lng == -20
        assert wp_2.lat == -10
        wp_3 = Nav.WayPoint(0, 0)
        assert wp_3.lng == 0
        assert wp_3.lat == 0
        wp_4 = Nav.WayPoint(-180, -90)
        assert wp_4.lng == -180
        assert wp_4.lat == -90
        wp_5 = Nav.WayPoint(+180, +90)
        assert wp_5.lng == 180
        assert wp_5.lat == 90
        wp_6 = Nav.WayPoint(+179.99999, +89.99999)
        assert wp_6.lng == 179.99999
        assert wp_6.lat == 89.99999
        wp_7 = Nav.WayPoint(+179.888888, +89.888888)  # Round to 5 decimal (1 meeter on GPS)
        assert wp_7.lng == 179.88889
        assert wp_7.lat == 89.88889

    def test___init__invalid(self):
        # Invalid Tests
        with self.assertRaises(ValueError):
            Nav.WayPoint('str', 'str')  # Error - Both values string
            Nav.WayPoint(10, 'str')  # Error - Lat is string
            Nav.WayPoint('str', 20)  # Error - Lng is string
            Nav.WayPoint(200, 100)  # Error - Both values to large
            Nav.WayPoint(200, 10)  # Error - Lon is too large
            Nav.WayPoint(20, 100)  # Error - Lat is too large
            Nav.WayPoint(20, 90.0001)  # Error - Lat is too large
            Nav.WayPoint(180.1, 70)  # Error - Lon is too large


class TestKmlImport(TestCase):

    def test__init__valid(self):
        # Valid Tests
        test = Nav.KmlImport("/home/pi/Scripts/Python/AutoBoat/LakeMerced.kml", "{http://www.opengis.net/kml/2.2}",
                             "home/pi/AutoBoat/Waypoint.csv")
        assert test.kml_file == "/home/pi/Scripts/Python/AutoBoat/LakeMerced.kml"
        assert test.namespace == "{http://www.opengis.net/kml/2.2}"
        assert test.waypoint_file == "home/pi/AutoBoat/Waypoint.csv"

        test = Nav.KmlImport("C:/Users/rwnei/Documents/Hobby/LakeMerced.kml", "{http://www.opengis.net/kml/2.2}",
                             "C:/Users/rwnei/Documents/Hobby/Waypoint.csv")
        assert test.kml_file == "C:/Users/rwnei/Documents/Hobby/LakeMerced.kml"
        assert test.namespace == "{http://www.opengis.net/kml/2.2}"
        assert test.waypoint_file == "C:/Users/rwnei/Documents/Hobby/Waypoint.csv"

    def test__init_Invalid(self):
        # Invalid Tests
        with self.assertRaises(ValueError):  # Non String kml file
            test = Nav.KmlImport(1, "{http://www.opengis.net/kml/2.2}", "home/pi/AutoBoat/Waypoint.csv")
        with self.assertRaises(ValueError):  # Non String namespace
            test = Nav.KmlImport("/home/pi/Scripts/Python/AutoBoat/LakeMerced.kml", 1, "home/pi/AutoBoat/Waypoint.csv")
        with self.assertRaises(ValueError):  # Non String waypoint_file
            test = Nav.KmlImport("/home/pi/Scripts/Python/AutoBoat/LakeMerced.kml", "{http://www.opengis.net/kml/2.2}",
                                 1)


class TestWaypointsFile(TestCase):
    # Valid Tests
    def test__init__valid(self):
        test = Nav.WaypointList("home/pi/AutoBoat/Waypoint.csv")
        assert test.waypoint_file == "home/pi/AutoBoat/Waypoint.csv"

    def test__init_Invalid(self):
        # Invalid Tests
        with self.assertRaises(ValueError):  # Non String Waypoints file
            test = Nav.WaypointList(1)


"""class TestKmlImport(TestCase):

    def setUp(self):
        self.test_kml_import = Nav.KmlImport("/home/pi/Scripts/Python/AutoBoat/LakeMerced.kml",
                                             "{http://www.opengis.net/kml/2.2}", "home/pi/AutoBoat/Waypoint.csv")
        self.test_list = ["123.45678, 67.89012, 300", "123.56789, 67.90123, 310", "123.67890, 67.01234, 320"]

    def test_parse_csv_text_to_dict(self):
        test = Nav.KmlImport.parse_csv_text_to_dict(self.test_kml_import, self.test_list, )
        assert type(test) is dict
        assert test['lng'][1] == 123.56789
        assert test['lat'][0] == 67.89012
        assert test['alt'][2] == 320"""
