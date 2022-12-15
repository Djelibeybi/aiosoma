# Usage

To use this package, import `AioSoma`:

```python
from aiosoma import AioSoma
```

Next, create an `AioSoma` object using either the hostname or IP address and port
of your SOMA Connect. Using a static IP address is recommended.

```python
soma = AioSoma("soma-connect.local", 3000)
```

## Methods

### list_devices()

Use to list all the devices visible to SOMA Connect. The `mac` address of the
shade you want to control is a required parameter for all the other methods.

```json
{
  "result": "success",
  "version": "2.3.1",
  "shades": [
    {
      "name": "Office",
      "mac": "aa:bb:cc:dd:ee:ff",
      "type": "shade",
      "gen": "2S"
    },
    {
      "name": "Kitchen",
      "mac": "aa:b1:cc:d1:ee:f1",
      "type": "shade",
      "gen": "2S"
    },
    {
      "name": "Lounge",
      "mac": "a1:bb:c1:dd:e1:ff",
      "type": "shade",
      "gen": "2S"
    }
  ]
}
```

### get_shade_state(mac)

Returns the firmware version and current position of the shade:

```json
{
  "result": "success",
  "version": "2.3.1",
  "mac": "aa:bb:cc:dd:ee:ff",
  "position": 0
}
```

### open_shade(mac)

This method will open the shade unless stopped by manually calling `stop_shade()`.

Returns:

```json
{ "result": "success", "version": "2.3.1", "mac": "aa:bb:cc:dd:ee:ff" }
```

### close_shade(mac)

This method will close the shade unless stopped by manually calling `stop_shade()`.

Returns:

```json
{ "result": "success", "version": "2.3.1", "mac": "aa:bb:cc:dd:ee:ff" }
```

### stop_shade(mac)

This method will stop any movement currently in progress.

Returns:

```json
{ "result": "success", "version": "2.3.1", "mac": "aa:bb:cc:dd:ee:ff" }
```

### set_shade_position(MAC, position: int, close_upwards: bool = False, morning_mode: bool = False)

This method will set the shade to `position`, where 0 is fully open
and 100 is fully closed. To close Tilt shades upwards, set `close_upwards` to `True`.
To enable the slower and quieter morning mode, set `morning_mode` to `True`.

Returns:

```json
{ "result": "success", "version": "2.3.1", "mac": "aa:bb:cc:dd:ee:ff" }
```

### get_battery_level(mac)

Returns the current battery level of the shade:

```json
{
  "result": "success",
  "version": "2.3.1",
  "mac": "aa:bb:cc:dd:ee:ff",
  "battery_level": 420,
  "battery_percentage": 100
}
```

### get_light_level(mac)

Returns the current solar panel light level from the device, if the solar panel
charger is connected. This requires a connect to the SOMA shade and should not
be polled often or across multiple devices at the same time.

```json
{
  "result": "success",
  "version": "2.3.1",
  "mac": "aa:bb:cc:dd:ee:ff",
  "light_level": 5153
}
```
