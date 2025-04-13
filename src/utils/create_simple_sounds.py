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
    """Create a more intense and immersive background music loop with dynamic elements"""
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
            crossfade_duration = 2.0  # seconds at each end (longer for smoother transition)
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

            # Create tension curve that builds and releases throughout the loop
            # This creates a more dynamic and engaging feel
            tension_cycle = 0.5 + 0.5 * math.sin(2 * math.pi * (loop_pos * 2 - 0.25))  # Full cycle twice in duration

            # Base frequency that changes with tension
            # Lower pitch during low tension, higher during high tension
            base_freq = 180 + 60 * tension_cycle

            # Minor key for more intense feel (root, minor third, fifth)
            root = 0.2 * math.sin(2 * math.pi * base_freq * t)
            minor_third = 0.15 * math.sin(2 * math.pi * (base_freq * 1.2) * t)  # Minor third (6/5 ratio)
            fifth = 0.15 * math.sin(2 * math.pi * (base_freq * 1.5) * t)
            octave = 0.1 * math.sin(2 * math.pi * (base_freq * 2) * t)

            # Add some pulsing synth pad that increases with tension
            pad_freq = base_freq * 2
            pad_pulse_rate = 4 + 4 * tension_cycle  # Pulse faster during high tension
            pad_amp = 0.15 * (0.7 + 0.3 * math.sin(2 * math.pi * pad_pulse_rate * t))
            pad = pad_amp * math.sin(2 * math.pi * pad_freq * t)

            # Add some arpeggios that get more complex with tension
            arp_cycles = math.floor(duration / 2)  # 2-second arpeggio cycle
            arp_pattern_length = 4 + int(4 * tension_cycle)  # Pattern length increases with tension
            arp_pattern = int((loop_pos * arp_cycles * arp_pattern_length) % arp_pattern_length)

            # Different frequency multipliers for more complex arpeggios
            arp_freq_multipliers = [1.0, 1.2, 1.5, 2.0, 0.8, 1.8, 1.33, 2.5]
            arp_freq_multiplier = arp_freq_multipliers[arp_pattern % len(arp_freq_multipliers)]
            arp_freq = base_freq * arp_freq_multiplier

            # Arpeggio gets louder with tension
            arp_amp = 0.08 + 0.12 * tension_cycle
            # Faster attack during high tension
            arp_attack = 0.01 + 0.04 * (1 - tension_cycle)

            # Calculate position within current arpeggio note
            arp_note_duration = 0.125  # 1/8th note
            arp_note_pos = (t % arp_note_duration) / arp_note_duration

            # Apply envelope to each arpeggio note
            if arp_note_pos < arp_attack:
                arp_env = arp_note_pos / arp_attack
            else:
                arp_env = 1.0 - (arp_note_pos - arp_attack) / (1.0 - arp_attack)

            arpeggio = arp_amp * arp_env * math.sin(2 * math.pi * arp_freq * t)

            # Add a driving bass line that follows the chord progression and tension
            bass_freq = base_freq / 2  # One octave down
            bass_pattern = int((loop_pos * arp_cycles * 2) % 4)  # Slower pattern than arpeggio

            # Bass pattern changes with tension
            if tension_cycle > 0.7:  # High tension - more movement
                if bass_pattern == 0:
                    bass_freq *= 1.0  # Root
                elif bass_pattern == 1:
                    bass_freq *= 0.8  # Down a major third
                elif bass_pattern == 2:
                    bass_freq *= 1.2  # Up a major third
                else:  # bass_pattern == 3
                    bass_freq *= 1.5  # Up a fifth
            else:  # Low tension - simpler
                if bass_pattern == 0 or bass_pattern == 2:
                    bass_freq *= 1.0  # Root
                else:
                    bass_freq *= 0.8  # Down a major third

            # Bass gets more distorted with tension
            bass_clean = math.sin(2 * math.pi * bass_freq * t)
            bass_dist = math.tanh(3 * math.sin(2 * math.pi * bass_freq * t))  # Distorted version
            bass_mix = (1 - tension_cycle) * bass_clean + tension_cycle * bass_dist
            bass_amp = 0.15 + 0.1 * tension_cycle
            bass = bass_amp * bass_mix

            # Add rhythmic percussion that intensifies with tension
            percussion = 0
            # Basic beat - quarter notes
            beat_interval = 0.5  # Half-second between beats
            if t % beat_interval < 0.02:  # 20ms percussion hit
                perc_amp = 0.1 + 0.1 * tension_cycle
                percussion += perc_amp * math.exp(-50 * (t % beat_interval)) * (2 * random.random() - 1)

            # Add eighth notes during higher tension
            if tension_cycle > 0.5 and t % (beat_interval/2) < 0.015:
                perc_amp = 0.05 + 0.1 * (tension_cycle - 0.5) * 2
                percussion += perc_amp * math.exp(-60 * (t % (beat_interval/2))) * (2 * random.random() - 1)

            # Add sixteenth notes during highest tension
            if tension_cycle > 0.8 and t % (beat_interval/4) < 0.01:
                perc_amp = 0.05 + 0.1 * (tension_cycle - 0.8) * 5
                percussion += perc_amp * math.exp(-70 * (t % (beat_interval/4))) * (2 * random.random() - 1)

            # Add atmospheric sounds
            # Sweeping filter effect that follows tension
            sweep_freq = 2000 + 4000 * tension_cycle * math.sin(2 * math.pi * 0.2 * t)
            sweep_amp = 0.05 * tension_cycle
            sweep = sweep_amp * math.sin(2 * math.pi * sweep_freq * t)

            # Add occasional risers during tension build-up
            riser = 0
            if 0.4 < tension_cycle < 0.9 and tension_cycle > loop_pos % 0.5:
                riser_freq = 500 + 2000 * ((tension_cycle - 0.4) / 0.5)
                riser = 0.1 * math.sin(2 * math.pi * riser_freq * t) * ((tension_cycle - 0.4) / 0.5)

            # Combine all components with different stereo positioning
            # Left channel
            left_value = (root * 0.9 + minor_third * 1.1 + fifth * 0.8 + octave * 0.9 +
                         pad * 0.9 + arpeggio * 1.1 + bass * 1.0 + percussion * 0.9 +
                         sweep * 0.8 + riser * 0.9) * fade_factor

            # Right channel with variations for wider stereo field
            right_value = (root * 1.1 + minor_third * 0.9 + fifth * 1.2 + octave * 1.1 +
                          pad * 1.1 + arpeggio * 0.9 + bass * 1.0 + percussion * 1.1 +
                          sweep * 1.2 + riser * 1.1) * fade_factor

            # Add stereo width with phase differences
            left_value += 0.08 * math.sin(2 * math.pi * (base_freq * 0.99) * t + 0.2) * fade_factor
            right_value += 0.08 * math.sin(2 * math.pi * (base_freq * 1.01) * t - 0.2) * fade_factor

            # Apply soft clipping for a more aggressive sound during high tension
            def soft_clip(x, drive):
                return math.tanh(x * drive) / math.tanh(drive)

            drive = 1.0 + 2.0 * tension_cycle  # More distortion during high tension
            left_value = soft_clip(left_value, drive)
            right_value = soft_clip(right_value, drive)

            # Convert to 16-bit PCM
            left_sample = int(left_value * 32000)  # Using 32000 instead of 32767 for safety
            right_sample = int(right_value * 32000)  # Using 32000 instead of 32767 for safety

            # Write samples
            wav_file.writeframes(struct.pack('hh', left_sample, right_sample))

    print(f"Created enhanced background music: {filepath}")

