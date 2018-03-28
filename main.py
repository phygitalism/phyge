import pandas as pd
import tensorflow as tf
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from matplotlib import pyplot as plt

tf.logging.set_verbosity(tf.logging.ERROR)
pd.options.display.max_rows = 10
pd.options.display.float_format = '{:.1f}'.format

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

view()
