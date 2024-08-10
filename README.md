# SuriBeast
A two-part linux daemon for automating an adaptive firewall via suricata.

This repository will contain the following: Code for the suricata traffic analysis and firewall creation, necessary files for rule creation and notation, and an explanation of how it works & how you may further optomize this for yourself.

There is no licensing, copyrights, etc involved. Feel free to use and reproduce this however you wish!

A video guide will be coming soon. Stay tuned!
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

To get started, you will need to install suricata. You can find official documentation and steps here: https://docs.suricata.io/en/suricata-6.0.0/install.html

Once you have it installed, you will need to make some changes to the suricata.yaml file in the /etc/suricata directory. 

For starters, do a search for the line containing "af-packet". This will bring you to the linux high speed capture support section. On the interface setting, ensure this is set to your correct default network interface (eth0, br0, wlp1s0, etc).

Then, do a search for the line containing "platform libpcap capture support". Again, ensure this interface setting is set to your correct default network interface that you will be using. 

Next, search for reputation-categories-file, and this will take us to the IP reputation settings. Ensure these settings are set as so:
reputation-categories-file: /etc/suricata/iprep/categories.txt
default-reputation-path: /etc/suricata/iprep
reputation-files: reputation.list

Finally, search for default-rule-path, this will bring us to the rules settings. Ensure that you add custom.rules to the rule-files section. 

Once completed, save the changes to the suricata.yaml file and exit out of your text editor. We will now move on to adding in the custom rules and configuration files!

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

To begin with adding in our custom configurations, we will start with our custom.rules file. Venture over to the rules directory via /etc/suricata/rules and create a new text document following the directions listed in https://github.com/Noa808/SuriBeast/blob/main/Custom.Rules

Once the custom.rules has been added to the rules directory, go ahead and use the command cd .. to move back to the /etc/suricata directory. We will now add in our IPREP rules. To start, we will need to create a new directory inside /etc/suricata called iprep.

To achieve this, use the command mkdir iprep. Once the directory is created, go ahead and create your categories.txt and reputation.list files utilizing the directions listed in:
https://github.com/Noa808/SuriBeast/blob/main/Categories.txt
https://github.com/Noa808/SuriBeast/blob/main/Reputation.list

Next, we will be adding in our SuriBeast python script. Venture over to your home user directory (cd /home/...) and create a new text document named suribeast.py (or any name of your choosing!) and write in the script from https://github.com/Noa808/SuriBeast/blob/main/SuriBeast.py

Once that is saved, venture over to /etc/supervisor/conf.d and create a new text file named suribeast.conf , utilizing the instructions from https://github.com/Noa808/SuriBeast/blob/main/SuriBeast.conf.

Lastly, set up the suricata daemon using the instructions found in https://github.com/Noa808/SuriBeast/blob/main/Suricata.service

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

That's all for the setup! There are many different ways you can personally customize the rulesets of custom.rules, the IP reputations, etc - way too much for me to explain in one post here! 

Here are some basic commands that you will be using throughout the process:

1. suricata --af-packet=(interface)    |     Begins the packet capture. replace (interface) with your interface, ex. eth0, br0, wlp1s0, etc

2. iptables -nL -t raw                 |     Shows your current firewall ruleset.

3. iptables -F -t raw                  |     Resets your firewall ruleset.

4. supervisorctl start suribeast       |     Begins the suribeast daemon that reads the pcap logs and adds rules to the firewall.

5. supervisorctl stop suribeast        |     Ends the suribeast daemon.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Helpful tips:
Before messing around with the daemon, try running the processes manually just by running the suribeast.py script! 
This will show you what is happening while it is running and help you debug any issues with rulesets that you implement. Once everything is working properly and to your liking, go ahead and implement it via the daemon!
