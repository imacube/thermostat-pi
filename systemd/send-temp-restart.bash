#!/bin/bash

journalctl -u send-temp.service -n1 | grep -q 'digi.xbee.exception.XBeeException: Packet listener is not running.' &&\
 systemctl restart send-temp.service
