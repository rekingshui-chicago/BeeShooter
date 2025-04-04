#!/usr/bin/env python3
"""
Script to generate simple sound effects for the Bee Shooter game.
This creates WAV files using numpy to generate simple waveforms.
"""

import os
import numpy as np
from scipy.io import wavfile

# Make sure the sounds directory exists
os.makedirs('assets/sounds', exist_ok=True)

# Sample rate for all sounds
SAMPLE_RATE = 44100

# Function to create a simple laser sound
def create_laser_sound():
    # Duration in seconds
    duration = 0.2
    
    # Create a time array
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    # Generate a frequency sweep (from high to low)
    freq_start = 1000
    freq_end = 500
    freq = np.linspace(freq_start, freq_end, len(t))
    
    # Generate a sine wave with decreasing frequency
    note = np.sin(2 * np.pi * freq * t)
    
    # Apply an amplitude envelope (fade out)
    envelope = np.linspace(1.0, 0.0, len(t)) ** 0.5
    note = note * envelope
    
    # Normalize to 16-bit range and convert to int16
    audio = np.int16(note * 32767)
    
    # Save to file
    wavfile.write('assets/sounds/laser.wav', SAMPLE_RATE, audio)
    print("Created laser.wav")

# Function to create a simple explosion sound
def create_explosion_sound():
    # Duration in seconds
    duration = 0.5
    
    # Create a time array
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    # Generate white noise
    noise = np.random.uniform(-1, 1, len(t))
    
    # Apply a low-pass filter (simple moving average)
    window_size = 50
    noise_smooth = np.convolve(noise, np.ones(window_size)/window_size, mode='same')
    
    # Apply an amplitude envelope (quick attack, slow decay)
    envelope = np.exp(-5 * t)
    audio = noise_smooth * envelope
    
    # Normalize to 16-bit range and convert to int16
    audio = np.int16(audio / np.max(np.abs(audio)) * 32767)
    
    # Save to file
    wavfile.write('assets/sounds/explosion.wav', SAMPLE_RATE, audio)
    print("Created explosion.wav")

# Function to create a game over sound
def create_game_over_sound():
    # Duration in seconds
    duration = 1.0
    
    # Create a time array
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    # Generate three descending notes
    freqs = [440, 349, 220]  # A4, F4, A3
    note_duration = duration / len(freqs)
    
    audio = np.array([])
    for i, freq in enumerate(freqs):
        # Time array for this note
        t_note = np.linspace(0, note_duration, int(SAMPLE_RATE * note_duration), False)
        
        # Generate a sine wave
        note = np.sin(2 * np.pi * freq * t_note)
        
        # Apply an amplitude envelope
        envelope = np.exp(-3 * t_note)
        note = note * envelope
        
        # Add to the audio array
        audio = np.append(audio, note)
    
    # Normalize to 16-bit range and convert to int16
    audio = np.int16(audio / np.max(np.abs(audio)) * 32767)
    
    # Save to file
    wavfile.write('assets/sounds/game_over.wav', SAMPLE_RATE, audio)
    print("Created game_over.wav")

if __name__ == "__main__":
    create_laser_sound()
    create_explosion_sound()
    create_game_over_sound()
    print("All sound files created successfully!")
