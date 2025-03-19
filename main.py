import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

df = pd.read_csv('heart.csv')

x, y = df.drop('target', axis=1), df['target']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.8, random_state = 0)

model = GradientBoostingClassifier()
model.fit(x_train, y_train)

pred = model.predict([[57, 0, 1, 130, 236, 0, 0, 174, 0, 0.0, 1, 1, 2]])

print("Neural Network Accuracy: {:.2f}%".format(model.score(x_test, y_test) * 100))
print("Prdicted Value is : ", format(pred))

print(model.score(x_test, y_test) * 100)

if pred[0] == 0:
    print("Estás saludable")
else:
    print("No estás saludable.")

# param_grid = {
#     'n_estimators': [100, 200, 500],
#     'max_depth': [None, 10, 20, 30],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4],
#     'max_features': ['sqrt', 'log2', None]
# }

# forest = RandomForestClassifier(n_jobs=-1, random_state=9)

# grid_search = GridSearchCV(forest, param_grid, cv=3, n_jobs=-1, verbose=2)

# grid_search.fit(x_train, y_train)

# best_forest = grid_search.best_estimator_

# feature_importances = best_forest.feature_importances_
# features = best_forest.feature_names_in_

# sorted_idx = np.argsort(feature_importances)
# sorted_features = features[sorted_idx]
# sorted_importances = feature_importances[sorted_idx]

# colors = plt.cm.YlGn(sorted_importances / max(sorted_importances))

# plt.barh(sorted_features, sorted_importances, color=colors)
# plt.xlabel('Feature Importance')
# plt.ylabel('Features')
# plt.title('Feature Importances')
# plt.show()

# plt.figure(figsize=(12,10))
# sns.heatmap(abs(df.corr()), annot=True, cmap='YlGn')

# best_forest.predict([57, 0, 1, 130, 236, 0, 0, 174, 0, 0.0, 1, 1, 2])