import matplotlib.pyplot as plt
from collections import Counter
import random
import pandas as pd

import utils.dbmanager as dbmanager


def drawing_observation_of_number_distribution_analysis_chart():
    """
    :desc:
        Historical Data Analysis Method - Number Distribution Observation
        Analyse open prize number of history data distribution observation, ex: to divide front area number 01-12、13-24、25-35 three area interval,
        Observal frequency even area number, Determnine which intervals are likely to be hot zones and which ones are cold zones in the recent periond.
        So as to make reasonable combinations when choosing numbers. Intervals to divided are little, the analysis is more accurate.
    """

    # SECTION - Read history data open prize from database then package data structure
    db = dbmanager.DBManager()
    sql = "select * from t_bus_daletou"
    result_data = db.queryall(sql)
    db.close()

    # NOTE - Package data structure as follows:
    # lottery_data = [
    #     [1, 5, 10, 20, 30],
    #     [2, 6, 12, 22, 32],
    #     [3, 7, 14, 24, 34],
    #     [4, 8, 16, 26, 35],
    #     [5, 9, 18, 28, 33]
    # ]
    lottery_data = []
    for i in range(len(result_data)):
        front_intervals_numbers = [result_data[i][2], result_data[i][3], result_data[i][4], result_data[i][5], result_data[i][6]]
        back_intervals_numbers = [result_data[i][7], result_data[i][8]]
        open_result_numbers = (front_intervals_numbers, back_intervals_numbers)
        lottery_data.append(open_result_numbers)

    # NOTE - The front area number interval division
    front_intervals = [(1, 3), (4, 7), (8, 11), (12, 15), (16, 19), (20, 23), (24, 27), (28, 31), (32, 35)]
    # NOTE - The back area number interval division
    back_intervals = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12)]

    def count_numbers_in_intervals(data, intervals):
        """
        :desc: Count the number of occurrences of each number within each interval.
        :param data: Open prize number data
        :param intervals: Interval list
        :return: Count the number of occurrences of each number within each interval.
        """
        counter = Counter()
        for draw in data:
            for num in draw:
                for i, (start, end) in enumerate(intervals):
                    if start <= num <= end:
                        counter[i] += 1
        return counter

    # SECTION - Count the number of occurrences of each number within each interval.
    # NOTE - Count distribution of the front area number.
    front_data = [draw[0] for draw in lottery_data]
    front_counter = count_numbers_in_intervals(front_data, front_intervals)

    # NOTE - Count distribution of the back area number. 
    back_data = [draw[1] for draw in lottery_data]
    back_counter = count_numbers_in_intervals(back_data, back_intervals)

    # NOTE - Drawing bar graph of the front area number distribution.
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.bar(range(len(front_intervals)), [front_counter[i] for i in range(len(front_intervals))])
    plt.xticks(range(len(front_intervals)), [f"{start}-{end}" for start, end in front_intervals])
    plt.xlabel('Front Area Number Interval')
    plt.ylabel('Occurrence Number')
    plt.title('Front Area Number Intercal Distribution')

    # NOTE -Drawing bar graph of the back area number distribution.
    plt.subplot(1, 2, 2)
    plt.bar(range(len(back_intervals)), [back_counter[i]for i in range(len(back_intervals))])
    plt.xticks(range(len(back_intervals)), [f"{start}-{end}" for start, end in back_intervals])
    plt.xlabel('Back Area Number Interval')
    plt.ylabel('Occurrence Number')
    plt.title('Back Area Number Intercal Distribution')

    plt.tight_layout()
    plt.show()


