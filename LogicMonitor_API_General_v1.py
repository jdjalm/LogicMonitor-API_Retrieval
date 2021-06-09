#The following Python script can be tweaked for general usage when needing to retrieve LogicMonitor node information. A template provided by LogicMonitor was used.
#In its current state, it is set to retrieve all node sub-groups under the specific node group ID of 596.
#Sensitive information has been removed/replaced for privacy.

import requests
import json
import hashlib
import base64
import time
import hmac
import csv

#API account credentials
AccessId = 'xxxxxx'
AccessKey = 'xxxxxx'
Company = 'xxxxxx'

#Request method
httpVerb = 'GET'

#Groups request
resourcePath = '/device/groups/596'
queryParams = '?fields=id,name,numOfDirectSubGroups,subGroups'

#For POST requests
data = ''

#Prefix name for the JSON/CSV files which will be produced
oname = "Company-groups_"

#Construct URL 
url = 'https://'+ Company +'.logicmonitor.com/santaba/rest' + resourcePath + queryParams

#Get current time in milliseconds
epoch = str(int(time.time() * 1000))

#Concatenate Request details
requestVars = httpVerb + epoch + data + resourcePath

#Construct signature
hmac1 = hmac.new(AccessKey.encode(),msg=requestVars.encode(),digestmod=hashlib.sha256).hexdigest()
signature = base64.b64encode(hmac1.encode())

#Construct headers
auth = 'LMv1 ' + AccessId + ':' + signature.decode() + ':' + epoch
headers = {'Content-Type':'application/json','Authorization':auth}

#Make request
jsonresponse = requests.get(url, data=data, headers=headers)
jrt = jsonresponse.text
#Create a JSON object from the string response
json_data = json.loads(jrt)

#Export the API jsonresponse for later usage, naming it according to the data pulled (group ID and name)
oname = oname + str(json_data['data']['id']) + '_' + str(json_data['data']['name'])
with open(oname + ".json", "w") as f:
    f.write(jrt)

#Open a new CSV file for writing the JSON reponse output
csvout = open(oname + ".csv", 'w', newline='')
csvwriter = csv.writer(csvout)
#Write out the first row of the reponse (these are the headers)
csvwriter.writerow(json_data['data']['subGroups'][0].keys())
#Write out the remaining rows in the reponse (this is the relevant node info)
for jditem in json_data['data']['subGroups']:
    csvwriter.writerow(jditem.values())
#Close the CSV file
csvout.close()