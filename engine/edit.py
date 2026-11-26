"""A shared edit list keeps picture and sound on the same timeline."""
import math
import numpy as np
import subprocess


def validate_edit(scenes, edit):
    for duration, start, end in edit:
        if not all(math.isfinite(v) for v in (duration, start, end)) or duration <= 0 or end <= start:
            raise ValueError("Edit ranges and durations must be finite and positive")
        if not any(a <= start < end <= b + 1e-8 for a, b, _ in scenes):
            raise ValueError(f"Edit range {start}:{end} crosses a scene boundary")


def edited_draw(scenes, edit, fps=30):
    validate_edit(scenes, edit)
    shots = []
    output_start = 0.0
    for duration, start, end in edit:
        a, _, fn = next(s for s in scenes if s[0] <= start < end <= s[1] + 1e-8)
        shots.append((output_start, output_start + duration, start, end, a, fn))
        output_start += duration

    def draw(context, time, frame):
        for output_start, output_end, start, end, scene_start, fn in shots:
            if output_start <= time < output_end:
                source_time = start + (time - output_start) / (output_end - output_start) * (end - start)
                context.save()
                fn(context, source_time - scene_start, int(source_time * fps), source_time)
                context.restore()
                return
        raise ValueError(f"Frame time {time} outside edit")

    return draw


def edited_audio(samples, sample_rate, edit):
    """Match each source sound to its edited action, with short click-free edges."""
    chunks = []
    for duration, start, end in edit:
        count = round(duration * sample_rate)
        if round(end * sample_rate) > len(samples):
            raise ValueError("Audio edit exceeds source samples")
        source = samples[round(start * sample_rate):round(end * sample_rate)].astype('<f8')
        speed = (end - start) / duration
        result = subprocess.run([
            'ffmpeg', '-v', 'error', '-f', 'f64le', '-ar', str(sample_rate), '-ac', '1', '-i', 'pipe:0',
            '-af', f'atempo={speed},apad=whole_len={count}', '-f', 'f64le', '-ar', str(sample_rate),
            '-ac', '1', 'pipe:1'], input=source.tobytes(), capture_output=True, check=True)
        chunk = np.frombuffer(result.stdout, dtype='<f8')[:count].copy()
        if len(chunk) != count:
            raise ValueError('Audio time stretch returned an unexpected duration')
        fade = min(round(0.008 * sample_rate), count // 2)
        if fade:
            chunk[:fade] *= np.linspace(0, 1, fade)
            chunk[-fade:] *= np.linspace(1, 0, fade)
        chunks.append(chunk)
    return np.concatenate(chunks)
