@echo off

SET time=5
SET dir=%~dp0
echo %dir%

SET cmd=schtasks /create /sc minute /mo %time% /tn "Slack Stat Schedule" /tr "'%dir%slackstat.exe' '%dir%config.ini'"
echo %cmd%
%cmd%