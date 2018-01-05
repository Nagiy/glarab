# -*- coding: utf-8 -*-
import urllib, re
import json
import os
import time
import sys
import base64
import traceback


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


def getGLArabURL(channelid):

    gl_serialno = "6e4f187bf050415bb199b23fe00f950a"
    gl_serialid = "6e4f187bf050415bb199b23fe00f950a"
    gl_macaddress = "58307c8f96cf41c3bb4c66ff19684d76"
    gl_macid = "58307c8f96cf41c3bb4c66ff19684d76"
    gl_authcode = "7Y3PX6SEAC"
    gl_authcodeused = "7Y3PX6SEAC"

    url = ""

    #base64.b64decode('aHR0cHM6Ly9hcGkuZ2xpcHR2LmNvbS9hdXRoLmFzcHg=')
    auth_url = 'https://api.gliptv.com/auth.aspx'

    try:
        #apikey = base64.b64decode("OGRhZmFjMzY5Y2I0NDVmYjg5Mzk1NDI4ZTY0YWQ1NmU=")
        #apipwd = base64.b64decode("OTBjODgzYjFjNDdhNGI5OWFhNWE4MmU2YjMyOTUxYTU=")

        data = {"f": "maincheck", "action": "maincheck"}
        header = [('User-Agent', '')]
        sessionpage = getUrl(auth_url, post=data, headers=header)
        sessionpage = json.loads(sessionpage)["resp"]
        apipwd = sessionpage[0]["APIPassword"]
        apikey = sessionpage[0]["APIKey"]

        if gl_authcode != "" and gl_authcode != gl_authcodeused:
            try:
                #d.update(50, 'Trying to register the code  %s'%gl_authcode)
                data = {
                    "gmt": "0",
                    "APIPassword": apipwd,
                    "APIKey": apikey,
                    "token": gl_authcode,
                    "appVersion": "4.5",
                    "deviceType": "7",
                    "deviceFirmware": "4.4.4",
                    "deviceModel": "GT-I9300",
                    "action": "useToken",
                    "deviceInfo": "samsung-m0-amlogic-19",
                    "applicationType": "5"
                }
                rethtml = getUrl(auth_url, post=data, headers=header)
                url = json.loads(rethtml)["resp"]
                gl_serialid = url["Serial"]
                gl_macid = url["MacAddress"]
                gl_authcodeused = gl_authcode
                #d.update(80, 'SUCCESS to register the code  %s'%gl_authcode)
            except:
                #d.update(80, 'FAILED to register the code  %s'%gl_authcode)
                pass
        if gl_serialid != "":
            gl_serialno, gl_macaddress = gl_serialid, gl_macid
        if gl_serialno == "":
            #d.update(80, "No Global or personal code available. For GL HD create GL code, follow the forum post.")
            return
        data = {
            "gmt": "0",
            "APIPassword": apipwd,
            "APIKey": apikey,
            "appVersion": "4.5",
            "deviceType": "7",
            "deviceFirmware": "4.4.4",
            "deviceModel": "GT-I9300",
            "action": "checkNewDevice",
            "serialNumber": gl_serialno,
            "macAddress": gl_macaddress,
            "deviceInfo": "samsung-m0-amlogic-19",
            "applicationType": "5"
        }
        header = [('User-Agent', '')]
        sessionpage = getUrl(auth_url, post=data, headers=header)
        sessionpage = json.loads(sessionpage)
        glpw = sessionpage["keys"]["pw"]
        gltoken = sessionpage["keys"]["token"]
        gldeviceid = str(sessionpage["devicebox"]["deviceID"])
        glboxid = str(sessionpage["devicebox"]["BoxID"])

        data = {
            "ContentType_ID": "4",
            "f": "getStreamURL",
            "itemName": channelid + '_HD',
            "APIPassword": apipwd,
            "APIKey": apikey,
            "DeviceID": gldeviceid,
            "DeviceType": "7",
            "streamProtocal": "hls",
            "BoxID": glboxid,
            "User_Country": "",
            "appVersion": "4.5",
            "ClusterName": "zixi",
            "token": gltoken,
            "action": "getStreamURL",
            "streamType": "live",
            "content_ID": "301493",
            "pw": glpw,
            "DUID": "",
            "User_Province": "",
            "PackageID": "1"
        }
        header = [('User-Agent', '')]
        sessionpage = getUrl(auth_url, post=data, headers=header)

        url = json.loads(sessionpage)["resp"]
        if url.startswith("http"):
            return url
    except:
        traceback.print_exc(file=sys.stdout)
    return url
