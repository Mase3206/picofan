# picofan
Picofan is a Raspberry Pi Pico-based fan controller supporting PWM fans, speed measurement, and automatic speed adjustment. A RP2040-based PCB will be published in the future.

## Hardware Requirements

### Fans

Currenly, only PWM fans are supported due to their ease of digital control. Support for voltage-controlled fans may be implemented in the future.

picofan is fan voltage-agnostic by controlling fan power with individual transistors. <!-- TODO: add info about board vcc voltages when PCB and schematics are added to repo -->

### Temperature Sensors

Fan speed can be set to adjust automatically via a default or user-defined curve with feedback from one or more temperature sensors. Only analogue sensors are supported at this time, and they must be connected to a static serial shift register, such as the [Texas Instruments CD4021B](https://www.ti.com/product/CD4021B#pps). The RP2040 has four ADCs, three of which are available to the user on the Pico; one is reserved for the on-board temperature sensor.

### Control

picofan can be controlled by a Raspberry Pi 2 or later at the moment, but support for any device with a UART interface is planned. For my development, I am using a Raspberry Pi 3b. 

## Software

picofan has two software components:
1. Pico code, written in MicroPython
2. Companion device code, written in standard Python 3

The two devices communicate via a [custom protocol](./docs/protocol.md) over UART0 and use unique addresses to identify the command sender and recipient.