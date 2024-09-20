from __future__ import annotations
from dataclasses import dataclass
from math import inf


Point = tuple[float, float]
""" (x, y) """


LineSegment = tuple[Point, Point]
""" (start, end) """


@dataclass(frozen=True, slots=True)
class Rectangle:
    x_min: float
    y_min: float
    x_max: float
    y_max: float


@dataclass(frozen=True, slots=True)
class Line:
    """ ax + by = c """
    a: float
    b: float
    c: float
    
    @classmethod
    def horizontal(cls, y: float) -> Line:
        return cls(0, 1, y)
    
    @classmethod
    def vertical(cls, x: float) -> Line:
        return cls(1, 0, x)
    
    @classmethod
    def thru_points(cls, p1: Point, p2: Point) -> Line:
        x1, y1 = p1
        x2, y2 = p2
        return cls(y2 - y1, x1 - x2, x1 * y2 - x2 * y1)
    
    def intersect_with(self, other: Line) -> Point:
        d = self.a * other.b - self.b * other.a
        dx = self.c * other.b - self.b * other.c
        dy = self.a * other.c - self.c * other.a
        return (divide(dx, d), divide(dy, d))
    
    def clip(self, rect: Rectangle) -> LineSegment | None:
        points = []
        y = divide(self.c - self.a * rect.x_min, self.b)
        if rect.y_min <= y <= rect.y_max:
            points.append((rect.x_min, y))
        x = divide(self.c - self.b * rect.y_min, self.a)
        if rect.x_min <= x <= rect.x_max:
            points.append((x, rect.y_min))
        y = divide(self.c - self.a * rect.x_max, self.b)
        if rect.y_min <= y <= rect.y_max:
            points.append((rect.x_max, y))
        x = divide(self.c - self.b * rect.y_max, self.a)
        if rect.x_min <= x <= rect.x_max:
            points.append((x, rect.y_max))
        
        if len(points) < 2:
            return None
        start = points[0]
        end = max(points[1:], key=lambda p: abs(p[0] - start[0]) + abs(p[1] - start[1]))
        return (start, end)


def divide(a: float, b: float) -> float:
    """ Floating-point division without raising ZeroDivisionError """
    try:
        return a / b
    except ZeroDivisionError:
        return inf