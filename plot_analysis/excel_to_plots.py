"""
Basics for excel to plots
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel (os.path.join("reports", "mer_results.xlsx"))
# df = pd.read_excel("mer_results.xlsx")

x, y, z = df['x'], df['y'], df['z']
v1, v2, v3 =df['y'], df['z'], df['x']

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# ax = plt.axes(projection='3d')

# ax.plot3D(x, y, z, 'green')
# ax.plot3D(v1, v2, v3, 'blue')
ax.plot3D(x, y, z, 'green', label='svf_data_path')

ax.set_title('Site Vector Frame Data Analysis (Path traced by MER2)')
ax.set_xlabel('$X$')
ax.set_ylabel('$Y$')
ax.set_zlabel('$Z$')

ax.legend(loc='upper left')
plt.savefig('reports\mer_result_plot_2021-11-01-18-16-21.png', format='png', dpi=1080)
plt.show()