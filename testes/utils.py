def draw_line(ax, start, end, color='black'):
    x = [start[0], end[0]]
    y = [start[1], end[1]]
    z = [start[2], end[2]]
    ax.plot(x, y, z, color)
    
def draw_point(ax, point, color='black', s=100):
    ax.scatter(*point, color, s)
    
def draw_sequence_lines(ax, sequence, color='black'):
    for i in range(len(sequence) - 1):
        draw_line(ax, sequence[i], sequence[i + 1], color)