def create_explosion_sound(filename="explosion.wav", duration=1.2):
    """Create a more realistic and intense explosion sound effect"""
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

            # Initial impact - very short, intense burst at the beginning
            impact_factor = 1.0 if t < 0.02 else math.exp(-50 * (t - 0.02))
            impact = impact_factor * 0.9 * (2.0 * random.random() - 1.0)

            # Initial explosion - loud noise burst that fades
            # More aggressive attack and slower decay for more intensity
            noise_amplitude = 1.0 * math.exp(-3 * t)  # Slower exponential decay
            noise = noise_amplitude * (2.0 * random.random() - 1.0)

            # Low frequency rumble with longer sustain
            # Lower base frequency and slower decay for more "boom" feeling
            rumble_freq = 40 + 30 * math.exp(-1.5 * t)  # Lower frequency drops over time
            rumble = 0.8 * math.sin(2 * math.pi * rumble_freq * t) * math.exp(-2 * t)

            # Add sub-bass impact for physical sensation
            sub_bass_freq = 30 * math.exp(-0.5 * t)  # Very low frequency
            sub_bass = 0.7 * math.sin(2 * math.pi * sub_bass_freq * t) * math.exp(-1.5 * t)

            # Mid frequency components with more harmonics
            mid_freq = 180 * math.exp(-0.8 * t)  # Decaying frequency
            mid = 0.4 * math.sin(2 * math.pi * mid_freq * t) * math.exp(-3 * t)

            # Add harmonic distortion to mid frequencies for more "grit"
            mid_harmonic1 = 0.2 * math.sin(2 * math.pi * mid_freq * 2 * t) * math.exp(-3 * t)
            mid_harmonic2 = 0.1 * math.sin(2 * math.pi * mid_freq * 3 * t) * math.exp(-3 * t)

            # High frequency debris and shrapnel sounds
            debris_freq = 2000 + 500 * math.sin(t * 10)
            debris_amp = 0.15 * math.exp(-6 * t) * (0.5 + 0.5 * math.sin(t * 20))
            debris = debris_amp * math.sin(2 * math.pi * debris_freq * t)

            # Combine all components
            left_value = impact + noise + rumble + sub_bass + mid + mid_harmonic1 + mid_harmonic2 + debris

            # Right channel slightly different for enhanced stereo effect
            # Add slight delay and phase differences to create spatial impression
            t_right = max(0, t - 0.002)  # 2ms delay for right channel
            right_impact = impact * 0.95
            right_noise = noise_amplitude * 0.95 * (2.0 * random.random() - 1.0)
            right_rumble = 0.8 * math.sin(2 * math.pi * rumble_freq * t_right + 0.2) * math.exp(-2 * t)
            right_sub_bass = 0.7 * math.sin(2 * math.pi * sub_bass_freq * t_right + 0.1) * math.exp(-1.5 * t)
            right_mid = 0.4 * math.sin(2 * math.pi * mid_freq * t_right + 0.3) * math.exp(-3 * t)
            right_mid_harmonic1 = 0.2 * math.sin(2 * math.pi * mid_freq * 2 * t_right + 0.2) * math.exp(-3 * t)
            right_mid_harmonic2 = 0.1 * math.sin(2 * math.pi * mid_freq * 3 * t_right + 0.4) * math.exp(-3 * t)
            right_debris = debris_amp * 0.9 * math.sin(2 * math.pi * (debris_freq + 100) * t_right)

            right_value = right_impact + right_noise + right_rumble + right_sub_bass + right_mid + right_mid_harmonic1 + right_mid_harmonic2 + right_debris

            # Add some crackle effects throughout with more intensity and variation
            if random.random() < 0.2 * math.exp(-1.5 * t):
                crackle_intensity = 0.9 * math.exp(-2 * t)  # Stronger at beginning
                crackle = crackle_intensity * (random.random() - 0.5)
                left_value += crackle
                # Slightly different crackle in right channel for better stereo image
                right_value += crackle * 0.8 + 0.2 * (random.random() - 0.5) * crackle_intensity

            # Add secondary explosions for more complexity
            if 0.1 < t < 0.5 and random.random() < 0.01:
                secondary_exp = 0.6 * (random.random() - 0.3)
                left_value += secondary_exp
                right_value += secondary_exp * (0.7 + 0.3 * random.random())

            # Ensure values are in range [-1.0, 1.0] with soft clipping for more natural sound
            def soft_clip(x):
                # Soft clipping function to avoid harsh digital distortion
                if x > 0.8:
                    return 0.8 + 0.2 * math.tanh((x - 0.8) / 0.2)
                elif x < -0.8:
                    return -0.8 + 0.2 * math.tanh((x + 0.8) / 0.2)
                return x

            left_value = soft_clip(left_value)
            right_value = soft_clip(right_value)

            # Convert to 16-bit PCM
            left_sample = int(left_value * 32000)  # Using 32000 instead of 32767 for safety
            right_sample = int(right_value * 32000)

            # Write samples
            wav_file.writeframes(struct.pack('hh', left_sample, right_sample))

    print(f"Created enhanced explosion sound: {filepath}")

