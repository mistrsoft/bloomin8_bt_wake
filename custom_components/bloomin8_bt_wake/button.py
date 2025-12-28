import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.components.bluetooth import async_ble_device_from_address
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

import bleak
from bleak import BleakClient

from .const import (
    DOMAIN,
    BLE_SERVICE_UUID,
    BLE_CHAR_UUID,
    BLE_WAKE_PAYLOAD1,
    BLE_WAKE_PAYLOAD2,
    CONF_MAC_ADDRESS,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the button entity."""
    mac_address = entry.data[CONF_MAC_ADDRESS]
    name = entry.title
    
    async_add_entities([Bloomin8WakeButton(hass, mac_address, name)])


class Bloomin8WakeButton(ButtonEntity):
    """Representation of a Bloomin8 Wake Button."""

    def __init__(self, hass: HomeAssistant, mac_address: str, name: str) -> None:
        """Initialize the button."""
        self.hass = hass
        self._mac = mac_address
        self._attr_name = name
        self._attr_unique_id = f"{mac_address}_wake_button"
        self._attr_icon = "mdi:bluetooth-connect"

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.info("Sending BLE wake signal to %s", self._mac)
        
        # Use HA's bluetooth manager to find the device
        device = async_ble_device_from_address(self.hass, self._mac, connectable=True)
        
        if not device:
             _LOGGER.warning("Device %s not found in HA Bluetooth cache or not connectable", self._mac)
             return

        try:
            async with BleakClient(device) as client:
                if not client.is_connected:
                     _LOGGER.error("Failed to connect to %s", self._mac)
                     return

                # Write the confirmed magic bytes
                await client.write_gatt_char(BLE_CHAR_UUID, BLE_WAKE_PAYLOAD1, response=True)
                _LOGGER.info("Wake signal 1 sent successfully!")
                await client.write_gatt_char(BLE_CHAR_UUID, BLE_WAKE_PAYLOAD2, response=True)
                _LOGGER.info("Wake signal 2 sent successfully!")
                
        except Exception as e:
            _LOGGER.error("Failed to send wake signal: %s", e)


