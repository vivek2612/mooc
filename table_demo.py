"""
Demo of table function to display a table within a plot.
"""
import numpy as np
import matplotlib.pyplot as plt


data = [[  66386,  174296,   75131,  577908,   32015],
        [  58230,  381139,   78045,   99308,  160454],
        [  89135,   80552,  152558,  497981,  603535],
        [  78415,   81858,  150656,  193263,   69638],
        [ 139361,  331509,  343164,  781380,   52269]]

data = [[  3.        ,   3.        ,   3.1       ,   2.21276596,
          2.37837838,   2.77777778,   2.        ,   2.42857143,   2.        ],
       [  0.375     ,   0.        ,   0.4       ,   0.08510638,
          0.05405405,   0.22222222,   0.        ,   0.14285714,   0.        ],
       [  0.46875   ,   0.625     ,   0.575     ,   0.38297872,
          0.43243243,   0.59259259,   0.28571429,   0.42857143,   0.        ],
       [ 11.84375   ,   8.625     ,  14.175     ,  10.12765957,
         12.32432432,  10.40740741,   7.28571429,  11.14285714,   5.        ],
       [  1.53125   ,   0.75      ,   1.8       ,   0.80851064,
          0.59459459,   0.55555556,   0.14285714,   0.85714286,   0.        ]]


# columns = ('Freeze', 'Wind', 'Flood', 'Quake', 'Hail')
columns = ['AA', 'FR', 'AB', 'BB', 'BC', 'CC', 'DD', 'CD', 'AU']

rows = ['cluster %d ' % x for x in range(1,6)]

values = np.arange(0, 2500, 500)
value_increment = 1000

# Get some pastel shades for the colors
colors = plt.cm.BuPu(np.linspace(0, 0.5, len(columns)))
n_rows = len(data)

index = np.arange(len(columns)) + 0.3
bar_width = 0.4

# Initialize the vertical-offset for the stacked bar chart.
y_offset = np.array([0.0] * len(columns))

# Plot bars and create text labels for the table
cell_text = []
for row in range(n_rows):
    plt.bar(index, data[row], bar_width, bottom=y_offset, color=colors[row])
    y_offset = y_offset + data[row]
    print y_offset
    cell_text.append(['%1.2f' % x for x in y_offset])
# Reverse colors and text labels to display the last value at the top.
colors = colors[::-1]
cell_text.reverse()

# Add a table at the bottom of the axes
the_table = plt.table(cellText=cell_text,
                      rowLabels=rows,
                      rowColours=colors,
                      colLabels=columns,
                      loc='bottom')

# Adjust layout to make room for the table:
plt.subplots_adjust(left=0.2, bottom=0.2)

plt.ylabel("Avearge # sessions")
# plt.yticks(values * value_increment, ['%d' % val for val in values])
plt.xticks([])
plt.title('Analyzing different users')

plt.show()
