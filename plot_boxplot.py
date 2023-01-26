import json
import matplotlib.pyplot as plt

# To read data from file:
boxplot_data = json.load(open("Json/boxplot_data.json"))

print(boxplot_data.keys())
print(len(boxplot_data['0']))
# print(boxplot_data['0'][:50])
print(len(boxplot_data['1']))
print(len(boxplot_data['2']))
print(len(boxplot_data['3']))

fig, ax = plt.subplots()

# Creating plot
bp = ax.boxplot(boxplot_data.values())
ax.set_xticklabels(boxplot_data.keys())
ax.set_xlabel('Lane Index')
ax.set_ylabel('Number of waiting vehicles')
# ax.set_suptitle('Title')
plt.suptitle('Number of vehicles waiting at each lane with\n '
             'dynamic arrivals with peak 0.4.')
# show plot)
plt.show()