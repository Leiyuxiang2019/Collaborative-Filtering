# Collaborative-Filtering
user-item Collaborative Filtering
使用pearson相似度公式依次计算目标用户与

所有用户的pearson相关系数，
得到相关系数矩阵，再由公式 


进行计算，得到每一个电影的预测的分数，将分数进行排序得到推荐的结果进行输出，

再将test中出现的用户-电影的评分结果进行保存，于真实值进行比较计算得到协方差sse。


将数据集movies.csv中的电影类别作为特征值，

计算这些特征值的tf-idf值，

得到关于电影与特征值的n（电影个数）*m（特征值个数）的tf-idf特征矩阵。

根据得到的tf-idf特征矩阵，用余弦相似度的计算方法，得到电影之间的相似度矩阵。
