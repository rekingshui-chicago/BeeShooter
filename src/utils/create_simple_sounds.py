"""
Create simple sound files for the game without using numpy
"""
import os
import wave
import struct
import math
import random

def create_simple_sound(filename, duration=0.3, frequency=440.0, volume=0.5, sound_type="sine", stereo=False):
    """Create a sound file with the given parameters

    Args:
        filename: Name of the output file
        duration: Length of the sound in seconds
        frequency: Base frequency in Hz
        volume: Volume level (0.0 to 1.0)
        sound_type: Type of sound wave ("sine", "square", "sawtooth", "noise", "complex")
        stereo: Whether to create a stereo sound
    """
    # Parameters
    sample_rate = 44100  # samples per second
    num_samples = int(duration * sample_rate)
    nchannels = 2 if stereo else 1

    # Apply envelope to avoid clicks and pops
    def apply_envelope(sample_index, total_samples, sample_value):
        # Attack-Decay-Sustain-Release (ADSR) envelope
        attack = int(total_samples * 0.05)  # 5% attack
        decay = int(total_samples * 0.1)    # 10% decay
        release = int(total_samples * 0.2)  # 20% release
        sustain_level = 0.8                 # 80% of peak during sustain

        if sample_index < attack:
            # Attack phase: ramp up
            envelope = sample_index / attack
        elif sample_index < attack + decay:
            # Decay phase: ramp down to sustain level
            decay_progress = (sample_index - attack) / decay
            envelope = 1.0 - (1.0 - sustain_level) * decay_progress
        elif sample_index > total_samples - release:
            # Release phase: ramp down to zero
            release_progress = (sample_index - (total_samples - release)) / release
            envelope = sustain_level * (1.0 - release_progress)
        else:
            # Sustain phase: constant level
            envelope = sustain_level

        return sample_value * envelope

    # Generate samples based on sound type
    left_samples = []
    right_samples = [] if stereo else None

    for i in range(num_samples):
        t = i / sample_rate  # Time in seconds
        phase = 2 * math.pi * frequency * t

        # Generate base sample based on sound type
        if sound_type == "sine":
            sample = math.sin(phase)
        elif sound_type == "square":
            sample = 1.0 if math.sin(phase) >= 0 else -1.0
        elif sound_type == "sawtooth":
            sample = 2.0 * (t * frequency - math.floor(0.5 + t * frequency))
        elif sound_type == "noise":
            sample = 2.0 * random.random() - 1.0
        elif sound_type == "complex":
            # Complex tone with harmonics
            fundamental = math.sin(phase)
            second_harmonic = 0.5 * math.sin(2 * phase)
            third_harmonic = 0.3 * math.sin(3 * phase)
            fifth_harmonic = 0.15 * math.sin(5 * phase)
            sample = fundamental + second_harmonic + third_harmonic + fifth_harmonic
            # Normalize to avoid clipping
            sample = sample / 1.95
        else:  # Default to sine
            sample = math.sin(phase)

        # Apply envelope to avoid clicks
        sample = apply_envelope(i, num_samples, sample)

        # Apply volume
        sample = volume * sample

        # Add to samples list
        left_samples.append(sample)

        # For stereo, create a slightly different right channel
        if stereo:
            # Slight phase and amplitude difference for stereo effect
            right_phase = 2 * math.pi * frequency * 1.01 * t
            if sound_type == "sine":
                right_sample = math.sin(right_phase)
            elif sound_type == "square":
                right_sample = 1.0 if math.sin(right_phase) >= 0 else -1.0
            elif sound_type == "sawtooth":
                right_sample = 2.0 * (t * frequency * 1.01 - math.floor(0.5 + t * frequency * 1.01))
            elif sound_type == "noise":
                right_sample = 2.0 * random.random() - 1.0
            elif sound_type == "complex":
                fundamental = math.sin(right_phase)
                second_harmonic = 0.5 * math.sin(2 * right_phase)
                third_harmonic = 0.3 * math.sin(3 * right_phase)
                fifth_harmonic = 0.15 * math.sin(5 * right_phase)
                right_sample = fundamental + second_harmonic + third_harmonic + fifth_harmonic
                right_sample = right_sample / 1.95
            else:
                right_sample = math.sin(right_phase)

            right_sample = apply_envelope(i, num_samples, right_sample)
            right_sample = volume * 0.95 * right_sample  # Slightly lower volume for right channel
            right_samples.append(right_sample)

    # Convert to 16-bit PCM
    left_samples = [int(sample * 32000) for sample in left_samples]  # Using 32000 for safety margin
    if stereo:
        right_samples = [int(sample * 32000) for sample in right_samples]

    # Create directory if it doesn't exist
    os.makedirs(os.path.join("assets", "sounds"), exist_ok=True)

    # Write to file
    filepath = os.path.join("assets", "sounds", filename)
    with wave.open(filepath, 'w') as wav_file:
        # Set parameters
        sampwidth = 2  # 16-bit
        framerate = sample_rate
        nframes = num_samples
        comptype = 'NONE'
        compname = 'not compressed'

        wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))

        # Write frames
        if stereo:
            # Interleave left and right channels
            for left, right in zip(left_samples, right_samples):
                wav_file.writeframes(struct.pack('hh', left, right))
        else:
            for sample in left_samples:
                wav_file.writeframes(struct.pack('h', sample))

    print(f"Created sound file: {filepath}")

