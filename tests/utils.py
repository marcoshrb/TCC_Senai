import math


def draw_line(ax, start, end, color='black'):
    x = [start[0], end[0]]
    y = [start[1], end[1]]
    z = [start[2], end[2]]
    ax.plot(x, y, z, color)
    
def draw_point(ax, point, color='black', s=100):
    ax.scatter(*point, color=color, s=s)
    
def draw_sequence_lines(ax, sequence, color='black'):
    for i in range(len(sequence) - 1):
        draw_line(ax, sequence[i], sequence[i + 1], color)
        
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

def distanceTo(point, direction, distance):
    return tuple([point[i] + direction[i] * distance for i in range(len(point))])

def landmarkToTuple(landmark):
    return (landmark.x, landmark.y, landmark.z)