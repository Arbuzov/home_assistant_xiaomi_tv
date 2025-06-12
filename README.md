# Xiaomi TV Custom Component

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![License](https://img.shields.io/github/license/Arbuzov/home_assistant_xiaomi_tv?style=for-the-badge)](https://github.com/Arbuzov/home_assistant_xiaomi_tv/blob/master/LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/Arbuzov/home_assistant_xiaomi_tv?style=for-the-badge)](https://github.com/Arbuzov/home_assistant_xiaomi_tv/releases)
[![Latest Release](https://img.shields.io/badge/dynamic/json?style=for-the-badge&color=41BDF5&logo=home-assistant&label=integration%20usage&suffix=%20installs&cacheSeconds=15600&url=https://analytics.home-assistant.io/custom_integrations.json&query=$.xiaomi_tv.total)](https://analytics.home-assistant.io/custom_integrations.json)
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Arbuzov&repository=home_assistant_xiaomi_tv&category=integration)
[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=xiaomi_tv)
![Company logo](https://brands.home-assistant.io/xiaomi_tv/logo.png)

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