def create_laser_sound(filename="laser.wav", duration=0.2):
    """Create a more realistic laser/energy weapon sound"""
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

            # Base frequency with upward sweep
            base_freq = 1200 + 800 * (t / duration)  # Sweep from 1200Hz to 2000Hz

            # Add frequency modulation for more electronic feel
            mod_freq = 80  # Modulation frequency
            mod_depth = 100 * (1 - t/duration)  # Modulation depth decreases over time
            freq = base_freq + mod_depth * math.sin(2 * math.pi * mod_freq * t)

            # Main tone with harmonics
            main_tone = math.sin(2 * math.pi * freq * t)

            # Add harmonics for richness
            harmonic1 = 0.5 * math.sin(2 * math.pi * freq * 2 * t)  # 1st harmonic
            harmonic2 = 0.25 * math.sin(2 * math.pi * freq * 3 * t)  # 2nd harmonic

            # Add some noise for texture
            noise = 0.1 * (2.0 * random.random() - 1.0) * (1 - t/duration)

            # Apply envelope
            # Fast attack, slight decay, sustain, quick release
            if t < 0.01:  # Attack (10ms)
                envelope = t / 0.01
            elif t < 0.03:  # Decay (20ms)
                envelope = 1.0 - 0.2 * ((t - 0.01) / 0.02)
            elif t < duration - 0.03:  # Sustain
                envelope = 0.8
            else:  # Release (30ms)
                envelope = 0.8 * (1 - (t - (duration - 0.03)) / 0.03)

            # Combine all components
            combined = (main_tone + harmonic1 + harmonic2 + noise) * envelope

            # Add slight stereo effect
            left_value = combined * 0.8
            right_value = combined * 0.8

            # Add slight delay to right channel for stereo width
            if i > 0.001 * sample_rate:  # 1ms delay
                right_idx = i - int(0.001 * sample_rate)
                right_t = right_idx / sample_rate
                right_freq = 1200 + 800 * (right_t / duration)
                right_freq_mod = right_freq + mod_depth * math.sin(2 * math.pi * mod_freq * right_t)
                right_main = math.sin(2 * math.pi * right_freq_mod * right_t)
                right_h1 = 0.5 * math.sin(2 * math.pi * right_freq_mod * 2 * right_t)
                right_h2 = 0.25 * math.sin(2 * math.pi * right_freq_mod * 3 * right_t)

                if right_t < 0.01:  # Attack
                    right_env = right_t / 0.01
                elif right_t < 0.03:  # Decay
                    right_env = 1.0 - 0.2 * ((right_t - 0.01) / 0.02)
                elif right_t < duration - 0.03:  # Sustain
                    right_env = 0.8
                else:  # Release
                    right_env = 0.8 * (1 - (right_t - (duration - 0.03)) / 0.03)

                right_value = (right_main + right_h1 + right_h2 + noise) * right_env * 0.8

            # Ensure values are in range [-1.0, 1.0]
            left_value = max(min(left_value, 1.0), -1.0)
            right_value = max(min(right_value, 1.0), -1.0)

            # Convert to 16-bit PCM
            left_sample = int(left_value * 32000)
            right_sample = int(right_value * 32000)

            # Write samples
            wav_file.writeframes(struct.pack('hh', left_sample, right_sample))

    print(f"Created laser sound: {filepath}")

