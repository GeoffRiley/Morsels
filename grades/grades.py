from statistics import mean

GRADES = {
    (0, 60): 'F',
    (60, 70): 'D',
    (70, 80): 'C',
    (80, 90): 'B',
    (90, 101): 'A'
}

SUFFIX = {(0, 3): '-', (3, 7): '', (7, 11): '+'}

GPA_VALUES = {
    'A+': 4.33,
    'A': 4.00,
    'A-': 3.67,
    'B+': 3.33,
    'B': 3.00,
    'B-': 2.67,
    'C+': 2.33,
    'C': 2.00,
    'C-': 1.67,
    'D+': 1.33,
    'D': 1.00,
    'D-': 0.67,
    'F': 0.00,
}


def percent_to_grade(pcent: float,
                     *,
                     suffix: bool = False,
                     round: bool = False) -> str:
    if round:
        pcent = int(pcent + 0.5)
    for (pl, ph), g in GRADES.items():
        if pl <= pcent < ph:
            if not suffix or g == 'F':
                return g
            pcent_last_digit = pcent - (
                (pcent // 10) * 10) + (10 if pcent == 100 else 0)
            for (dl, dh), sfx in SUFFIX.items():
                if dl <= pcent_last_digit < dh:
                    return g + sfx
    raise ValueError(f'Percentage mark ({pcent}) not recognised')


def calculate_gpa(lst: list) -> float:
    return mean(GPA_VALUES[g] for g in lst)
