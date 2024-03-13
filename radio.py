import RPi.GPIO as GPIO
from pydub import AudioSegment
import array
import time
import smbus



# Initialize I2C (SMBus)
bus = smbus.SMBus(1) # use 1 for raspberry pi 2/3/4/5. use 0 for raspberry pi 1.

# MCP4725 default address
MCP4725_DEFAULT_ADDRESS = 0x62

# MCP4725 Command
MCP4725_CMD_WRITEDAC = 0x40

# Function to set DAC voltage
def set_dac_voltage(voltage):
	dac_value = int((voltage / 3.3) * 4095) # Convert voltage to 12-bit DAC value
	high_byte = (dac_value >> 8) & 0xFF # high byte
	low_byte = dac_value & 0xFF #Low byte

	# Send data to MCP4725
	bus.write_i2c_block_data(MCP4725_DEFAULT_ADDRESS, MCP4725_CMD_WRITEDAC, [high_byte, low_byte])



# set gpio mode and pin
GPIO.setmode(GPIO.BCM)
output_pin = 18 # desiered gipo pin, pin 18

# set the pin as output
GPIO.setup(output_pin, GPIO.OUT)

# create a PWM object with a frequency (Hz)
pwm = GPIO.PWM(output_pin, 44100) # Use the audio sample rate as the frequency

try:
	#load WAV file
	audio = AudioSegment.from_file("portal-radio.wav")

	# convert to raw data (16-bit PCM)
	audio_data = array.array("h", audio.raw_data)

	# Normalise the data to the range [0, 1]
	normalized_data = [((sample + 32768) / 65535.0) for sample in audio_data]

	# Scale the data to the PWM range (0-100)
	pwm_data = [int(sample * 100) for sample in normalized_data]

	# start PWM
	#pwm.start(50) # Start with a 50% duty cycle        If you want PWM on pin 18 as well.

	# Send PWM data
	for duty_cycle in pwm_data:
		# set the DAC voltage based on the PWM duty cycle
		voltage = (duty_cycle / 100.0) * 3.3
		set_dac_voltage(voltage)
		#pwm.ChangeDutyCycle(duty_cycle)             IF you want PWM on pin 18 as well.
		time.sleep(1 / 44100) # Sleep for the duration of one audio sample

finally:
	# cleanup GPIO on exit
	pwm.stop()
	GPIO.cleanup()
