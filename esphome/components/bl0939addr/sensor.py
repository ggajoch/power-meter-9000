import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import (
    CONF_ID,
    CONF_VOLTAGE,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_VOLTAGE,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
    UNIT_AMPERE,
    UNIT_KILOWATT_HOURS,
    UNIT_VOLT,
    UNIT_WATT,
    CONF_ADDRESS,
)

DEPENDENCIES = ["uart"]

CONF_CURRENT_1 = "current_1"
CONF_CURRENT_2 = "current_2"
CONF_ACTIVE_POWER_1 = "active_power_1"
CONF_ACTIVE_POWER_2 = "active_power_2"
CONF_ENERGY_1 = "energy_1"
CONF_ENERGY_2 = "energy_2"
CONF_ENERGY_TOTAL = "energy_total"
CONF_CURRENT_REFERENCE = "current_reference"
CONF_VOLTAGE_REFERENCE = "voltage_reference"
CONF_POWER_REFERENCE = "power_reference"
CONF_ENERGY_REFERENCE = "energy_reference"
CONF_WA_CREEP = "wa_creep"


# https://datasheet.lcsc.com/lcsc/2108071830_BL-Shanghai-Belling-BL0939_C2841044.pdf
# (unfortunately chinese, but the formulas can be easily understood)
# Sonoff Dual R3 V2 has the exact same resistor values for the current shunts (RL=1miliOhm)
# and for the voltage divider (R1=0.51kOhm, R2=5*390kOhm)
# as in the manufacturer's reference circuit, so the same formulas were used here (Vref=1.218V)
default_current_reference = 324004 * 1 / 1.218
default_voltage_reference = 79931 * 0.51 * 1000 / (1.218 * (5 * 390 + 0.51))
default_power_reference = 4046 * 1 * 0.51 * 1000 / (1.218 * 1.218 * (5 * 390 + 0.51))
default_energy_reference = 3.6e6 * 4046 * 1 * 0.51 * 1000 / (1638.4 * 256 * 1.218 * 1.218 * (5 * 390 + 0.51))

bl0939_ns = cg.esphome_ns.namespace("bl0939")
BL0939 = bl0939_ns.class_("BL0939", cg.PollingComponent, uart.UARTDevice)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(BL0939),
            cv.Optional(CONF_VOLTAGE): sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_VOLTAGE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_CURRENT_1): sensor.sensor_schema(
                unit_of_measurement=UNIT_AMPERE,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_CURRENT,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_CURRENT_2): sensor.sensor_schema(
                unit_of_measurement=UNIT_AMPERE,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_CURRENT,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_ACTIVE_POWER_1): sensor.sensor_schema(
                unit_of_measurement=UNIT_WATT,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_ACTIVE_POWER_2): sensor.sensor_schema(
                unit_of_measurement=UNIT_WATT,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_ENERGY_1): sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT_HOURS,
                accuracy_decimals=3,
                device_class=DEVICE_CLASS_ENERGY,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            cv.Optional(CONF_ENERGY_2): sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT_HOURS,
                accuracy_decimals=3,
                device_class=DEVICE_CLASS_ENERGY,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            cv.Optional(CONF_ENERGY_TOTAL): sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT_HOURS,
                accuracy_decimals=3,
                device_class=DEVICE_CLASS_ENERGY,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            cv.Optional(CONF_ADDRESS, default=5): cv.uint8_t,
            cv.Optional(CONF_CURRENT_REFERENCE, default=default_current_reference): cv.float_,
            cv.Optional(CONF_VOLTAGE_REFERENCE, default=default_voltage_reference): cv.float_,
            cv.Optional(CONF_POWER_REFERENCE, default=default_power_reference): cv.float_,
            cv.Optional(CONF_ENERGY_REFERENCE, default=default_energy_reference): cv.float_,
            cv.Optional(CONF_WA_CREEP, default=0x0B): cv.uint8_t,
        }
    )
    .extend(cv.polling_component_schema("60s"))
    .extend(uart.UART_DEVICE_SCHEMA)
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    # cg.add()

    if voltage_config := config.get(CONF_VOLTAGE):
        sens = await sensor.new_sensor(voltage_config)
        cg.add(var.set_voltage_sensor(sens))
    if current_1_config := config.get(CONF_CURRENT_1):
        sens = await sensor.new_sensor(current_1_config)
        cg.add(var.set_current_sensor_1(sens))
    if current_2_config := config.get(CONF_CURRENT_2):
        sens = await sensor.new_sensor(current_2_config)
        cg.add(var.set_current_sensor_2(sens))
    if active_power_1_config := config.get(CONF_ACTIVE_POWER_1):
        sens = await sensor.new_sensor(active_power_1_config)
        cg.add(var.set_power_sensor_1(sens))
    if active_power_2_config := config.get(CONF_ACTIVE_POWER_2):
        sens = await sensor.new_sensor(active_power_2_config)
        cg.add(var.set_power_sensor_2(sens))
    if energy_1_config := config.get(CONF_ENERGY_1):
        sens = await sensor.new_sensor(energy_1_config)
        cg.add(var.set_energy_sensor_1(sens))
    if energy_2_config := config.get(CONF_ENERGY_2):
        sens = await sensor.new_sensor(energy_2_config)
        cg.add(var.set_energy_sensor_2(sens))
    if energy_total_config := config.get(CONF_ENERGY_TOTAL):
        sens = await sensor.new_sensor(energy_total_config)
        cg.add(var.set_energy_sensor_sum(sens))
    if address_config := config.get(CONF_ADDRESS):
        cg.add(var.set_address(address_config))
    if current_reference_config := config.get(CONF_CURRENT_REFERENCE):
        cg.add(var.set_current_reference(current_reference_config))
    if voltage_reference_config := config.get(CONF_VOLTAGE_REFERENCE):
        cg.add(var.set_voltage_reference(voltage_reference_config))
    if power_reference_config := config.get(CONF_POWER_REFERENCE):
        cg.add(var.set_power_reference(power_reference_config))
    if energy_reference_config := config.get(CONF_ENERGY_REFERENCE):
        cg.add(var.set_energy_reference(energy_reference_config))
    if wa_creep_config := config.get(CONF_WA_CREEP):
        cg.add(var.set_wa_creep(wa_creep_config))