def drawing_odd_even_ratio_analysis_chart():
    """
    :desc: 
        历史数据分析法-奇偶比例分析
        统计历史开奖号码中奇数和偶数的比例，一般来说，奇偶比例在长期内会趋近于平衡，但在短期内可能会出现偏差。
        可以根据近期的奇偶走势来选择号码，例如如果连续几期奇数号码较多，那么下期可以适当关注偶数号码。
    """

    db = dbmanager.DBManager()
    sql = "select * from t_bus_daletou"
    result_data = db.queryall(sql)
    db.close()

    lottery_data = []
    for i in range(len(result_data)):
        front_intervals_numbers = [result_data[i][2], result_data[i]
                                   [3], result_data[i][4], result_data[i][5], result_data[i][6]]
        back_intervals_numbers = [result_data[i][7], result_data[i][8]]
        open_result_numbers = (front_intervals_numbers, back_intervals_numbers)
        lottery_data.append(open_result_numbers)

    def analyze_odd_even_ratio(data):
        """
        分析号码的奇偶比例
        :param data: 开奖号码数据
        :return: 每期的奇偶比例列表
        """
        ratios = []
        for draw in data:
            odd_count = sum(num % 2 != 0 for num in draw)
            even_count = len(draw) - odd_count
            if even_count == 0:
                ratio = float('inf')
            else:
                ratio = odd_count / even_count
            ratios.append(ratio)
        return ratios


    # 分析前区号码奇偶比例
    front_data = [draw[0] for draw in lottery_data]
    front_ratios = analyze_odd_even_ratio(front_data)

    # 分析后区号码奇偶比例
    back_data = [draw[1] for draw in lottery_data]
    back_ratios = analyze_odd_even_ratio(back_data)

    # 绘制前区奇偶比例折线图
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(range(1, len(front_ratios) + 1), front_ratios, marker='o')
    plt.xlabel('期数')
    plt.ylabel('奇偶比例')
    plt.title('前区号码奇偶比例走势')

    # 绘制后区奇偶比例折线图
    plt.subplot(1, 2, 2)
    plt.plot(range(1, len(back_ratios) + 1), back_ratios, marker='o')
    plt.xlabel('期数')
    plt.ylabel('奇偶比例')
    plt.title('后区号码奇偶比例走势')

    plt.tight_layout()
    plt.show()


def drawing_count_duplicates_analysis_chart():
    """
    :desc:
        历史数据分析法-重号分析
        观察历史数据中重复出现的号码，即重号。有些号码可能会在短期内频繁出现，而有些号码则可能长时间不出现。对重号的分析可以帮助我们确定是否选择近期出现过的号码。
    """

    db = dbmanager.DBManager()
    sql = "select * from t_bus_daletou"
    result_data = db.queryall(sql)
    db.close()

    lottery_data = []
    for i in range(len(result_data)):
        item = [result_data[i][2], result_data[i][3], result_data[i][4], result_data[i][5], result_data[i][6], result_data[i][7], result_data[i][8]]
        lottery_data.append(item)

    def count_duplicates(data, interval=1):
        """
        统计指定间隔期数的重号数量
        :param data: 开奖号码数据
        :param interval: 期数间隔，默认为 1
        :return: 每期的重号数量列表
        """
        duplicate_counts = []
        for i in range(len(data) - interval):
            current_draw = set(data[i])
            next_draw = set(data[i + interval])
            duplicates = current_draw.intersection(next_draw)
            duplicate_counts.append(len(duplicates))
        return duplicate_counts


    # 统计相邻两期的重号数量
    adjacent_duplicates = count_duplicates(lottery_data)

    # 统计间隔两期的重号数量（可根据需要调整间隔期数）
    interval_duplicates = count_duplicates(lottery_data, interval=2)

    # 绘制相邻两期重号数量折线图
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(range(1, len(adjacent_duplicates) + 1), adjacent_duplicates, marker='o')
    plt.xlabel('期数')
    plt.ylabel('重号数量')
    plt.title('相邻两期重号数量走势')

    # 绘制间隔两期重号数量折线图
    plt.subplot(1, 2, 2)
    plt.plot(range(1, len(interval_duplicates) + 1), interval_duplicates, marker='o')
    plt.xlabel('期数')
    plt.ylabel('重号数量')
    plt.title('间隔两期重号数量走势')

    plt.tight_layout()
    plt.show()


