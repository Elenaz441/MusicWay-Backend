import pytest
from utils import convert_russian_note_to_international, get_common_note
from fastapi import HTTPException

from unittest.mock import patch, MagicMock
import numpy as np


@pytest.mark.parametrize('russian, expected', [
    ('до первой октавы', 'C4'),
    ('ре диез второй октавы', 'D#5'),
    ('ми бемоль малой октавы', 'D#3'),
    ('соль бемоль второй октавы', 'F#5'),
    ('ля', 'A4'),
])
def test_convert_russian_note_to_international_valid(russian, expected):
    assert convert_russian_note_to_international(russian) == expected


def test_convert_russian_note_to_international_invalid_note():
    with pytest.raises(ValueError):
        convert_russian_note_to_international('им первой октавы')


def test_convert_cb_edge_case():
    assert convert_russian_note_to_international('до бемоль первой октавы') == 'B3'


@patch('utils.AudioSegment.from_file')
@patch('utils.aubio.pitch')
@patch('utils.aubio.freq2note')
def test_get_common_note_valid(mock_freq2note, mock_pitch_class, mock_from_file):
    mock_audio = MagicMock()
    mock_audio.get_array_of_samples.return_value = np.ones(40960, dtype=np.int16)
    mock_audio.frame_rate = 44100
    mock_from_file.return_value = mock_audio

    mock_pitch = MagicMock()
    mock_pitch.return_value = [440.0]
    mock_pitch_class.return_value = mock_pitch

    mock_freq2note.return_value = 'A4'

    result = get_common_note(b'fake_audio_data')
    assert result == 'A4'


@patch('utils.AudioSegment.from_file', side_effect=Exception('decode error'))
def test_get_common_note_exception(mock_from_file):
    with pytest.raises(HTTPException) as exc:
        get_common_note(b'broken_audio')
    assert exc.value.status_code == 400
    assert 'Audio processing error' in str(exc.value.detail)
