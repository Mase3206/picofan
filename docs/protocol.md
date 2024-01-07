[Return to README](../README.md)

# Initialization Protocol

Sensor and device configuration on the Pico(s) is done through Yaml files on the companion device. Once all devices are configured in companion.py, it will communicate with the Pico(s) to initialize them. The following is an example init message:

`fd  01 02 01  01 01  04 05 06  88 fe  00 00 00 00 00`

- `fd` - begin msg
- `01` - tx addr
- `02` - rx addr
- `01` - initialize device command
- `01` - sensor/device type
- `01` - sensor/device addr
- Sensor/device parameters:
	- Fan: (this example)
		- `04` - Power control pin (out)
		- `05` - PWM pin (out)
		- `06` - Tachometer pin (in)
	- Temperature:
		- `1f` - Pico pin connected to shift register (out)
		- `01` - pin on shift register (out)
- `88` - checksum
- `fe` - end msg
- `00 ...` message filler



# Control Protocol

picofan uses a custom protocol with a simple checksum for communicating between the companion and pico(s).

Example message: `fd  01 02 03  01 01 00   7a fe  00 00 00 00 00 00 00`
- `fd` - begin msg
- `01` - tx addr
- `02` - rx addr
- `03` - command (init, init ack, set, get)
	- `01` = init
	- `02` = set
	- `03` = get
- `01` - sensor/device type (fan, temp, etc.)
	- `01` = fan
	- `02` = temp
- `01` - sensor/device addr 
- `00` - value to set/get (speed, temperature, etc.)
	- Fans:
		- `00` = speed
	- Thermal probes
		- `00` = temperature
- `7a` - checksum
- `fe` - end msg
- `00 ...` - message filler

## Checksum

The checksum is calculated in a similar manner to UPC codes:
1. Sum all evens, then multiply by 77. <sup>1</sup>
2. Sum all odds.
3. Take the mod 255 of the sum of both components. <sup>2</sup>
4. Subtract 255 by the previous result. This is your checksum. <sup>2</sup>

> [!NOTE]
> - [1] UPC codes multiply by 3.
> - [2] UPC codes use mod 10 and subtract 10 by the result.


# Examples

I have provided example messages and an ImHex Pattern Language parser in the `docs/examples` directory. 