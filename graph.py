from typing import Callable
from svgwrite import Drawing

from geometry import Point, Rectangle, Line


scale = 840
margin_x = 50
margin_y = 25
eps = 0

period = 1
x_min = 0
x_max = 1


class Graph:
    def __init__(self, y_min: float, y_max: float, aspect_ratio: float):
        scale_x = scale
        scale_y = scale / (y_max - y_min) / aspect_ratio
        self.transform: Callable[[Point], Point] = lambda point: (
            margin_x + scale_x * (point[0] - x_min),
            margin_y - scale_y * (point[1] - y_max),
        )
        self.clip_rect = Rectangle(x_min - eps, y_min - eps, x_max + eps, y_max + eps)
        
        width  = margin_x * 2 + (x_max - x_min) * scale_x
        height = margin_y * 2 + (y_max - y_min) * scale_y
        self.svg = Drawing(size=(width, height))
        self.svg.add(self.svg.rect(size=(width, height), fill='white'))
        self.canvas = self.svg.g(stroke_width=0.25, stroke_linecap='round', stroke_linejoin='round')
        self.svg.add(self.canvas)
    
    def draw_point(self, point: Point, color: str, size: float=1) -> None:
        self.canvas.add(self.svg.circle(center=self.transform(point), r = size, fill=color))
    
    def draw_line(self, line: Line, color: str) -> None:
        segment = line.clip(self.clip_rect)
        if segment is not None:
            start, end = segment
            self.canvas.add(self.svg.line(start=self.transform(start), end=self.transform(end), stroke=color))
    
    def draw_text(self, point: Point, text: str, padding: Point=(0, 0), text_anchor='start', color: str='black', font_size=7) -> None:
        tx, ty = self.transform(point)
        px, py = padding
        insert = (tx + font_size * px, ty + font_size * py)
        self.canvas.add(self.svg.text(text=text, insert=insert, font_size=font_size, text_anchor=text_anchor, fill=color))
    
    def draw_periodic_point(self, point: Point, name:str, color: str, name_color: str, size: float=1) -> None:
        x, y = point
        if self.clip_rect.y_min <= y <= self.clip_rect.y_max:
            xp = x - (x - self.clip_rect.x_min) // period * period
            while xp <= self.clip_rect.x_max:
                self.draw_point((xp, y), color, size)
                self.draw_text((xp, y), name, (0.1, -0.1), color=name_color)
                xp += period
    
    def draw_periodic_line(self, line: Line, color: str) -> None:
        try:
            x0 = (line.c - line.b * self.clip_rect.y_min) / line.a
            x1 = (line.c - line.b * self.clip_rect.y_max) / line.a
            p = max((x0 - self.clip_rect.x_min) // period, (x1 - self.clip_rect.x_min) // period)
            xp0 = x0 - p * period
            xp1 = x1 - p * period
            while xp0 <= self.clip_rect.x_max or xp1 <= self.clip_rect.x_max:
                self.draw_line(Line.thru_points((xp0, self.clip_rect.y_min), (xp1, self.clip_rect.y_max)), color)
                xp0 += period
                xp1 += period
        except ZeroDivisionError:
            self.draw_line(line, color)
