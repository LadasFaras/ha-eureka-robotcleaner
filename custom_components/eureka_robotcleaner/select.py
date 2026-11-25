"""Select platform for Eureka Robot: suction, mop water level and voice pack."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import protocol
from .const import FAN_SPEEDS, STARTABLE_MODES, WATER_LEVELS, WORK_MODES
from .coordinator import PowerBotConfigEntry, PowerBotDataUpdateCoordinator
from .entity import PowerBotEntity

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PowerBotConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the selects."""
    coordinator = entry.runtime_data
    if not coordinator.supported:
        return
    entities: list[SelectEntity] = [PowerBotSuction(coordinator), PowerBotWorkMode(coordinator)]
    # Skip the water level on a robot that reports no mop
    if coordinator.has_mop is not False:
        entities.append(PowerBotWaterLevel(coordinator))
    if coordinator.voices:
        entities.append(PowerBotVoice(coordinator))
    async_add_entities(entities)


class PowerBotSuction(PowerBotEntity, SelectEntity):
    """Suction power, the same as the vacuum's fan speed, for dashboards."""

    _attr_translation_key = "suction"
    _attr_options = FAN_SPEEDS

    def __init__(self, coordinator: PowerBotDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "suction")

    @property
    def current_option(self) -> str | None:
        return self.coordinator.fan_speed

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.async_send(
            protocol.set_suction(*self.coordinator.levels(fan=option))
        )


class PowerBotWaterLevel(PowerBotEntity, SelectEntity):
    """Mop water level; can be changed before or during a clean."""

    _attr_translation_key = "water_level"
    _attr_options = list(WATER_LEVELS)

    def __init__(self, coordinator: PowerBotDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "water_level")

    @property
    def current_option(self) -> str | None:
        return self.coordinator.water_level

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.async_send(
            protocol.set_suction(*self.coordinator.levels(water=option))
        )
        self.coordinator.last_water = option
        self.async_write_ha_state()


class PowerBotWorkMode(PowerBotEntity, SelectEntity):
    """Pick a clean mode and start a clean in it right away.

    This sends the same start command as pressing play on the vacuum entity,
    just with a different mode byte, and it also becomes the mode the vacuum
    entity's own Start button uses next, so the two controls stay in sync.
    """

    _attr_translation_key = "work_mode"
    _attr_options = list(STARTABLE_MODES)

    def __init__(self, coordinator: PowerBotDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "work_mode")

    @property
    def current_option(self) -> str | None:
        # While the robot is actually cleaning, show what it reports; otherwise
        # show the mode a plain Start would use (last one picked here).
        work = self.coordinator.work
        reported = WORK_MODES.get(work.work_mode) if work else None
        if reported in STARTABLE_MODES:
            return reported
        for name, value in STARTABLE_MODES.items():
            if value == self.coordinator.desired_work_mode:
                return name
        return None

    async def async_select_option(self, option: str) -> None:
        self.coordinator.desired_work_mode = STARTABLE_MODES[option]
        await self.coordinator.async_send(
            protocol.start(*self.coordinator.levels(), mode=STARTABLE_MODES[option])
        )
        self.async_write_ha_state()


class PowerBotVoice(PowerBotEntity, SelectEntity):
    """Voice pack. The robot downloads a newly chosen pack by itself."""

    _attr_translation_key = "voice"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator: PowerBotDataUpdateCoordinator) -> None:
        super().__init__(coordinator, "voice")
        self._attr_options = list(coordinator.voices.values())

    @property
    def current_option(self) -> str | None:
        voice = self.coordinator.voice
        return self.coordinator.voices.get(voice) if voice is not None else None

    async def async_select_option(self, option: str) -> None:
        index = next(i for i, name in self.coordinator.voices.items() if name == option)
        await self.coordinator.async_send(protocol.select_voice(index))
        self.coordinator.voice = index
        self.async_write_ha_state()
