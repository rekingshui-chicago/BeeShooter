#!/usr/bin/env python3
"""
Script to generate a missile sound effect for the Bee Shooter game.
"""

import os
import numpy as np
from scipy.io import wavfile

# Make sure the sounds directory exists
os.makedirs('assets/sounds', exist_ok=True)

# Sample rate
SAMPLE_RATE = 44100

def create_missile_sound():
    # Duration in seconds
    duration = 0.8
    
    # Create a time array
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    # Generate a missile launch sound (whoosh + engine)
    
    # Engine component - low frequency rumble
    engine_freq = 80
    engine = np.sin(2 * np.pi * engine_freq * t) * 0.5
    
    # Add some noise to make it sound more realistic
    noise = np.random.uniform(-0.3, 0.3, len(t))
    
    # Whoosh component - frequency sweep
    freq_start = 2000
    freq_end = 500
    freq = np.linspace(freq_start, freq_end, len(t))
    whoosh = np.sin(2 * np.pi * freq * t) * 0.3
    
    # Combine components
    audio = engine + noise + whoosh
    
    # Apply an amplitude envelope
    envelope = np.ones_like(t)
    attack_time = int(SAMPLE_RATE * 0.05)  # 50ms attack
    decay_time = int(SAMPLE_RATE * 0.3)    # 300ms decay
    
    # Attack phase (fade in)
    envelope[:attack_time] = np.linspace(0, 1, attack_time)
    
    # Decay phase (fade out)
    envelope[-decay_time:] = np.linspace(1, 0.2, decay_time)
    
    # Apply envelope
    audio = audio * envelope
    
    # Add a doppler effect (pitch shift)
    doppler_shift = np.linspace(1.0, 0.8, len(t))
    t_doppler = np.cumsum(doppler_shift) * duration / np.sum(doppler_shift)
    t_doppler = np.minimum(t_doppler, duration - 0.001)  # Ensure we don't exceed duration
    
    # Resample the audio with the doppler effect
    indices = np.minimum(np.floor(t_doppler * SAMPLE_RATE).astype(int), len(audio) - 1)
    audio_doppler = audio[indices]
    
    # Normalize to 16-bit range and convert to int16
    audio_doppler = np.int16(audio_doppler / np.max(np.abs(audio_doppler)) * 32767 * 0.8)
    
    # Save to file
    wavfile.write('assets/sounds/missile.wav', SAMPLE_RATE, audio_doppler)
    print("Created missile.wav")

if __name__ == "__main__":
    create_missile_sound()
    print("Missile sound created successfully!")