def create_background_music(filename="background_music.wav", duration=30.0):
    """Create a more complex background music loop with smooth transitions for looping"""
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

            # Normalized position in the loop (0.0 to 1.0)
            loop_pos = t / duration

            # Create a smooth transition for looping by ensuring start and end match
            # Use a crossfade approach at the beginning and end
            crossfade_duration = 1.0  # seconds at each end
            crossfade_samples = int(crossfade_duration * sample_rate)

            # Apply crossfade if in the beginning or end regions
            if i < crossfade_samples:
                # Beginning of loop - fade in
                fade_factor = i / crossfade_samples
            elif i > num_samples - crossfade_samples:
                # End of loop - fade out
                fade_factor = (num_samples - i) / crossfade_samples
            else:
                # Middle of loop - full volume
                fade_factor = 1.0

            # Base frequency that changes slowly over time with smooth looping
            # Use sine functions with periods that divide evenly into the duration
            cycles_in_duration = math.floor(duration / 4)  # 4-second cycle
            base_freq = 220 + 20 * math.sin(2 * math.pi * cycles_in_duration * loop_pos)

            # Create a chord (root, fifth, octave)
            root = 0.2 * math.sin(2 * math.pi * base_freq * t)
            fifth = 0.15 * math.sin(2 * math.pi * (base_freq * 1.5) * t)
            octave = 0.1 * math.sin(2 * math.pi * (base_freq * 2) * t)

            # Add some slow arpeggios that complete full cycles within the duration
            arp_cycles = math.floor(duration / 2)  # 2-second arpeggio cycle
            arp_pattern = int((loop_pos * arp_cycles * 4) % 4)  # 0, 1, 2, 3 pattern
            arp_freq_multiplier = 1.0
            if arp_pattern == 0:
                arp_freq_multiplier = 1.0
            elif arp_pattern == 1:
                arp_freq_multiplier = 1.5
            elif arp_pattern == 2:
                arp_freq_multiplier = 2.0
            else:  # arp_pattern == 3
                arp_freq_multiplier = 1.25

            arp_freq = base_freq * arp_freq_multiplier

            # Smooth amplitude modulation for the arpeggio
            arp_amp_mod = 0.5 + 0.5 * math.sin(2 * math.pi * arp_cycles * 2 * loop_pos)
            arpeggio = 0.12 * math.sin(2 * math.pi * arp_freq * t) * arp_amp_mod

            # Add a bass line that follows the chord progression
            bass_freq = base_freq / 2  # One octave down
            bass_pattern = int((loop_pos * arp_cycles * 2) % 4)  # Slower pattern than arpeggio
            if bass_pattern == 0 or bass_pattern == 2:
                bass_freq *= 1.0  # Root
            elif bass_pattern == 1:
                bass_freq *= 0.8  # Down a major third
            else:  # bass_pattern == 3
                bass_freq *= 1.2  # Up a major third

            bass = 0.15 * math.sin(2 * math.pi * bass_freq * t)

            # Add some ambient pad sounds
            pad_freq1 = base_freq * 1.5  # Fifth
            pad_freq2 = base_freq * 2.0  # Octave
            pad1 = 0.07 * math.sin(2 * math.pi * pad_freq1 * t)
            pad2 = 0.07 * math.sin(2 * math.pi * pad_freq2 * t)

            # Occasional subtle percussion
            percussion = 0
            beat_interval = 0.5  # Half-second between beats
            if t % beat_interval < 0.02:  # 20ms percussion hit
                percussion = 0.1 * math.exp(-50 * (t % beat_interval)) * (2 * random.random() - 1)

            # Combine all components
            left_value = (root + fifth + octave + arpeggio + bass + pad1 + percussion) * fade_factor
            right_value = (root + fifth + octave + arpeggio + bass + pad2 + percussion) * fade_factor

            # Add slight stereo effect
            left_value += 0.05 * math.sin(2 * math.pi * (base_freq * 0.99) * t) * fade_factor
            right_value += 0.05 * math.sin(2 * math.pi * (base_freq * 1.01) * t) * fade_factor

            # Ensure values are in range [-1.0, 1.0]
            left_value = max(min(left_value, 1.0), -1.0)
            right_value = max(min(right_value, 1.0), -1.0)

            # Convert to 16-bit PCM
            left_sample = int(left_value * 32000)  # Using 32000 instead of 32767 for safety
            right_sample = int(right_value * 32000)  # Using 32000 instead of 32767 for safety

            # Write samples
            wav_file.writeframes(struct.pack('hh', left_sample, right_sample))

    print(f"Created background music: {filepath}")