def drawing_hot_cold_analysis_chart():
    """
    :desc:
        冷热号分析法-确定冷热号
        根据历史开奖数据，设定一个时间段，比如过去 30 期或 50 期，统计每个号码出现的次数。出现次数较多的号码称为 “热号”，出现次数较少的号码称为 “冷号”。
    """

    db = dbmanager.DBManager()
    sql = "select * from t_bus_daletou"
    result_data = db.queryall(sql)
    db.close()

    lottery_data = []
    for i in range(len(result_data)):
        item = [result_data[i][2], result_data[i][3], result_data[i][4], result_data[i][5], result_data[i][6], result_data[i][7], result_data[i][8]]
        lottery_data.append(item)

    # 合并所有开奖号码
    all_numbers = []
    for draw in lottery_data:
        all_numbers.extend(draw)

    # 统计每个号码的出现次数
    number_counts = Counter(all_numbers)

    # 假设前 5 个出现次数最多的号码为热号，后 5 个出现次数最少的号码为冷号
    sorted_numbers = sorted(number_counts.items(), key=lambda x: x[1], reverse=True)
    hot_numbers = sorted_numbers[:5]
    cold_numbers = sorted_numbers[-5:]

    # 打印冷热号
    print("热号：", hot_numbers)
    print("冷号：", cold_numbers)

    # 可视化展示号码出现次数
    numbers = list(number_counts.keys())
    counts = list(number_counts.values())

    plt.figure(figsize=(12, 6))
    plt.bar(numbers, counts)
    plt.xlabel('号码')
    plt.ylabel('出现次数')
    plt.title('大乐透号码出现次数统计')
    plt.xticks(rotation=45)
    plt.show()
        

def generate_combination():
    """
    :desc:
        冷热号分析法-选号组合生成
        一般建议在选号时兼顾冷热号，既选择一些近期表现活跃的热号，也适当搭配一些长时间未出的冷号，以增加中奖的可能性。
    """

    db = dbmanager.DBManager()
    sql = "select * from t_bus_daletou"
    result_data = db.queryall(sql)
    db.close()

    lottery_data = []
    for i in range(len(result_data)):
        item = [result_data[i][2], result_data[i][3], result_data[i][4], result_data[i][5], result_data[i][6], result_data[i][7], result_data[i][8]]
        lottery_data.append(item)

    # 合并所有开奖号码
    all_numbers = []
    for draw in lottery_data:
        all_numbers.extend(draw)

    # 统计每个号码的出现次数
    number_counts = Counter(all_numbers)

    # 假设前 5 个出现次数最多的号码为热号，后 5 个出现次数最少的号码为冷号
    sorted_numbers = sorted(number_counts.items(), key=lambda x: x[1], reverse=True)
    hot_numbers = [num for num, _ in sorted_numbers[:5]]
    cold_numbers = [num for num, _ in sorted_numbers[-5:]]

    # 定义前区和后区号码范围
    front_range = list(range(1, 36))
    back_range = list(range(1, 13))

    def generate_combination():
        """
        生成一个大乐透号码组合
        """
        # 从前区热号中选 1 - 2 个号码
        num_hot_front = random.randint(1, 2)
        selected_hot_front = random.sample(hot_numbers, num_hot_front)
        # 从前区冷号中选 1 个号码
        selected_cold_front = random.choice([num for num in cold_numbers if num in front_range])
        # 从前区剩余号码中选剩下的号码
        remaining_front = [num for num in front_range if num not in selected_hot_front and num != selected_cold_front]
        num_remaining_front = 5 - num_hot_front - 1
        selected_remaining_front = random.sample(remaining_front, num_remaining_front)
        # 前区最终组合
        front_combination = sorted(selected_hot_front + [selected_cold_front] + selected_remaining_front)

        # 从后区热号中选 0 - 1 个号码
        num_hot_back = random.randint(0, 1)
        hot_back = [num for num in hot_numbers if num in back_range]
        if hot_back:
            selected_hot_back = random.sample(hot_back, num_hot_back)
        else:
            selected_hot_back = []
        # 从后区冷号中选 0 - 1 个号码
        cold_back = [num for num in cold_numbers if num in back_range]
        if cold_back:
            num_cold_back = random.randint(0, 1)
            selected_cold_back = random.sample(cold_back, num_cold_back)
        else:
            num_cold_back = 0
            selected_cold_back = []
        # 从后区剩余号码中选剩下的号码
        remaining_back = [num for num in back_range if num not in selected_hot_back and num not in selected_cold_back]
        num_remaining_back = 2 - num_hot_back - num_cold_back
        selected_remaining_back = random.sample(remaining_back, num_remaining_back)
        # 后区最终组合
        back_combination = sorted(selected_hot_back + selected_cold_back + selected_remaining_back)

        return front_combination, back_combination

    # 生成 5 个号码组合示例
    for _ in range(5):
        front, back = generate_combination()
        print(f"前区: {front}, 后区: {back}")


