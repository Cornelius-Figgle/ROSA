
# ROSA

ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

An emotional smart assistant that doesn't listen to you

## Installation

### Windows

Download the `ROSA.exe` / `ROSA` file from the `/bin` dir at [GitHub](https://github.com/Cornelius-Figgle/ROSA/tree/main/bin)

## Usage

### Prerequisites

- [ROSA binary file](https://github.com/Cornelius-Figgle/ROSA/tree/main/bin)

### Setup

- If you are on a Raspberry Pi that has LEDs connected to the GPIO header/breadboard/etc, you can download the [`gpio.ini`](https://github.com/Cornelius-Figgle/ROSA/blob/main/gpio.ini) file from GitHub and stick it in the same directory you saved the executable/binary file
- You can then write the pin numbers in the file to let ROSA use the LEDS. You can also write the pin number for a push button that will run the RPi shutdown command when pressed (useful if you are using ROSA without a monitor). [See the file for more info](https://github.com/Cornelius-Figgle/ROSA/blob/main/gpio.ini)
- Please make sure you have connected your mic and speakers
- Your internet connection is stable (used to transcribe speech via Google Speech Recognition)

Then you should be able to run the `ROSA.exe` / `ROSA` file from wherever saved it

## License

[MIT](https://github.com/Cornelius-Figgle/ROSA/blob/main/LICENSE)
