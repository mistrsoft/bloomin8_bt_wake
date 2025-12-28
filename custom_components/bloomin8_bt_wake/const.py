"""Constants for the Bloomin8 Bluetooth Wake integration."""

DOMAIN = "bloomin8_bt_wake"

CONF_MAC_ADDRESS = "mac_address"

# Confirmed BLE Details from Reverse Engineering
BLE_SERVICE_UUID = "0000f000-0000-1000-8000-00805f9b34fb"
BLE_CHAR_UUID = "0000f001-0000-1000-8000-00805f9b34fb"
BLE_WAKE_PAYLOAD1 = b"\x01"
BLE_WAKE_PAYLOAD2 = b"\x00"

DEFAULT_NAME = "Bloomin8 Wake Button"
