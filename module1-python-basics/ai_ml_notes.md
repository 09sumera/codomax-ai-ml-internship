Codomax AI/ML Internship – Module 1 Learning Notes
Module: 1 – Introduction to AI & Python
 Duration: Day 1 – Day 4
 Internship: Codomax AI/ML Internship
 Name: Sumera Anjum

1. Introduction to Artificial Intelligence

Artificial Intelligence (AI) is a branch of computer science that focuses on creating machines and software systems that can perform tasks that normally require human intelligence.

AI systems can perform tasks such as:

Learning from data
Recognizing patterns
Understanding language
Recognizing images
Making predictions
Solving problems
Making decisions
Generating text, images, audio, and other content

Examples of Artificial Intelligence
Some common real-world examples of AI are:
Chatbots and virtual assistants
Face recognition systems
Recommendation systems
Voice assistants
Fraud detection systems
Medical image analysis
Self-driving and driver-assistance systems
Language translation
Generative AI applications


2. What is Machine Learning?

Machine Learning (ML) is a subset of Artificial Intelligence.
It allows computers to learn patterns from data and make predictions or decisions without being explicitly programmed for every individual situation.

Example
Suppose we have information about houses such as:
Area
Number of bedrooms
Location
Number of bathrooms
Previous selling price

A machine learning algorithm can learn patterns from existing house data and use those patterns to predict the price of a new house.


Basic Machine Learning Process
Collect Data
     ↓
Clean and Prepare Data
     ↓
Train Machine Learning Model
     ↓
Test the Model
     ↓
Make Predictions
     ↓
Evaluate Results


3. What is Deep Learning?

Deep Learning is a subset of Machine Learning that uses artificial neural networks with multiple layers to learn complex patterns from large amounts of data.

Deep learning is particularly useful for tasks involving:
Images
Speech
Text
Video
Natural language
Examples
Image recognition
Speech recognition
Facial recognition
Natural Language Processing
Generative AI
Autonomous driving systems

4. Difference Between AI, ML and Deep Learning

Artificial Intelligence, Machine Learning, and Deep Learning are related concepts.

Artificial Intelligence
        ↓
Machine Learning
        ↓
Deep Learning


Artificial Intelligence


Machine Learning



Deep Learning
Broad field of creating intelligent systems
Subset of AI
Subset of ML
Can use different techniques
Learns patterns from data
Uses multi-layer neural networks
Includes ML and other approaches
Uses algorithms to learn from data
Usually requires larger datasets and computational resources
Example: intelligent assistant
Example: spam detection
Example: image recognition

In simple words:
AI → Making machines intelligent.
ML → Teaching machines to learn from data.
Deep Learning → Using deep neural networks to learn complex patterns.

5. Types of Machine Learning
Machine Learning can broadly be divided into three major types.
5.1 Supervised Learning
In supervised learning, the model learns from labeled data.
The dataset contains both:
Input features
Correct output/target
Examples
House price prediction
Student score prediction
Email spam detection
Disease classification
Example
Study Hours → Student Score
2 hours     → 55
4 hours     → 70
6 hours     → 85
The model learns the relationship between study hours and scores.

5.2 Unsupervised Learning
In unsupervised learning, the data does not have predefined labels.
The model tries to discover patterns or groups within the data.
Examples
Customer segmentation
Grouping similar documents
Finding patterns in customer behavior
One common technique is clustering.

5.3 Reinforcement Learning
In reinforcement learning, an agent learns by interacting with an environment.
The agent receives:
Rewards for good actions
Penalties for undesirable actions
The goal is to learn a strategy that maximizes the total reward.
Examples
Game-playing AI
Robotics
Autonomous systems
Resource optimization

6. Real-World Applications of AI
Artificial Intelligence is used in many different areas.
Healthcare
AI can assist with:
Medical image analysis
Disease prediction
Patient monitoring
Medical decision support
Finance
AI and ML can be used for:
Fraud detection
Risk analysis
Credit assessment
Transaction monitoring
Education
AI can support:
Personalized learning
Automated feedback
Intelligent tutoring systems
Question generation
E-Commerce
AI is commonly used for:
Product recommendations
Customer behavior analysis
Search optimization
Chatbots
Transportation
AI can be used for:
Route optimization
Traffic prediction
Driver-assistance systems
Autonomous vehicle technologies
Entertainment
AI can provide:
Movie recommendations
Music recommendations
Personalized content
Natural Language Processing
AI can process and understand human language for:
Chatbots
Translation
Text summarization
Sentiment analysis
Speech recognition

7. Introduction to Python
Python is a high-level, interpreted programming language known for its simple syntax and readability.
Python is widely used in:
Artificial Intelligence
Machine Learning
Data Analysis
Web Development
Automation
Scientific Computing
Python is particularly popular in AI and ML because it has a large collection of libraries and frameworks.
Popular Python Libraries

Library
Purpose
NumPy
Numerical computing
Pandas
Data analysis
Matplotlib
Data visualization
Scikit-learn
Machine Learning
TensorFlow
Deep Learning
PyTorch
Deep Learning


8. Variables in Python
A variable is a name used to store a value in a program.
Example
name = "Sumera"
age = 20
cgpa = 9.35
is_student = True
In this example:
name stores a string.
age stores an integer.
cgpa stores a floating-point value.
is_student stores a Boolean value.

