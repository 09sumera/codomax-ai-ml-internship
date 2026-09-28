# CODOMAX AI/ML INTERNSHIP - MODULE 1
# Introduction to AI & Python
# 1. VARIABLES AND DATA TYPES

name = "Sumera"
age = 20
cgpa = 9.35
is_student = True

print("Name:", name)
print("Age:", age)
print("CGPA:", cgpa)
print("Student:", is_student)


# 2. USER INPUT

user_name = input("Enter your name: ")
user_age = int(input("Enter your age: "))

print("Hello", user_name)
print("Your age is", user_age)


# 3. IF-ELSE

number = int(input("Enter a number: "))

if number > 0:
    print("Positive number")
elif number < 0:
    print("Negative number")
else:
    print("Zero")


# 4. EVEN OR ODD

number = int(input("Enter a number: "))

if number % 2 == 0:
    print("Even number")
else:
    print("Odd number")


# 5. FOR LOOP

print("Numbers from 1 to 10:")

for i in range(1, 11):
    print(i)


# 6. WHILE LOOP

i = 1

while i <= 5:
    print("Count:", i)
    i += 1


# 7. LIST

numbers = [10, 20, 30, 40, 50]

print("List:", numbers)
print("First element:", numbers[0])
print("Largest:", max(numbers))
print("Smallest:", min(numbers))


# 8. LIST LOOP

for number in numbers:
    print("Number:", number)


# 9. FUNCTION

def greet(name):
    return "Hello, " + name


message = greet("Sumera")
print(message)


# 10. FUNCTION TO FIND SQUARE

def square(number):
    return number * number


print("Square:", square(5))


# 11. SUM OF NUMBERS

numbers = [10, 20, 30, 40, 50]

total = 0

for number in numbers:
    total += number

print("Sum:", total)


# 12. FIND LARGEST NUMBER

numbers = [25, 10, 45, 30, 15]

largest = numbers[0]

for number in numbers:
    if number > largest:
        largest = number

print("Largest number:", largest)


# 13. SIMPLE CALCULATOR

a = float(input("Enter first number: "))
b = float(input("Enter second number: "))

print("Addition:", a + b)
print("Subtraction:", a - b)
print("Multiplication:", a * b)

if b != 0:
    print("Division:", a / b)
else:
    print("Cannot divide by zero")


# 14. CHECK PRIME NUMBER

number = int(input("Enter a number: "))

if number < 2:
    print("Not a prime number")
else:
    is_prime = True

    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            is_prime = False
            break

    if is_prime:
        print("Prime number")
    else:
        print("Not a prime number")


# 15. FIBONACCI SERIES

n = int(input("Enter number of terms: "))

a = 0
b = 1

for i in range(n):
    print(a, end=" ")
    a, b = b, a + b

print()