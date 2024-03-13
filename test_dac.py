import smbus

# Initialize I2C (SMBus)
bus = smbus.SMBus(1)  # For Raspberry Pi 2/3/4, use 1. For Raspberry Pi 1, use 0.

# MCP4725 default address
MCP4725_DEFAULT_ADDRESS = 0x60

# MCP4725 Command
MCP4725_CMD_WRITEDAC = 0x40

# Function to set DAC voltage
def set_dac_voltage(voltage):
    dac_value = int((voltage / 3.3) * 4095)  # Convert voltage to 12-bit DAC value
    high_byte = (dac_value >> 8) & 0xFF  # High byte
    low_byte = dac_value & 0xFF  # Low byte
    # Send data to MCP4725
    bus.write_i2c_block_data(MCP4725_DEFAULT_ADDRESS, MCP4725_CMD_WRITEDAC, [high_byte, low_byte])

# Set the desired output voltage
desired_voltage = 0.0  # Example voltage (in volts)
set_dac_voltage(desired_voltage)
print(desired_voltage)
