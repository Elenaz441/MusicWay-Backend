from io import BytesIO
from pydub import AudioSegment
import numpy as np
import aubio
from fastapi import HTTPException


def convert_russian_note_to_international(russian_note: str) -> str:
    """Конвертирует русские названия нот с октавами в международный формат."""

    note_map = {
        'до': 'C',
        'ре': 'D',
        'ми': 'E',
        'фа': 'F',
        'соль': 'G',
        'ля': 'A',
        'си': 'B'
    }

    alteration_map = {
        'диез': '#',
        'бемоль': 'b'
    }

    octave_map = {
        'малой': 3,
        'первой': 4,
        'второй': 5
    }

    parts = russian_note.lower().split()
    base_note = parts[0]

    alteration = ''
    for part in parts[1:]:
        if part in alteration_map:
            alteration = alteration_map[part]
            break

    octave = 4
    for part in parts[1:]:
        if part in octave_map:
            octave = octave_map[part]
            break

    international_note = note_map.get(base_note, '')
    if not international_note:
        raise ValueError(f'Неизвестная нота: {base_note}')

    return f'{international_note}{alteration}{octave}'


def get_common_note(audio_bytes: bytes, file_format: str = 'wav') -> str:
    """Анализирует аудио и возвращает наиболее часто встречающуюся ноту"""
    try:
        audio = AudioSegment.from_file(BytesIO(audio_bytes), format=file_format)
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
        sample_rate = audio.frame_rate

        samples /= np.max(np.abs(samples))

        pitch_o = aubio.pitch('yinfft', 4096, 2048, sample_rate)
        pitch_o.set_unit('Hz')
        pitch_o.set_tolerance(0.8)

        notes = {}
        for i in range(0, len(samples), 2048):
            chunk = samples[i:i + 2048]
            if len(chunk) < 2048:
                break
            pitch = pitch_o(chunk)[0]
            if pitch != 0:
                try:
                    note = aubio.freq2note(pitch)
                    if note not in notes:
                        notes[note] = 0
                    notes[note] += 1
                except ValueError:
                    continue
        print(notes)
        most_common_note = max(notes.items(), key=lambda x: x[1])[0]
        return most_common_note
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Audio processing error: {str(e)}")
