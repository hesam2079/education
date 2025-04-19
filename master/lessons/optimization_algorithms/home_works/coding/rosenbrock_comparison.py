import numpy as np

from gradient_descent import  gradient_descent, prediction
from newtoon import newton_method

def rosenbrock(x):
    return 100 * (x[1] - x[0]**2)**2 + (1 - x[0])**2

def create_rosenbrock_data():
    x_data = np.array([[0], [1]])
    y_data = np.zeros(2)
    for i in range(2):
        y_data[i] = rosenbrock([x_data[i, 0], x_data[i, 0]**2])
    return x_data, y_data

def adapt_gradient_descent(learning_rate, iterations, degree, lambda_coefficient):
    x_data, y_data = create_rosenbrock_data()
    weights, mean_x, std_x = gradient_descent(x_data, y_data, degree, learning_rate, iterations, lambda_coefficient)
    x_poly = np.ones((2, degree + 1))
    for d in range(1, degree + 1):
        for i in range(2):
            x_poly[i, d] = x_data[i, 0] ** d
    y_pred = prediction(x_poly, weights)
    cost = 0
    for i in range(2):
        cost += (y_pred[i] - y_data[i])**2
    cost = cost / 2
    return weights, cost

def adapt_newton_method(iterations, degree, lambda_coefficient):
    x_data, y_data = create_rosenbrock_data()
    weights, mean_x, std_x = newton_method(x_data, y_data, degree, iterations, lambda_coefficient)
    x_poly = np.ones((2, degree + 1))
    for d in range(1, degree + 1):
        for i in range(2):
            x_poly[i, d] = x_data[i, 0] ** d
    y_pred = prediction(x_poly, weights)
    cost = 0
    for i in range(2):
        cost += (y_pred[i] - y_data[i])**2
    cost = cost / 2
    return weights, cost

if __name__ == '__main__':
    learning_rate = 0.01
    iterations = 500
    degree = 5
    lambda_coefficient = 0.01
    weights_gd, cost_gd = adapt_gradient_descent(learning_rate, iterations, degree, lambda_coefficient)
    print("گرادیان دیسنت - وزن‌های نهایی:", weights_gd)
    print("گرادیان دیسنت - مقدار هزینه:", cost_gd)
    weights_newton, cost_newton = adapt_newton_method(iterations, degree, lambda_coefficient)
    print("نیوتن - وزن‌های نهایی:", weights_newton)
    print("نیوتن - مقدار هزینه:", cost_newton)