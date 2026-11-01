# Eureka Robot Cleaner pro Home Assistant (neoficiální)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz)
[![Validate](https://github.com/LadasFaras/ha-eureka-robotcleaner/actions/workflows/validate.yml/badge.svg)](https://github.com/LadasFaras/ha-eureka-robotcleaner/actions/workflows/validate.yml)
[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=LadasFaras&repository=ha-eureka-robotcleaner&category=integration)


[English](README.md) | **Čeština**

Vlastní integrace Home Assistantu pro **robotické vysavače Eureka** (ověřeno na
**Eureka NER E10s**). Integrace pro tyto roboty dosud neexistovala, proto
komunikuje přímo s cloudem výrobce.

## Jak to vzniklo

- Aplikace Eureka běží na stejném cloudu Midea jako Samsung POWERbot-S
  (`mzrobo.com`) a používá stejnou rodinu protokolu.
- [TSOrest/powerbot-s-ha](https://github.com/TSOrest/powerbot-s-ha) už
  podporovalo Samsung, tento projekt je jeho fork (MIT, díky!).
- Vlastní client ID aplikace Eureka (`1301`) jsme zjistili analýzou přihlášení
  a provozu aplikace, přidali kód modelu E10s (`9A0VR870`) a výběr módu úklidu.

## Instalace

**HACS:** přidejte tento repozitář jako vlastní repozitář (kategorie
*Integration*), nainstalujte a restartujte Home Assistant.

**Ručně:** zkopírujte `custom_components/eureka_robot/` do `config/custom_components/`.

Potom *Nastavení → Zařízení a služby → Přidat integraci → Eureka Robot Cleaner* a
přihlaste se e-mailem a heslem z aplikace Eureka.

## Známá omezení

- `vacuum.locate` na E10s nefunguje (bajty příkazu jsou ze Samsungu; je nutný
  záchyt skutečného požadavku aplikace).
- Ověřen je jen model E10s. Jiné modely mohou fungovat, pokud sdílí protokol,
  ale jejich kód modelu je nutné přidat do `SUPPORTED_SN8`.
- Funguje jen přes cloud: potřebuje internet a účet Eureka.

Není spojeno s Eureka ani Midea. Licence MIT.
