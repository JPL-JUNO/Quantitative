"""
@Title: 运行测试代码
@Author(s): Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime: 2023-08-30 17:03:46
@Description: 
"""

from data import DataLoader
from knn import KNNClassifier
from sample import Sample
from hyperparameter import HyperParameter

raw_data = [
    {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4,
        "petal_width": 0.2, "label": "Iris-setosa"},
    {"sepal_length": 5.0, "sepal_width": 3.5, "petal_length": 1.4,
        "petal_width": 0.2, "label": "Iris-setosa"},
    {"sepal_length": 4.9, "sepal_width": 3.5, "petal_length": 1.4,
        "petal_width": 0.2, "label": "Iris-setosa"},
    {"sepal_length": 5.5, "sepal_width": 3.6, "petal_length": 1.4,
        "petal_width": 0.2, "label": "Iris-setosa"},
    {"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7,
        "petal_width": 1.4, "label": "Iris-versicolor"},
    {"sepal_length": 7.9, "sepal_width": 3.2, "petal_length": 4.7,
        "petal_width": 1.4, "label": "Iris-versicolor"},
    {"sepal_length": 7.9, "sepal_width": 3.1, "petal_length": 4.7,
        "petal_width": 1.4, "label": "Iris-versicolor"},
    {"sepal_length": 7.8, "sepal_width": 3.2, "petal_length": 4.7,
        "petal_width": 1.4, "label": "Iris-versicolor"},
    {"sepal_length": 7.9, "sepal_width": 3.3, "petal_length": 4.7,
        "petal_width": 1.4, "label": "Iris-versicolor"},
]


dl = DataLoader()
dl.load(raw_data)

model = KNNClassifier()
model.fit(dl.training, dl.testing)
X_prediction = Sample(5.0, 3.5, 1.4, 0.2)
prediction = model.predict(X_prediction)

params_grid = {"k": [5, 3], "p": [1, 2]}
hy = HyperParameter(model, parameters=params_grid)
hy.fit()
print(hy.best_params_dict)

# 最优的模型，如果多个参数的性能相同，那么参数出现的顺序就会比较重要
model = KNNClassifier(k=3, p=1)
