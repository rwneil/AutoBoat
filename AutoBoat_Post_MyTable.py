# First testing file to send events from Raspberry Pi to AWS web service
# Writtem in Pyton Python 3.5

# importing the requests library
import requests
import datetime

# defining the api-endpoint
API_ENDPOINT = "https://qo8k2n8335.execute-api.us-west-1.amazonaws.com/Production/"

# your API key here
API_KEY = "XXXXXXXXXXXXXXXXX"

# Generate Unique Key
source = 'AutoBoat001'
currdatetime = str(datetime.datetime.now())
UniqueID = source + "|" + currdatetime

MessageType = 'Testing'

# data to be sent to api
data = {
    "ID" : UniqueID,
    "MessageType" : MessageType,
    "DateTime" : "04/19/2019 16:37",

    "Lon" : "200",
    "Lat" : "100"
 }

print(data)

# sending post request and saving response as response object
r = requests.post(url = API_ENDPOINT, json = data)

# extracting response text
pastebin_url = r.text
print("The pastebin URL is:%s"%pastebin_url)
