import datetime
import requests
import logging

logger = logging.getLogger(__name__)


class CloudMessage:
    """Holds the message information that will be sent to the cloud"""

    def __init__(self, message_type, source, message_txt, lng, lat, error_code=0):
        self.message_type = message_type
        self.source = source
        self.message_time = str(datetime.datetime.now())
        self.message_txt = message_txt
        self.lng = lng
        self.lat = lat
        self.error_code = error_code
        if not isinstance(self.message_type, str):
            raise ValueError("Message type must be a string")
        if self.message_type == "":
            raise ValueError("Message type can not be blank")
        if not isinstance(self.source, str):
            raise ValueError("Source must be a string")
        if self.source == "":
            raise ValueError("Source can not be blank")
        if not isinstance(self.message_txt, str):
            raise ValueError("Message text must be a string")
        if self.message_txt == "":
            raise ValueError("Message text not be blank")
        if isinstance(self.lng, str):
            raise ValueError("Longitude must be numeric between -180 and +180")
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
                             "respectively.(<-90) {0}".format(self.lat))
        if self.lat > 90:
            raise ValueError("Latitude must be between -90 and +90 for he southern and northern hemisphere "
                             "respectively. (>90) {0}".format(self.lat))
        if not isinstance(self.error_code, int):
            raise ValueError("Error Code must be numeric between 1000 and 9999 or 0")
        if 0 < self.error_code < 1000:
            raise ValueError("Error Code must be numeric between 1000 and 9999 or 0")
        if self.error_code > 9999:
            raise ValueError("Error Code must be numeric between 1000 and 9999 or 0")

    @property
    def message_id(self):
        return self.source + "|" + str(self.message_time)

    @property
    def message_data(self):
        return {
            "ID": self.message_id,
            "MessageType": self.message_type,
            "DateTime": str(self.message_time),
            "Lon": str(self.lng),
            "Lat": str(self.lat),
            "ErrorCode": str(self.error_code),
            "MessageText": self.message_txt
        }

    def write_cloud_message(self):
        """This module writes a normal log message to the cloud database
            Normal messages are those that do not contain errors"""
        cloud_message_1 = CloudMessage(self.message_type, self.source, self.message_txt,
                                       self.lng, self.lat, self.error_code)
        cloud_connection_1 = CloudConnection()
        requests_1 = requests.post(url=cloud_connection_1.api_endpoint, json=cloud_message_1.message_data)
        pastebin_url = requests_1.text
        logger.info("The pastebin URL is:%s" % pastebin_url)


class CloudConnection:
    """ Holds cloud connection information """

    def __init__(self):
        self.api_endpoint = "https://qo8k2n8335.execute-api.us-west-1.amazonaws.com/Production/"
        self.api_key = "1Z9zf9dOQ95mvhY5ozsPD7UnO9siPNwgMhFKJwXe"


path = "/home/pi/Scripts/Python/AutoBoat/AutoBoat_config.ini"
