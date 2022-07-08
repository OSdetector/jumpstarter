from itertools import cycle
import pandas as pd
import yaml

from utils import data_process
from algorithm.cluster import cluster



if __name__ == '__main__':
    config = 'detector-config.yml'
    with open(config, 'r', encoding='utf8') as file:
        config_dict = yaml.load(file, Loader=yaml.Loader)
    data = pd.read_csv(config_dict['data']['path'], header=None)

    n, d = data.shape

    # Normalize each dimension
    data = data.values
    for i in range(d):
        data[:, i] = data_process.normalization(data[:, i]) 


        
    # Get clustered group
    cluster_threshold = config_dict['detector_arguments']['cluster_threshold']
    windows_per_cycle = config_dict['data']['rec_windows_per_cycle']
    windows = config_dict['data']['reconstruct']['window']
    cycle = windows * windows_per_cycle
    cycle_groups = []
    group_index = 0
    # 周期开始的index
    cb = 0
    while cb < n:
        # 周期结束的index
        ce = min(n, cb + cycle)  # 一周期数据为data[cb, ce)
        # 初始化追加列表引用
        if group_index == 0:
            # 没有历史数据
            # 分组默认每个kpi一组
            init_group = []
            for i in range(d):
                init_group.append([i])
            cycle_groups.append(init_group)
        else:
            cycle_groups.append(cluster(data[cb:ce], cluster_threshold))
        group_index +=1
        cb += cycle
        
    print("Done")