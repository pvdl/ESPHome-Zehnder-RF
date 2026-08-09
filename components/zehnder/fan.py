import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import fan
from esphome.const import CONF_ID, CONF_UPDATE_INTERVAL

from esphome.components.nrf905 import nRF905Component
from . import zehnder_ns, ZehnderRF


DEPENDENCIES = ["nrf905"]

CONF_NRF905 = "nrf905"
CONF_PRESET_MODES = "preset_modes"

CONFIG_SCHEMA = fan.fan_schema(ZehnderRF).extend(
    {
        cv.Required(CONF_NRF905): cv.use_id(nRF905Component),
        cv.Optional(CONF_UPDATE_INTERVAL, default="30s"): cv.update_interval,
        cv.Optional(CONF_PRESET_MODES): cv.ensure_list(cv.string_strict),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await fan.register_fan(var, config)

    nrf905 = await cg.get_variable(config[CONF_NRF905])
    cg.add(var.set_rf(nrf905))
    cg.add(var.set_update_interval(config[CONF_UPDATE_INTERVAL]))

    if CONF_PRESET_MODES in config:
        cg.add(var.set_supported_preset_modes(config[CONF_PRESET_MODES]))
