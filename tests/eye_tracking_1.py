import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from utils import draw_line, draw_point, draw_sequence_lines

face_left   = (0.6694955825805664,  0.361983060836792,      0.09792782366275787)
face_center = (0.6144697070121765,  0.33753475546836853,    -0.031630001962184906)
face_right  = (0.492043673992157,   0.36959004402160645,    0.04289006441831589)
left_eye_1  = (0.6406434178352356,  0.3604418635368347,     0.004836307838559151)
left_eye_2  = (0.6391898989677429,  0.3729094862937927,     0.00774157652631402)
left_eye_3  = (0.6527047753334045,  0.3598087728023529,     0.011264350265264511)
left_eye_4  = (0.6509537696838379,  0.3716781735420227,     0.013929076492786407)
left_eye_5  = (0.6289421319961548,  0.3701968789100647,     0.006444016937166452)
left_eye_6  = (0.6580685973167419,  0.3640631437301636,     0.023414332419633865)
right_eye_1 = (0.5559569001197815,  0.3635804057121277,     -0.019560417160391808)
right_eye_2 = (0.5597713589668274,  0.37535330653190613,    -0.016010621562600136)
right_eye_3 = (0.5691121220588684,  0.3621540069580078,     -0.018439121544361115)
right_eye_4 = (0.5730513334274292,  0.3741667866706848,     -0.014864765107631683)
right_eye_5 = (0.5467172265052795,  0.3684508800506592,     -0.012340568006038666)
right_eye_6 = (0.5836833119392395,  0.370613157749176,      -0.009705213829874992)
left_pupil  = (0.5620282888412476,  0.3672904968261719,     -0.01492978073656559)
right_pupil = (0.6461473107337952,  0.36536380648612976,    0.01136911753565073)

face = [face_left, face_center, face_right]
left_eye = [left_eye_1, left_eye_2, left_eye_3, left_eye_4, left_eye_5, left_eye_6]
right_eye = [right_eye_1, right_eye_2, right_eye_3, right_eye_4, right_eye_5, right_eye_6]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.grid(False)

draw_sequence_lines(ax, face)
for point in left_eye:
    draw_point(ax, point)
for point in right_eye:
    draw_point(ax, point)
draw_point(ax, left_pupil)
draw_point(ax, right_eye)

ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.show()