# Xiaomi TV Custom Component

This repository provides a Home Assistant custom component for controlling Xiaomi televisions. The integration extends the official Xiaomi TV implementation and includes additional features for convenient management via the Home Assistant UI.

## Features

- Configuration via the Home Assistant user interface (config flow).
- External status control to synchronize the TV power state.
- Input source management for switching HDMI ports or casting.
- Browsing and launching installed applications directly from Home Assistant.
- Volume control, mute support and wake/sleep functionality.

## Installation

1. Install through [HACS](https://hacs.xyz/) by adding this repository as a custom source, or manually copy the `custom_components/xiaomi_tv` directory to your Home Assistant configuration.
2. Restart Home Assistant to load the integration.

## Configuration

Use the Home Assistant UI to add the integration:

1. Navigate to **Settings** → **Devices & Services**.
2. Click **Add Integration** and search for **Xiaomi TV**.
3. Enter the TV name and IP address when prompted.

You may alternatively set up the integration in `configuration.yaml`:

```yaml
xiaomi_tv:
  host: 192.168.1.100
  name: Living Room TV
```

## Disclaimer

This project is an independent effort and is not affiliated with Xiaomi. Use it at your own risk.
