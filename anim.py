import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def my_function(x):
    return (2 * np.sin(x) + np.sqrt(1 / x)) / (x ** 2 + 53 + np.exp(x))


def update(frame):
    global klatki_animacji, theta0, p0, x_arm, y_arm, curve, okrag, pkt_promien, x_curve_points, y_curve_points, os_x
    if is_running:
        tx_step.set_text('Czas [ms]:' + str(klatki_animacji))
        th = - klatki_animacji / 5.
        theta0 = (theta0_init + th) % (2 * np.pi)
        p0_x = p0_x_init - r0 * th
        p0 = [p0_x, my_function(p0_x) * p0_x + 0.05]  # wsp y
        okrag.center = p0
        x_arm = p0[0] + r0 * np.cos(theta0)
        y_arm = p0[1] + r0 * np.sin(theta0)
        line_arm.set_data([p0[0], x_arm], [p0[1], y_arm])

        # dodawanie punktow (czerwony)
        x_curve_points.append(x_arm)
        y_curve_points.append(y_arm)

        red_point_trajectory.append([p0[0], p0[1] - 0.05])

        if len(x_curve_points) > 1:
            curve.set_data(x_curve_points, y_curve_points)
            # linia czerwonego srodka
            red_point_trajectory_x, red_point_trajectory_y = zip(*red_point_trajectory)
            red_point_trajectory_line.set_data(red_point_trajectory_x, red_point_trajectory_y)

        pkt_promien.center = [p0[0], p0[1]]  # czerwony srodek

        klatki_animacji += 1


# wartosci poczatkowe kola i promienia
is_running = True
x_min, x_max = -0.1, 6
y_min, y_max = -0.1, 0.2
klatki_animacji = 0
num_of_points = 1000

# Zakres wartości x
x_values = np.linspace(x_min, x_max, num_of_points)
p0_x_init = 0.01
p0 = [x_min, my_function(x_min) * x_min]  # poczatkowa pozycja srodka
theta0_init = - np.pi / 2.
theta0 = theta0_init
r0 = 0.05

x_curve_points = []
y_curve_points = []
red_point_trajectory = []
# ustawienia wykresu
fig, ax1 = plt.subplots()
ax1.grid()
ax1.set_title('animacja')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_xlim(x_min, x_max)
ax1.set_ylim(y_min, y_max)
# ax1.set_aspect("equal")

# plot elements
tx_step = ax1.text(x_min, y_max * 0.9, "Czas [ms]:" + str(0))
okrag = plt.Circle(p0, r0, fill=False, color='blue')
ax1.add_patch(okrag)

x_arm = p0[0] + np.cos(theta0)
y_arm = p0[1] + np.sin(theta0)

line_arm, = ax1.plot([p0[0], x_arm], [p0[1], y_arm], color='blue')
pkt_promien = plt.Circle([p0[0], p0[1]], r0 * 0.05, color='red')  # Point marking the path
ax1.add_patch(pkt_promien)
curve, = ax1.plot(x_curve_points, y_curve_points)

red_point_trajectory_line, = ax1.plot([], [], color='red', linestyle='-', linewidth=2, label='f(x)')

ani = animation.FuncAnimation(fig, update, frames=num_of_points, interval=50, repeat=False)

ax1.legend()
plt.show()
