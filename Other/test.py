# Variables
# int - 1,2,3,4,5,
# flot - 1.2,1.4
# string - "hi"
# char - 'h'
# bool - False or True

# print("Hello world")

a = 5 # int
b = 4.5 # float

# c = 'HI'

# c = a + b

# c = "a"+"bwsfwedf"

# print(c)

# Operators

# + * - /
# = < > != >= <=

# country = "Japan"
# condition statements

# if country == 'japan':
#     # then
#     continent = 'Asia'
# elif country == 'USA':
#     continent = 'NAM'
# else:
#     continent = 'other'


# a = 5
# b = 4.5

# # operation = '+'
# operation = 'AAAA'

# if operation == '+': # False
#     print("You have choosen " + operation)
#     print(a + b)
# elif operation == '-': # True
#     print("You have choosen " + operation)
#     print(a - b)
# elif operation == '*':
#     print("You have choosen " + operation)
#     print(a * b)
# elif operation == '/':
#     print("You have choosen " + operation)
#     print(a / b)    
# else:
#     print("You have choosen " + operation)
#     print("Invalid operator")

# Loops and range

# a = 5
# b = 4.5

# for i in range(1,11): # start = 0, stop = 10 (excluding) 1,2,3,4,5,6,7,8,9,10
#     print("Iteration--> ", i)
#     print('HI') # operation

# while
# a = 5

# while a != 0:
#     print("Iteration--> ", a)
#     a = a - 1

# Data Structures - Lists, Tuples, Sets, Dictionary

# Lists

# a = [10,3,4,6,6] # mutable, allow duplicates, follows order
# 0,1,2,3,4
# index, value

# i want 3 from above
# print(a[2] + 6)

# b = [50] # [10, [10,3,4,6,6]]

# c = b + a
# a[1] = 1000
# print(a)

# a = [10,3,4,6,6]

# for i in a:
#     print("Iteration--> ", i)
#     print('HI') # operation
#     print("mail sent")

# Tuple
# a = (10,3,4,6,6) # immutable, allow duplicates, follows order

# print(a[0:5])

# b = (1,2,3)

# c = a + b
# print(c)

# Sets - # mutable, doesn't allow duplicates, not follows order
# a = {1,2,3,4,4}
# it will be created a in memory as set

# print(a)

# states = ['A', 'B', 'C', 'B']

# unique_states = set(states)

# print(states)
# print(unique_states)

# Dictionary - mutable to values by keys, doesn't allow duplicate keys,
#  order will not be present but based on keys

# apple : "AAA"

# {key : value} # key value pairs

# student = {
#     'student': 'A',
#     'grade' : 10,
#     'school' : 'ABC'
# }

# print(student)

# student['location'] = 'XYZ' # new key
# student['grade'] = 12  # existing key

# print(student)

# List comprehensions

# a = [10,20,30] # X by 3
# # b = [30, 60, 90] 

# c = { i*3 for i in a } # {operation iteration-loop}

# print(c)

# b = []
# for i in a:
#     b.append(i*3)

# print(b)


# functions

# a = [10,20,30]

# b = []

# for i in a:
#     b.append(i*3)

# print(b)


# def list_multiplier(x, multiplier=3):
   
#     b = []
#     for i in x:
#         b.append(i * multiplier)

#     return b

# a = [10,20,30]
# n = [[11,2,4,[12,34]],[1,21,23]]


# print(list_multiplier(a,5))



# Even or Odd: Take a number from the user and print whether it is even or odd.

# def even_odd(a):
#     if a%2 == 0:
#         return "Even"
#     else:
#         return "Odd"
    
# print(even_odd(11))

# 10/2 = 0

# 11/2 = 1

# 11%2 = 1
        

# def print1_10(start, end):
#     for i in range(start, end):
#         print(i)

# print1_10(1, 21)


# Exception handling

def even_or_odd(a):
    try:
        # peform operation/any code
        # pass
        print("You have entered -> ", a)
        
        if a%2 == 0:
            print("EVEN")
        else:
            print("ODD")

    except Exception as e:
        print(e)
        print("Error occured")

    finally:
        print("add")

# a = int(input("Enter the number:"))

# even_or_odd(a)

# Modules import

import math # all import
import os
import json
import time
import calendar

from math import sqrt # absolute import

# print(sqrt(25))

# OOP

# Person records - 1000 people in tokyo - Org
# properties
# name
# age
# gender
# location
# profession

# # methods
# greet() = "Hello"
# bye() = "Bye"


# # Employee records - company A
# name
# age
# gender
# location
# profession,

# # methods
# greet() = "Hello"
# bye() = "Bye"

# +
# employee_id,
# designation


class Person:
    # constructor
    def __init__(self, name, age, gender, location, profession):
        self.name = name
        self.age = age
        self.gender = gender
        self.location  = location
        self.profession = profession

    def greet(self):
        print(f"HI I am {self.name}")

    def bye(self):
        print(f"HI I am {self.name} and from {self.location}")

# name, age, gender, location, profession
# p1 = Person('Prakash', '28', 'Male', 'India', 'Mentor')
# p2 = Person('Nanami', '16', 'Male', 'Singapore', 'Student')
# p3 = Person('Nanami', '16', 'Male', 'Singapore', 'Student')
# p4 = Person('Nanami', '16', 'Male', 'Singapore', 'Student')
# p5 = Person('Nanami', '16', 'Male', 'Singapore', 'Student')

# p1.greet()
# p1.bye()

class Employee(Person):
    def __init__(self, name, age, gender, location, profession, employee_id, designation):
        super().__init__(name, age, gender, location, profession)
        self.employee_id = employee_id
        self.designation  = designation

    def greet2(self):
        print(f"I am a subclass of Person with employee id {self.employee_id}")

# p1 = Employee('Prakash', '28', 'Male', 'India', 'Mentor', 1, "ABC")
p1 = Person('Prakash', '28', 'Male', 'India', 'Mentor')


    
















    







