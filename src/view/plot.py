import os

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

file_path = os.path.abspath('src/data/data.json')


def plot_data():
    data = pd.read_json(file_path)

    df = data.explode(['x', 'y'])

    g = sns.relplot(kind='line', data=df, x='x', y='y', hue='name', marker='.')

    plt.show()
