# Spark-Space-Archive
Archive messages from a Cisco Spark Space to one single HTML file

![Example](/README.md_screenshot.jpg)

# REQUIREMENTS
* A [Cisco Spark](https://www.ciscospark.com/) account
* Python 3.x
* Python '[requests](http://docs.python-requests.org/en/master/user/install/#install)' library
* Be a member of the Spark Space you want to archive
# Features
### DOES: 
* Archive all messages
* Group per month
* Display hyperlinks
* Display attached file-names
* (currently) Retrieve the last 1,000 messages

### DOESN'T: 
* Show full names (would require 1 API call per person)
* Archive (download) shared files
* Display "@mentions" in a different color
* Show people's avatar (would require 1 API call per person)

# Configuration
Edit the following variables in the python file:

> myToken = "YOUR_TOKEN_HERE"

Personal Token: you can find this on [developer.ciscospark.com](https://developer.ciscospark.com), login and then click your name on top right.

> myRoom = "YOUR_ROOM_ID_HERE"

Room ID: you can find this on [Spark Developer List rooms](https://developer.ciscospark.com/endpoint-rooms-get.html), make sure you're logged in, set the 'max' parameter to '900' and click Run.
If you don't see the RUN button, make sure 'test mode' is turned on (top of page, under "Documentation")
> outputFileName = "./message-archive.html"

Enter the file name of the output HTML file.
> myDomain = ""

(optional) changes color of email addresses outside your organisation. (your email domain).
If empty: it will use your account domain as the 'local' domain and change the color of any other domain.
(this is just like how the Cisco Spark client does it)


# Roadmap
* DATE: display in different color (easier to scan for specific day)
* DATE: include 'day-of-week'? i.e. "monday, february 2 2016"
* DATE: use local Date format settings? (yyyy/mm/dd vs. dd-mm-yyyy)
* FILE: add date in generated html filename?
* DISPLAY: reverse order of messages, from old to new?
* ATTACHMENTS: attached? show file names
* ATTACHMENTS: download?
* MESSAGES: support markup text
* MESSAGES: support retrieving >1000 messages
* THIS TOOL: make it web-based
   * Login using Spark
   * Select room to archive
   * Room messages are exported to an HTML file
   * User receives 1:1 message from tool bot with the HTML file attached





