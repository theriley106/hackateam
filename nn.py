from sklearn import tree

features = [[14, 21, 22, 12], [11, 13, 14, 11], [28, 24, 28, 27], [24, 14, 17, 22], [17, 15, 16, 15], [11, 26, 22, 19], [15, 14, 17, 19]]
labels = [1, 0, 0, 1, 1, 1, 1]
clf = tree.DecisionTreeClassifier()
clf = clf.fit(features, labels)

print clf.predict([28, 26, 25, 14])