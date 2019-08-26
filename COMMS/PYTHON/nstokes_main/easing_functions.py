import math

def easelist():
    return [0.0, 0.050000000000000003, 0.10000000000000001, 0.15000000000000002, 0.20000000000000001, 0.25, 0.30000000000000004, 0.35000000000000003, 0.40000000000000002, 0.45000000000000001, 0.5, 0.55000000000000004, 0.60000000000000009, 0.65000000000000002, 0.70000000000000007, 0.75, 0.80000000000000004, 0.85000000000000009, 0.90000000000000002, 0.95000000000000007, 1.0, 1.05, 1.1000000000000001, 1.1500000000000001, 1.2000000000000002, 1.25, 1.3, 1.3500000000000001, 1.4000000000000001, 1.4500000000000002, 1.5, 1.55, 1.6000000000000001, 1.6500000000000001, 1.7000000000000002, 1.75, 1.8, 1.8500000000000001, 1.9000000000000001, 1.9500000000000002, 2.0, 2.0500000000000003, 2.1000000000000001, 2.1499999999999999, 2.2000000000000002, 2.25, 2.3000000000000003, 2.3500000000000001, 2.4000000000000004, 2.4500000000000002, 2.5, 2.5500000000000003, 2.6000000000000001, 2.6500000000000004, 2.7000000000000002, 2.75, 2.8000000000000003, 2.8500000000000001, 2.9000000000000004, 2.9500000000000002, 3.0, 3.0500000000000003, 3.1000000000000001, 3.1500000000000004, 3.2000000000000002, 3.25, 3.3000000000000003, 3.3500000000000001, 3.4000000000000004, 3.4500000000000002, 3.5, 3.5500000000000003, 3.6000000000000001, 3.6500000000000004, 3.7000000000000002, 3.75, 3.8000000000000003, 3.8500000000000001, 3.9000000000000004, 3.9500000000000002, 4.0, 4.0499999999999998, 4.1000000000000005, 4.1500000000000004, 4.2000000000000002, 4.25, 4.2999999999999998, 4.3500000000000005, 4.4000000000000004, 4.4500000000000002, 4.5, 4.5499999999999998, 4.6000000000000005, 4.6500000000000004, 4.7000000000000002, 4.75, 4.8000000000000007, 4.8500000000000005, 4.9000000000000004, 4.9500000000000002, 5.0, 5.0500000000000007, 5.1000000000000005, 5.1500000000000004, 5.2000000000000002, 5.25, 5.3000000000000007, 5.3500000000000005, 5.4000000000000004, 5.4500000000000002, 5.5, 5.5500000000000007, 5.6000000000000005, 5.6500000000000004, 5.7000000000000002, 5.75, 5.8000000000000007, 5.8500000000000005, 5.9000000000000004, 5.9500000000000002, 6.0, 6.0500000000000007, 6.1000000000000005, 6.1500000000000004, 6.2000000000000002, 6.25, 6.3000000000000007, 6.3500000000000005, 6.4000000000000004, 6.4500000000000002, 6.5, 6.5500000000000007, 6.6000000000000005, 6.6500000000000004, 6.7000000000000002, 6.75, 6.8000000000000007, 6.8500000000000005, 6.9000000000000004, 6.9500000000000002, 7.0, 7.0500000000000007, 7.1000000000000005, 7.1500000000000004, 7.2000000000000002, 7.25, 7.3000000000000007, 7.3500000000000005, 7.4000000000000004, 7.4500000000000002, 7.5, 7.5500000000000007, 7.6000000000000005, 7.6500000000000004, 7.7000000000000002, 7.75, 7.8000000000000007, 7.8500000000000005, 7.9000000000000004, 7.9500000000000002, 8.0, 8.0500000000000007, 8.0999999999999996, 8.1500000000000004, 8.2000000000000011, 8.25, 8.3000000000000007, 8.3499999999999996, 8.4000000000000004, 8.4500000000000011, 8.5, 8.5500000000000007, 8.5999999999999996, 8.6500000000000004, 8.7000000000000011, 8.75, 8.8000000000000007, 8.8499999999999996, 8.9000000000000004, 8.9500000000000011, 9.0, 9.0500000000000007, 9.0999999999999996, 9.1500000000000004, 9.2000000000000011, 9.25, 9.3000000000000007, 9.3499999999999996, 9.4000000000000004, 9.4500000000000011, 9.5, 9.5500000000000007, 9.6000000000000014, 9.6500000000000004, 9.7000000000000011, 9.75, 9.8000000000000007, 9.8500000000000014, 9.9000000000000004, 9.9500000000000011, 10.0, 10.050000000000001, 10.100000000000001, 10.15, 10.200000000000001, 10.25, 10.300000000000001, 10.350000000000001, 10.4, 10.450000000000001, 10.5, 10.550000000000001, 10.600000000000001, 10.65, 10.700000000000001, 10.75, 10.800000000000001, 10.850000000000001, 10.9, 10.950000000000001, 11.0, 11.050000000000001, 11.100000000000001, 11.15, 11.200000000000001, 11.25, 11.300000000000001, 11.350000000000001, 11.4, 11.450000000000001, 11.5, 11.550000000000001, 11.600000000000001, 11.65, 11.700000000000001, 11.75, 11.800000000000001, 11.850000000000001, 11.9, 11.950000000000001, 12.0, 12.050000000000001, 12.100000000000001, 12.15, 12.200000000000001, 12.25, 12.300000000000001, 12.350000000000001, 12.4, 12.450000000000001, 12.5, 12.550000000000001, 12.600000000000001, 12.65, 12.700000000000001, 12.75, 12.800000000000001, 12.850000000000001, 12.9, 12.950000000000001, 13.0, 13.050000000000001, 13.100000000000001, 13.15, 13.200000000000001, 13.25, 13.300000000000001, 13.350000000000001, 13.4, 13.450000000000001, 13.5, 13.550000000000001, 13.600000000000001, 13.65, 13.700000000000001, 13.75, 13.800000000000001, 13.850000000000001, 13.9, 13.950000000000001, 14.0, 14.050000000000001, 14.100000000000001, 14.15, 14.200000000000001, 14.25, 14.300000000000001, 14.350000000000001, 14.4, 14.450000000000001, 14.5, 14.550000000000001, 14.600000000000001, 14.65, 14.700000000000001, 14.75, 14.800000000000001, 14.850000000000001, 14.9, 14.950000000000001]

