The following commands will install, test, and finally enable the service.

```shell script
sudo cp send-temp.service /etc/systemd/system/send-temp.service
sudo systemctl start send-temp.service
sudo systemctl stop send-temp.service
sudo systemctl enable send-temp.service
sudo cp send-temp-restart.bash /usr/local/bin/
sudo chmod +x /usr/local/bin/send-temp-restart.bash
```

Add the following line to root's crontab:

```shell script
sudo crontab -e -u root
```

```
* * * * * /usr/local/bin/send-temp-restart.bash 1>/dev/shm/send-temp-restart.log 2>&1
```