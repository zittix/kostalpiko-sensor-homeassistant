# kostalpiko-sensor-homeassistant
A custom component to get the readings of a Kostal Piko v2.5 or later.

The component is based on reading the 'live chart' data from web interface, using the XML file.
You can try like this
```
http://<YOUR_INVERTER_IP>/all.xml
```
Otherwise it will not work

```
sensor:
  - platform: kostal
    host: !secret kostal_host  # "http://192.168.xx.xx"
    username: !secret kostal_username
    password: !secret kostal_password
    monitored_conditions:
      - solar_generator_power
      - ac_voltage
      - ac_current
```
