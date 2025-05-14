def convert_russian_note_to_international(russian_note: str) -> str:
    """Конвертирует русские названия нот с октавами в международный формат.

    :param russian_note: Название ноты на русском (например "до диез первой октавы").

    :return: Название ноты в международном формате.
    """

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

    flat_to_sharp_map = {
        'Cb': 'B',
        'Db': 'C#',
        'Eb': 'D#',
        'Fb': 'E',
        'Gb': 'F#',
        'Ab': 'G#',
        'Bb': 'A#'
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

    if alteration == 'b':
        note_with_flat = f'{international_note}{alteration}'
        if note_with_flat in flat_to_sharp_map:
            international_note = flat_to_sharp_map[note_with_flat]
            if note_with_flat == 'Cb':
                octave -= 1
        alteration = ''

    return f'{international_note}{alteration}{octave}'


def parse_note(note: str) -> (str, int):
    """Разбивает ноту на букву и октаву

    :param note: Нота (например, C4 или F#5)

    :return: Кортеж, где первое значение содержит букву и знак (при наличии), а второе - номер октавы.
    """
    letter_part = []
    for char in note:
        if not char.isdigit():
            letter_part.append(char)
        else:
            break
    letter = ''.join(letter_part)
    octave = int(note[len(letter):])
    return letter, octave


def calculate_interval(note1: str, note2: str) -> str:
    """Считает интервал на основе полутонов.

    :param note1: Первая нота.
    :param note2: Вторая нота.

    :return: Направление и наименование интервала.
    """
    note_to_semitone = {
        'C': 0, 'C#': 1, 'D': 2, 'D#': 3,
        'E': 4, 'F': 5, 'F#': 6, 'G': 7,
        'G#': 8, 'A': 9, 'A#': 10, 'B': 11
    }

    letter1, octave1 = parse_note(note1)
    letter2, octave2 = parse_note(note2)

    semitone1 = note_to_semitone[letter1] + 12 * octave1
    semitone2 = note_to_semitone[letter2] + 12 * octave2
    semitone_diff = semitone2 - semitone1

    if semitone_diff > 0:
        direction = 'восходящая'
    elif semitone_diff < 0:
        direction = 'нисходящая'
    else:
        direction = ''  # унисон

    semitone_diff_abs = abs(semitone_diff)

    interval_table = {
        0: 'ч.1', 1: 'м.2', 2: 'б.2', 3: 'м.3', 4: 'б.3',
        5: 'ч.4', 6: 'ум.5', 7: 'ч.5', 8: 'м.6',
        9: 'б.6', 10: 'м.7', 11: 'б.7', 12: 'ч.8'
    }

    semitone_mod = semitone_diff_abs
    if semitone_mod > 12:
        semitone_mod %= 12
    interval_name = interval_table.get(semitone_mod, 'неизвестный интервал')

    if semitone_diff_abs == 0:
        return interval_name
    else:
        return f'{direction} {interval_name}'


# def calculate_interval(note1, note2):
#     """Считает интервал на основе нотной записи."""
#     note_to_semitone = {
#         'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
#         'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
#         'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
#     }
#
#     letter1, octave1 = parse_note(note1)
#     letter2, octave2 = parse_note(note2)
#
#     semitone1 = note_to_semitone[letter1] + 12 * octave1
#     semitone2 = note_to_semitone[letter2] + 12 * octave2
#     semitone_diff = semitone2 - semitone1
#
#     if semitone_diff > 0:
#         direction = 'восходящая'
#     elif semitone_diff < 0:
#         direction = 'нисходящая'
#     else:
#         direction = ''
#     semitone_diff_abs = abs(semitone_diff)
#
#     note_order = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
#     idx1 = note_order.index(letter1[0])
#     idx2 = note_order.index(letter2[0])
#     steps = (idx2 - idx1) % 7 + 1
#
#     interval_map = {
#         1: {0: 'ч.1', 1: 'ув.1'},
#         2: {0: 'ум.2', 1: 'м.2', 2: 'б.2', 3: 'ув.2'},
#         3: {2: 'ум.3', 3: 'м.3', 4: 'б.3', 5: 'ув.3'},
#         4: {4: 'ум.4', 5: 'ч.4', 6: 'ув.4'},
#         5: {6: 'ум.5', 7: 'ч.5', 8: 'ув.5'},
#         6: {7: 'ум.6', 8: 'м.6', 9: 'б.6', 10: 'ув.6'},
#         7: {9: 'ум.7', 10: 'м.7', 11: 'б.7', 12: 'ув.7'},
#         8: {12: 'ч.8'}
#     }
#
#     interval_name = (interval_map
#                      .get(steps, {})
#                      .get(semitone_diff_abs,
#                      f'неизвестный интервал ({steps} ступеней, {semitone_diff_abs} полутонов)'))
#
#     if steps == 1 and semitone_diff_abs == 0:
#         return interval_name
#     else:
#         return f'{direction} {interval_name}'
