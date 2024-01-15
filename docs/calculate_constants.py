import math

def parallel(a, b):
    return a*b/(a+b)


# Voltage divider resistors

#####################
# 230 V RMS -----
#               |
#               |
#            ------
#            |    |
#            | R1 |
#            |    |
#            ------
#               |
#               |---------------
#               |              |
#            ------         ------
#            |    |         |    |
#            | R2 |         | R3 |
#            |    |         |    |
#            ------         ------
#              |               |
#              |               |----------------- BL0939 - 70mV RMS
#              |               |
#              |            ------
#              |            |    |
#              |            | R4 |
#              |            |    |
#              |            ------
#              |               |
# N/PE -------------------------


R1 = 5*499e3
R2 = 100e3/2
R3 = 27e3
R4 = 1e3

# R1 = 5*499e3
# R2 = 22e3
# R3 = 10e3
# R4 = 1e3

# Voltage divider ratio
r234 = parallel(R2, R3 + R4)
intermediate = r234 / (R1 + r234)
print(f'Intermediate voltage: {round(230*intermediate, 3)}')
divider = intermediate * R4 / (R3 + R4)
output = 230 * divider
print(f"Voltage divider output: {round(output, 6)}")

print(f"Fault voltage: {round(230*2*R2/(R1+2*R2), 3)}")

# ADC range
adc_range = 70e-3
adc_utilization = output / adc_range
print(f"ADC full scale utilization: {round(100*adc_utilization, 3)}%")

# Max measurable voltage
max_voltage = adc_range / divider
print(f"Max measurable voltage: {round(max_voltage, 3)}")


Vref = 1.218
# voltage = register / calibration
# voltage = register * Vref / (79931 * 1000 * divider)
voltage_constant = (79931 * 1000 * divider) / Vref
print(f"Voltage Constant: {round(voltage_constant, 3)}")


# -------------------------------------------------------
# Current transformer
print('----------------------')

Rsamp = 3.3
Rfilt = 1e3
Cfilt = 33e-9
Tratio = 2000

# current = register / calibration
# current = register * Vref * Tratio / (324004 * Rsamp * 1000)

current_constant = 324004 * Rsamp * 1000 / (Vref * Tratio)

print(f"Current Constant: {round(current_constant, 3)}")

adc_range = 35e-3
# voltage = current/Tratio * Rsamp
# current = voltage * Tratio / Rsamp
max_measurable_current = adc_range * Tratio / Rsamp
print(f"Max measurable current: {round(max_measurable_current, 3)} A")


# low pass filter
fcutoff = 1/(2*math.pi*Rfilt*Cfilt)
print(f"Low pass filter cutoff frequency: {round(fcutoff, 3)} Hz")



# -------------------------------------------------------
# Power
print('----------------------')
# power_reference = current_reference * voltage_reference * 2023 / 12948981862
power_constant = current_constant * voltage_constant * 2023 / 12948981862
print(f"Power Constant: {round(power_constant, 3)}")


# -------------------------------------------------------
# Energy
print('----------------------')
# energy_reference = 3.6e6/(1638.4 * 256) * power_reference
energy_constant = 3.6e6/(1638.4 * 256) * power_constant
print(f"Energy Constant: {round(energy_constant, 3)}")



# -------------------------------------------------------
# Yaml
print('----------------------')
    # current_reference: 438921.675 # 324004*(3.3*1000)/2000/1.218
    # voltage_reference: 17483.267 # 79931 * 0.97 * 1000 / (1.218 * (3640 + 0.97))
    # power_reference: 1198.864 # current_reference * voltage_reference * 2023 / 12948981862
    # energy_reference: 10289.932 # 3.6e6/(1638.4 * 256) * power_reference
print(f"    current_reference: {round(current_constant, 3)}")
print(f"    voltage_reference: {round(voltage_constant, 3)}")
print(f"    power_reference: {round(power_constant, 3)}")
print(f"    energy_reference: {round(energy_constant, 3)}")