def create_missile_sound(filename="missile.wav", duration=0.8):
    """Create a realistic missile launch sound with thrust and whoosh effects"""
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

            # Phase 1: Initial ignition (0-0.1s)
            # Phase 2: Thrust buildup (0.1-0.3s)
            # Phase 3: Full thrust and whoosh (0.3-0.8s)

            # Noise component (rocket thrust)
            if t < 0.1:  # Ignition phase
                noise_amp = t * 10  # Ramp up from 0 to 1 over 0.1s
            elif t < 0.3:  # Thrust buildup
                noise_amp = 1.0
            else:  # Full thrust
                noise_amp = 1.0

            # White noise for thrust
            thrust_noise = noise_amp * 0.7 * (2.0 * random.random() - 1.0)

            # Add low-frequency rumble for power
            rumble_freq = 80 + 20 * math.sin(t * 8)  # Slight variation
            rumble = noise_amp * 0.6 * math.sin(2 * math.pi * rumble_freq * t)

            # Add mid-frequency components for body
            mid_freq = 250 + 50 * math.sin(t * 5)
            mid_component = noise_amp * 0.3 * math.sin(2 * math.pi * mid_freq * t)

            # Add whoosh effect (increasing frequency sweep)
            whoosh_freq = 500 + 1500 * (t / duration)  # Sweep from 500Hz to 2000Hz
            whoosh_amp = 0.0
            if t > 0.2:  # Start whoosh after initial thrust
                # Amplitude follows a bell curve peaking at 60% of duration
                peak_time = duration * 0.6
                whoosh_amp = 0.4 * math.exp(-10 * ((t - peak_time) / duration) ** 2)
            whoosh = whoosh_amp * math.sin(2 * math.pi * whoosh_freq * t)

            # Add crackling/popping for realism
            crackle = 0.0
            if random.random() < 0.1:  # 10% chance of a crackle at any sample
                crackle = 0.3 * noise_amp * (random.random() - 0.5)

            # Combine all components
            left_value = thrust_noise + rumble + mid_component + whoosh + crackle

            # Right channel with slight variations for stereo effect
            right_thrust = noise_amp * 0.7 * (2.0 * random.random() - 1.0)
            right_rumble = noise_amp * 0.6 * math.sin(2 * math.pi * (rumble_freq - 5) * t + 0.2)
            right_mid = noise_amp * 0.3 * math.sin(2 * math.pi * (mid_freq + 10) * t + 0.3)
            right_whoosh = whoosh_amp * math.sin(2 * math.pi * (whoosh_freq + 20) * t + 0.1)
            right_crackle = 0.0
            if random.random() < 0.1:
                right_crackle = 0.3 * noise_amp * (random.random() - 0.5)

            right_value = right_thrust + right_rumble + right_mid + right_whoosh + right_crackle

            # Apply overall envelope
            if t < 0.05:  # Quick attack
                envelope = t / 0.05
            elif t > duration - 0.1:  # Gradual release
                envelope = 1.0 - (t - (duration - 0.1)) / 0.1
            else:
                envelope = 1.0

            left_value *= envelope
            right_value *= envelope

            # Add doppler effect in the later part (pitch shift as missile moves away)
            if t > duration * 0.7:
                # Reduce high frequencies to simulate doppler effect
                left_value = left_value * 0.8 + left_value * 0.2 * (1.0 - (t - duration * 0.7) / (duration * 0.3))
                right_value = right_value * 0.8 + right_value * 0.2 * (1.0 - (t - duration * 0.7) / (duration * 0.3))

            # Ensure values are in range [-1.0, 1.0] with soft clipping
            def soft_clip(x):
                # Soft clipping function to avoid harsh digital distortion
                if x > 0.8:
                    return 0.8 + 0.2 * math.tanh((x - 0.8) / 0.2)
                elif x < -0.8:
                    return -0.8 + 0.2 * math.tanh((x + 0.8) / 0.2)
                return x

            left_value = soft_clip(left_value)
            right_value = soft_clip(right_value)

            # Convert to 16-bit PCM
            left_sample = int(left_value * 32000)
            right_sample = int(right_value * 32000)

            # Write samples
            wav_file.writeframes(struct.pack('hh', left_sample, right_sample))

    print(f"Created missile sound: {filepath}")

