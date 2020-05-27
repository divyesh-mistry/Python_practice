import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0.0, 4.0*np.pi, 100, endpoint=True)
y = np.sin(x)

plt.figure(figsize=(10,10))

plt.plot(x, y, 'b-', label=r'$sin(x)$', linewidth=4.0)

plt.xlabel(r'$x$', fontsize=24)
plt.ylabel(r'$y$', fontsize=24)

plt.xticks([0.0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi, 5*np.pi/2, 3*np.pi, 7*np.pi/2, 4.0*np.pi], [r'$0$', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$', r'$\frac{5\pi}{2}$', r'$3\pi$', r'$\frac{7\pi}{2}$', r'$4\pi$'])
plt.yticks([-1.0, -0.5, 0.0, 0.5, 1.0])

plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

plt.legend(loc='best', fontsize=20)
plt.grid()

plt.savefig('sine.pdf')
