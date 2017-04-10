# coding=utf-8
# ----------------------------------------------------------------------------
# Create single HTML file with the messages of a Spark space
# Requirements/Features/Restrictions:
# https://tools.sparkintegration.club/sparkarchive
# ----------------------------------------------------------------------------
import json
import requests
import codecs
import datetime
import re

#         Personal Token: you can find this on developer.ciscospark.com, login, click name on top right
myToken = "____YOUR_TOKEN_HERE_____"
#         Room ID: you can find this on developer.ciscospark.com, list all rooms, 'max 900'
myRoom = "____YOUR_ROOM_ID_HERE_____"
outputFileName = "./message-archive.html"
myDomain = ""
#         Your 'local' domain. Users with a different domain will have a different color
#           Format: "domain.com". If EMPTY, it uses your domain

#-------------------- NO CHANGES BELOW --------------------






myCounter = 0
maxMessages = 999       # increasing this could break API calls (rate-limiting, error 429)
previousEmail = ""
previousMonth = ""
currentDate = datetime.datetime.now()
htmldata = """<html><head><style media='screen' type='text/css'>
.cssRoomName {
    font-family: 'HelveticaNeue-Light';
    height: 66px;
    background-color: #029EDB;
    /* original background color was gray: FBFBFB */
    font-size: 34px;
    color: #fff;
    display: flex;
    padding-left: 30px;
    align-items: center;
}
.cssNewMonth {
    font-family: 'HelveticaNeue-Light', 'Helvetica Neue Light';
    height: 65px;
    background-color: #F2FFE8;
    font-size: 50px;
    color: #D9DBDB;
}
.cssNewMonth span {
    color: #C3C4C7;
}
.css_email {   /*  ---- NAME  ----- */
    color: rgb(133, 134, 136);
}
.css_email_external {   /*  ---- NAME  ----- */
    color: #F0A30B;
}
.css_created {   /*  ---- DATE  ----- */
    color: #C0C0C1;
    font-size: 11px;
}
.css_messagetext {   /*  ---- MESSAGE TEXT  ----- */
    color: rgb(79, 80, 81);
    font-size: 14.7px;
    font-weight: 400;
    margin-bottom: 20px;
    margin-top: 6px;
    margin-left: 20px;

}
.css_message:hover {
    background-color: #FBFBFB;
}
.css_message {
    font-family: 'HelveticaNeue-Light', 'Helvetica Neue Light', 'Helvetica Neue';
    padding-left: 30px;
}</style>
</head><body>"""


def convertDate(inputdate):
    return datetime.datetime.strptime(inputdate, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%b %d, %H:%M  %A  (%Y)")

def get_monthday(inputdate):
    myyear = datetime.datetime.strptime(inputdate, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y")
    mymonth = datetime.datetime.strptime(inputdate, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%b")
    return myyear, mymonth

def convertURL(inputtext):
    outputtext = inputtext
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', inputtext)
    if len(urls) > 0:
        for replaceThisURL in urls:
            outputtext = outputtext.replace(replaceThisURL,"<a href='" + replaceThisURL + "'>" + replaceThisURL + "</a>")
    return outputtext

def get_messages(mytoken, myroom, myMaxMessages):
    headers = {'Authorization': 'Bearer ' + mytoken, 'content-type': 'application/json; charset=utf-8'}
    payload = {'roomId': myroom, 'max': myMaxMessages}
    result = requests.get('https://api.ciscospark.com/v1/messages', headers=headers, params=payload)
    return result.text

def get_roomname(mytoken, myroom):
    headers = {'Authorization': 'Bearer ' + mytoken, 'content-type': 'application/json; charset=utf-8'}
    result = requests.get('https://api.ciscospark.com/v1/rooms/' + myroom, headers=headers)
    return result.json()['title']

def get_me(mytoken):
    header = {'Authorization':"Bearer " + mytoken, 'content-type':'application/json; charset=utf-8'}
    result = requests.get(url='https://api.ciscospark.com/v1/people/me', headers=header)
    return result.json()

def get_filename(mytoken,fileURL):
    header = {'Authorization':"Bearer " + mytoken, 'content-type':'application/json; charset=utf-8'}
    result = requests.get(url=fileURL, headers=header)
    myContentDisposition = result.headers.get('Content-Disposition', None)
    print(myContentDisposition)
    myContentDisposition = myContentDisposition.split("filename=")[1]
    return myContentDisposition



# ===== Get Space Title
try:
    roomName = get_roomname(myToken, myRoom)
except:
    roomName = "** error getting space name **"
    print(roomName)

# ===== Get Messages
try:
    SparkMessages = json.loads(get_messages(myToken, myRoom, maxMessages))
except:
    print("-- ERROR retrieving messsages --\n please check your token is good and the room ID exists")
    exit()

# ===== Get My Domain - IF it's empty
if myDomain == "":
    try:
        myEmail = "".join(get_me(myToken)['emails'])
        myDomain = myEmail.split("@")[1]
        print(myEmail)
        print(myDomain)
    except:
        print("-- ERROR getting your email address --\n please check your token is good")



# ====== GENERATE HTML FILE
print("Messages Processed:  " + str(len(SparkMessages['items'])))
htmldata += "<div class='cssRoomName'>   " + roomName + "&nbsp;&nbsp;&nbsp; <span style='display:inline-block;float:right;font-size:10px;'> CREATED: "+ str(currentDate) +"</span></div><br>"
for msg in SparkMessages['items']:
    if len(msg) < 5: continue          # empty msg?
    if 'text' not in msg: continue     # msg without 'text' key, move to next messsage
    data_created = convertDate(str(msg['created']))             # ------- MESSAGE DATE
    data_text = convertURL(str(msg['text']))                    # ------- MESSAGE TEXT
    data_email = str(msg['personEmail'])                        # ------- MESSAGE AUTHOR
    messageYear, messageMonth = get_monthday(msg['created'])
    if messageMonth != previousMonth:   # Used to group messages per month
        htmldata += "<div class='cssNewMonth'>   " + messageYear + "    <span style='color:#C3C4C7'>" + messageMonth + "</span></div>"
    htmldata += "<div class='css_message'>"
    if data_email != previousEmail:             # if PREVIOUS email equals current email, then skip header
        msgDomain = data_email.split("@")[1]    # Get message sender domain
        if myDomain == msgDomain:               # If domain <> own domain, use different color
            htmldata += "<span class='css_email'>" + data_email + "   </span>"
        else:
            htmldata += "<span class='css_email_external'>" + data_email + "   </span>"
        htmldata += "<span class='css_created'>" + data_created + "   </span>"
    htmldata += "<div class='css_messagetext'>" + data_text
    if 'files' in msg:                          # Attached files? Get filename
        htmldata += "<span style='color:brown'> "
        for myfilename in msg['files']:
            htmldata += "<br>attached file: " + get_filename(myToken,myfilename) + ""
        htmldata += "</span>"
    htmldata += "</div>"
    htmldata += "</div>"
    previousEmail = data_email
    previousMonth = messageMonth

htmldata += "</body></html>"


# ---- WRITE HTML to FILE
target = open(outputFileName, 'w')
target.write(htmldata)
target.close()
