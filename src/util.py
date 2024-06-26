from __future__ import annotations
import numpy as np
import pygame as pg
from typing import Protocol, TypeVar, Generic, Any
import colorsys

# --------------------------------------------- #

LMB: int = 0
MMB: int = 1
RMB: int = 2
MMB_UP: int = 4
MMB_DOWN: int = 5

# --------------------------------------------- #

FArray = np.ndarray[float, Any]
IArray = np.ndarray[int, Any]

# --------------------------------------------- #

def interpolate_v3(v1: V3[int], v2: V3[int], x: float) -> V3[int]:
    r1: float = (1.0 - x) * v1[0] + x * v2[0]
    r2: float = (1.0 - x) * v1[1] + x * v2[1]
    r3: float = (1.0 - x) * v1[2] + x * v2[2]

    return V3(r1, r2, r3).to_int()

def bilinear_interpolate_v3(v1: V3[int], v2: V3[int], v3: V3[int], v4: V3[int], x: float, y: float) -> V3[int]:
    i1: V3[int] = interpolate_v3(v1, v2, x)
    i2: V3[int] = interpolate_v3(v3, v4, x)
    return interpolate_v3(i1, i2, y)

def interpolate_hsv(v1: V3[int], v2: V3[int], x: float) -> V3[int]:
    hsv1: tuple[float, float, float] = colorsys.rgb_to_hsv(*(v1.scalar_truediv(255).get()))
    hsv2: tuple[float, float, float] = colorsys.rgb_to_hsv(*(v2.scalar_truediv(255).get()))

    h: float = (1.0 - x) * hsv1[0] + x * hsv2[0]
    s: float = (1.0 - x) * hsv1[1] + x * hsv2[1]
    v: float = (1.0 - x) * hsv1[2] + x * hsv2[2]

    hsv: tuple[float, float, float] = colorsys.hsv_to_rgb(h, s, v)
    return V3(*hsv).scalar_mul(255).to_int()

def bilinear_interpolate_hsv(v1: V3[int], v2: V3[int], v3: V3[int], v4: V3[int], x: float, y: float) -> V3[int]:
    hsv1: V3[float] = V3(*colorsys.rgb_to_hsv(*(v1.scalar_truediv(255).get())))
    hsv2: V3[float] = V3(*colorsys.rgb_to_hsv(*(v2.scalar_truediv(255).get())))
    hsv3: V3[float] = V3(*colorsys.rgb_to_hsv(*(v3.scalar_truediv(255).get())))
    hsv4: V3[float] = V3(*colorsys.rgb_to_hsv(*(v4.scalar_truediv(255).get())))
    hsv: V3[float] =  hsv1.scalar_mul((1 - x) * (1 - y)) + hsv3.scalar_mul((1 - x) * y) + hsv2.scalar_mul(x * (1 - y)) + hsv4.scalar_mul(x * y)
    return V3(*colorsys.hsv_to_rgb(*(hsv.get()))).scalar_mul(255).to_int()

def get_v3_from_colour(c: pg.Color) -> V3[int]:
    return V3(c[0], c[1], c[2])

# --------------------------------------------- #

_T = TypeVar("_T")
class Numeric(Protocol):
    def __add__(self: _T, __other: _T) -> _T: ...
    def __sub__(self: _T, __other: _T) -> _T: ...
    def __mul__(self: _T, __other: _T) -> _T: ...
    def __truediv__(self: _T, __other: _T) -> Any: ...
    def __floordiv__(self: _T, __other: _T) -> _T: ...
    def __mod__(self: _T, __other: _T) -> _T: ...
    def __eq__(self: _T, __other: _T) -> bool: ...
    def __ne__(self: _T, __other: _T) -> bool: ...
    def __int__(self: _T) -> Any: ... # type: ignore
    def __float__(self: _T) -> Any: ... # type: ignore
    def __gt__(self: _T, __other: _T) -> bool: ...

T = TypeVar("T", bound=Numeric)

