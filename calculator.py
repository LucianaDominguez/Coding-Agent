# Basic Calculator Program
import math


def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y != 0:
        return x / y
    else:
        return 'Error: Division by zero'

def power(x, y):
    return x ** y

def square_root(x):
    return math.sqrt(x)

def modulus(x, y):
    return x % y

# User Interface
if __name__ == '__main__':
    print('Select operation:')
    print('1. Add')
    print('2. Subtract')
    print('3. Multiply')
    print('4. Divide')
    print('5. Power')
    print('6. Square Root')
    print('7. Modulus')

    choice = input('Enter choice (1/2/3/4/5/6/7): ')

    if choice in ['5', '6', '7']:
        num1 = float(input('Enter first number: '))
        if choice == '5':
            num2 = float(input('Enter exponent: '))
            print(f'{num1} ^ {num2} = {power(num1, num2)}')
        elif choice == '6':
            print(f'Square root of {num1} = {square_root(num1)}')
        elif choice == '7':
            num2 = float(input('Enter second number: '))
            print(f'Modulus of {num1} % {num2} = {modulus(num1, num2)}')
    else:
        num1 = float(input('Enter first number: '))
        num2 = float(input('Enter second number: '))

        if choice == '1':
            print(f'{num1} + {num2} = {add(num1, num2)}')
        elif choice == '2':
            print(f'{num1} - {num2} = {subtract(num1, num2)}')
        elif choice == '3':
            print(f'{num1} * {num2} = {multiply(num1, num2)}')
        elif choice == '4':
            print(f'{num1} / {num2} = {divide(num1, num2)}')
        else:
            print('Invalid Input')
