import numpy as np
import pandas as pd
import random
# تو این تابع فقط هدف ما اینه که دیتا رو بخونیم و خب یه بخشی از دیتا که میخوایم روش عملیات انجام بدیم رو جدا کنیم
def read_data_from_csv(data_path):
    data = pd.read_csv(data_path)
    x = data.iloc[:, 5].values.reshape(-1, 1)
    y = data.iloc[:, -1].values
    return x, y
# این تابع برای نرمالایز کردن داده هاست که کارش اینه داده ها رو به توزیع گوسی برسونه
def normalize_data(x_data):
    mean_x = np.mean(x_data)
    std_x = np.std(x_data)
    if std_x == 0:
        std_x = 1
    x_norm = (x_data - mean_x) / std_x
    return x_norm, mean_x, std_x
# هدف از این تابع اینه که داده هامونو به شکل اماده برای رگرسیون چند جمله ای تبدیل کنیم
def create_polynomial_features(x_data, degree):
    x_poly = np.ones((x_data.shape[0], degree + 1))
    for d in range(1, degree + 1):
        for i in range(x_data.shape[0]):
            x_poly[i, d] = x_data[i, 0] ** d
    return x_poly
# در این تابع وزن های اولیه رو تولید میکنیم که تلاش شده به صورت رندوم باشن
def generate_weight_vector(x_data, degree):
    x_max = x_data.max()
    x_min = x_data.min()
    weight_vector = np.ones(degree + 1)
    for i in range(degree + 1):
        random_number = random.uniform(x_min, x_max)
        weight_vector[i] = random_number / 10
    return weight_vector
# برای پیدا کردن مقدار y_predict از این تابع استفاده کردیم
def prediction(x_poly, weight_vector):
    x_rows = x_poly.shape[0]
    y_prediction = np.zeros(x_rows)
    for i in range(x_rows):
        y_prediction[i] = 0
        for j in range(len(weight_vector)):
            y_prediction[i] += weight_vector[j] * x_poly[i, j]
    return y_prediction
# این تابع هم که وزن ها رو آپیدت میکنه و تلاش شده کاملا ساده و بر اساس همون تابع آپدیت وزن ها نوشته بشه
def update_weight_vector(x_poly, y_data, y_predict, lambda_coefficient, alpha, weight_vector):
    m = len(y_data)
    new_weight_vector = np.zeros(len(weight_vector))
    for j in range(len(weight_vector)):
        gradient = 0
        for i in range(m):
            gradient += (y_predict[i] - y_data[i]) * x_poly[i, j]
        gradient = (1/m) * gradient + 2 * lambda_coefficient * weight_vector[j]
        new_weight_vector[j] = weight_vector[j] - alpha * gradient
    return new_weight_vector
# تابع محاسبه گرادیان هست که وزن های گام بعدی رو هندل میکنه
def gradient_descent(x_data, y_data, degree, learning_rate, iterations, lambda_coefficient):
    x_norm, mean_x, std_x = normalize_data(x_data)
    x_poly = create_polynomial_features(x_norm, degree)
    weight_vector = generate_weight_vector(x_norm, degree)
    for _ in range(iterations):
        y_predict = prediction(x_poly, weight_vector)
        weight_vector = update_weight_vector(x_poly, y_data, y_predict, lambda_coefficient, learning_rate, weight_vector)
    return weight_vector, mean_x, std_x
# تو این تمرین برای اینکه بتونم صحت کدمو چک کنم از دیتا ستی که اقای شال استفاده کرده بودن استفاده کردم که بتونم مقادیر عددی خروجیم رو با ایشون چک کنم
if __name__ == '__main__':
    learning_rate = 0.01
    iterations = 2000
    degree = 1
    lambda_coefficient = 0.01
    data_path = 'my_data.csv'
    x, y = read_data_from_csv(data_path)
    weights, mean_x, std_x = gradient_descent(x, y, degree, learning_rate, iterations, lambda_coefficient)
    print("وزن‌های نهایی:", weights)