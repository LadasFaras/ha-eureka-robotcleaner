# Eureka Robot Cleaner for Home Assistant (unofficial)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz)
[![Validate](https://github.com/LadasFaras/ha-eureka-robotcleaner/actions/workflows/validate.yml/badge.svg)](https://github.com/LadasFaras/ha-eureka-robotcleaner/actions/workflows/validate.yml)
[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=LadasFaras&repository=ha-eureka-robotcleaner&category=integration)


[English](README.md) | [Čeština](README.cs.md)

Home Assistant custom integration for **Eureka robot vacuums** (tested on the
**Eureka NER E10s**). No HA integration for these robots existed, so this one
talks to the vendor cloud directly.

## How it came about

- The Eureka app turned out to run on the same Midea cloud as the Samsung
  POWERbot-S (`mzrobo.com`), using the same protocol family.
- [TSOrest/powerbot-s-ha](https://github.com/TSOrest/powerbot-s-ha) already
  supported the Samsung model, so this project is a fork of it (MIT, thanks!).
- The Eureka app's own client ID (`1301`) was found by inspecting the app's
  login flow and traffic, the E10s model code (`9A0VR870`) was added, and a
  clean-mode select was introduced.

## Install

**HACS:** add this repo as a custom repository (category *Integration*),
install, restart Home Assistant.

**Manual:** copy `custom_components/eureka_robot/` into your HA `config/custom_components/`.

Then go to *Settings → Devices & services → Add integration → Eureka Robot*
and sign in with your Eureka app e-mail and password.

## Known limitations

- `vacuum.locate` does not work on the E10s (the command bytes come from the
  Samsung and are wrong here; a capture of the real app request is needed).
- Only the E10s is verified. Other Eureka models may work if they share the
  protocol, but their model code must be added to `SUPPORTED_SN8`.
- Cloud-only: needs internet and your Eureka account.

Not affiliated with Eureka or Midea. Licensed under MIT.
