import time
from neopixel import *
import argparse

# LED strip configuration:
LED_COUNT      = 1000      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
CUBE_DIM       = 10      # define cube dimension
LIT_LEDS       = 100     # number of LEDs lit at one time

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def cubeCorrect(litLEDS):
    for i in range(LIT_LEDS):
        led = 100*litLEDS[i][1] + 10*litLEDS[i][2] + litLEDS[i][0]
        x = led % (2*CUBE_DIM)
        if( x >= CUBE_DIM):
            litLEDS[i][0] = litLEDS[i][0] + (-1)*((x - CUBE_DIM) - (CUBE_DIM - 1))

def mapCube(strip, litLEDS):
    """use litLEDinfo to light necessary LEDs"""

    for i in range(LIT_LEDS):
        led = 100*litLEDS[i][1] + 10*litLEDS[i][2] + litLEDS[i][0]
        color = Color(litLEDS[i][4], litLEDS[i][3], litLEDS[i][5])
        strip.setPixelColor(led, color)
        strip.show()

    


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    #create cube arrays
    cube = [[[0 for z in range (10)] for y in range (10)] for x in range (10)]
    litLEDS = [[1 for i in range (6)] for j in range (100)]

    litLEDS[0] = [0,0,0,255,0,0]
    litLEDS[1] = [2,0,0,0,255,0]
    litLEDS[2] = [4,0,0,0,0,255]
    litLEDS[3] = [0,0,1,255,0,0]
    litLEDS[4] = [5,0,1,234,123,85]

    try: 
        cubeCorrect(litLEDS)
        while True:
            mapCube(strip, litLEDS)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)