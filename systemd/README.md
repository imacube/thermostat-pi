The following commands will install, test, and finally enable the service.

```shell script
sudo cp send-temp.service /etc/systemd/system/send-temp.service
sudo systemctl start send-temp.service
sudo systemctl stop send-temp.service
sudo systemctl enable send-temp.service
```