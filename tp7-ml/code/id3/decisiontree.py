from copy import copy
from math import log2

import pandas as pd
from sklearn import metrics


class Node:
    __slots__ = 'label', 'children'

    def __init__(self, label):
        self.label = label
        self.children = dict()


class DecisionTreeClassifier:
    __slots__ = 'tree'

    def __init__(self):
        self.tree = None

    def fit(self, examples, feature):
        self.tree = learn_decision_tree(
            attributes=examples.columns.to_list(),
            examples=examples,
            feature=feature,
            parent_examples=None
        )

    def predict(self, data: pd.DataFrame):
        # Check if the classifier was fitted.
        if self.tree is None:
            raise Exception('Fit the classifier first!')

        # Travel the tree
        result = None
        current = self.tree
        while result is None:
            value = data[current.label].values[0]

            if current.children[value] in {True, False}:
                result = current.children[value]
            else:
                current = current.children[value]

        return result


def learn_decision_tree(attributes: list,
                        examples: pd.DataFrame,
                        parent_examples: pd.DataFrame | None,
                        feature: str):
    # No examples remaining. Get plurality from parents
    if examples.empty:
        return plurality_value(parent_examples)

    # All the examples have the same classification
    e_counts = examples[feature].value_counts()
    if e_counts.size == 1:
        return examples[feature].values[0]

    # No attributes remaining. Get plurality from examples
    if len(attributes) == 0:
        return plurality_value(examples[feature])

    # General case. Partition
    # Attribute selection
    att = None
    att_importance = None
    att_counts = None

    for attribute in attributes:
        if attribute == feature:
            continue

        current_counts = examples[attribute].value_counts()
        current_importance = importance(examples, e_counts, current_counts, feature)

        if att is None or att_importance < current_importance:
            att = attribute
            att_importance = current_importance
            att_counts = current_counts

    # Make node and continue recursion
    node = Node(att)
    new_attributes = copy(attributes)
    new_attributes.remove(att)

    for value in att_counts.index:
        new_examples = examples.query(f'{att} == "{value}"')
        child = learn_decision_tree(new_attributes, new_examples, examples, feature)
        node.children[value] = child

    return node


def plurality_value(df: pd.DataFrame):
    values = df.value_counts()
    return values.index[values.argmax()]


def importance(examples, e_counts: pd.DataFrame, a_counts: pd.DataFrame, feature):
    # Calc gain in terms of entropy
    # Gain(A) = B(p/(p+n)) − Remainder(A).

    # Initial entropy
    e_sum = e_counts.sum()
    e_true = e_counts[True]

    entropy = B(e_true / e_sum)

    # Calc remainder
    remainder = 0
    for i in range(len(a_counts)):
        a_true = examples.query(f'{a_counts.name} == "{a_counts.axes[0][i]}" and {feature} == True').shape[0]
        a_count = a_counts[i]

        ratio = a_true / a_count
        if ratio not in {1, 0}:
            remainder += (a_count / e_sum) * B(ratio)

    # Return gain
    return entropy - remainder


def B(q):
    p = 1 - q
    return -(q * log2(q) + p * log2(p))


def print_tree(node: Node, depth=0, prev=None):
    print(f'{" " * depth} [{node.label}]')
    for key, val in zip(node.children.keys(), node.children.values()):
        if isinstance(val, Node):
            print(f'{" " * (depth + 2)} [{key}]')
            print_tree(val, depth + 4, prev=key)
        else:
            print(f'{" " * (depth + 2)} [{key}, {val}]')


def main():
    # Read and prepare data
    data = pd.read_csv('./tennis.csv')
    data['play'] = data['play'].map({'yes': True, 'no': False})
    data['windy'] = data['windy'].map({True: 'True', False: 'False'})

    # Make and fit classifier
    dtc = DecisionTreeClassifier()
    dtc.fit(
        examples=data,
        feature='play'
    )

    # Print class prediction tree
    print_tree(dtc.tree)

    # Predict with data and show confusion matrix
    reference = data['play'].to_list()
    predicted = list()

    for i in range(data.shape[0]):
        obs = data[i:i + 1]
        predicted.append(dtc.predict(obs))

    confusion_matrix = metrics.confusion_matrix(reference, predicted)
    print(f"\nConfusion Matrix:\n{confusion_matrix}")


if __name__ == '__main__':
    main()
