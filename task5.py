import math

def safe_apply(func, data):
    results = []
    errors = []
    
    for element in data:
        try:
            result = func(element)
            results.append(result)
        except Exception as e:
            errors.append((element, type(e).__name__))
    
    return results, errors


data = ['4', '16', 'text', '-25', '9.0']


sqrt_lambda = lambda x: math.sqrt(float(x))

results, errors = safe_apply(sqrt_lambda, data)

print("Успешные результаты:")
for i, result in enumerate(results):
    print(f"sqrt({data[i]}) = {result:.2f}")

print("\nОшибки:")
for element, error_type in errors:
    print(f"Элемент '{element}': {error_type}")