def create_bomb_sound(filename="bomb.wav", duration=1.5):
    """Create a powerful bomb sound effect with deep bass and shockwave"""
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

            # Initial detonation - very short, intense burst at the beginning
            detonation_factor = 1.0 if t < 0.01 else math.exp(-100 * (t - 0.01))
            detonation = detonation_factor * 0.95 * (2.0 * random.random() - 1.0)

            # Massive low-frequency shockwave that builds quickly and decays slowly
            # This creates the feeling of a powerful explosion with physical impact
            if t < 0.05:  # Quick buildup
                shockwave_amp = t / 0.05
            else:  # Long decay
                shockwave_amp = math.exp(-1.5 * (t - 0.05))

            # Very low frequency for physical impact
            shockwave_freq = 25 + 15 * math.exp(-2 * t)  # Start at 40Hz and drop to 25Hz
            shockwave = shockwave_amp * 0.9 * math.sin(2 * math.pi * shockwave_freq * t)

            # Add sub-bass rumble for extended power
            sub_bass_freq = 50 * math.exp(-0.5 * t)  # Dropping frequency
            sub_bass = shockwave_amp * 0.8 * math.sin(2 * math.pi * sub_bass_freq * t)

            # Add mid-range explosion body
            mid_freq = 150 * math.exp(-2 * t)  # Dropping frequency
            mid_body = shockwave_amp * 0.6 * math.sin(2 * math.pi * mid_freq * t)

            # Add debris and destruction sounds (mid-high frequencies)
            debris_amp = 0.0
            if t > 0.1:  # Debris starts after initial explosion
                debris_amp = 0.4 * math.exp(-3 * (t - 0.1))

            # Multiple debris frequencies for richness
            debris1_freq = 800 + 200 * math.sin(t * 7)
            debris2_freq = 1200 + 300 * math.sin(t * 5)
            debris3_freq = 1800 + 400 * math.sin(t * 3)

            debris1 = debris_amp * 0.3 * math.sin(2 * math.pi * debris1_freq * t)
            debris2 = debris_amp * 0.2 * math.sin(2 * math.pi * debris2_freq * t)
            debris3 = debris_amp * 0.1 * math.sin(2 * math.pi * debris3_freq * t)

            # Add crackling and popping throughout
            crackle = 0.0
            if random.random() < 0.2 * math.exp(-1 * t):  # More frequent at beginning
                crackle_intensity = 0.5 * math.exp(-2 * t)
                crackle = crackle_intensity * (random.random() - 0.5)

            # Combine all components for left channel
            left_value = detonation + shockwave + sub_bass + mid_body + debris1 + debris2 + debris3 + crackle

            # Right channel with variations for enhanced stereo field
            # Slight phase and timing differences create a more immersive experience
            right_detonation = detonation * 0.98
            right_shockwave = shockwave_amp * 0.9 * math.sin(2 * math.pi * shockwave_freq * t + 0.1)
            right_sub_bass = shockwave_amp * 0.8 * math.sin(2 * math.pi * sub_bass_freq * t + 0.2)
            right_mid_body = shockwave_amp * 0.6 * math.sin(2 * math.pi * mid_freq * t + 0.15)

            # Different debris patterns in right channel
            right_debris1 = debris_amp * 0.3 * math.sin(2 * math.pi * (debris1_freq - 50) * t + 0.3)
            right_debris2 = debris_amp * 0.2 * math.sin(2 * math.pi * (debris2_freq + 70) * t + 0.2)
            right_debris3 = debris_amp * 0.1 * math.sin(2 * math.pi * (debris3_freq - 100) * t + 0.1)

            # Different crackle in right channel
            right_crackle = 0.0
            if random.random() < 0.2 * math.exp(-1 * t):
                right_crackle = crackle * 0.9 + 0.1 * (random.random() - 0.5) * math.exp(-2 * t)

            # Combine all components for right channel
            right_value = right_detonation + right_shockwave + right_sub_bass + right_mid_body + \
                         right_debris1 + right_debris2 + right_debris3 + right_crackle

            # Add secondary explosions for more complexity and realism
            if 0.2 < t < 0.8 and random.random() < 0.005:  # Occasional secondary explosions
                secondary_exp = 0.7 * (random.random() - 0.3) * math.exp(-2 * (t - 0.2))
                left_value += secondary_exp
                # Slightly delayed in right channel for spatial effect
                if i + 50 < num_samples:  # 50 samples = ~1ms delay
                    right_value += secondary_exp * 0.9

            # Ensure values are in range [-1.0, 1.0] with soft clipping for more natural sound
            def soft_clip(x):
                # Soft clipping function to avoid harsh digital distortion
                if x > 0.8:
                    return 0.8 + 0.2 * math.tanh((x - 0.8) / 0.2)
                elif x < -0.8:
                    return -0.8 + 0.2 * math.tanh((x + 0.8) / 0.2)
                return x

            left_value = soft_clip(left_value)
            right_value = soft_clip(right_value)

            # Convert to 16-bit PCM
            left_sample = int(left_value * 32000)  # Using 32000 instead of 32767 for safety
            right_sample = int(right_value * 32000)

            # Write samples
            wav_file.writeframes(struct.pack('hh', left_sample, right_sample))

    print(f"Created bomb sound: {filepath}")

