# If you do not want to use the functions of the package but only use the package style,
# simply import the package at the beginning of your notebook/script
import matplotlib.pyplot as plt
import plothist

x = [1, 2, 3, 4, 5]

fig, ax = plt.subplots()

ax.plot(x, [i ** 2 for i in x], ".", label="$y=x^2$")
ax.plot(x, [i ** 3 for i in x], ".", label="$y=x^3$")

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()

plt.show()
