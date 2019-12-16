# Packages

```shell
sudo apt install tmux vim
```

# Python

```shell
pip install -r requirements.txt --upgrade
```

# RabbitMQ

```shell
sudo apt install rabbitmq-server
sudo rabbitmq-plugins enable rabbitmq_management
sudo rabbitmqctl add_user admin admin
sudo rabbitmqctl set_user_tags admin administrator
```

# Testing

Generate a convergence report.

```shell script
pytest --cov-report=html --cov=thermopi
```

# Example reading from a dsb1820

```
89 01 4b 46 7f ff 0c 10 0e : crc=0e YES
89 01 4b 46 7f ff 0c 10 0e t=24562
```

```python
import glob
import time

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

while True:
    print(read_temp())
    time.sleep(1)
```
