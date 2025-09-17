import librosa, random, math

from utils import resource_path

def beatarray(file_name):
    """
    Generate a beatmap directly from the beats of the chosen song
    Each beat is assigned a random lane (1-6).
    """

    # Load audio file
    y, sr = librosa.load(resource_path(file_name), mono=True)

    # Detect beats (returns frame numbers)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    # Convert frames to ms
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    beat_times_ms = [int(bt * 1000) for bt in beat_times]
    note_travel_time = 2000
    visual_latency = note_travel_time

    # Build beatmap
    beatmap = []
    for idx, time in enumerate(beat_times_ms):
        if time <= 2500: # Skip first ~2.5s to give time before notes
            continue

        beatmap.append(
            {
                "position": random.randint(1, 6), # Random lane for now
                "time": time - visual_latency,
                "hit": False
            }
        )
        

    # Calculate ending time of song
    duration = librosa.get_duration(y=y, sr=sr)
    ending = (math.ceil(duration) * 1000) + 2500

    print(f"Generated {len(beatmap)} notes from {file_name}")
    return beatmap, ending