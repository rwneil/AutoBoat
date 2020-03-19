from unittest import TestCase
import datetime

import AutoBoat_CloudCommunications as CloudCom


class TestCloudMessage(TestCase):
    # Valid Tests
    def test___init__valid(self):
        test = CloudCom.CloudMessage("SuccessTest", "Vehicle Name", "This is a test Message",
                                     -122.497885, 37.726946, 1999)
        assert test.message_type == "SuccessTest"
        assert test.source == "Vehicle Name"
        assert test.message_txt == "This is a test Message"
        assert test.lng == -122.497885
        assert test.lat == 37.726946
        assert test.error_code == 1999
        assert test.message_time < str(datetime.datetime.now())

        test = CloudCom.CloudMessage("SuccessTest", "Vehicle Name", "This is a test Message",
                                     -179.999, -89.999, 1999)
        assert test.lng == -179.999  # Checks minimum allowed latitude and longitude values
        assert test.lat == -89.999

        test = CloudCom.CloudMessage("SuccessTest", "Vehicle Name", "This is a test Message",
                                     +179.999, 89.999, 1000)
        assert test.lng == 179.999  # Checks minimum allowed latitude and longitude values
        assert test.lat == 89.999
        assert test.error_code == 1000  # Checks minimum allowed error code
        test = CloudCom.CloudMessage("SuccessTest", "Vehicle Name", "This is a test Message",
                                     179.999, 89.999, 9999)
        assert test.error_code == 9999  # Checks maximum allowed error code
        test = CloudCom.CloudMessage("SuccessTest", "Vehicle Name", "This is a test Message",
                                     179.999, 89.999, 0)
        assert test.error_code == 0  # Error code can be blank or 0
        test = CloudCom.CloudMessage("SuccessTest", "Vehicle Name", "This is a test Message",
                                     179.999, 89.999)
        assert test.error_code == 0  # Error code can be blank or 0

    # Invalid Tests
    def test___init__invalid(self):
        with self.assertRaises(ValueError):  # Non String Message Type
            test = CloudCom.CloudMessage(99.99, "Vehicle Name", "This is a test Message",
                                         -122.497885, 37.726946, 1999)
        with self.assertRaises(ValueError):  # Empty Message Type
            test = CloudCom.CloudMessage("", "Vehicle Name", "This is a test Message",
                                         -122.497885, 37.726946, 1999)
        with self.assertRaises(ValueError):  # Non String Vehicle Name
            test = CloudCom.CloudMessage("ErrorTest", 99, "This is a test Message",
                                         -122.497885, 37.726946, 1999)
        with self.assertRaises(ValueError):  # Empty Vehicle Name
            test = CloudCom.CloudMessage("ErrorTest", "", "This is a test Message",
                                         -122.497885, 37.726946, 1999)
        with self.assertRaises(ValueError):  # Non String Message
            test = CloudCom.CloudMessage("ErrorTest", "Vehicle Name", 999.99,
                                         -122.497885, 37.726946, 1999)
        with self.assertRaises(ValueError):  # Empty Message Text
            test = CloudCom.CloudMessage("ErrorTest", "Vehicle Name", "",
                                         -122.497885, 37.726946, 1999)
        with self.assertRaises(ValueError):  # String is an invalid latitude
            test = CloudCom.CloudMessage("ErrorTest", "Vehicle Name", "This is a test Message",
                                         -122.497885, "37.726946", 1999)
        with self.assertRaises(ValueError):  # Latitude must be between -90 and +90
            test = CloudCom.CloudMessage("ErrorTest", "Vehicle Name", "This is a test Message",
                                         -122.497885, -90.001, 1999)
        with self.assertRaises(ValueError):  # Latitude must be between -90 and +90
            test = CloudCom.CloudMessage("ErrorTest", "Vehicle Name", "This is a test Message",
                                         -122.497885, 90.001, 1999)
        with self.assertRaises(ValueError):  # String is an invalid Longitude
            test = CloudCom.CloudMessage("ErrorTest", "Vehicle Name", "This is a test Message",
                                         "-122.497885", 37.726946, 1999)
        with self.assertRaises(ValueError):  # Longitude must be between -180 and +180
            test = CloudCom.CloudMessage("ErrorTest", "Vehicle Name", "This is a test Message",
                                         -180.01, 37.726946, 1999)
        with self.assertRaises(ValueError):  # Longitude must be between -180 and +180
            test = CloudCom.CloudMessage("ErrorTest", "Vehicle Name", "This is a test Message",
                                         180.01, 37.726946, 1999)
        with self.assertRaises(ValueError):  # Error Code must be an integer (not string)
            test = CloudCom.CloudMessage("ErrorTest", "Vehicle Name", "This is a test Message",
                                         -122.497885, 37.726946, "1999")
        with self.assertRaises(ValueError):  # Error Code must be an integer (not decimal)
            test = CloudCom.CloudMessage("ErrorTest", "Vehicle Name", "",
                                         -122.497885, 37.726946, 1999.9)
        with self.assertRaises(ValueError):  # Error Code must be between 1000 and 9999
            test = CloudCom.CloudMessage("ErrorTest", "Vehicle Name", "",
                                         180.01, 37.726946, 999)
        with self.assertRaises(ValueError):  # Error Code must be between 1000 and 9999
            test = CloudCom.CloudMessage("ErrorTest", "Vehicle Name", "",
                                         180.01, 37.726946, 10000)
