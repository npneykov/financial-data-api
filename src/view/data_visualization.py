import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from src.data.constants import (
    DATA_FILE_PATH,
    EXCH_FILE_PATH,
    FINA_FILE_PATH,
)


class DataVisualization:
    def __init__(self):
        pass

    def plot_data(self, file_path):
        if file_path == DATA_FILE_PATH:
            data = pd.read_json(DATA_FILE_PATH)
            df = data.explode(['x', 'y'])

            g = sns.relplot(kind='line', data=df, x='x', y='y', hue='name', marker='.')

            plt.show()

        elif file_path == EXCH_FILE_PATH:
            exchange_data = pd.read_json(EXCH_FILE_PATH)
            df = pd.json_normalize(exchange_data['results'])
            df.plot()
            plt.show()

        financial_data = pd.read_json(FINA_FILE_PATH)
        df_financials = pd.json_normalize(financial_data['results'])
        print(df_financials)
