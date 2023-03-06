# check-mk-homeassistant
A Check MK plug in for homeassistant

# Installation
* Log into Check MK as your site user
* `pip3 install beautifulsoup`
* Install this plug-in into `~/local/bin`

# Then pick **one** of the following two configuration options:
**Check the HomeAssistant observer ONLY**
  * Create a rule in Check MK for `Individual program call instead of agent access` to call `check_haobserver.py $HOSTNAME$` instead of the Check MK agent
  * Perform service discovery
  
**Use the Linux `check_mk_agent` in addition to checking the HomeAssistant observer**
  * Set up monitoring via SSH as in this thread:
    https://forum.checkmk.com/t/homeassistant-monitoring-plugin/36753
  * Add this agent after the SSH commandline separated by a semi-colon and append the option `local` as below:
    `ssh -T siteuser@homeassistant /config/check_mk_agent; check_haobserver.py homeassistant local`
  * Perform service discovery
  
# Monitored services
After service discovery, you should see services for Supervisor, Supported, and Healthy
These services have perfdata labeled `connected` which is the CSS class used to determine if the haobserver sees a problem.