9. Python Data Types
Python provides several built-in data types.
Integer
Used for whole numbers.
age = 20
Float
Used for decimal numbers.
cgpa = 9.35
String
Used for text.
name = "Sumera"
Boolean
Stores either True or False.
is_student = True
List
Stores multiple values.
numbers = [10, 20, 30, 40]
Tuple
Stores an ordered collection of values.
coordinates = (10, 20)
Set
Stores unique values.
numbers = {1, 2, 3, 4}
Dictionary
Stores data in key-value pairs.
student = {
    "name": "Sumera",
    "age": 20
}

10. Input and Output in Python
The input() function is used to receive information from the user.
The print() function is used to display information.
Example
name = input("Enter your name: ")
print("Hello", name)
age = int(input("Enter your age: "))
print("Age:", age)

11. Conditional Statements
Conditional statements allow a program to make decisions.
Python provides:
if
elif
else
Example
marks = 85

if marks >= 90:
    print("Excellent")
elif marks >= 60:
    print("Good")
else:
    print("Needs Improvement")
The program checks the condition and executes the appropriate block of code.

12. Loops in Python
Loops are used to execute a block of code repeatedly.
Python mainly provides:
for loop
while loop
12.1 For Loop
A for loop is useful when we want to iterate over a sequence or a known range of values.
Example
for i in range(1, 6):
    print(i)
Output:
1
2
3
4
5

12.2 While Loop
A while loop continues executing as long as a condition is true.
Example
i = 1
while i <= 5:
    print(i)
    i += 1
Output:
1
2
3
4
5

13. Lists in Python
A list is a collection that can store multiple values.
Example
fruits = ["Apple", "Banana", "Mango"]
print(fruits[0])
Output:
Apple
Adding an Element
  fruits.append("Orange")
Removing an Element
fruits.remove("Banana")
Finding Length
print(len(fruits))
Iterating Through a List
for fruit in fruits:
    print(fruit)

14. Functions in Python
A function is a reusable block of code designed to perform a specific task.
Functions help make programs:
Organized
Reusable
Easier to understand
Easier to maintain
Example
def add(a, b):
    return a + b
result = add(10, 20)
print(result)
Output:
30
Here:
def is used to define a function.
a and b are parameters.
return sends the result back to the caller.

15. Beginner Python Programs Practiced
As part of this module, I practiced several beginner-level Python programs.
Program 1: Check Even or Odd
number = int(input("Enter a number: "))
if number % 2 == 0:
    print("Even number")
else:
    print("Odd number")

Program 2: Check Positive, Negative or Zero
number = int(input("Enter a number: "))
if number > 0:
    print("Positive number")
elif number < 0:
    print("Negative number")
else:
    print("Zero")

Program 3: Print Numbers Using a Loop
for i in range(1, 11):
    print(i)

Program 4: Find the Sum of a List
numbers = [10, 20, 30, 40, 50]
total = 0
for number in numbers:
    total += number
print("Sum:", total)
Output:
Sum: 150

Program 5: Find the Largest Number
numbers = [25, 10, 45, 30, 15]
largest = numbers[0]
for number in numbers:
    if number > largest:
        largest = number
print("Largest number:", largest)
Output:
Largest number: 45

Program 6: Simple Calculator
a = float(input("Enter first number: "))
b = float(input("Enter second number: "))
print("Addition:", a + b)
print("Subtraction:", a - b)
print("Multiplication:", a * b)
if b != 0:
print("Division:", a / b)
else:
    print("Cannot divide by zero")

Program 7: Check Prime Number
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

Program 8: Fibonacci Series
n = int(input("Enter number of terms: "))
a = 0
b = 1
for i in range(n):
    print(a, end=" ")
    a, b = b, a + b

Program 9: Function to Find Square
def square(number):
    return number * number
result = square(5)
print("Square:", result)
Output:
Square: 25

16. Key Learnings
Through this module, I learned the fundamental concepts of Artificial Intelligence, Machine Learning and Deep Learning.
I understood the relationship between AI, ML and Deep Learning and explored different applications of AI in real-world domains such as healthcare, finance, education, e-commerce and transportation.
I also learned the fundamentals of Python programming, including:
Variables
Data types
Input and output
Conditional statements
For loops
While loops
Lists
Functions
I practiced these concepts by implementing beginner-friendly Python programs such as an even/odd checker, calculator, prime number checker, Fibonacci series and list operations.
These concepts provide a foundation for learning data analysis, machine learning and AI-based applications in the upcoming modules.

17. Conclusion
Module 1 provided me with a foundation in Artificial Intelligence and Python programming.
I learned how AI systems are used in real-world applications and understood the differences between Artificial Intelligence, Machine Learning and Deep Learning.
I also strengthened my Python programming fundamentals by writing and executing basic programs using variables, conditional statements, loops, lists and functions.
The knowledge gained from this module will help me progress toward data analysis, machine learning and AI project development in the upcoming modules of the Codomax AI/ML Internship.
📌 Module 1 Completion
Topics Covered:
✅ Artificial Intelligence fundamentals
✅ Machine Learning fundamentals
✅ Deep Learning fundamentals
✅ AI vs ML vs Deep Learning
✅ Real-world AI applications
✅ Python fundamentals
✅ Variables and data types
✅ Conditional statements
✅ Loops
✅ Lists
✅ Functions
✅ Beginner Python programs
GitHub Repository:
 https://github.com/09sumera/codomax-ai-ml-internship/tree/main/module1-python-basics
Learning Notes:
 https://docs.google.com/document/d/1wD6hGJkDxJ02lOYrf8FgWHyYBf8zxaWML1QuN7gLSxo/edit?usp=sharing


