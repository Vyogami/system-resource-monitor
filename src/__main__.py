import psutil
import time
import streamlit as st
import pandas as pd
import numpy as np


class SystemResourceMonitor:
    def __init__(self, interval=1):
        self.interval = interval
        self.columns = [
            'Time',
            'CPU Usage',
            'Memory Used',
            'Disk Usage',
            'Network Bandwith Used'
        ]
        self.df = pd.DataFrame(columns=self.columns)
        self.cpu_chart_data = pd.DataFrame(columns=['Time', 'CPU Usage'])
        self.memory_chart_data = pd.DataFrame(columns=['Time', 'Memory Used'])
        self.disk_chart_data = pd.DataFrame(columns=['Time', 'Disk Usage'])
        self.network_bandwith_used_data = pd.DataFrame(columns=['Time', 'Network Bandwith Used'])

        self.col1, self.col2 = st.columns(2) # Divide screen into 3 columns
        
        self.cpu_chart = self.create_chart(self.col1, 'CPU Usage')
        self.memory_chart = self.create_chart(self.col2, 'Memory Usage')
        self.disk_chart = self.create_chart(self.col1, 'Disk Usage')
        self.network_bandwith_used_chart = self.create_chart(self.col2, 'Network Bandwith Used')

    def create_chart(self, column, title):
        column.write(title)
        chart = column.line_chart(pd.DataFrame(columns=['Time', title]))
        return chart

    def start_monitoring(self):
        while True:
            current_time = pd.Timestamp.now()

            cpu_percent = self.get_cpu_usage()
            memory_percent = self.get_memory_usage()
            disk_percent = self.get_disk_usage()
            network_bandwith_used = self.get_network_bandwidth_usage()

            new_row = pd.Series({
                'Time': current_time,
                'CPU Usage': cpu_percent,
                'Memory Used': memory_percent,
                'Disk Usage': disk_percent,
                'Network Bandwith Used': network_bandwith_used
            })

            self.update_dataframe(new_row)
            self.cpu_chart_data = self.update_chart(self.cpu_chart, self.cpu_chart_data, current_time, cpu_percent)
            self.memory_chart_data = self.update_chart(self.memory_chart, self.memory_chart_data, current_time, memory_percent)
            self.disk_chart_data = self.update_chart(self.disk_chart, self.disk_chart_data, current_time, disk_percent)
            self.network_bandwith_used_data = self.update_chart(self.network_bandwith_used_chart, self.network_bandwith_used_data, current_time, network_bandwith_used)

            time.sleep(self.interval)

    def get_cpu_usage(self):
        return psutil.cpu_percent()

    def get_memory_usage(self):
        return psutil.virtual_memory().percent

    def get_disk_usage(self):
        return psutil.disk_usage('/').percent

    def get_network_bandwidth_usage(self):
        network_stats = psutil.net_io_counters()
        return (network_stats.bytes_sent / (1024**3)) + (network_stats.bytes_recv / (1024**3))  # In GB

    def update_dataframe(self, new_row):
        self.df = pd.concat([self.df, new_row], ignore_index=True)

    def update_chart(self, chart, chart_data, current_time, value):
        chart_data = pd.concat([chart_data, pd.DataFrame({'Time': current_time, chart_data.columns[1]: value}, index=[0])], ignore_index=True)
        chart.line_chart(chart_data.set_index('Time'))
        return chart_data


if __name__ == '__main__':
    monitor = SystemResourceMonitor(interval=1)
    monitor.start_monitoring()
