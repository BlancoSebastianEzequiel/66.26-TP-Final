import json
import os
import pandas as pd
from subprocess import call
import matplotlib.pyplot as plt


class OutputData:
    def __init__(self):
        self.data = {
            'number_of_threads': [],
            'parallel_median_time': [],
            'parallel_error': [],
            'serial_median_time': [],
            'serial_error': [],
            'matrix_dimension': []
        }
        self._colors = ['b-', 'g-', 'r-', 'c-', 'm-', 'y-', 'k-', 'w-']
        self.dfs_data = []
        self.pics_path = './docs/report/pics/'
        self.files_path = './src/data/'

    def add_data(self, serial, parallel, num_workers, matrix_dimension):
        self.data['number_of_threads'].append(num_workers)
        self.data['parallel_median_time'].append(parallel.get_mean())
        self.data['parallel_error'].append(parallel.get_error())
        self.data['serial_median_time'].append(serial.get_mean())
        self.data['serial_error'].append(serial.get_error())
        self.data['matrix_dimension'].append(matrix_dimension)

    @staticmethod
    def gustafson_speed_up(a, b, p):
        return (a + p * b) / (a + b)

    @staticmethod
    def amdahl_speed_up(s, p, n):
        return (s + p) / (s + p/n)

    @staticmethod
    def amdahl_max_speed_up(s, p):
        return 1 + p/s

    def save_data(self, df_name):
        df = pd.DataFrame(data=self.data)
        self.save_df_data(df, [], '', {}, df_name, False)

    def save_df_in_image(self, df, df_name):
        path = self.pics_path + df_name
        df.to_html('table.html')
        command = f'wkhtmltoimage -f png --width 0 table.html {path}'
        call(command, shell=True)
        call('rm table.html', shell=True)

    def df_to_csv(self, df, df_name):
        path = self.files_path + df_name
        df.to_csv(path, index=False, sep=',', encoding='utf-8-sig')

    def graph_amdahl_speed_up(self, filename):
        df = pd.DataFrame(data=self.data)
        columns = [
            'number_of_threads',
            'parallel_median_time',
            'serial_median_time'
        ]
        df = df.loc[:, columns]
        df['theoretical_speed_up'] = [0]*len(df.index)
        df['theoretical_speed_up'] = df.apply(
            lambda x: self.amdahl_speed_up(
                self.data['serial_median_time'][0],
                self.data['parallel_median_time'][0],
                x['number_of_threads']
            ),
            axis=1
        )
        df['real_speed_up'] = [0]*len(df.index)
        df['real_speed_up'] = df.apply(
            lambda x: self.amdahl_speed_up(
                x['serial_median_time'],
                x['parallel_median_time'],
                x['number_of_threads']
            ),
            axis=1
        )

        df['max_speed_up'] = [0] * len(df.index)
        df['max_speed_up'] = df.apply(
            lambda x: self.amdahl_max_speed_up(
                x['serial_median_time'],
                x['parallel_median_time']
            ),
            axis=1
        )

        columns = [
            'number_of_threads',
            'theoretical_speed_up',
            'real_speed_up',
            'max_speed_up'
        ]
        df = df.loc[:, columns]
        self.save_df_data(
            df,
            ['theoretical_speed_up', 'real_speed_up', 'max_speed_up'],
            'number_of_threads',
            {
                'theoretical_speed_up': 'b-',
                'real_speed_up': 'r-',
                'max_speed_up': 'g-'
            },
            filename,
            True
        )

    def graph(self, df, y_axis, x_axis, colors, graph_name):
        for field in y_axis:
            plt.plot(df[x_axis], df[field], colors[field], label=field)
        plt.xlabel(x_axis)
        plt.legend(loc='best')
        plt.savefig(self.pics_path + graph_name)
        plt.clf()

    @staticmethod
    def file_exists(path):
        return os.path.isfile(path) and os.access(path, os.R_OK)

    @classmethod
    def delete_all_data(cls):
        os.system('rm -rf src/data/*')

    def save_df_data_to_json(self):
        path = 'src/data/data.json'
        data = []
        if self.file_exists(path):
            with open('src/data/data.json', encoding='utf-8-sig') as json_file:
                text = json_file.read()
                if text:
                    data = json.loads(text)
        with open('src/data/data.json', 'w') as f:
            json.dump(self.dfs_data+data, f)

    def save_df_data(self, df, y_axis, x_axis, colors, graph_name, has_graph):
        df_graph_name = graph_name.split('.png')[0] + '_table.csv'
        self.df_to_csv(df, df_graph_name)
        self.dfs_data.append({
            'has_graph': has_graph,
            'df_path_name': df_graph_name,
            'y_axis': y_axis,
            'x_axis': x_axis,
            'colors': colors,
            'graph_name': graph_name
        })

    def read_dfs_data_from_json(self):
        with open('src/data/data.json', encoding='utf-8-sig') as json_file:
            text = json_file.read()
            self.dfs_data = json.loads(text)

    def graph_dfs(self):
        for df_data in self.dfs_data:
            df_name = df_data['df_path_name']
            table_graph_name = df_name.split('.csv')[0] + '.png'
            df_path_name = self.files_path + df_name
            df = pd.read_csv(df_path_name, low_memory=False, sep=',')
            self.save_df_in_image(df, table_graph_name)
            if df_data['has_graph']:
                y_axis = df_data['y_axis']
                x_axis = df_data['x_axis']
                colors = df_data['colors']
                graph_name = df_data['graph_name']
                self.graph(df, y_axis, x_axis, colors, graph_name)

    def graph_gustafson_exec_time(self, filename):
        df = pd.DataFrame(data=self.data)
        columns = [
            'matrix_dimension',
            'parallel_median_time',
            'serial_median_time'
        ]
        df = df.loc[:, columns]
        self.save_df_data(
            df,
            ['parallel_median_time', 'serial_median_time'],
            'matrix_dimension',
            {
                'parallel_median_time': 'b-',
                'serial_median_time': 'r-'
            },
            filename,
            True
        )

    def graph_gustafson_speed_up(self, filename):
        df = pd.DataFrame(data=self.data)
        columns = [
            'matrix_dimension',
            'parallel_median_time',
            'serial_median_time'
        ]
        df = df.loc[:, columns]
        df['speed_up'] = [0] * len(df.index)
        df['speed_up'] = df.apply(
            lambda x: self.gustafson_speed_up(
                x['serial_median_time'],
                x['parallel_median_time'],
                x['matrix_dimension']
            ),
            axis=1
        )
        df = df.loc[:, ['matrix_dimension', 'speed_up']]
        self.save_df_data(
            df,
            ['speed_up'],
            'matrix_dimension',
            {'speed_up': 'b-'},
            filename,
            True
        )