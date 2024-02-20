import os

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from src.data.settings import AGG_FILE_PATH, EXCH_FILE_PATH

file_path = os.path.abspath('src/data/data.json')


class ViewData:
    def __init__(self):
        pass

    def plot_data(self, file_path):
        data = pd.read_json(file_path)

        df = data.explode(['x', 'y'])

        g = sns.relplot(kind='line', data=df, x='x', y='y', hue='name', marker='.')

        plt.show()