def create_game_over_sound(filename="game_over.wav", duration=2.5):
    """Create a dramatic game over sound with descending tones and impact"""
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

            # Phase 1: Initial descending tone (0-1.0s)
            # Phase 2: Low rumble and impact (1.0-2.0s)
            # Phase 3: Final echo and fade (2.0-2.5s)

            # Dramatic descending tone that signifies defeat
            # Start with a higher pitch and descend to create tension
            if t < 1.0:
                # Exponential frequency drop for more dramatic effect
                desc_freq = 300 * math.exp(-2 * t) + 80
                # Amplitude builds slightly then fades
                if t < 0.1:
                    desc_amp = t / 0.1 * 0.8  # Fade in
                else:
                    desc_amp = 0.8 * (1 - (t - 0.1) / 0.9)  # Gradual fade out

                # Main tone with harmonics for richness
                desc_tone = desc_amp * math.sin(2 * math.pi * desc_freq * t)
                desc_harm1 = desc_amp * 0.5 * math.sin(2 * math.pi * desc_freq * 2 * t)
                desc_harm2 = desc_amp * 0.25 * math.sin(2 * math.pi * desc_freq * 3 * t)

                # Add slight vibrato for more emotion
                vibrato_freq = 5 + 3 * t  # Increasing vibrato rate
                vibrato_depth = 10 * t  # Increasing vibrato depth
                vibrato = desc_amp * 0.3 * math.sin(2 * math.pi * (desc_freq + vibrato_depth * math.sin(2 * math.pi * vibrato_freq * t)) * t)

                descending = desc_tone + desc_harm1 + desc_harm2 + vibrato
            else:
                descending = 0

            # Low impact and rumble after the descending tone
            if 0.8 < t < 2.0:
                # Normalized time within this phase
                impact_t = (t - 0.8) / 1.2

                # Initial impact
                impact_amp = 0.0
                if 0.8 < t < 0.9:
                    impact_amp = 0.9 * (1 - (t - 0.8) / 0.1)
                    impact = impact_amp * (2.0 * random.random() - 1.0)
                else:
                    impact = 0

                # Low rumble that follows the impact
                if 0.85 < t < 2.0:
                    rumble_t = (t - 0.85) / 1.15
                    rumble_freq = 50 * (1 - rumble_t * 0.5)  # Gradually decreasing frequency
                    rumble_amp = 0.7 * math.exp(-1.5 * rumble_t)
                    rumble = rumble_amp * math.sin(2 * math.pi * rumble_freq * t)

                    # Add some grit to the rumble
                    rumble_noise = rumble_amp * 0.3 * (2.0 * random.random() - 1.0) * math.exp(-3 * rumble_t)
                else:
                    rumble = 0
                    rumble_noise = 0

                # Combine impact components
                impact_combined = impact + rumble + rumble_noise
            else:
                impact_combined = 0

            # Final echo and fade
            if t > 1.8:
                # Echo of the initial descending tone, but much quieter and more reverberant
                echo_t = t - 1.8
                echo_freq = 100 * math.exp(-1 * echo_t) + 60
                echo_amp = 0.3 * math.exp(-2 * echo_t)

                # Multiple echoes with different delays for reverb effect
                echo1 = echo_amp * math.sin(2 * math.pi * echo_freq * echo_t)
                if echo_t > 0.05:  # First echo
                    echo2 = echo_amp * 0.7 * math.sin(2 * math.pi * echo_freq * (echo_t - 0.05))
                else:
                    echo2 = 0
                if echo_t > 0.12:  # Second echo
                    echo3 = echo_amp * 0.5 * math.sin(2 * math.pi * echo_freq * (echo_t - 0.12))
                else:
                    echo3 = 0
                if echo_t > 0.2:  # Third echo
                    echo4 = echo_amp * 0.3 * math.sin(2 * math.pi * echo_freq * (echo_t - 0.2))
                else:
                    echo4 = 0

                echo_combined = echo1 + echo2 + echo3 + echo4
            else:
                echo_combined = 0

            # Combine all components for left channel
            left_value = descending + impact_combined + echo_combined

            # Right channel with variations for enhanced stereo field
            # Slight phase and timing differences create a more immersive experience
            if t < 1.0:
                # Slightly different frequency and phase for stereo width
                right_desc_freq = 300 * math.exp(-2 * t) + 80 - 2  # Slightly lower pitch
                if t < 0.1:
                    right_desc_amp = t / 0.1 * 0.8
                else:
                    right_desc_amp = 0.8 * (1 - (t - 0.1) / 0.9)

                right_desc_tone = right_desc_amp * math.sin(2 * math.pi * right_desc_freq * t + 0.1)  # Phase offset
                right_desc_harm1 = right_desc_amp * 0.5 * math.sin(2 * math.pi * right_desc_freq * 2 * t + 0.2)
                right_desc_harm2 = right_desc_amp * 0.25 * math.sin(2 * math.pi * right_desc_freq * 3 * t + 0.15)

                right_vibrato_freq = 5 + 3 * t
                right_vibrato_depth = 10 * t
                right_vibrato = right_desc_amp * 0.3 * math.sin(2 * math.pi * (right_desc_freq + right_vibrato_depth *
                                                                           math.sin(2 * math.pi * right_vibrato_freq * t + 0.1)) * t)

                right_descending = right_desc_tone + right_desc_harm1 + right_desc_harm2 + right_vibrato
            else:
                right_descending = 0

            # Impact and rumble with slight variations
            if 0.8 < t < 2.0:
                right_impact_t = (t - 0.8) / 1.2

                if 0.8 < t < 0.9:
                    right_impact_amp = 0.9 * (1 - (t - 0.8) / 0.1)
                    right_impact = right_impact_amp * (2.0 * random.random() - 1.0)
                else:
                    right_impact = 0

                if 0.85 < t < 2.0:
                    right_rumble_t = (t - 0.85) / 1.15
                    right_rumble_freq = 50 * (1 - right_rumble_t * 0.5) - 1  # Slightly different frequency
                    right_rumble_amp = 0.7 * math.exp(-1.5 * right_rumble_t)
                    right_rumble = right_rumble_amp * math.sin(2 * math.pi * right_rumble_freq * t + 0.2)  # Phase offset

                    right_rumble_noise = right_rumble_amp * 0.3 * (2.0 * random.random() - 1.0) * math.exp(-3 * right_rumble_t)
                else:
                    right_rumble = 0
                    right_rumble_noise = 0

                right_impact_combined = right_impact + right_rumble + right_rumble_noise
            else:
                right_impact_combined = 0

            # Echo with different timing for enhanced stereo
            if t > 1.8:
                right_echo_t = t - 1.8
                right_echo_freq = 100 * math.exp(-1 * right_echo_t) + 60 - 1  # Slightly different frequency
                right_echo_amp = 0.3 * math.exp(-2 * right_echo_t)

                # Different echo timing for stereo width
                right_echo1 = right_echo_amp * math.sin(2 * math.pi * right_echo_freq * right_echo_t + 0.1)
                if right_echo_t > 0.06:  # Slightly different delay
                    right_echo2 = right_echo_amp * 0.7 * math.sin(2 * math.pi * right_echo_freq * (right_echo_t - 0.06) + 0.15)
                else:
                    right_echo2 = 0
                if right_echo_t > 0.14:  # Slightly different delay
                    right_echo3 = right_echo_amp * 0.5 * math.sin(2 * math.pi * right_echo_freq * (right_echo_t - 0.14) + 0.2)
                else:
                    right_echo3 = 0
                if right_echo_t > 0.23:  # Slightly different delay
                    right_echo4 = right_echo_amp * 0.3 * math.sin(2 * math.pi * right_echo_freq * (right_echo_t - 0.23) + 0.1)
                else:
                    right_echo4 = 0

                right_echo_combined = right_echo1 + right_echo2 + right_echo3 + right_echo4
            else:
                right_echo_combined = 0

            # Combine all components for right channel
            right_value = right_descending + right_impact_combined + right_echo_combined

            # Apply overall envelope to ensure smooth start and end
            if t < 0.05:  # Smooth start
                envelope = t / 0.05
            elif t > duration - 0.1:  # Smooth end
                envelope = (duration - t) / 0.1
            else:
                envelope = 1.0

            left_value *= envelope
            right_value *= envelope

            # Ensure values are in range [-1.0, 1.0] with soft clipping for more natural sound
            def soft_clip(x):
                # Soft clipping function to avoid harsh digital distortion
                if x > 0.8:
                    return 0.8 + 0.2 * math.tanh((x - 0.8) / 0.2)
                elif x < -0.8:
                    return -0.8 + 0.2 * math.tanh((x + 0.8) / 0.2)
                return x

            left_value = soft_clip(left_value)
            right_value = soft_clip(right_value)

            # Convert to 16-bit PCM
            left_sample = int(left_value * 32000)  # Using 32000 instead of 32767 for safety
            right_sample = int(right_value * 32000)

            # Write samples
            wav_file.writeframes(struct.pack('hh', left_sample, right_sample))

    print(f"Created game over sound: {filepath}")

def create_game_sounds():
    """Create all the sound files needed for the game"""
    # Create shoot sound (higher pitch, shorter, with harmonics)
    create_laser_sound("shoot.wav")

    # Also create a separate laser sound for variety
    create_laser_sound("laser.wav")

    # Create explosion sound (custom complex sound)
    create_explosion_sound("explosion.wav")

    # Create game over sound (dramatic and intense)
    create_game_over_sound("game_over.wav")

    # Create powerup sound (higher pitch, with harmonics)
    create_simple_sound("powerup.wav", duration=0.4, frequency=1320.0, volume=0.6,
                       sound_type="complex", stereo=True)

    # Create bomb sound (powerful low-frequency explosion)
    create_bomb_sound("bomb.wav")

    # Create missile sound (more realistic with thrust and whoosh)
    create_missile_sound("missile.wav")

    # Note: Background music is now a downloaded file (Space Heroes by Oblidivm)
    # from OpenGameArt.org under CC-BY 3.0 license
    # We don't need to generate it anymore
    # create_background_music("background_music.wav", duration=15.0)

if __name__ == "__main__":
    create_game_sounds()
