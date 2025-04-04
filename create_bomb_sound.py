#!/usr/bin/env python3
"""
Script to generate a bomb sound effect for the Bee Shooter game.
"""

import os
import numpy as np
from scipy.io import wavfile

# Make sure the sounds directory exists
os.makedirs('assets/sounds', exist_ok=True)

# Sample rate
SAMPLE_RATE = 44100

def create_bomb_sound():
    # Duration in seconds
    duration = 1.0
    
    # Create a time array
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    # Generate a low frequency explosion sound
    freq_start = 200
    freq_end = 50
    
    # Create a frequency sweep (from high to low)
    freq = np.linspace(freq_start, freq_end, len(t))
    
    # Generate a sine wave with decreasing frequency
    sine_wave = np.sin(2 * np.pi * freq * t)
    
    # Generate white noise
    noise = np.random.uniform(-0.8, 0.8, len(t))
    
    # Apply a low-pass filter to the noise (simple moving average)
    window_size = 100
    noise_smooth = np.convolve(noise, np.ones(window_size)/window_size, mode='same')
    
    # Combine the sine wave and noise
    audio = sine_wave * 0.6 + noise_smooth * 0.4
    
    # Apply an amplitude envelope (quick attack, slow decay)
    envelope = np.exp(-3 * t)
    envelope[:int(SAMPLE_RATE * 0.05)] = np.linspace(0, 1, int(SAMPLE_RATE * 0.05))
    audio = audio * envelope
    
    # Add a bass boost
    bass_freq = 60
    bass_boost = np.sin(2 * np.pi * bass_freq * t) * np.exp(-6 * t)
    audio = audio + bass_boost * 0.5
    
    # Add a "boom" effect
    boom_freq = 30
    boom = np.sin(2 * np.pi * boom_freq * t) * np.exp(-4 * t)
    audio = audio + boom * 0.7
    
    # Normalize to 16-bit range and convert to int16
    audio = np.int16(audio / np.max(np.abs(audio)) * 32767)
    
    # Save to file
    wavfile.write('assets/sounds/bomb.wav', SAMPLE_RATE, audio)
    print("Created bomb.wav")

if __name__ == "__main__":
    create_bomb_sound()
    print("Bomb sound created successfully!")
