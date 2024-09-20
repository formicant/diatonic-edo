from math import sqrt

from music import get_harmonic, fifth, get_first_n_notes, get_note_name, Edo
from geometry import Line
from graph import Graph


color_harmonic = 'magenta'
color_edo = 'blue'


def get_gray_color(value: float) -> str:
    value = max(0, min(1, value))
    c = round(240 * sqrt(value))
    return f'#{c:02x}{c:02x}{c:02x}'
    


def draw_diatonic_edo(max_edo: int, y_min: float, y_max: float, file_name: str) -> None:
    graph = Graph(y_min, y_max, aspect_ratio=1)
    
    # draw slopes
    slope_count = max_edo // 2 * 2 + 1  # always odd
    for note in reversed(list(get_first_n_notes(slope_count))):
        line = Line.thru_points((0, 0), (note, 1))
        transparency = abs(note) / (max_edo // 2)
        graph.draw_periodic_line(line, get_gray_color(transparency))
    
    # draw harmonics
    graph.draw_line(Line.horizontal(fifth), color_harmonic)
    for h in range(2, 19):
        x = get_harmonic(h)
        graph.draw_line(Line.vertical(x), color_harmonic)
        if h < 10 or h % 2 == 0:
            graph.draw_text((x, y_min), f'{h}', (0, 1.5), 'middle', color_harmonic)
            graph.draw_text((x, y_max), f'{h}', (0, -1), 'middle', color_harmonic)
    
    # draw EDOs
    transparency_factor = 0.8 / ((slope_count + 3) // 7)
    for number in range(1, max_edo + 1):
        edo = Edo(number)
        y = float(edo.fraction)
        if not y_min <= y <= y_max:
            continue
        
        graph.draw_line(Line.horizontal(y), color_edo)
        graph.draw_text((0, y), f'{number} edo', (-1, 0.3), 'end', color_edo)
        graph.draw_text((1, y), f'{edo.fraction}', (1.75, 0.3), 'start', color_edo)
        
        for note in edo.notes:
            transparency = transparency_factor * abs((note + 3) // 7)
            graph.draw_periodic_point((note * y, y), get_note_name(note), color_edo, get_gray_color(transparency))
    
    graph.svg.saveas(file_name)


if __name__ == '__main__':
    draw_diatonic_edo(
        max_edo=53,
        y_min=4/7, # 1/2,
        y_max=3/5, # 1,
        file_name='diatonic-edo.svg'
    )
