[Return to README](../README.md)

# Protocol

picofan uses a custom protocol with a simple checksum for communicating between the companion and pico(s).

Example message: `fd  01 0a 01  01 01 01   be fe`
- `fd` - start msg
- `01` - tx addr
- `0a` - rx addr
- `01` - command (set, get, etc.)
- `01` - sensor/device type (fan, temp, etc.)
- `01` - sensor/device addr 
- `01` - value to set/get (speed, temperature, etc.)
- `be` - checksum
- `fe` - end msg

## Checksum

The checksum is calculated in the same manner as UPC codes:
1. Sum all evens, then multiply by 3.
2. Sum all odds.
3. Take the mod 255 of the sum of both components. 
4. Subtract 255 by the previous result. This is your checksum.

> [!NOTE]
> UPC codes use mod 10 and subtract 10 by the result. Standard decimal is base-10, but one byte of hex is base 255, so 255 is substituted for 10.