def drawing_count_numbers_in_intervals_analysis_chart():
    """
    :desc:
        区间分析法-区间号码统计
        将前区号码按照一定的规则划分为不同的区间，如按照号码大小平均划分，或者根据号码的特征划分，如质数区间、合数区间等。
    """

    db = dbmanager.DBManager()
    sql = "select * from t_bus_daletou"
    result_data = db.queryall(sql)
    db.close()

    lottery_data = []
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


    # 统计前区号码在各区间的出现次数
    front_data = [draw[0] for draw in lottery_data]
    front_counter = count_numbers_in_intervals(front_data, front_intervals)

    # 统计后区号码在各区间的出现次数
    back_data = [draw[1] for draw in lottery_data]
    back_counter = count_numbers_in_intervals(back_data, back_intervals)

    # 打印前区各区间号码出现次数
    print("前区各区间号码出现次数：")
    for i, (start, end) in enumerate(front_intervals):
        print(f"区间 {start}-{end}: {front_counter[i]} 次")

    # 打印后区各区间号码出现次数
    print("\n后区各区间号码出现次数：")
    for i, (start, end) in enumerate(back_intervals):
        print(f"区间 {start}-{end}: {back_counter[i]} 次")

    # 可视化前区号码区间分布
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.bar(range(len(front_intervals)), [front_counter[i] for i in range(len(front_intervals))])
    plt.xticks(range(len(front_intervals)), [f"{start}-{end}" for start, end in front_intervals])
    plt.xlabel('前区号码区间')
    plt.ylabel('出现次数')
    plt.title('前区号码区间分布')

    # 可视化后区号码区间分布
    plt.subplot(1, 2, 2)
    plt.bar(range(len(back_intervals)), [back_counter[i] for i in range(len(back_intervals))])
    plt.xticks(range(len(back_intervals)), [f"{start}-{end}" for start, end in back_intervals])
    plt.xlabel('后区号码区间')
    plt.ylabel('出现次数')
    plt.title('后区号码区间分布')

    plt.tight_layout()
    plt.show()


def drawing_analyze_interval_trend_analysis_chart():
    """
    :desc:
        区间分析法-区间走势分析
        观察每个区间在历史开奖中的出号情况，分析其走势规律，例如某个区间是否连续多期出号较少，那么下期该区间可能有出号反弹的趋势。
    """
    db = dbmanager.DBManager()
    sql = "select * from t_bus_daletou"
    result_data = db.queryall(sql)
    db.close()

    lottery_data = []
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

    def analyze_interval_trend(data, intervals):
        """
        分析各区间的走势，统计每期各区间的出号数量
        :param data: 开奖号码数据
        :param intervals: 区间列表
        :return: 包含各区间每期出号数量的 DataFrame
        """
        num_intervals = len(intervals)
        interval_counts = []
        for draw in data:
            current_counts = [0] * num_intervals
            for num in draw:
                for i, (start, end) in enumerate(intervals):
                    if start <= num <= end:
                        current_counts[i] += 1
            interval_counts.append(current_counts)
        columns = [f'Interval {i + 1} ({start}-{end})' for i, (start, end) in enumerate(intervals)]
        return pd.DataFrame(interval_counts, columns=columns)


    # 分析前区号码区间走势
    front_data = [draw[0] for draw in lottery_data]
    front_trend = analyze_interval_trend(front_data, front_intervals)

    # 分析后区号码区间走势
    back_data = [draw[1] for draw in lottery_data]
    back_trend = analyze_interval_trend(back_data, back_intervals)

    # 绘制前区号码区间走势折线图
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    for col in front_trend.columns:
        plt.plot(front_trend[col], label=col)
    plt.xlabel('期数')
    plt.ylabel('出号数量')
    plt.title('前区号码区间走势')
    plt.legend()

    # 绘制后区号码区间走势折线图
    plt.subplot(1, 2, 2)
    for col in back_trend.columns:
        plt.plot(back_trend[col], label=col)
    plt.xlabel('期数')
    plt.ylabel('出号数量')
    plt.title('后区号码区间走势')
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    drawing_observation_of_number_distribution_analysis_chart()
    pass
