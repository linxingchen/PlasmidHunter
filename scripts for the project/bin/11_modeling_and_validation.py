#! python

from sklearn.decomposition import PCA
exec(open('/home/tianrm/software/scripts/machine_learning/lib/functions.py', 'r').read())

df = pd.read_pickle('modeling/training_data.pkl')
y = [1 if i.split('-')[-1]=='plasmid' else 0 if i.split('-')[-1]=='chromosome' else 2 for i in df.index]
X = np.array(df)

out = {}
# modeling
for m in [RandomForestClassifier(max_depth=20,random_state=0), DecisionTreeClassifier(max_depth=20,random_state=0), GaussianNB(), LogisticRegression()]:
    o = modeling(X, y, task='c', scaler=0, k_list=0, models=[m])
    out[str(m)] = o

# PCA transformation and modeling
pca = PCA(30)
Xp = pca.fit_transform(X)
for m in [RandomForestClassifier(max_depth=20,random_state=0), DecisionTreeClassifier(max_depth=20,random_state=0), GaussianNB(), LogisticRegression(), KNeighborsClassifier(n_neighbors=7)]:
    o = modeling(Xp, y, task='c', scaler=0, k_list=0, models=[m])
    out['PCA '+str(m)] = o

pickle.dump(out, open('modeling/out.pkl', 'wb'))
