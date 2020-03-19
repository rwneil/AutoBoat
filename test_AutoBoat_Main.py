from unittest import TestCase
import AutoBoat_Main


class TestConfig_read(TestCase):
    def test_config_read(self):
        # Valid Tests
        path = "/home/pi/Scripts/Python/AutoBoat/AutoBoat_config.ini"
        test_001 = AutoBoat_Main.config_read(path)
        assert test_001 is None
        assert AutoBoat_Main.config_Vehicle_Name == "AutoBoat003"
        assert AutoBoat_Main.config_Vehicle_Type == "Boat"
        assert isinstance(AutoBoat_Main.config_log_status_wait, int)
        assert isinstance(AutoBoat_Main.config_log_error_wait, int)
        assert isinstance(AutoBoat_Main.config_new_heading_wait, int)
        assert isinstance(AutoBoat_Main.config_time_turn_360, int)

        # Invalid Tests
        path = "/BadLocation/AutoBoat_config.ini"
        test_002 = AutoBoat_Main.config_read(path)
        assert test_002 is not None


class TestWrite_cloud_error_message(TestCase):
    def test_write_cloud_error_message(self):
        # Valid Tests
        test_003 = AutoBoat_Main.write_cloud_error_message("This is a valid Message", 1001)
        assert  test_003 is None

        # Invalid Tests
        """ Most of the invalid tests are in the CloudMessage Class in the CloudCommunications.py module """
