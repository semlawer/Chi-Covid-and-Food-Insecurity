import seaborn as sns
import matplotlib.pyplot as plt # plt.show() shows the plots
sns.set()
# Data for the plots
height = [62, 64, 69, 75, 66, 68, 65, 71, 76, 73]
weight = [120, 136, 148, 175, 137, 165, 154, 172, 200, 187]
animal_counts = [1,4,5,6]
animals = ["Cat", "Dog", "Fish", "Bird"]

# Create the axes and figure
f, axes = plt.subplots(1, 2) # Has space for two plots 1*2

# Create the scatterplots. Assign the ax keyword argument to a
# Axis object from the axes lists
sns.scatterplot(x=height, y=weight, ax=axes[0])
sns.scatterplot(x=animals, y=animal_counts, ax= axes[1])

axes[0].set_title("Weight Height Plot")
axes[0].set_ylabel("Weight")
axes[0].set_xlabel("Height")

axes[1].set_title("Animal Plot")
axes[1].set_ylabel("Counts")
axes[1].set_xlabel("Animal")

f.suptitle("My ScatterPlots")

plt.savefig("scatterplots.svg")
#splt.show()
