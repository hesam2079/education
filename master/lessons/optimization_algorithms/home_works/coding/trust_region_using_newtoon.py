import numpy as np
import pandas as pd
import random

def read_data_from_csv(data_path):
    data = pd.read_csv(data_path)
    x = data.iloc[:, 5].values.reshape(-1, 1)
    y = data.iloc[:, -1].values
    return x, y

def normalize_data(x_data):
    mean_x = np.mean(x_data)
    std_x = np.std(x_data)
    if std_x == 0:
        std_x = 1
    x_norm = (x_data - mean_x) / std_x
    return x_norm, mean_x, std_x

def create_polynomial_features(x_data, degree):
    x_poly = np.ones((x_data.shape[0], degree + 1))
    for d in range(1, degree + 1):
        for i in range(x_data.shape[0]):
            x_poly[i, d] = x_data[i, 0] ** d
    return x_poly

def generate_weight_vector(x_data, degree):
    x_max = x_data.max()
    x_min = x_data.min()
    weight_vector = np.ones(degree + 1)
    for i in range(degree + 1):
        random_number = random.uniform(x_min, x_max)
        weight_vector[i] = random_number / 10
    return weight_vector

def prediction(x_poly, weight_vector):
    x_rows = x_poly.shape[0]
    y_prediction = np.zeros(x_rows)
    for i in range(x_rows):
        y_prediction[i] = 0
        for j in range(len(weight_vector)):
            y_prediction[i] += weight_vector[j] * x_poly[i, j]
    return y_prediction

def compute_cost(x_poly, y_data, weight_vector, lambda_coefficient):
    m = len(y_data)
    y_predict = prediction(x_poly, weight_vector)
    cost = 0
    for i in range(m):
        cost += (y_predict[i] - y_data[i]) ** 2
    cost = cost / m
    for j in range(len(weight_vector)):
        cost += lambda_coefficient * weight_vector[j] ** 2
    return cost

def compute_gradient(x_poly, y_data, weight_vector, lambda_coefficient):
    m = len(y_data)
    y_predict = prediction(x_poly, weight_vector)
    gradient = np.zeros(len(weight_vector))
    for j in range(len(weight_vector)):
        grad_sum = 0
        for i in range(m):
            grad_sum += (y_predict[i] - y_data[i]) * x_poly[i, j]
        gradient[j] = (2/m) * grad_sum + 2 * lambda_coefficient * weight_vector[j]
    return gradient

def compute_hessian(x_poly, weight_vector, lambda_coefficient):
    n = len(weight_vector)
    m = x_poly.shape[0]
    hessian = np.zeros((n, n))
    for j in range(n):
        for k in range(n):
            sum_h = 0
            for i in range(m):
                sum_h += x_poly[i, j] * x_poly[i, k]
            hessian[j, k] = (2/m) * sum_h
            if j == k:
                hessian[j, k] += 2 * lambda_coefficient
    return hessian

def trust_region_newton(x_data, y_data, degree, iterations, delta_max, delta_init, lambda_coefficient):
    x_norm, mean_x, std_x = normalize_data(x_data)
    x_poly = create_polynomial_features(x_norm, degree)
    weight_vector = generate_weight_vector(x_norm, degree)
    delta = delta_init
    for _ in range(iterations):
        grad = compute_gradient(x_poly, y_data, weight_vector, lambda_coefficient)
        hessian = compute_hessian(x_poly, weight_vector, lambda_coefficient)
        direction = -np.linalg.solve(hessian, grad)
        norm_direction = 0
        for j in range(len(direction)):
            norm_direction += direction[j]**2
        norm_direction = np.sqrt(norm_direction)
        if norm_direction > delta:
            for j in range(len(direction)):
                direction[j] = direction[j] * delta / norm_direction
        new_weights = np.zeros(len(weight_vector))
        for j in range(len(weight_vector)):
            new_weights[j] = weight_vector[j] + direction[j]
        actual_reduction = compute_cost(x_poly, y_data, weight_vector, lambda_coefficient) - compute_cost(x_poly, y_data, new_weights, lambda_coefficient)
        predicted_reduction = 0
        for j in range(len(grad)):
            predicted_reduction -= grad[j] * direction[j]
        for j in range(len(direction)):
            for k in range(len(direction)):
                predicted_reduction += 0.5 * direction[j] * hessian[j, k] * direction[k]
        rho = actual_reduction / predicted_reduction
        if rho < 0.25:
            delta = delta / 4
        elif rho > 0.75 and norm_direction >= delta:
            delta = min(2 * delta, delta_max)
        if rho > 0.1:
            for j in range(len(weight_vector)):
                weight_vector[j] = new_weights[j]
    return weight_vector, mean_x, std_x

if __name__ == '__main__':
    iterations = 100
    degree = 1
    lambda_coefficient = 0.01
    delta_max = 1.0
    delta_init = 0.1
    data_path = 'my_data.csv'
    x, y = read_data_from_csv(data_path)
    weights, mean_x, std_x = trust_region_newton(x, y, degree, iterations, delta_max, delta_init, lambda_coefficient)
    print("ناحیه اعتماد - وزن‌های نهایی:", weights)