import math

# 一次関数
def linear(t):
    return t

# 二次関数
def quadIn(t):
    return t * t
def quadOut(t):
    return -t * (t - 2)
def quadInOut(t):
    if t <= 0.5:
        return t * t * 2
    else:
        return 1 - (t - 1) * (t - 1) * 2

# 三次関数
def cubeIn(t):
    return t * t * t
def cubeOut(t):
    return 1 + (t - 1) * (t - 1) * (t - 1)
def cubeInOut(t):
    if t <= 0.5:
        return t * t * t * 4
    else :
        return 1 + (t - 1) * (t - 1) * (t - 1) * 4

# 四次関数
def quartIn(t):
    return t * t * t * t
def quartOut(t):
    return 1 - (t - 1) * (t - 1) * (t - 1) * (t - 1)
def quartInOut(t):
    if t <= 0.5:
        return t * t * t * t * 8
    else:
        t = t * 2 - 2
        return (1 - t * t * t * t) / 2 + 0.5

# 五次関数
def quintIn(t):
    return t * t * t * t * t	
def quintOut(t):
    t = t - 1
    return t * t * t * t * t + 1
def quintInOut(t):
    t *= 2
    if (t < 1):
        return (t * t * t * t * t) / 2
    else:
        t -= 2
        return (t * t * t * t * t + 2) / 2

# スムーズ曲線
def smoothStepIn(t):
    return 2 * smoothStepInOut(t / 2)
def smoothStepOut(t):
    return 2 * smoothStepInOut(t / 2 + 0.5) - 1
def smoothStepInOut(t):
    return t * t * (t * -2 + 3)
	
# よりスムーズな曲線
def smootherStepIn(t):
    return 2 * smootherStepInOut(t / 2)
def smootherStepOut(t):
    return 2 * smootherStepInOut(t / 2 + 0.5) - 1
def smootherStepInOut(t):
    return t * t * t * (t * (t * 6 - 15) + 10)
	
# SIN関数(0〜90度)
def sineIn(t):
    return -math.cos(math.pi/2 * t) + 1
def sineOut(t):
    return math.sin(math.pi/2 * t)
def sineInOut(t):
    return -math.cos(math.pi * t) / 2 + .5

# バウンス関数	
def bounceIn(t):
    B1 = 1 / 2.75
    B2 = 2 / 2.75
    B3 = 1.5 / 2.75
    B4 = 2.5 / 2.75
    B5 = 2.25 / 2.75
    B6 = 2.625 / 2.75
    t = 1 - t
    if (t < B1): return 1 - 7.5625 * t * t
    if (t < B2): return 1 - (7.5625 * (t - B3) * (t - B3) + .75)
    if (t < B4): return 1 - (7.5625 * (t - B5) * (t - B5) + .9375)
    
    return 1 - (7.5625 * (t - B6) * (t - B6) + .984375)

def bounceOut(t):
    B1 = 1 / 2.75
    B2 = 2 / 2.75
    B3 = 1.5 / 2.75
    B4 = 2.5 / 2.75
    B5 = 2.25 / 2.75
    B6 = 2.625 / 2.75
    if (t < B1): return 7.5625 * t * t
    if (t < B2): return 7.5625 * (t - B3) * (t - B3) + .75
    if (t < B4): return 7.5625 * (t - B5) * (t - B5) + .9375
    
    return 7.5625 * (t - B6) * (t - B6) + .984375

def bounceInOut(t):
    B1 = 1 / 2.75
    B2 = 2 / 2.75
    B3 = 1.5 / 2.75
    B4 = 2.5 / 2.75
    B5 = 2.25 / 2.75
    B6 = 2.625 / 2.75
    if (t < .5):
        t = 1 - t * 2
        if (t < B1): return (1 - 7.5625 * t * t) / 2
        if (t < B2): return (1 - (7.5625 * (t - B3) * (t - B3) + .75)) / 2
        if (t < B4): return (1 - (7.5625 * (t - B5) * (t - B5) + .9375)) / 2

        return (1 - (7.5625 * (t - B6) * (t - B6) + .984375)) / 2
    else:
        t = t * 2 - 1
        if (t < B1): return (7.5625 * t * t) / 2 + .5
        if (t < B2): return (7.5625 * (t - B3) * (t - B3) + .75) / 2 + .5
        if (t < B4): return (7.5625 * (t - B5) * (t - B5) + .9375) / 2 + .5

        return (7.5625 * (t - B6) * (t - B6) + .984375) / 2 + .5

# 円	
def circIn(t):
    return -(math.sqrt(1 - t * t) - 1)
def circOut(t):
    return math.sqrt(1 - (t - 1) * (t - 1))
def circInOut(t):
    if t <= .5:
        return (math.sqrt(1 - t * t * 4) - 1) / -2
    else:
        return (math.sqrt(1 - (t * 2 - 2) * (t * 2 - 2)) + 1) / 2

# 指数関数
def expoIn(t):
    return math.pow(2, 10 * (t - 1))
def expoOut(t):
    return -math.pow(2, -10*t) + 1
def expoInOut(t):
    if t < .5:
        return math.pow(2, 10 * (t * 2 - 1)) / 2
    else:
        return (-math.pow(2, -10 * (t * 2 - 1)) + 2) / 2

# バック
def backIn(t):
    return t * t * (2.70158 * t - 1.70158)
def backOut(t):
    return 1 - (t - 1) * (t-1) * (-2.70158 * (t-1) - 1.70158)
def backInOut(t):
    t *= 2
    if (t < 1):
        return t * t * (2.70158 * t - 1.70158) / 2
    else:
        t -= 1
        return (1 - (t - 1) * (t - 1) * (-2.70158 * (t - 1) - 1.70158)) / 2 + .5

# 弾力関数
def elasticIn(t):
    ELASTIC_AMPLITUDE = 1
    ELASTIC_PERIOD = 0.4
    t -= 1
    return -(ELASTIC_AMPLITUDE * math.pow(2, 10 * t) * math.sin( (t - (ELASTIC_PERIOD / (2 * math.pi) * math.asin(1 / ELASTIC_AMPLITUDE))) * (2 * math.pi) / ELASTIC_PERIOD))
def elasticOut(t):
    ELASTIC_AMPLITUDE = 1
    ELASTIC_PERIOD = 0.4
    return (ELASTIC_AMPLITUDE * math.pow(2, -10 * t) * math.sin((t - (ELASTIC_PERIOD / (2 * math.pi) * math.asin(1 / ELASTIC_AMPLITUDE))) * (2 * math.pi) / ELASTIC_PERIOD) + 1)
def elasticInOut(t):
    #ELASTIC_AMPLITUDE = 1
    ELASTIC_PERIOD = 0.4
    if (t < 0.5):
        t -= 0.5
        return -0.5 * (math.pow(2, 10 * t) * math.sin((t - (ELASTIC_PERIOD / 4)) * (2 * math.pi) / ELASTIC_PERIOD))
    else:
        t -= 0.5
        return math.pow(2, -10 * t) * math.sin((t - (ELASTIC_PERIOD / 4)) * (2 * math.pi) / ELASTIC_PERIOD) * 0.5 + 1
