import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from joblib import Parallel, delayed

np.random.seed(0)
n_pts = 500
X, y = datasets.make_circles(n_samples=n_pts, random_state=123, noise=0.1, factor=0.20)
plt.scatter(X[y==0, 0], X[y==0, 1])
plt.scatter(X[y==1, 0], X[y==1, 1])
plt.show()

model = Sequential()
model.add(Dense(3, input_shape=(2,), activation='sigmoid'))
model.add(Dense(1, activation='sigmoid'))
model.compile(Adam(learning_rate=0.03), 'binary_crossentropy', metrics=['accuracy'])
h = model.fit(x=X, y=y, verbose=1, batch_size=20, epochs=100, shuffle=True, workers=4, use_multiprocessing=True)

plt.plot(h.history['accuracy'])
plt.xlabel('Epoch')
plt.plot(h.history['loss'])
plt.xlabel('Epoch')
plt.legend(['Loss'])
plt.title('Loss with 3 hidden layers')
plt.legend(['Accuracy'])

def predict_parallel(model, grid):
    return model.predict(grid)

def plot_decision_boundery(X, y, model):
    x_span = np.linspace(min(X[:, 0])-1, max(X[:, 0])+1, 50)
    y_span = np.linspace(min(X[:, 1])-1, max(X[:, 1])+1, 50)
    xx, yy = np.meshgrid(x_span, y_span)
    xx_, yy_ = xx.ravel(), yy.ravel()
    grid = np.c_[xx_, yy_]
    pred_func = Parallel(n_jobs=-1)(delayed(predict_parallel)(model, grid[i:i+100]) for i in range(0, len(grid), 100))
    pred_func = np.concatenate(pred_func, axis=0)
    z = pred_func.reshape(xx.shape)
    plt.contourf(xx, yy, z)
    plt.scatter(X[:n_pts, 0], X[:n_pts, 1])
    plt.scatter(X[n_pts:, 0], X[n_pts:, 1])
    plt.title('Accuracy with 3 hidden layers')
    
plot_decision_boundery(X, y, model)
x = 0
y = 2
point = np.array([[x, y]])
prediction = model.predict(point)
plt.plot([x], [y], marker="o", markersize=10, color="red")
print(str(np.round(prediction*100)) + "%")
