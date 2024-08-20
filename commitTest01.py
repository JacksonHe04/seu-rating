# 这是一个测试，用于测试提交

def fibonacci(n):
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

# 打印前 10 个 Fibonacci 数
if __name__ == "__main__":
    n = 10
    fib_sequence = fibonacci(n)
    print(f"前 {n} 个 Fibonacci 数列: {fib_sequence}")
