import time
import numpy as np
from numpy.linalg import det, inv, solve

class Timer:
    def __enter__(self):
        self.start = time.time()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        print(f"\nВремя выполнения: {end - self.start:.4f} секунд")

np.random.seed(42)
with Timer():
    A = np.random.randint(1, 11, size=(5, 5))
    B = np.random.randint(1, 11, size=(5, 5))

    print("Матрица A:")
    print(A)
    print("\nМатрица B:")
    print(B)

    elementwise_product = A * B
    print("\nПоэлементное произведение A и B:")
    print(elementwise_product)

    matrix_product = np.dot(A, B)
    print("\nМатричное произведение A и B:")
    print(matrix_product)

    det_A = det(A)
    print(f"\nОпределитель матрицы A: {det_A:.2f}")

    B_transposed = B.T
    print("\nТранспонированная матрица B:")
    print(B_transposed)

    try:
        A_inv = inv(A)
        print("\nОбратная матрица для A:")
        print(A_inv)
    except np.linalg.LinAlgError:
        print("\nОбратной матрицы не существует")

    C = A.sum(axis=1).reshape(-1, 1)  # вектор-столбец сумм строк
    try:
        x = solve(A, C)
        print("\nРешение системы уравнений A*x = C:")
        print(x)
    except np.linalg.LinAlgError:
        print("\nСистема уравнений не имеет решения")
