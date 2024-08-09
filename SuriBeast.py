#!/usr/bin/python3
import datetime
import time
import traceback
from subprocess import PIPE, Popen

def cmdline(command): #Defines our function to run a command in the shell and capture its output
        process = Popen(
                args = command,
                stdout = PIPE,
                shell = True,
                universal_newlines=True
        )
        return process.communicate()[0]
debug = True
while True: #Starts a loop to continuously monitor logs and block IPs
        try:
                print('Reading logs...')  #Prints a message indicating the script is reading our log
                the_time=datetime.datetime.now() #Gets the current date and time for logging purposes
                fast_log = cmdline('cat /var/log/suricata/fast.log') #Runs a shell command to read the Suricata log file and capture its output
                fast_log = fast_log.split('\n') #Splits the log output into individual lines
                for i in fast_log:
                        if "CUSTOM" in i: #Checks if the line contains the keyword "CUSTOM" which indicates one of our firewall rules has been flagged
                                ip = i.split('-> ')[1].split(':')[0] #Extracts the flagged IP address from the line
                                check_ip = cmdline('iptables -t raw -nL') #Runs a shell command to list the firewall rules and capture its output
                                if ip not in check_ip:
                                        print(f'BLocking IP: {ip}') #Prints a message indicating the IP is going to being blocked
                                        output = cmdline(f'iptables -t raw -A PREROUTING -s {ip} -j DROP')  #Runs a shell command to add a new rule to the firewall to block the IP address
                                        print(f'iptables output: {output}')  #Prints the output of the new firewall rules
                                        log_entry = f'{the_time} blocked {ip} \n' #Creates a log entry indicating the IP was blocked
                                        print(log_entry) 
                                        with  open('/var/log/blocks.log','a') as f:  #Opens the blocks log file in append mode and write the log entry to it
                                                f.write(log_entry)
                                else:
                                        print(f'IP {ip} already blocked') #Prints a message indicating the IP is already blocked
                print('Sleeping...')
                print('==========' * 7) 
                time.sleep(30) #Sleeps for 30 seconds before reading the logs again - you can modify this as you please
        except KeyboardInterrupt: #Prints a message and breaks the loop if the script is interrupted by the user
                print("Interrupted by user, exiting...")
                break
        except Exception as e:
                if debug: #If an exception occurs, print the traceback if debug mode is enabled
                        print(traceback.format_exc())
                        error_time = datetime.datetime.now()
                        with open('/var/log/suribeast.error.log','a') as g: #Opens the error log file in append mode and writes the error details to it
                                g.write(f'{error_time}\n{trafeback.format_exc()}\n')
