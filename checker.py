
import time
import logging
import subprocess
import requests
from pyHS100 import SmartPlug
#declaring and zeroing failed ping counter
failed_ping_count = 0

#configuration
ifttt_webhook_url = 'WEBHOOK'
plug = SmartPlug("SMARTPLUG IP")
external_host_IP = "EXTERNAL HOST"
modem_IP = "WIP" #forgot what i was gonna use this for
reboot_threshold = 15
reboot_time_allowance = 15
shutdown_time = 5

#Setting logging configuration
logging.basicConfig(filename='internet.log',level=logging.DEBUG, format='%(asctime)s : %(message)s')

#Takes hostname and pings one time, returns 1 for successfull 0 for fail
def check_ping(hostname):
    pingresponse = subprocess.Popen(['ping',hostname,'-c','1',"-W","2"])
    pingresponse.wait()
    return not pingresponse.poll()
    
def reboot_modem():
    print_and_log("FAILURE DETECTED CUTTING POWER FOR " + str(shutdown_time) + " SECONDS", 1)
    #INSERT SMART SWITCH CUT CODE HERE
    plug.turn_off()
    #INSERT SMART SWITCH CUT CODE HERE
    time.sleep(shutdown_time)
    #INSERT SMART SWITCH RESUME CODE HERE
    plug.turn_on()
    #INSERT SMART SWITCH RESUME CODE HERE 
    print_and_log("MODEM POWER RESUMED ALLOWING " + str(reboot_time_allowance) + " SECONDS FOR REBOOT", 2)
    time.sleep(reboot_time_allowance)
    try:
        requests.post(ifttt_webhook_url)
    except:
        print_and_log("IFTTT Notify failed", 2)
    return

def print_and_log(message, severity):
    print(message)
    if severity == 1:
        logging.warning(message)
    elif severity == 2:
        logging.info(message)
    
while True:	
    while failed_ping_count < reboot_threshold:
        time.sleep(1)
        if check_ping(external_host_IP) == True:
            print("Successful Ping")
            failed_ping_count = 0
        else:
            failed_ping_count = failed_ping_count + 1
            print("Pings Failing: "+ str(failed_ping_count))
    reboot_modem()
    failed_ping_count = 0
    

