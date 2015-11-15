#! /usr/bin/env python

import RPi.GPIO as GPIO
import time

def led_init(gpio_num):
    GPIO.setup(gpio_num, GPIO.OUT)	# set GPIO5 output

	
def led_on(gpio_num):
    GPIO.output(gpio_num, GPIO.HIGH)	# LED ON

	
def led_off(gpio_num):	
    GPIO.output(gpio_num, GPIO.LOW)	# LED OFF


def main():	

    #Flashing number of times
    FLASH_LED_NUM = 5 

    #start
    GPIO.setmode(GPIO.BCM)		# use GPIO Number

    
    gpio_num = 5			# gpio_num --> GPIO5
    led_init(gpio_num)

    for i in range(FLASH_LED_NUM):
        led_on(gpio_num)
        time.sleep(0.5)

        led_off(gpio_num)
        time.sleep(0.5)

    GPIO.cleanup()

    print("led done")
    
    return 0


if __name__ == "__main__":
    main()
