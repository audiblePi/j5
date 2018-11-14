# Following code is tested with Raspberry Pi 3
# Import the Libraries Required
import RPi.GPIO as GPIO
# import time

# SERVO_PIN = 12

# if __name__ == '__main__':
# 	# Setting the GPIO Mode to BOARD => Pin Count Mapping 
# 	GPIO.setmode(GPIO.BOARD)

# 	# Setting the GPIO Mode to BCM => GPIO Mapping 
# 	# Uncomment below line for to use GPIO number
# 	# GPIO.setmode(GPIO.BCM)

# 	# Setting the GPIO 18 as PWM Output 
# 	GPIO.setup(SERVO_PIN,GPIO.OUT)

# 	# Disable the warning from the GPIO Library
# 	GPIO.setwarnings(False)

# 	# Starting the PWM and setting the initial position of the servo with 50Hz frequency 
# 	servo = GPIO.PWM(SERVO_PIN,50)
# 	servo.start(0)
# 	while True:
# 		try:
# 			# Changing the Duty Cycle to rotate the motor 
# 			servo.ChangeDutyCycle(7.5)
# 			# Sleep for 5 Seconds 
# 			time.sleep(5)
# 			servo.ChangeDutyCycle(12.5)
# 			time.sleep(5)
# 			servo.ChangeDutyCycle(2.5)
# 			time.sleep(5)

# 		#except KeyboardInterrupt:
# 		#	servo.stop()
# 		#s	GPIO.cleanup()
# # End of the Script

# Servo Control
# import time
# import wiringpi
 
# # use 'GPIO naming'
# wiringpi.wiringPiSetupGpio()
 
# # set #18 to be a PWM output
# wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT) #pan
# wiringpi.pinMode(13, wiringpi.GPIO.PWM_OUTPUT) #tilt
 
# # set the PWM mode to milliseconds stype
# wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
 
# # divide down clock
# wiringpi.pwmSetClock(192)
# wiringpi.pwmSetRange(2000)
 
# delay_period = 0.01
# pan_MAX = 230
# pan_MIN = 70
# tilt_MAX = 100
# tilt_MIN = 230
 
# while True:
#     for pulse in range(pan_MIN, pan_MAX, 1):
#             wiringpi.pwmWrite(18, pulse)
#             time.sleep(delay_period)
#     for pulse in range(pan_MAX, pan_MIN, -1):
#             wiringpi.pwmWrite(18, pulse)
#             time.sleep(delay_period)



