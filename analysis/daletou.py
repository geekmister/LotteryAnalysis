import matplotlib.pyplot as plt
from collections import Counter

import utils.dbmanager as dbmanager


def observation_of_number_distribution():
    # 示例历史开奖数据，实际应用中需从数据源获取真实数据
    lottery_data = []
    db = dbmanager.DBManager()
    sql = "select * from t_bus_daletou"
    result_data = db.queryall(sql)
    db.close()
    for i in range(len(result_data)):
        front_intervals_numbers = [result_data[i][2], result_data[i]
                                   [3], result_data[i][4], result_data[i][5], result_data[i][6]]
        back_intervals_numbers = [result_data[i][7], result_data[i][8]]
        open_result_numbers = (front_intervals_numbers, back_intervals_numbers)
        lottery_data.append(open_result_numbers)

    # 前区号码区间划分
    front_intervals = [(1, 12), (13, 24), (25, 35)]
    # 后区号码区间划分
    back_intervals = [(1, 4), (5, 8), (9, 12)]

    def count_numbers_in_intervals(data, intervals):
        """
        统计每个区间内号码出现的次数
        :param data: 开奖号码数据
        :param intervals: 区间列表
        :return: 每个区间的号码出现次数
        """
        counter = Counter()
        for draw in data:
            for num in draw:
                for i, (start, end) in enumerate(intervals):
                    if start <= num <= end:
                        counter[i] += 1
        return counter

    # 统计前区号码分布
    front_data = [draw[0] for draw in lottery_data]
    front_counter = count_numbers_in_intervals(front_data, front_intervals)

    # 统计后区号码分布
    back_data = [draw[1] for draw in lottery_data]
    back_counter = count_numbers_in_intervals(back_data, back_intervals)

    # 绘制前区号码分布柱状图
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.bar(range(len(front_intervals)), [
            front_counter[i] for i in range(len(front_intervals))])
    plt.xticks(range(len(front_intervals)), [
        f"{start}-{end}" for start, end in front_intervals])
    plt.xlabel('前区号码区间')
    plt.ylabel('出现次数')
    plt.title('前区号码分布')

    # 绘制后区号码分布柱状图
    plt.subplot(1, 2, 2)
    plt.bar(range(len(back_intervals)), [back_counter[i]
            for i in range(len(back_intervals))])
    plt.xticks(range(len(back_intervals)), [
        f"{start}-{end}" for start, end in back_intervals])
    plt.xlabel('后区号码区间')
    plt.ylabel('出现次数')
    plt.title('后区号码分布')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    observation_of_number_distribution()
