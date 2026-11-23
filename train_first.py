import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree

from config import FEATURES, TARGET, baseline_predict, load_splits

train, valid, test = load_splits()       # test stays locked until Session 5
print('Train rows:', len(train), '| Validation rows:', len(valid))

baseline = (baseline_predict(valid) == valid[TARGET]).mean()
model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(train[FEATURES], train[TARGET])
print(f'Baseline accuracy:   {baseline:.1%}')
print(f'Train accuracy:      {model.score(train[FEATURES], train[TARGET]):.1%}')
print(f'Validation accuracy: {model.score(valid[FEATURES], valid[TARGET]):.1%}')

for name, value in zip(FEATURES, model.feature_importances_):
    print(f'{name:20s} {value:.2f}')
plot_tree(model, feature_names=FEATURES, filled=True, fontsize=8)
plt.show()