import pytest
from utils import convert_russian_note_to_international, parse_note, calculate_interval


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


@pytest.mark.parametrize('note, expected', [
    ('C4', ('C', 4)),
    ('F#5', ('F#', 5)),
    ('A#3', ('A#', 3)),
    ('G#10', ('G#', 10)),
    ('D0', ('D', 0)),
])
def test_parse_note(note, expected):
    assert parse_note(note) == expected


@pytest.mark.parametrize('note1, note2, expected', [
    ('C4', 'C4', 'ч.1'),
    ('C4', 'D4', 'восходящая б.2'),
    ('C4', 'B3', 'нисходящая м.2'),
    ('C4', 'E4', 'восходящая б.3'),
    ('G4', 'E4', 'нисходящая м.3'),
    ('F#4', 'C5', 'восходящая ум.5'),
    ('C4', 'C5', 'восходящая ч.8'),
    ('C4', 'A4', 'восходящая б.6'),
    ('C4', 'A#4', 'восходящая м.7'),
    ('C4', 'C#5', 'восходящая м.2'),
])
def test_calculate_interval_valid(note1, note2, expected):
    assert calculate_interval(note1, note2) == expected
