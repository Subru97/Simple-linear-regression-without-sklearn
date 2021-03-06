import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def split_train_test(dataset, test_size=0.25):
    dataset = dataset.sample(frac=1 ,random_state=200)
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, 1].values
    dataset_size = dataset.shape[0]
    split_index = int(round(dataset_size * test_size)) 
    return X[split_index:], y[split_index:], X[:split_index], y[:split_index]  


def matrix_regressor(X, y):
    X = np.vstack((X.T, np.ones(len(X))))
    A = np.linalg.inv(X @ X.T) @ X @ y
    return A

    
def mean_sqaure_error(m, c, X_train, y_train):
    error = 0
    n = len(X_train)
    for i in range(n):    
        error += (y_train[i] - ((m*X_train[i]) + c))**2
    return (1/n)*error

    
def gradient_descent(m, c, learning_rate, X, y):
    m_gradient = 0
    c_gradient = 0
    convergence = False
    n = len(X)
    for i in range(n):
        m_gradient += - (2/n) * X[i] * (y[i] - ((m * X[i]) + c))
        c_gradient += - (2/n) * (y[i] - ((m * X[i]) + c))
    
    if (np.around(np.linalg.norm(m_gradient), 2) == 0.000) and (np.around(np.linalg.norm(c_gradient), 2) == 0.000):
        print(f"Gradient with respect to m is {m_gradient[0]} and with respect to c is {c_gradient[0]} \n")
        convergence = True
        
    new_m = m - (m_gradient * learning_rate)
    new_c = c - (c_gradient * learning_rate)
    return new_m, new_c, convergence


def build_model(initial_m, initial_c, learning_rate, X, y, num_iterations):
    m = initial_m
    c = initial_c
    convergence = False
    
    while not convergence:
        m,c, convergence = gradient_descent(m, c, learning_rate, X, y)
    return [m,c]


def predict(model, x):
    y = model[0] * x + model[1]
    return y


if __name__ == "__main__":
    file_loc = "Salary_Data.csv"
    dataset = pd.read_csv(file_loc)     
    
    X_train, y_train, X_test, y_test = split_train_test(dataset, 0.2)
    
    learning_rate = 0.01
    initial_m = 0
    initial_c = 0
    num_iterations = 1000
    
    model = [m,c] = build_model(initial_m, initial_c, learning_rate, X_train, y_train, num_iterations)
            
    mat_reg = matrix_regressor(X_train, y_train)
    
    print(f"Model based on gradient descent is {model}")
    print(f"Model based on mathematical formula is {mat_reg} \n")

    print(f"Mean square error for m={initial_m} and c={initial_c} is {mean_sqaure_error(initial_m, initial_c, X_train, y_train)[0]}")
    print(f"Mean square error for m={model[0][0]} and c={model[1][0]} is {mean_sqaure_error(model[0], model[1], X_train, y_train)[0]} \n")
  
    for i in range(len(X_test)):        
        print(f"Predicted value for x={i} is {predict(model, X_test[i])[0]} where actual value is {y_test[i]}")

    y_pred = []
    for i in range(len(X_train)):        
        y_pred.append(predict(model, X_train[i]))

    # Visualising the Training set results
    plt.scatter(X_train, y_train, color = 'red')
    plt.plot(X_train, y_pred, color = 'blue')
    plt.title('Salary vs Experience (Training set)')
    plt.xlabel('Years of experience')
    plt.ylabel('Salary')
    plt.show()