def create_explosion_sound(filename="explosion.wav", duration=0.7):
    """Create a more realistic explosion sound effect"""
    # Parameters
    sample_rate = 44100  # samples per second
    num_samples = int(duration * sample_rate)

    # Create directory if it doesn't exist
    os.makedirs(os.path.join("assets", "sounds"), exist_ok=True)

    # Create file path
    filepath = os.path.join("assets", "sounds", filename)

    # Open wave file (stereo for more immersive effect)
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

            # Initial explosion - loud noise burst that fades
            noise_amplitude = 1.0 * math.exp(-4 * t)  # Exponential decay
            noise = noise_amplitude * (2.0 * random.random() - 1.0)

            # Low frequency rumble
            rumble_freq = 60 + 30 * math.exp(-2 * t)  # Frequency drops over time
            rumble = 0.7 * math.sin(2 * math.pi * rumble_freq * t) * math.exp(-3 * t)

            # Mid frequency components
            mid_freq = 220 * math.exp(-t)  # Decaying frequency
            mid = 0.3 * math.sin(2 * math.pi * mid_freq * t) * math.exp(-5 * t)

            # Combine components
            left_value = noise + rumble + mid
            # Right channel slightly different for stereo effect
            right_value = noise * 0.95 + rumble * 1.05 + mid * 0.9

            # Add some crackle effects in the tail
            if t > 0.1 and random.random() < 0.1 * math.exp(-2 * t):
                crackle = 0.8 * (random.random() - 0.5)
                left_value += crackle
                right_value += crackle * 0.9

            # Ensure values are in range [-1.0, 1.0]
            left_value = max(min(left_value, 1.0), -1.0)
            right_value = max(min(right_value, 1.0), -1.0)

            # Convert to 16-bit PCM
            left_sample = int(left_value * 32000)  # Using 32000 instead of 32767 for safety
            right_sample = int(right_value * 32000)

            # Write samples
            wav_file.writeframes(struct.pack('hh', left_sample, right_sample))

    print(f"Created explosion sound: {filepath}")

def create_game_sounds():
    """Create all the sound files needed for the game"""
    # Create shoot sound (higher pitch, shorter, with harmonics)
    create_simple_sound("shoot.wav", duration=0.15, frequency=880.0, volume=0.4,
                       sound_type="complex", stereo=True)

    # Create explosion sound (custom complex sound)
    create_explosion_sound("explosion.wav")

    # Create game over sound (lower pitch, longer, with harmonics)
    create_simple_sound("game_over.wav", duration=1.5, frequency=110.0, volume=0.7,
                       sound_type="complex", stereo=True)

    # Create powerup sound (higher pitch, with harmonics)
    create_simple_sound("powerup.wav", duration=0.4, frequency=1320.0, volume=0.6,
                       sound_type="complex", stereo=True)

    # Create bomb sound (medium pitch, sawtooth wave for more impact)
    create_simple_sound("bomb.wav", duration=0.8, frequency=220.0, volume=0.8,
                       sound_type="sawtooth", stereo=True)

    # Create missile sound (medium-high pitch, with noise component)
    create_simple_sound("missile.wav", duration=0.5, frequency=660.0, volume=0.6,
                       sound_type="complex", stereo=True)

    # Create background music (15 seconds loop - longer for better looping)
    create_background_music("background_music.wav", duration=15.0)

if __name__ == "__main__":
    create_game_sounds()
