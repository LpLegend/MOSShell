from ghoshell_common.contracts import LoggerItf
from ghoshell_container import IoCContainer

from ghoshell_moss.core.blueprint.mindflow import (
    NucleusMeta,
    Nucleus,
    SignalMeta,
    Priority,
    Signal,
    Impulse,
)
from ghoshell_moss.core.mindflow.audio_signal import AudioAction, AudioSignal
from ghoshell_moss.core.mindflow.buffer_nucleus import BufferNucleus

__all__ = [
    "AudioNucleus",
    "AudioNucleusMeta",
]


class AudioNucleus(BufferNucleus):
    """Audio signal nucleus — aggregate ASR signals into attention impulses.

    SPEECH_STARTED (incomplete) signals are buffered but do NOT interrupt
    the current attention — they accumulate until a SPEECH_FINAL arrives.
    SPEECH_FINAL purges incomplete predecessors, produces a complete Impulse
    with interrupt=True, and triggers the articulate→action loop.

    Only complete (SPEECH_FINAL) impulses carry interrupt=True.  Incomplete
    impulses (SPEECH_STARTED only, without a matching FINAL) do not interrupt
    — they are buffered silently and expire via the pulse beat mechanism.
    """

    async def _process_signal(self, signal: Signal) -> None:
        audio_meta = AudioSignal.from_signal(signal)
        if audio_meta and audio_meta.action == AudioAction.SPEECH_FINAL:
            # Purge incomplete signals (SPEECH_STARTED) so FINAL produces
            # a complete Impulse.  _process_signal runs under self._lock.
            self._signals = [s for s in self._signals if s.complete]
        await super()._process_signal(signal)

    def _rebuild_impulse(self) -> Impulse | None:
        impulse = super()._rebuild_impulse()
        if impulse is not None and impulse.complete:
            impulse.interrupt = True
        return impulse


class AudioNucleusMeta(NucleusMeta):
    """音频感知核工厂 — 生产监听 audio 信号的 AudioNucleus。"""

    def name(self) -> str:
        return "audio_nucleus"

    def description(self) -> str:
        return "audio perception signal nucleus — aggregates audio signals from ASR/listener"

    def signals(self) -> list[type[SignalMeta]]:
        return [AudioSignal]

    def factory(self, container: IoCContainer) -> Nucleus:
        return AudioNucleus(
            name="audio_nucleus",
            description="audio perception signal nucleus",
            target_signal="audio",
            default_prompt="User spoke via voice input. Process the speech.",
            suppress_seconds=0.5,
            buffer_size=5,
            min_priority=Priority.WARNING,
            pulse_beat_interval=3.0,
            logger=container.force_fetch(LoggerItf),
        )