class EasingBase:
    limit = (0, 1)

    def __init__(self, start=0, end=1, duration=1):
        self.start = start
        self.end = end
        self.duration = duration

    @classmethod
    def func(cls, t):
        raise NotImplementedError

    def ease(self, alpha):
        t = self.limit[0] * (1 - alpha) + self.limit[1] * alpha
        t /= self.duration
        a = self.func(t)
        return self.end * a + self.start * (1 - a)


"""
Quadratic easing functions
"""


class QuadEaseInOut(EasingBase):
    def func(self, t):
        if t < 0.5:
            return 2 * t * t
        return (-2 * t * t) + (4 * t) - 1


class QuadEaseIn(EasingBase):
    def func(self, t):
        return t * t


class QuadEaseOut(EasingBase):
    def func(self, t):
        return -(t * (t - 2))


"""
Cubic easing functions
"""


class CubicEaseIn(EasingBase):
    def func(self, t):
        return t * t * t


class CubicEaseOut(EasingBase):
    def func(self, t):
        return (t - 1) * (t - 1) * (t - 1) + 1


class CubicEaseInOut(EasingBase):
    def func(self, t):
        if t < 0.5:
            return 4 * t * t * t
        p = 2 * t - 2
        return 0.5 * p * p * p + 1


"""
Quartic easing functions
"""


class QuarticEaseIn(EasingBase):
    def func(self, t):
        return t * t * t * t


class QuarticEaseOut(EasingBase):
    def func(self, t):
        return (t - 1) * (t - 1) * (t - 1) * (1 - t) + 1


class QuarticEaseInOut(EasingBase):
    def func(self, t):
        if t < 0.5:
            return 8 * t * t * t * t
        p = t - 1
        return -8 * p * p * p * p + 1


"""
Quintic easing functions
"""


class QuinticEaseIn(EasingBase):
    def func(self, t):
        return t * t * t * t * t


class QuinticEaseOut(EasingBase):
    def func(self, t):
        return (t - 1) * (t - 1) * (t - 1) * (t - 1) * (t - 1) + 1


