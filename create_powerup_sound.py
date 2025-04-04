#!/usr/bin/env python3
"""
Script to generate a power-up sound effect for the Bee Shooter game.
"""

import os
import numpy as np
from scipy.io import wavfile

# Make sure the sounds directory exists
os.makedirs('assets/sounds', exist_ok=True)

# Sample rate
SAMPLE_RATE = 44100

def create_powerup_sound():
    # Duration in seconds
    duration = 0.5
    
    # Create a time array
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    # Generate an ascending series of tones
    freqs = [440, 554, 659, 880]  # A4, C#5, E5, A5 (A major chord ascending)
    note_duration = duration / len(freqs)
    
    audio = np.array([])
    for i, freq in enumerate(freqs):
        # Time array for this note
        t_note = np.linspace(0, note_duration, int(SAMPLE_RATE * note_duration), False)
        
        # Generate a sine wave
        note = np.sin(2 * np.pi * freq * t_note)
        
        # Apply an amplitude envelope (quick attack, slow decay)
        envelope = np.ones_like(t_note)
        envelope[:int(len(t_note)*0.1)] = np.linspace(0, 1, int(len(t_note)*0.1))
        envelope[int(len(t_note)*0.7):] = np.linspace(1, 0.7, len(t_note) - int(len(t_note)*0.7))
        note = note * envelope
        
        # Add to the audio array
        audio = np.append(audio, note)
    
    # Add a slight vibrato effect
    vibrato_freq = 8  # Hz
    vibrato_amount = 0.03
    vibrato = 1.0 + vibrato_amount * np.sin(2 * np.pi * vibrato_freq * t)
    audio = audio * vibrato[:len(audio)]
    
    # Normalize to 16-bit range and convert to int16
    audio = np.int16(audio / np.max(np.abs(audio)) * 32767 * 0.8)
    
    # Save to file
    wavfile.write('assets/sounds/powerup.wav', SAMPLE_RATE, audio)
    print("Created powerup.wav")

if __name__ == "__main__":
    create_powerup_sound()
    print("Power-up sound created successfully!")
