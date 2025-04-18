import numpy as np
import pandas as pd
# داده‌ها رو از CSV می‌خونه (ستون اول ویژگی، ستون آخر برچسب)
def snatch_data(some_file):
    table = pd.read_csv(some_file)
    x_vals = table.iloc[:, 5].values.reshape(-1, 1)
    y_vals = table.iloc[:, -1].values
    return x_vals, y_vals
# ویژگی‌ها رو نرمال‌سازی می‌کنه (میانگین صفر، انحراف معیار یک)
def normalize_features(x_data):
    mean_x = np.mean(x_data)
    std_x = np.std(x_data)
    if std_x == 0:
        std_x = 1
    x_norm = (x_data - mean_x) / std_x
    return x_norm, mean_x, std_x
# ماتریس ویژگی‌ها رو می‌سازه (ستون ۱ها و x)
def make_poly_features(x_data, degree):
    poly_x = np.ones((x_data.shape[0], 1))
    for d in range(1, degree + 1):
        poly_x = np.c_[poly_x, x_data ** d]
    return poly_x
# تعداد ردیف و ستون داده خام رو برمی‌گردونه
def count_stuff(matrix):
    rows = matrix.shape[0]
    cols = 1
    return rows, cols
# ریج رگرسیون رو با گرادیان دیسنت اجرا می‌کنه
def ridge_it_up(raw_x, y_data, lamda, poly_deg, learn_rate, n_iters):
    n, _ = count_stuff(raw_x)
    x_norm, _, _ = normalize_features(raw_x)
    x_poly = make_poly_features(x_norm, poly_deg)
    weights = np.zeros(poly_deg + 1)
    
    for i in range(n_iters):
        y_pred = np.dot(x_poly, weights)
        errors = y_pred - y_data
        gradients = np.zeros(poly_deg + 1)
        gradients[0] = (2/n) * np.sum(errors)
        for j in range(1, poly_deg + 1):
            gradients[j] = (2/n) * np.dot(errors, x_poly[:, j]) + 2 * lamda * weights[j]
        
        if np.any(np.isnan(gradients)) or np.any(np.isinf(gradients)):
            print(f"گرادیان تو تکرار {i} خراب شد! دیتا یا تنظیمات رو چک کن.")
            return weights
        
        weights -= learn_rate * gradients
    
    return weights

def kick_it():
    penalty = 0.1
    poly_degree = 1
    learn_rate = 0.001
    num_iters = 1000
    data_file = "my_data.csv"
    
    try:
        x_raw, y_raw = snatch_data(data_file)
    except:
        print(f"وای! فایل {data_file} انگار گم شده. یه نگاه به مسیر بنداز.")
        return
    
    n_rows, n_cols = count_stuff(x_raw)
    print(f"داده: {n_rows} تا ردیف، {n_cols} تا ستون ورودی")
    
    final_weights = ridge_it_up(x_raw, y_raw, penalty, poly_degree, learn_rate, num_iters)
    print(f"وزن‌ها (بایاس + بقیه): {final_weights}")

if __name__ == "__main__":
    kick_it()