class QuinticEaseInOut(EasingBase):
    def func(self, t):
        if t < 0.5:
            return 16 * t * t * t * t * t
        p = (2 * t) - 2
        return 0.5 * p * p * p * p * p + 1


"""
Sine easing functions
"""


class SineEaseIn(EasingBase):
    def func(self, t):
        return math.sin((t - 1) * math.pi / 2) + 1


class SineEaseOut(EasingBase):
    def func(self, t):
        return math.sin(t * math.pi / 2)


class SineEaseInOut(EasingBase):
    def func(self, t):
        return 0.5 * (1 - math.cos(t * math.pi))


"""
Circular easing functions
"""


class CircularEaseIn(EasingBase):
    def func(self, t):
        return 1 - math.sqrt(1 - (t * t))


class CircularEaseOut(EasingBase):
    def func(self, t):
        return math.sqrt((2 - t) * t)


class CircularEaseInOut(EasingBase):
    def func(self, t):
        if t < 0.5:
            return 0.5 * (1 - math.sqrt(1 - 4 * (t * t)))
        return 0.5 * (math.sqrt(-((2 * t) - 3) * ((2 * t) - 1)) + 1)


"""
Exponential easing functions
"""


class ExponentialEaseIn(EasingBase):
    def func(self, t):
        if t == 0:
            return 0
        return math.pow(2, 10 * (t - 1))


class ExponentialEaseOut(EasingBase):
    def func(self, t):
        if t == 1:
            return 1
        return 1 - math.pow(2, -10 * t)


class ExponentialEaseInOut(EasingBase):
    def func(self, t):
        if t == 0 or t == 1:
            return t

        if t < 0.5:
            return 0.5 * math.pow(2, (20 * t) - 10)
        return -0.5 * math.pow(2, (-20 * t) + 10) + 1


"""
Elastic Easing Functions
"""


class ElasticEaseIn(EasingBase):
    def func(self, t):
        return math.sin(13 * math.pi / 2 * t) * math.pow(2, 10 * (t - 1))


class ElasticEaseOut(EasingBase):
    def func(self, t):
        return math.sin(-13 * math.pi / 2 * (t + 1)) * math.pow(2, -10 * t) + 1


class ElasticEaseInOut(EasingBase):
    def func(self, t):
        if t < 0.5:
            return (
                0.5
                * math.sin(13 * math.pi / 2 * (2 * t))
                * math.pow(2, 10 * ((2 * t) - 1))
            )
        return 0.5 * (
            math.sin(-13 * math.pi / 2 * ((2 * t - 1) + 1))
            * math.pow(2, -10 * (2 * t - 1))
            + 2
        )


"""
Back Easing Functions
"""


class BackEaseIn(EasingBase):
    def func(self, t):
        return t * t * t - t * math.sin(t * math.pi)


class BackEaseOut(EasingBase):
    def func(self, t):
        p = 1 - t
        return 1 - (p * p * p - p * math.sin(p * math.pi))


class BackEaseInOut(EasingBase):
    def func(self, t):
        if t < 0.5:
            p = 2 * t
            return 0.5 * (p * p * p - p * math.sin(p * math.pi))

        p = 1 - (2 * t - 1)

        return 0.5 * (1 - (p * p * p - p * math.sin(p * math.pi))) + 0.5


"""
Bounce Easing Functions
"""


class BounceEaseIn(EasingBase):
    def func(self, t):
        return 1 - BounceEaseOut().func(1 - t)


class BounceEaseOut(EasingBase):
    def func(self, t):
        if t < 4 / 11:
            return 121 * t * t / 16
        elif t < 8 / 11:
            return (363 / 40.0 * t * t) - (99 / 10.0 * t) + 17 / 5.0
        elif t < 9 / 10:
            return (4356 / 361.0 * t * t) - (35442 / 1805.0 * t) + 16061 / 1805.0
        return (54 / 5.0 * t * t) - (513 / 25.0 * t) + 268 / 25.0


class BounceEaseInOut(EasingBase):
    def func(self, t):
        if t < 0.5:
            return 0.5 * BounceEaseIn().func(t * 2)
        return 0.5 * BounceEaseOut().func(t * 2 - 1) + 0.5
