import socket
from ssh2.session import Session
import random 
import string
import time
import urllib.request
import re

# If the script doesn't work, install the ssh2 module. It is going to say tha tthis is missing. I could not find another good way
# setup some information for later. Note: CHANGE THE USERNAME AND PASSWORD TO YOUR USERNAME AND PASSWORD
# If the host or port are different, you will have to change them

host = 'siberdefense.ddns.net'
user = 'username'
password = 'password'
port = 22

# The directory of the pile and a test nugget. The nugget will be different and will change to the last nugget that has been sent to the input function 
# It should loop for infinity until it finds a new nugget

pile_dir = "pile/"
old_nugget = 12345

# SSH and Randome setup 

letters = string.ascii_lowercase

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

session = Session()
session.handshake(sock)
session.userauth_password(user, password)
channel = session.open_session()

# function that crawles the website and finds the highest number. This is imported due to there being 3 Numbers. (8, 200 and the nugget)
# this function checks if the nugget is new and calls it's self or the input function for the ssh connection 

def web_grabber():     
    fp = urllib.request.urlopen("http://siberdefense.ddns.net/pileking/nugget.html")
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    temp = re.findall(r'\d+', mystr) 
    res = list(map(int, temp)) 
    print(max(res))
    if(max(res) != old_nugget):
        old_nugget = max(res)
        execute_command(max(res))
    else:
        time.sleep(0.1)
        web_grabber()


# This function generates a rendome string with lenght 20 and adds the words "nugget" and "pile" to it.
# If you want to put out two numbers or numbers and letters, you have to convert the number to a string with str(number)
# This function calls the webcrawler afterwords to start the scanning again

 
def execute_command(nugget_input): 
    message = ( ''.join(random.choice(letters) for i in range(20)) + " nugget pile" )
    channel.execute("echo" + " " + "'" + message + "'" + " " + ">" + " " + pile_dir +  str(nugget_input))
    size, data = channel.read()
    web_grabber()
    while size > 0: 
        print(data.decode())
        size, data = channel.read()
        break 


# Ignore this part. It would terminate the ssh connection. Feel free to add a "max nugget" function
# YOu have to start the connection process again after killing it. 

def close():
    channel.close()
    print("exit: {0}".format(channel.get_exit_status()))