class V2(Generic[T]):

    def __init__(self, a: T, b: T) -> None:
        self._t: tuple[T, T] = (a, b)

    def get(self) -> tuple[T, T]:
        return self._t

    def a(self) -> T:
        return self._t[0]
    def b(self) -> T:
        return self._t[1]
    
    def i(self) -> T:
        return self._t[0]
    def j(self) -> T:
        return self._t[1]
    
    def q(self) -> T:
        return self._t[0]
    def r(self) -> T:
        return self._t[1]
    
    def x(self) -> T:
        return self._t[0]
    def y(self) -> T:
        return self._t[1]

    def __add__(self, other: "V2[T]") -> "V2[T]":
        return V2(self._t[0] + other._t[0], self._t[1] + other._t[1])
    def scalar_add(self, value: T) -> "V2[T]":
        return V2(self._t[0] + value, self._t[1] + value)
    
    def __sub__(self, other: "V2[T]") -> "V2[T]":
        return V2(self._t[0] - other._t[0], self._t[1] - other._t[1])
    def scalar_sub(self, value: T) -> "V2[T]":
        return V2(self._t[0] - value, self._t[1] - value)

    def __mul__(self, other: "V2[T]") -> "V2[T]":
        return V2(self._t[0] * other._t[0], self._t[1] * other._t[1])
    def scalar_mul(self, value: T) -> "V2[T]":
        return V2(self._t[0] * value, self._t[1] * value)
    
    def __truediv__(self, other: "V2[T]") -> "V2[Any]":
        return V2(self._t[0] / other._t[0], self._t[1] / other._t[1])
    def scalar_truediv(self, value: T) -> "V2[Any]":
        return V2(self._t[0] / value, self._t[1] / value)
    
    def __floordiv__(self, other: "V2[T]") -> "V2[T]":
        return V2(self._t[0] // other._t[0], self._t[1] // other._t[1])
    def scalar_floordiv(self, value: T) -> "V2[T]":
        return V2(self._t[0] // value, self._t[1] // value)
    
    def __mod__(self, other: "V2[T]") -> "V2[T]":
        return V2(self._t[0] % other._t[0], self._t[1] % other._t[1])
    def scalar_mod(self, value: T) -> "V2[T]":
        return V2(self._t[0] % value, self._t[1] % value)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, V2):
            return self._t == other._t # type: ignore
        else:
            return super().__eq__(other)
        
    def __ne__(self, other: object) -> bool:
        if isinstance(other, V2):
            return not self.__eq__(other) # type: ignore
        else:
            return super().__ne__(other)
        
    def __gt__(self, other: object) -> bool:
        if isinstance(other, V2):
            return self._t > other._t # type: ignore
        else:
            return False
        
    def min(self, other: "V2[T]") -> "V2[T]":
        return V2(min(self._t[0], other._t[0]), min(self._t[1], other._t[1]))
    def max(self, other: "V2[T]") -> "V2[T]":
        return V2(max(self._t[0], other._t[0]), max(self._t[1], other._t[1]))
    
    def __getitem__(self, idx: int) -> T:
        assert idx == 0 or idx == 1, "idx out of range [0, 1]"
        return self._t[idx]

    def __int__(self) -> V2[int]:
        return V2(int(self._t[0]), int(self._t[1]))
    def to_int(self) -> V2[int]: # type: ignore
        return self.__int__()
    
    def __float__(self) -> V2[float]:
        return V2(float(self._t[0]), float(self._t[1]))
    def to_float(self) -> V2[float]:
        return self.__float__()
    
    def copy(self) -> V2[T]:
        return V2(self._t[0], self._t[1])

    def __str__(self) -> str:
        return "(" + str(self._t[0]) + ", " + str(self._t[1]) + ")"
    

class V3(Generic[T]):

    def __init__(self, a: T, b: T, c: T) -> None:
        self._t: tuple[T, T, T] = (a, b, c)

    def get(self) -> tuple[T, T, T]:
        return self._t
    
    def a(self) -> T:
        return self._t[0]
    def b(self) -> T:
        return self._t[1]
    def c(self) -> T:
        return self._t[2]
    
    def i(self) -> T:
        return self._t[0]
    def j(self) -> T:
        return self._t[1]
    def k(self) -> T:
        return self._t[2]
    
    def q(self) -> T:
        return self._t[0]
    def r(self) -> T:
        return self._t[1]
    def s(self) -> T:
        return self._t[2]
    
    def x(self) -> T:
        return self._t[0]
    def y(self) -> T:
        return self._t[1]
    def z(self) -> T:
        return self._t[2]

    def __add__(self, other: "V3[T]") -> "V3[T]":
        return V3(self._t[0] + other._t[0], self._t[1] + other._t[1], self._t[2] + other._t[2])
    def scalar_add(self, value: T) -> "V3[T]":
        return V3(self._t[0] + value, self._t[1] + value, self._t[2] + value)
    
    def __sub__(self, other: "V3[T]") -> "V3[T]":
        return V3(self._t[0] - other._t[0], self._t[1] - other._t[1], self._t[2] - other._t[2])
    def scalar_sub(self, value: T) -> "V3[T]":
        return V3(self._t[0] - value, self._t[1] - value, self._t[2] - value)

    def __mul__(self, other: "V3[T]") -> "V3[T]":
        return V3(self._t[0] * other._t[0], self._t[1] * other._t[1], self._t[2] * other._t[2])
    def scalar_mul(self, value: T) -> "V3[T]":
        return V3(self._t[0] * value, self._t[1] * value, self._t[2] * value)
    
    def __truediv__(self, other: "V3[T]") -> "V3[Any]":
        return V3(self._t[0] / other._t[0], self._t[1] / other._t[1], self._t[2] / other._t[2])
    def scalar_truediv(self, value: T) -> "V3[Any]":
        return V3(self._t[0] / value, self._t[1] / value, self._t[2] / value)
    
    def __floordiv__(self, other: "V3[T]") -> "V3[T]":
        return V3(self._t[0] // other._t[0], self._t[1] // other._t[1], self._t[2] // other._t[2])
    def scalar_floordiv(self, value: T) -> "V3[T]":
        return V3(self._t[0] // value, self._t[1] // value, self._t[2] // value)
    
    def __mod__(self, other: "V3[T]") -> "V3[T]":
        return V3(self._t[0] % other._t[0], self._t[1] % other._t[1], self._t[2] % other._t[2])
    def scalar_mod(self, value: T) -> "V3[T]":
        return V3(self._t[0] % value, self._t[1] % value, self._t[2] % value)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, V3):
            return self._t == other._t # type: ignore
        else:
            return super().__eq__(other)
        
    def __ne__(self, other: object) -> bool:
        if isinstance(other, V3):
            return not self.__eq__(other) # type: ignore
        else:
            return super().__ne__(other)
        
    def __gt__(self, other: object) -> bool:
        if isinstance(other, V3):
            return not self._t > other._t # type: ignore
        else:
            return False
        
    def min(self, other: "V3[T]") -> "V3[T]":
        return V3(min(self._t[0], other._t[0]), min(self._t[1], other._t[1]), min(self._t[2], other._t[2]))
    def max(self, other: "V3[T]") -> "V3[T]":
        return V3(max(self._t[0], other._t[0]), max(self._t[1], other._t[1]), max(self._t[2], other._t[2]))
    
    def __getitem__(self, idx: int) -> T:
        assert idx == 0 or idx == 1 or idx == 2, "idx out of range [0, 2]"
        return self._t[idx]

    def __int__(self) -> V3[int]:
        return V3(int(self._t[0]), int(self._t[1]), int(self._t[2]))
    def to_int(self) -> V3[int]:
        return self.__int__()
    
    def __float__(self) -> V3[float]:
        return V3(float(self._t[0]), float(self._t[1]), float(self._t[2]))
    def to_float(self) -> V3[float]:
        return self.__float__()
    
    def copy(self) -> V3[T]:
        return V3(self._t[0], self._t[1], self._t[2])

    def __str__(self) -> str:
        return "(" + str(self._t[0]) + ", " + str(self._t[1]) + ", " + str(self._t[2]) + ")"