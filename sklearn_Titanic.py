import pylab
import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from IPython.core.display import display, HTML
from sklearn.model_selection import train_test_split, cross_val_score

tf.logging.set_verbosity(tf.logging.ERROR)
pd.options.display.max_rows = 10
pd.options.display.float_format = '{:.4f}'.format

train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')


def process_age(dataframe, cut_points, label_names):
    age = dataframe['Age'].fillna(-0.5)
    dataframe['Age_categories'] = pd.cut(age, cut_points, labels=label_names)
    return dataframe


cut_points = [-1, 0, 5, 12, 18, 35, 60, 100]
label_names = ['Missing', 'Infant', 'Child', 'Teenager', 'Young Adult', 'Adult', 'Senior']
train = process_age(train, cut_points, label_names)
test = process_age(test, cut_points, label_names)


def create_dummies(dataframe, column_name):
    # global dummies
    dummies = pd.get_dummies(dataframe[column_name], prefix=column_name)
    return pd.concat([dataframe, dummies], axis=1)


for column in ['Pclass', 'Sex', 'Age_categories']:
    train = create_dummies(train, column)
    test = create_dummies(test, column)


def view_age_categories():
    pivot = train.pivot_table(index='Age_categories', values='Survived')
    pivot.plot.bar()
    plt.show()


def view_gender_hist():
    survived = train[train['Survived'] == 1]
    died = train[train['Survived'] == 0]
    survived['Age'].plot.hist(alpha=0.5, color='red', bins=50)
    died['Age'].plot.hist(alpha=0.5, color='blue', bins=50)
    plt.legend(['Survived', 'Died'])
    plt.show()


# columns = dummies
columns = ['Pclass_1', 'Pclass_2', 'Pclass_3', 'Sex_female', 'Sex_male',
           'Age_categories_Missing', 'Age_categories_Infant',
           'Age_categories_Child', 'Age_categories_Teenager',
           'Age_categories_Young Adult', 'Age_categories_Adult',
           'Age_categories_Senior']

all_features = train[columns]
all_target = train['Survived']

features_train, features_test, target_train, target_test = train_test_split(
    all_features, all_target, test_size=0.20, random_state=0)

logic_regression = LogisticRegression()
model = logic_regression.fit(features_train, target_train)
predictions = model.predict(features_test)
scores = cross_val_score(model, all_features, all_target, cv=10)
scores.sort()
accuracy = scores.mean()


def view():
    view_age_categories()
    view_gender_hist()
    print('Train DataFrame:\n', train.head())
    print('Predictions:\n', predictions)
    print('Accuracy: ', accuracy)
    print('Model:', model)

# view()

classifiers = [
    LogisticRegression(max_iter=200, penalty="l2"),
    SGDClassifier(loss="hinge", penalty="l2"),
    MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(3, 4)),
    RandomForestClassifier(n_estimators=60, max_depth=5),
    GradientBoostingClassifier(n_estimators=180, learning_rate=1.0, max_depth=4),
    DecisionTreeClassifier(),
    SVC(),
]

result = []
for classifier in classifiers:
    classifier.fit(features_train, target_train)
    report = accuracy_score(target_test, classifier.predict(features_test))
    result.append({'class': classifier.__class__.__name__, 'accuracy': report})

display(HTML('<h2>Result</h2>'))
display(pd.DataFrame(result))

model = xgb.XGBClassifier()
model.fit(features_train, target_train)

pylab.rcParams['figure.figsize'] = 7, 7
plt.style.use('ggplot')
pd.Series(model.feature_importances_).plot(kind='bar', xticks=features_train.index)
x_name = ['Pclass_1', 'Pclass_2', 'Pclass_3', 'Female', 'Male',
          'Missing', 'Infant', 'Child', 'Teenager', 'Adult', 'Adult', 'Senior']
plt.xticks(np.arange(0, 12), x_name, rotation=70)
plt.title('Feature Importances')
plt.show()

pd.DataFrame(result).to_csv('result.csv', index=False)
