import math


def center(points):
    length = len(points)
    dimensions = len(points[0])
    
    center = [0] * dimensions

    for point in points:
        for i in range(dimensions):
            center[i] += point[i]

    return tuple([c / length for c in center]) 

def direction(a, b):
    dir = [a[i] - b[i] for i in range(len(a))]
    length = math.sqrt(sum([d ** 2 for d in dir]))
    if length == 0:
        return [0] * len(dir)
    return tuple([dir[i] / length for i in range(len(dir))])

def distance(a, b):
    sumd = sum([(a[i] - b[i]) ** 2 for i in range(len(a))])
    return math.sqrt(sumd)

def normalize(value, min, max):
    return (value - min) / (max - min)

def rescale(value, originalscale, targetscale):
    return targetscale[0] + (normalize(value, originalscale[0], originalscale[1]) * (targetscale[1] - targetscale[0]))

def landmarkToTuple(landmark):
    return (landmark.x, landmark.y, landmark.z)