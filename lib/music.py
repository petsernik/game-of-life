from itertools import product
import pygame
import numpy as np

# Audio settings
SAMPLE_RATE = 44100
pygame.mixer.pre_init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=512)  # lower buffer for latency
pygame.init()
pygame.mixer.set_num_channels(64)  # allow up to 64 simultaneous voices

# --- precompute everything once into a cache ---
MAJOR_STEPS = [0, 2, 4, 5, 7, 9, 11]
ALL_STEPS = [12 * k + x for k, x in product(range(3), MAJOR_STEPS)] + [12 * 3]
TONALITIES = [36, 43, 38, 45, 40, 47, 42, 37]

_sound_cache = {}


def get_sound(midi: int, duration: float = 1.0) -> pygame.mixer.Sound:
    key = (midi, duration)
    if key not in _sound_cache:
        # generate and stash
        freq = 440.0 * 2 ** ((midi - 69) / 12)
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
        wave = (0.6 * np.sin(2 * np.pi * freq * t)
                + 0.3 * np.sin(2 * np.pi * 2 * freq * t)
                + 0.1 * np.sin(2 * np.pi * 3 * freq * t)
                + 0.05 * np.sin(2 * np.pi * 4 * freq * t))
        # ADSR
        attack, decay, sustain_level, release = 0.01, 0.1, 0.7, 0.2
        env = np.zeros_like(t)
        total_len = len(t)
        a = int(attack * SAMPLE_RATE)
        d = int(decay * SAMPLE_RATE)
        r = int(release * SAMPLE_RATE)

        if a + d + r > total_len:
            # Scale down A/D/R proportionally to fit total duration
            scale = total_len / (a + d + r)
            a = int(a * scale)
            d = int(d * scale)
            r = int(r * scale)

        s_start = a + d
        s_end = total_len - r

        if a > 0:
            env[:a] = np.linspace(0, 1, a)
        if d > 0:
            env[a:s_start] = np.linspace(1, sustain_level, d)
        if s_end > s_start:
            env[s_start:s_end] = sustain_level
        if r > 0:
            env[s_end:] = np.linspace(sustain_level, 0, total_len - s_end)
        wave *= env
        audio = np.clip(wave * 32767, -32767, 32767).astype(np.int16)
        _sound_cache[key] = pygame.mixer.Sound(buffer=audio.tobytes())
    return _sound_cache[key]


def normalize_volumes():
    # find truly busy channels
    busy = [pygame.mixer.Channel(i)
            for i in range(pygame.mixer.get_num_channels())
            if pygame.mixer.Channel(i).get_busy()]
    if busy:
        vol = 1.0 / len(busy)
        for ch in busy:
            ch.set_volume(vol)


def play_note(tonality_index, x, y, note_dur=1.0, pause=0.0, sequentially=False):
    midi = TONALITIES[tonality_index] + ALL_STEPS[2 * y + x]
    snd = get_sound(midi, note_dur)
    # grab a free channel, forcing if none free
    ch = pygame.mixer.find_channel(force=True)  # will steal oldest if needed :contentReference[oaicite:1]{index=1}
    ch.play(snd)
    normalize_volumes()
    if sequentially:
        while ch.get_busy():
            pygame.time.wait(5)
    else:
        pygame.time.wait(int(pause * 1000))
