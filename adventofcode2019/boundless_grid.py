import collections
import collections.abc
from enum import Enum
from typing import Callable, Iterator, MutableMapping, Tuple, TypeVar, Any, Iterable

T = TypeVar('T')


class Coord(collections.namedtuple('Coord', ('x', 'y'))):
    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(self.x + other.x, self.y + other.y)


class Orientation(Enum):
    NORMAL = 1
    INVERT_Y = 2


class BoundlessGrid(collections.abc.MutableMapping):
    axes = True
    default_factory = None
    margin = (1, 1, 1, 1)
    """top, right, bottom, left"""
    orientation = Orientation.NORMAL

    def __init__(self, default_factory: Callable[[], T] = None, **kwargs) -> None:
        self._default_factory = default_factory or self.default_factory
        self._grid: MutableMapping[Coord, T] = collections.defaultdict(self._default_factory)
        self._dirty_bounds = False
        self._bounds: Tuple[Coord, Coord] = (Coord(0, 0), Coord(0, 0))
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _cast_coord(self, value: Any) -> Coord:
        if isinstance(value, Coord):
            return value
        elif hasattr(value, 'x') and hasattr(value, 'y'):
            return Coord(value.x, value.y)
        elif isinstance(value, Iterable):
            return Coord(*value)
        raise ValueError("Invalid coordinate: %s", value)

    def __getitem__(self, item: Coord) -> T:
        coord = self._cast_coord(item)
        return self._grid[coord] if coord in self._grid else self._default_factory()

    def __setitem__(self, coord: Coord, value: T) -> None:
        coord = self._cast_coord(coord)
        if coord not in self._grid:
            self._dirty_bounds = True
        self._grid[coord] = value

    def __contains__(self, item: Coord) -> bool:
        return self._cast_coord(item) in self._grid

    def __delitem__(self, v: Coord) -> None:
        del self._grid[self._cast_coord(v)]

    def __len__(self) -> int:
        return len(self._grid)

    def __iter__(self) -> Iterator[Coord]:
        return iter(self._grid.keys())

    @property
    def bounds(self) -> Tuple[Coord, Coord]:
        if not self._dirty_bounds:
            return self._bounds
        left = right = (self._grid.keys() and set(self._grid.keys()).pop().x) or 0
        top = bottom = (self._grid.keys() and set(self._grid.keys()).pop().y) or 0
        for key in self._grid.keys():
            left = min(key.x, left)
            right = max(key.x, right)
            top = max(key.y, top) if self.orientation == Orientation.NORMAL else min(key.y, top)
            bottom = min(key.y, bottom) if self.orientation == Orientation.NORMAL else max(key.y,
                                                                                           bottom)
        self._dirty_bounds = False
        self._bounds = Coord(left, top), Coord(right, bottom)
        return self._bounds

    def str_for_coord(self, coord: Coord) -> str:
        return self.str_for_value(self._grid[coord]
                                  if coord in self._grid
                                  else self._default_factory())

    def str_for_value(self, value: T) -> str:
        """A single char representation of the value"""
        s_value = str(value)
        return s_value[-1] if s_value else ' '

    def __str__(self) -> str:
        lines = []
        bounds = self.bounds
        if self.orientation == Orientation.NORMAL:
            y_range = range(bounds[0].y + self.margin[0], bounds[1].y - self.margin[2] - 1, -1)
        elif self.orientation == Orientation.INVERT_Y:
            y_range = range(bounds[0].y - self.margin[0], bounds[1].y + self.margin[2] + 1)
        else:
            raise ValueError("Invalid orientation: %s", self.orientation)
        xrange = range(bounds[0][0] - self.margin[3], bounds[1][0] + self.margin[1] + 1)
        if self.axes:
            lines.append('  ' + ''.join(str(x)[-1] for x in xrange))
            lines.append(' +' + '-' * len(xrange))
        for y in y_range:
            y_axis = str(y)[-1] + '|' if self.axes else ''
            lines.append(y_axis + ''.join(self.str_for_coord((x, y)) for x in xrange))
        return '\n'.join(lines)
