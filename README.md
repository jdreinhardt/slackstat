# Slack Stat
A easy and customizable way to quickly get server status notifications into a Slack team

Due to the way that statistics are polled this script currently only runs on windows

## Requirements
Python 3
Modules
* winstats: <code>pip install winstats</code>
* requests: <code>pip install requests</code>
* configparser: <code>pip install configparser</code>

## Configuration
* MONITOR_CPU - Determines if updates are sent for CPU spikes. Valid parameters - True, False
* MONITOR_MEMORY - Determines if updates are sent for memory usage. Valid parameters - True, False
* MONITOR_DRIVES - Determines if updates are sent for attached hard drives. Valid parameters - True, False
* ALLOW_REMOTE_DISK - Determines if remote disks (network shares) are monitored. Valid parameters - True, False
* ADVISORY_LIMIT, WARNING_LIMIT, DANGER_LIMIT - Sets the percentage thresholds to send notifications
* SLACK_WEBHOOK - URL of pre-assinged incoming webhook in Slack
* CHANNEL_OVERRIDE - Allows for override of Slack channel specified in webhook configuration. Valid parameters - '', #<channel name>, @<username>
  * ie. USERNAME_OVERRIDE = #general
  * ie. USERNAME_OVERRIDE = @jdreinhardt
* USERNAME_OVERRIDE - Allows for override of bot username in Slack. Valid parameters - '', SystemID, any text
* ICON_OVERRIDE - Allows for override of bot icon in Slack. Valid parameters - '', full URL of image
