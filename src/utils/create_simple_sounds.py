"""
Create simple sound files for the game without using numpy
"""
import os
import wave
import struct
import math

def create_simple_sound(filename, duration=0.3, frequency=440.0, volume=0.5):
    """Create a simple sound file with the given parameters"""
    # Parameters
    sample_rate = 44100  # samples per second
    num_samples = int(duration * sample_rate)

    # Generate sine wave
    samples = []
    for i in range(num_samples):
        sample = volume * math.sin(2 * math.pi * frequency * i / sample_rate)
        samples.append(sample)

    # Convert to 16-bit PCM
    samples = [int(sample * 32767) for sample in samples]

    # Create directory if it doesn't exist
    os.makedirs(os.path.join("assets", "sounds"), exist_ok=True)

    # Write to file
    filepath = os.path.join("assets", "sounds", filename)
    with wave.open(filepath, 'w') as wav_file:
        # Set parameters
        nchannels = 1  # mono
        sampwidth = 2  # 16-bit
        framerate = sample_rate
        nframes = num_samples
        comptype = 'NONE'
        compname = 'not compressed'

        wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))

        # Write frames
        for sample in samples:
            wav_file.writeframes(struct.pack('h', sample))

    print(f"Created sound file: {filepath}")

def create_background_music(filename="background_music.wav", duration=30.0):
    """Create a simple background music loop"""
    # Parameters
    sample_rate = 44100  # samples per second
    num_samples = int(duration * sample_rate)

    # Create directory if it doesn't exist
    os.makedirs(os.path.join("assets", "sounds"), exist_ok=True)

    # Create file path
    filepath = os.path.join("assets", "sounds", filename)

    # Open wave file
    with wave.open(filepath, 'w') as wav_file:
        # Set parameters
        nchannels = 2  # stereo
        sampwidth = 2  # 16-bit
        framerate = sample_rate
        nframes = num_samples
        comptype = 'NONE'
        compname = 'not compressed'

        wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))

        # Generate and write samples
        for i in range(num_samples):
            # Time in seconds
            t = i / sample_rate

            # Base frequency that changes slowly over time
            base_freq = 220 + 20 * math.sin(2 * math.pi * 0.05 * t)

            # Create a chord (root, fifth, octave)
            root = 0.2 * math.sin(2 * math.pi * base_freq * t)
            fifth = 0.15 * math.sin(2 * math.pi * (base_freq * 1.5) * t)
            octave = 0.1 * math.sin(2 * math.pi * (base_freq * 2) * t)

            # Add some slow arpeggios
            arp_freq = base_freq * (1 + 0.5 * int(t % 4 // 1))
            arpeggio = 0.1 * math.sin(2 * math.pi * arp_freq * t) * (0.5 + 0.5 * math.sin(2 * math.pi * 0.25 * t))

            # Combine all components
            left_value = root + fifth + octave + arpeggio
            right_value = root + fifth + octave + arpeggio

            # Add slight stereo effect
            left_value += 0.05 * math.sin(2 * math.pi * (base_freq * 0.99) * t)
            right_value += 0.05 * math.sin(2 * math.pi * (base_freq * 1.01) * t)

            # Ensure values are in range [-1.0, 1.0]
            left_value = max(min(left_value, 1.0), -1.0)
            right_value = max(min(right_value, 1.0), -1.0)

            # Convert to 16-bit PCM
            left_sample = int(left_value * 32000)  # Using 32000 instead of 32767 for safety
            right_sample = int(right_value * 32000)  # Using 32000 instead of 32767 for safety

            # Write samples
            wav_file.writeframes(struct.pack('hh', left_sample, right_sample))

    print(f"Created background music: {filepath}")

def create_game_sounds():
    """Create all the sound files needed for the game"""
    # Create shoot sound (higher pitch, shorter)
    create_simple_sound("shoot.wav", duration=0.1, frequency=880.0, volume=0.3)

    # Create explosion sound (lower pitch, longer)
    create_simple_sound("explosion.wav", duration=0.5, frequency=220.0, volume=0.7)

    # Create game over sound (lower pitch, longer)
    create_simple_sound("game_over.wav", duration=1.0, frequency=110.0, volume=0.7)

    # Create powerup sound (higher pitch)
    create_simple_sound("powerup.wav", duration=0.3, frequency=1320.0, volume=0.5)

    # Create bomb sound (medium pitch)
    create_simple_sound("bomb.wav", duration=0.7, frequency=440.0, volume=0.8)

    # Create missile sound (medium-high pitch)
    create_simple_sound("missile.wav", duration=0.4, frequency=660.0, volume=0.6)

    # Create background music (10 seconds loop - shorter for faster creation)
    create_background_music("background_music.wav", duration=10.0)

if __name__ == "__main__":
    create_game_sounds()
