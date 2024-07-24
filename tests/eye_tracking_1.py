import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from utils import center, direction, distance, distanceTo, draw_line, draw_point, draw_sequence_lines

face_left   = (0.5789413452148438, 0.38011884689331055, 0.1471441388130188)
face_center = (0.45492228865623474, 0.3015148937702179, -0.03611652925610542)
face_right  = (0.28919851779937744, 0.3820362389087677, 0.10921341925859451)
left_eye_1  = (0.5121340155601501, 0.34886354207992554, 0.006470124237239361)
left_eye_2  = (0.5091149806976318, 0.3724062740802765, 0.009929264895617962)
left_eye_3  = (0.5331736207008362, 0.35120952129364014, 0.013162153773009777)
left_eye_4  = (0.5297144055366516, 0.37355637550354004, 0.01645396091043949)
left_eye_5  = (0.4897236227989197, 0.3660852611064911, 0.01213004719465971)
left_eye_6  = (0.5446235537528992, 0.3627241551876068, 0.030554475262761116)
right_eye_1 = (0.3612024188041687, 0.35077184438705444, -0.006898714229464531)
right_eye_2 = (0.36593154072761536, 0.3737955391407013, -0.0030721137300133705)
right_eye_3 = (0.3846029043197632, 0.34944987297058105, -0.008740615099668503)
right_eye_4 = (0.38933444023132324, 0.37200239300727844, -0.004818103276193142)
right_eye_5 = (0.3469381034374237, 0.3628503680229187, 0.007368059828877449)
right_eye_6 = (0.4103745222091675, 0.3665928542613983, 0.0015839249826967716)
left_pupil  = (0.5204094052314758, 0.35966262221336365, 0.01501416601240635)
right_pupil = (0.37390753626823425, 0.359592467546463, -0.0021094230469316244)

face = [face_left, face_center, face_right]
left_eye = [left_eye_1, left_eye_2, left_eye_3, left_eye_4, left_eye_5, left_eye_6]
right_eye = [right_eye_1, right_eye_2, right_eye_3, right_eye_4, right_eye_5, right_eye_6]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.grid(False)

draw_sequence_lines(ax, face)
for point in left_eye + right_eye:
    draw_point(ax, point, 'red')
draw_point(ax, left_pupil)
draw_point(ax, right_pupil)

vision_distance = 0.1

left_eye_center = center(left_eye)
left_eye_direction = direction(left_pupil, left_eye_center)
left_vision = distanceTo(left_pupil, left_eye_direction, vision_distance)
draw_point(ax, left_eye_center, 'blue')
draw_line(ax, left_pupil, left_vision, 'green')

right_eye_center = center(right_eye)
right_eye_direction = direction(right_pupil, right_eye_center)
right_vision = distanceTo(right_pupil, right_eye_direction, vision_distance)
draw_point(ax, right_eye_center, 'blue')
draw_line(ax, right_pupil, right_vision, 'green')

eyes_center = center(left_eye + right_eye)
vision_direction = center([left_eye_direction, right_eye_direction])
vision = distanceTo(eyes_center, vision_direction, vision_distance)
draw_line(ax, eyes_center, vision, 'pink')

ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.show()