import urequests as requests
import ujson
import network
from time import sleep

APIKEY = "pbZRUi49X48I56oL1Lq8y8NDjq6rPfzX3AQeNo3a"
CLIENT_ID = "3pjgjdmamlj759te85icf0lucv"
CLIENT_SECRET = "111fqsli1eo7mejcrlffbklvftcnfl4keoadrdv1o45vt9pndlef"

LOGIN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/login"
TOKEN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/oauth2/token"
REDIRECT_URI = "https://analysis.kubioscloud.com/v1/portal/login"

response = requests.post(
    url = TOKEN_URL,
    data = 'grant_type=client_credentials&client_id={}'.format(CLIENT_ID),
    headers = {'Content-Type':'application/x-www-form-urlencoded'},
    auth = (CLIENT_ID, CLIENT_SECRET))
    response = response.json() #Parse JSON response into a python dictionary
    access_token = response["access_token"] #Parse access token
    
#Interval data to be sent to Kubios Cloud. Replace with your own data:
intervals = [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812,
756, 820, 812, 800]

#Create the dataset dictionary HERE

# Make the readiness analysis with the given data
response = requests.post(
    url = "https://analysis.kubioscloud.com/v2/analytics/analyze",
    headers = { "Authorization": "Bearer {}".format(access_token), #use access token to
access your Kubios Cloud analysis session
 "X-Api-Key": APIKEY},
 json = dataset) #dataset will be automatically converted to JSON by the urequests
library

response = response.json()

#Print out the SNS and PNS values on the OLED screen here