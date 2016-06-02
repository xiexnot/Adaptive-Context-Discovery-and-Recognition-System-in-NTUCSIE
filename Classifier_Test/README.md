# Classifier Test for MARCS_Recognition 分类器测试

##在选择KNN作为Classifier的时候发现：

当只使用cluster_metric作为training data，n_neighbors=5时，对于除TV外的dataset做处理时，共有n_neighbors个群的概率落在6%到18%之间。而在n_neighbors=13时，possibility低的distribution普遍在3%以下。

##所以现在我们来有一个测试：

同样是KNN，只保留有用的feature（剔除环境feature），看其计算distance上有没有问题。




