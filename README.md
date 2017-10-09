# Weather-Alerter

A python script that will send an email using gmail when the outdoor vs indoor temperature changes.

I made this script because my home doesn't have air conditioning, so we open up the windows whenever the outside temperature is warmer than indoors, but then we close the windows once it's colder outside.

## Requirements

- Python
- An installed Ambient Weather Station that includes outdoor and indoor temperature sensors.  You'll also need to have access to the ambient weather observerIP 3.0 at the address 192.168.0.99

## Running the script

This uses insecure auth with gmail, so use at your own risk.

```
python script.py your-email@gmail.com PASSWORD another-to-email@email.com
```

I run this script using cron.
