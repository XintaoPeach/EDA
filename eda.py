import random


# 定义样本初始化
# 以概率 p 随机产生0和1的个体：当随机数大于p的时候设定为1，否则设定为0
def init_n(probability, dimension):
    data = []
    new = []
    for j in range(dimension):
        for i in probability:
            if random.random() >= i:
                data.append(1)
            else:
                data.append(0)
        new.append(data)
        data = []
    return new


# 定义适应度函数
def init_nn(weight, value, valuemax, init_list):
    total_value = 0
    total_weight = 0
    data = []
    for i in range(len(init_list)):
        for j in range(len(init_list[i])):
            if init_list[i][j] == 1 and total_value + value[j] <= valuemax:
                total_weight += weight[j]   # 物品总重量
                total_value += value[j]     # 物品总价值
            else:
                init_list[i][j] = 0
        data.append(total_weight)
        total_value = 0
        total_weight = 0
    return data


# 定义参数
time = 100  # 迭代次数
weight_list = [95, 4, 60, 32, 23, 72, 80, 62, 65, 46]   # 物品重量
value_list = [55, 10, 47, 5, 4, 50, 8, 61, 85, 87]  # 物品价值
value_max = 269     # 价值上限
population_num = 500    # 种群个体数
better_pop_num = int(population_num/2)  # 较优个体数量
now = 0
n = 10  # 矩阵维度
p = [0.5 for i in range(n)]     # 生成种群概率

# 初始化
init = init_n(probability=p, dimension=n)
f = init_nn(weight=weight_list, value=value_list, valuemax=value_max, init_list=init)

# 初始最优解和最优方案
new_data = []
most_f = max(f)     # 初始化最优解
most = init[f.index(max(f))].copy()     # 根据初始化最优解得到的最优方案


# 分布估计算法
while now < time:
    best_f = max(f)     # 当前最优解
    best = init[f.index(max(f))].copy()     # 当前最优方案
    # 如果当前最优解大于上一次最优解,则进行替换
    if best_f > most_f:
        most_f = best_f
        most = best.copy()
    # 选出较优个体，将m个较优个体存储在new_data中
    for i in range(better_pop_num):
        if f:
            better_f = init[f.index(max(f))].copy()  # 此时最优方案
            new_data.append(better_f)
            f.remove(max(f))
    """
    构建概率模型
    按照种群的适应度从高到低进行排序 
    这里设定较优个体数为m
    从种群中选出适应度较高的m个个体用来更新概率向量模型p
    更新概率模型。令pi=ni/m，其中ni为选出的较优个体中xi=1的个体数
    """
    P = []
    for i in range(len(new_data[0])):
        flag = 0
        for j in range(len(new_data)):
            flag += new_data[j][i]
        # 得到新的概率模型
        flag = flag/len(new_data)
        P.append(flag)
        flag = 0
    # 根据更新后的概率产生新的样本
    init = init_n(probability=P, dimension=population_num)
    # 得到适应度
    f = init_nn(weight=weight_list, value=value_list, valuemax=value_max, init_list=init)
    now += 1

print(f"最优解为：{ most_f }")
print(f"具体方案：{ most }")

