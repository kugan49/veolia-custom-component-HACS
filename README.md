# Veolia

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]


![logo][logoimg]

**This component will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show daily and monthly consumption from Veolia API.

![appareil][appareilimg]

![daily_consumption][daily_consumptionimg]

![monthly_consumption][monthly_consumptionimg]


## Installation

### HACS

Recommended as you get notifications of updates

* Add this repository https://github.com/kugan49/veolia-custom-component-HACS to HACS as a "custom repository" with category "integration". This option can be found in the ⋮ menu
* Install the integration from within HACS
* Restart Home Assistant

### Manual

* Extract the Zip file in the `custom_components` directory
* Restart Home Assistant

## Configuration is done in the UI

Just fill in your username and password when adding the integration

## Special Thanks

A big thanks to [@Pulpyyyy](https://github.com/Pulpyyyy), who helped me a lot in the research

<!---->
***

[commits-shield]: https://img.shields.io/github/commit-activity/y/kugan49/veolia-custom-component-HACS.svg?style=for-the-badge
[commits]: https://github.com/kugan49/veolia-custom-component-HACS/commits/master
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[logoimg]: images/logo.png
[appareilimg]: images/appareil.png
[daily_consumptionimg]: images/daily_consumption.png
[monthly_consumptionimg]: images/monthly_consumption.png
[license-shield]: https://img.shields.io/github/license/kugan49/veolia-custom-component-HACS.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40kugan49-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/kugan49/veolia-custom-component-HACS.svg?style=for-the-badge
[releases]: https://github.com/kugan49/veolia-custom-component-HACS/releases
[user_profile]: https://github.com/kugan49