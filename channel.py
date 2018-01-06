# -*- coding: utf-8 -*-
import urllib
import json
import sys
import traceback

DEVICE = {
    'serialno': '6e4f187bf050415bb199b23fe00f950a',
    'macaddress': '58307c8f96cf41c3bb4c66ff19684d76',
    'authcode': '7Y3PX6SEAC',
    'apikey': '', #base64.b64decode("OGRhZmFjMzY5Y2I0NDVmYjg5Mzk1NDI4ZTY0YWQ1NmU=")
    'apipwd': '', #base64.b64decode("OTBjODgzYjFjNDdhNGI5OWFhNWE4MmU2YjMyOTUxYTU=")
    'auth_url': 'https://api.gliptv.com/auth.aspx' #base64.b64decode('aHR0cHM6Ly9hcGkuZ2xpcHR2LmNvbS9hdXRoLmFzcHg=')
}

def initDevice(authcode=''):

    data = {"f": "maincheck", "action": "maincheck"}
    header = [('User-Agent', '')]
    sessionpage = getUrl(DEVICE['auth_url'], post=data, headers=header)
    sessionpage = json.loads(sessionpage)["resp"]

    DEVICE['apipwd'] = sessionpage[0]["APIPassword"]
    DEVICE['apikey'] = sessionpage[0]["APIKey"]

    if authcode != "":
        try:
            data = {
                "gmt": "0",
                "APIPassword": DEVICE['apipwd'],
                "APIKey": DEVICE['apikey'],
                "token": authcode,
                "appVersion": "4.5",
                "deviceType": "7",
                "deviceFirmware": "4.4.4",
                "deviceModel": "GT-I9300",
                "action": "useToken",
                "deviceInfo": "samsung-m0-amlogic-19",
                "applicationType": "5"
            }
            sessionpage = getUrl(DEVICE['auth_url'], post=data, headers=header)
            sessionpage = json.loads(sessionpage)
            
            DEVICE['serialno'] = sessionpage["resp"]["Serial"]
            DEVICE['macaddress'] = sessionpage["resp"]["MacAddress"]
            DEVICE['authcode'] = authcode

            sys.stdout.write('SUCCESS to register the code  %s'%authcode)
        except:
            sys.stderr.write('FAILED to register the code  %s'%authcode)
            traceback.print_exc(file=sys.stdout)
            return False
    return True

def getUrl(url, post, headers, timeout=20):

    opener = urllib.request.build_opener(urllib.request.HTTPBasicAuthHandler(),
                                         urllib.request.HTTPHandler())

    req = urllib.request.Request(url)
    req.add_header(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36'
    )
    req.add_header('Content-Type', 'application/json')

    for h, hv in headers:
        req.add_header(h, hv)

    data = urllib.parse.urlencode(post)
    data = data.encode('utf-8')
    response = opener.open(req, data, timeout=timeout)
    data = response.read()
    response.close()
    return data.decode('utf-8')

def getStreamingURL(channelid):
    url = ""

    try:

        data = {
            "gmt": "0",
            "APIPassword": DEVICE['apipwd'],
            "APIKey": DEVICE['apikey'],
            "appVersion": "4.5",
            "deviceType": "7",
            "deviceFirmware": "4.4.4",
            "deviceModel": "GT-I9300",
            "action": "checkNewDevice",
            "serialNumber": DEVICE['serialno'],
            "macAddress": DEVICE['macaddress'],
            "deviceInfo": "samsung-m0-amlogic-19",
            "applicationType": "5"
        }
        header = [('User-Agent', '')]
        sessionpage = getUrl(DEVICE['auth_url'], post=data, headers=header)
        sessionpage = json.loads(sessionpage)
        
        pw = sessionpage["keys"]["pw"]
        token = sessionpage["keys"]["token"]
        deviceid = str(sessionpage["devicebox"]["deviceID"])
        boxid = str(sessionpage["devicebox"]["BoxID"])

        data = {
            "ContentType_ID": "4",
            "f": "getStreamURL",
            "itemName": channelid + '_HD',
            "APIPassword": DEVICE['apipwd'],
            "APIKey": DEVICE['apikey'],
            "DeviceID": deviceid,
            "DeviceType": "7",
            "streamProtocal": "hls",
            "BoxID": boxid,
            "User_Country": "",
            "appVersion": "4.5",
            "ClusterName": "zixi",
            "token": token,
            "action": "getStreamURL",
            "streamType": "live",
            "content_ID": "301493",
            "pw": pw,
            "DUID": "",
            "User_Province": "",
            "PackageID": "1"
        }
        header = [('User-Agent', '')]
        sessionpage = getUrl(DEVICE['auth_url'], post=data, headers=header)

        url = json.loads(sessionpage)["resp"]
    except:
        traceback.print_exc(file=sys.stdout)
    return url
