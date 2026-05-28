"""
Smart Roadmap Generator Engine
Rule-based personalized roadmap generation logic
Generates day-wise study plans based on skill, level, hours, and duration
"""

from datetime import date, timedelta
from .models import Skill, Topic, Resource, Roadmap, RoadmapTask


# ─── Curated Topic Data ────────────────────────────────────────────────────────

SKILL_TOPICS = {
    'dsa': {
        'beginner': [
            {
                'name': 'Arrays & Array Operations',
                'desc': 'Fundamentals of arrays, indexing, traversal, and common operations.',
                'task': 'Implement array creation, insertion, deletion. Solve 5 easy array problems on LeetCode.',
                'url': 'https://leetcode.com/tag/array/',
                'resource': 'LeetCode Array Problems',
                'difficulty': 1, 'hours': 1.5, 'xp': 20
            },
            {
                'name': 'Strings & String Manipulation',
                'desc': 'String operations, palindromes, anagrams, and pattern matching basics.',
                'task': 'Practice reverse string, check palindrome, count vowels. Solve 5 string problems.',
                'url': 'https://leetcode.com/tag/string/',
                'resource': 'LeetCode String Problems',
                'difficulty': 1, 'hours': 1.5, 'xp': 20
            },
            {
                'name': 'Linked Lists — Singly',
                'desc': 'Node structure, traversal, insertion, and deletion in singly linked lists.',
                'task': 'Implement a singly linked list from scratch. Reverse a linked list.',
                'url': 'https://visualgo.net/en/list',
                'resource': 'VisuAlgo Linked Lists',
                'difficulty': 2, 'hours': 2.0, 'xp': 25
            },
            {
                'name': 'Stacks — Concepts & Implementation',
                'desc': 'LIFO principle, stack using arrays and linked lists, real-world uses.',
                'task': 'Implement stack. Solve: valid parentheses, min stack problems.',
                'url': 'https://leetcode.com/tag/stack/',
                'resource': 'LeetCode Stack Problems',
                'difficulty': 2, 'hours': 1.5, 'xp': 20
            },
            {
                'name': 'Queues — Concepts & Implementation',
                'desc': 'FIFO principle, circular queue, deque, and priority queue introduction.',
                'task': 'Implement queue with two stacks. Solve 3 queue problems.',
                'url': 'https://leetcode.com/tag/queue/',
                'resource': 'LeetCode Queue Problems',
                'difficulty': 2, 'hours': 1.5, 'xp': 20
            },
            {
                'name': 'Recursion & Backtracking Basics',
                'desc': 'Recursive thinking, base cases, recursion tree, factorial, fibonacci.',
                'task': 'Implement factorial, fibonacci, power function recursively. Trace recursion trees.',
                'url': 'https://www.geeksforgeeks.org/recursion/',
                'resource': 'GeeksForGeeks Recursion Guide',
                'difficulty': 2, 'hours': 2.0, 'xp': 30
            },
            {
                'name': 'Binary Search',
                'desc': 'Divide and conquer approach for sorted arrays. Time complexity O(log n).',
                'task': 'Implement binary search iteratively and recursively. Solve 5 binary search problems.',
                'url': 'https://leetcode.com/tag/binary-search/',
                'resource': 'LeetCode Binary Search',
                'difficulty': 2, 'hours': 1.5, 'xp': 25
            },
            {
                'name': 'Sorting Algorithms',
                'desc': 'Bubble sort, selection sort, insertion sort, merge sort, quick sort.',
                'task': 'Implement all 5 sorting algorithms. Compare time complexity.',
                'url': 'https://visualgo.net/en/sorting',
                'resource': 'VisuAlgo Sorting Visualizer',
                'difficulty': 2, 'hours': 2.5, 'xp': 30
            },
            {
                'name': 'Hash Tables & Hashing',
                'desc': 'Hash functions, collision handling, chaining, open addressing.',
                'task': 'Implement a hash map from scratch. Solve: two-sum, group anagrams.',
                'url': 'https://leetcode.com/tag/hash-table/',
                'resource': 'LeetCode Hash Table',
                'difficulty': 2, 'hours': 2.0, 'xp': 25
            },
            {
                'name': 'Trees — Binary Trees',
                'desc': 'Tree structure, traversals (in/pre/post-order), height, depth.',
                'task': 'Implement binary tree. Write all traversals recursively and iteratively.',
                'url': 'https://leetcode.com/tag/tree/',
                'resource': 'LeetCode Tree Problems',
                'difficulty': 3, 'hours': 2.5, 'xp': 35
            },
            {
                'name': 'Binary Search Trees',
                'desc': 'BST properties, insert, delete, search, validation.',
                'task': 'Implement BST. Validate BST, find kth smallest element.',
                'url': 'https://leetcode.com/tag/binary-search-tree/',
                'resource': 'LeetCode BST',
                'difficulty': 3, 'hours': 2.0, 'xp': 35
            },
            {
                'name': 'Graphs — BFS & DFS',
                'desc': 'Graph representation (adjacency list/matrix), BFS, DFS traversal.',
                'task': 'Implement graph BFS and DFS. Solve: number of islands, clone graph.',
                'url': 'https://leetcode.com/tag/graph/',
                'resource': 'LeetCode Graph Problems',
                'difficulty': 3, 'hours': 2.5, 'xp': 40
            },
            {
                'name': 'Dynamic Programming — Introduction',
                'desc': 'Memoization vs tabulation, optimal substructure, overlapping subproblems.',
                'task': 'Solve fibonacci with DP. Implement 0/1 knapsack, longest common subsequence.',
                'url': 'https://leetcode.com/tag/dynamic-programming/',
                'resource': 'LeetCode DP Problems',
                'difficulty': 4, 'hours': 3.0, 'xp': 50
            },
            {
                'name': 'Greedy Algorithms',
                'desc': 'Greedy choice property, activity selection, fractional knapsack.',
                'task': 'Implement activity selection. Solve: jump game, interval scheduling.',
                'url': 'https://leetcode.com/tag/greedy/',
                'resource': 'LeetCode Greedy',
                'difficulty': 3, 'hours': 2.0, 'xp': 35
            },
            {
                'name': 'Mixed Practice & Mock Test',
                'desc': 'Consolidate all DSA concepts with timed mock problems.',
                'task': 'Solve a 2-hour mock contest on LeetCode or Codeforces. Review weak areas.',
                'url': 'https://leetcode.com/problemset/',
                'resource': 'LeetCode Practice Set',
                'difficulty': 3, 'hours': 2.0, 'xp': 60
            },
        ],
        'intermediate': [
            {
                'name': 'Advanced Sorting — Heap Sort, Radix Sort',
                'desc': 'Heap sort using max-heap, counting sort, radix sort, and their use-cases.',
                'task': 'Implement heap sort and radix sort. Analyze when each is preferred.',
                'url': 'https://visualgo.net/en/sorting',
                'resource': 'VisuAlgo Advanced Sorting',
                'difficulty': 3, 'hours': 2.0, 'xp': 30
            },
            {
                'name': 'Heaps & Priority Queues',
                'desc': 'Min/max heaps, heapify, heap operations, top-K problems.',
                'task': 'Implement a min-heap. Solve: find kth largest, merge k sorted lists.',
                'url': 'https://leetcode.com/tag/heap-priority-queue/',
                'resource': 'LeetCode Heap Problems',
                'difficulty': 3, 'hours': 2.5, 'xp': 35
            },
            {
                'name': 'Graph Algorithms — Dijkstra',
                'desc': 'Shortest path algorithms: Dijkstra, Bellman-Ford for weighted graphs.',
                'task': 'Implement Dijkstra with priority queue. Solve network delay time problem.',
                'url': 'https://leetcode.com/tag/shortest-path/',
                'resource': 'LeetCode Shortest Path',
                'difficulty': 4, 'hours': 3.0, 'xp': 45
            },
            {
                'name': 'Union Find / Disjoint Set Union',
                'desc': 'Union-Find data structure, path compression, union by rank.',
                'task': 'Implement DSU. Solve: number of provinces, accounts merge.',
                'url': 'https://leetcode.com/tag/union-find/',
                'resource': 'LeetCode Union Find',
                'difficulty': 3, 'hours': 2.0, 'xp': 35
            },
            {
                'name': 'Tries (Prefix Trees)',
                'desc': 'Trie data structure for string search, autocomplete, word games.',
                'task': 'Implement trie. Solve: implement trie, word search II.',
                'url': 'https://leetcode.com/tag/trie/',
                'resource': 'LeetCode Trie',
                'difficulty': 3, 'hours': 2.5, 'xp': 40
            },
            {
                'name': 'Segment Trees & Fenwick Trees',
                'desc': 'Range query structures for sum, min, max with O(log n) updates.',
                'task': 'Implement segment tree for range sum query. Implement BIT (Fenwick tree).',
                'url': 'https://cp-algorithms.com/data_structures/segment_tree.html',
                'resource': 'CP-Algorithms Segment Tree',
                'difficulty': 4, 'hours': 3.0, 'xp': 50
            },
            {
                'name': 'Advanced DP — Interval & String DP',
                'desc': 'Matrix chain multiplication, palindrome partitioning, edit distance.',
                'task': 'Solve: edit distance, palindrome partitioning, burst balloons.',
                'url': 'https://leetcode.com/tag/dynamic-programming/',
                'resource': 'LeetCode Advanced DP',
                'difficulty': 4, 'hours': 3.0, 'xp': 55
            },
            {
                'name': 'Bit Manipulation',
                'desc': 'Bitwise operators, bit tricks, XOR properties, power of two.',
                'task': 'Implement count set bits, find single number, sum of two integers without +.',
                'url': 'https://leetcode.com/tag/bit-manipulation/',
                'resource': 'LeetCode Bit Manipulation',
                'difficulty': 3, 'hours': 2.0, 'xp': 35
            },
            {
                'name': 'Two Pointers & Sliding Window',
                'desc': 'Efficient techniques for array/string problems reducing O(n²) to O(n).',
                'task': 'Solve: container with most water, longest substring without repeating chars.',
                'url': 'https://leetcode.com/tag/sliding-window/',
                'resource': 'LeetCode Sliding Window',
                'difficulty': 3, 'hours': 2.5, 'xp': 40
            },
            {
                'name': 'Topological Sort & DAGs',
                'desc': 'Kahn\'s algorithm, DFS-based topological sort, cycle detection in DAGs.',
                'task': 'Implement topological sort. Solve: course schedule I & II.',
                'url': 'https://leetcode.com/tag/topological-sort/',
                'resource': 'LeetCode Topological Sort',
                'difficulty': 4, 'hours': 2.5, 'xp': 45
            },
        ],
    },
    'python': {
        'beginner': [
            {
                'name': 'Python Setup & Environment',
                'desc': 'Install Python, set up VS Code, understand REPL, write first script.',
                'task': 'Install Python 3.11+. Run hello world. Use print, variables, input().',
                'url': 'https://docs.python.org/3/tutorial/',
                'resource': 'Official Python Tutorial',
                'difficulty': 1, 'hours': 1.0, 'xp': 15
            },
            {
                'name': 'Data Types & Variables',
                'desc': 'int, float, str, bool, None. Type casting, variable naming rules.',
                'task': 'Create a program that takes user inputs and performs type conversions.',
                'url': 'https://realpython.com/python-data-types/',
                'resource': 'Real Python — Data Types',
                'difficulty': 1, 'hours': 1.5, 'xp': 15
            },
            {
                'name': 'Control Flow — If/Elif/Else',
                'desc': 'Conditional statements, comparison operators, logical operators.',
                'task': 'Build a grade calculator. Build a simple number guessing game.',
                'url': 'https://docs.python.org/3/tutorial/controlflow.html',
                'resource': 'Python Control Flow Docs',
                'difficulty': 1, 'hours': 1.5, 'xp': 15
            },
            {
                'name': 'Loops — for, while, comprehensions',
                'desc': 'Iteration with for and while, break/continue, list comprehensions.',
                'task': 'Print Fibonacci. Write fizzbuzz. Create a multiplication table.',
                'url': 'https://realpython.com/python-for-loop/',
                'resource': 'Real Python — Loops',
                'difficulty': 1, 'hours': 2.0, 'xp': 20
            },
            {
                'name': 'Functions & Scope',
                'desc': 'def, parameters, return, default args, *args, **kwargs, scope rules.',
                'task': 'Write 10 utility functions: max, min, factorial, is_prime, etc.',
                'url': 'https://realpython.com/defining-your-own-python-function/',
                'resource': 'Real Python — Functions',
                'difficulty': 2, 'hours': 2.0, 'xp': 25
            },
            {
                'name': 'Lists & Tuples',
                'desc': 'List operations, slicing, methods, nested lists, tuples vs lists.',
                'task': 'Implement a student grade tracker using lists.',
                'url': 'https://docs.python.org/3/tutorial/datastructures.html',
                'resource': 'Python Data Structures Docs',
                'difficulty': 1, 'hours': 1.5, 'xp': 20
            },
            {
                'name': 'Dictionaries & Sets',
                'desc': 'Dict creation, methods, iteration, nested dicts, sets, frozensets.',
                'task': 'Build a word frequency counter. Build a phonebook application.',
                'url': 'https://realpython.com/python-dicts/',
                'resource': 'Real Python — Dicts',
                'difficulty': 2, 'hours': 2.0, 'xp': 25
            },
            {
                'name': 'File I/O — Reading & Writing',
                'desc': 'open(), read/write modes, with statement, CSV basics.',
                'task': 'Build a contact manager that saves/loads from a text file.',
                'url': 'https://realpython.com/read-write-files-python/',
                'resource': 'Real Python — File I/O',
                'difficulty': 2, 'hours': 2.0, 'xp': 25
            },
            {
                'name': 'Exception Handling',
                'desc': 'try/except/finally, custom exceptions, raising exceptions.',
                'task': 'Add error handling to all previous programs.',
                'url': 'https://docs.python.org/3/tutorial/errors.html',
                'resource': 'Python Errors & Exceptions Docs',
                'difficulty': 2, 'hours': 1.5, 'xp': 20
            },
            {
                'name': 'OOP — Classes & Objects',
                'desc': 'Class definition, __init__, self, instance methods, class variables.',
                'task': 'Create a BankAccount class with deposit, withdraw, balance methods.',
                'url': 'https://realpython.com/python3-object-oriented-programming/',
                'resource': 'Real Python — OOP',
                'difficulty': 3, 'hours': 2.5, 'xp': 35
            },
            {
                'name': 'Inheritance & Polymorphism',
                'desc': 'Base and derived classes, method overriding, super(), MRO.',
                'task': 'Extend BankAccount with SavingsAccount and CheckingAccount classes.',
                'url': 'https://realpython.com/inheritance-composition-python/',
                'resource': 'Real Python — Inheritance',
                'difficulty': 3, 'hours': 2.0, 'xp': 30
            },
            {
                'name': 'Modules & Packages',
                'desc': 'import, from/import, __name__, creating packages, pip.',
                'task': 'Refactor your projects into modules. Install and use requests library.',
                'url': 'https://docs.python.org/3/tutorial/modules.html',
                'resource': 'Python Modules Docs',
                'difficulty': 2, 'hours': 1.5, 'xp': 20
            },
            {
                'name': 'Decorators & Lambda Functions',
                'desc': 'Higher-order functions, function decorators, lambda, map/filter.',
                'task': 'Write a timing decorator. Use map and filter on datasets.',
                'url': 'https://realpython.com/primer-on-python-decorators/',
                'resource': 'Real Python — Decorators',
                'difficulty': 3, 'hours': 2.0, 'xp': 30
            },
            {
                'name': 'Generators & Iterators',
                'desc': 'yield, generator expressions, custom iterators with __iter__/__next__.',
                'task': 'Build an infinite Fibonacci generator. Process large files with generators.',
                'url': 'https://realpython.com/introduction-to-python-generators/',
                'resource': 'Real Python — Generators',
                'difficulty': 3, 'hours': 2.0, 'xp': 30
            },
            {
                'name': 'Final Project — Python CLI App',
                'desc': 'Build a complete CLI application applying all concepts learned.',
                'task': 'Build a Task Manager CLI with file persistence and OOP design.',
                'url': 'https://realpython.com/',
                'resource': 'Real Python Project Ideas',
                'difficulty': 3, 'hours': 3.0, 'xp': 75
            },
        ],
    },
    'webdev': {
        'beginner': [
            {
                'name': 'HTML Foundations',
                'desc': 'Document structure, semantic tags, headings, paragraphs, links, images.',
                'task': 'Build a personal webpage with your bio, skills, and contact info.',
                'url': 'https://developer.mozilla.org/en-US/docs/Learn/HTML',
                'resource': 'MDN HTML Guide',
                'difficulty': 1, 'hours': 1.5, 'xp': 15
            },
            {
                'name': 'HTML Forms & Tables',
                'desc': 'Form elements, input types, validation, tables, and accessibility.',
                'task': 'Build a registration form and a class schedule table.',
                'url': 'https://developer.mozilla.org/en-US/docs/Learn/Forms',
                'resource': 'MDN Forms Guide',
                'difficulty': 1, 'hours': 1.5, 'xp': 15
            },
            {
                'name': 'CSS Basics — Selectors & Box Model',
                'desc': 'CSS syntax, selectors, box model, margin, padding, border.',
                'task': 'Style your HTML page with custom fonts, colors, and spacing.',
                'url': 'https://developer.mozilla.org/en-US/docs/Learn/CSS',
                'resource': 'MDN CSS Basics',
                'difficulty': 1, 'hours': 2.0, 'xp': 20
            },
            {
                'name': 'CSS Layouts — Flexbox',
                'desc': 'Flexbox model, justify-content, align-items, flex-direction, wrap.',
                'task': 'Build a navigation bar and a card grid using Flexbox.',
                'url': 'https://flexboxfroggy.com/',
                'resource': 'Flexbox Froggy Game',
                'difficulty': 2, 'hours': 2.0, 'xp': 25
            },
            {
                'name': 'CSS Grid',
                'desc': 'Grid container, rows/columns, areas, responsive design patterns.',
                'task': 'Recreate a magazine-style layout using CSS Grid.',
                'url': 'https://cssgridgarden.com/',
                'resource': 'CSS Grid Garden Game',
                'difficulty': 2, 'hours': 2.0, 'xp': 25
            },
            {
                'name': 'Responsive Design & Media Queries',
                'desc': 'Mobile-first design, breakpoints, viewport, responsive images.',
                'task': 'Make your website fully responsive for mobile, tablet, desktop.',
                'url': 'https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design',
                'resource': 'MDN Responsive Design',
                'difficulty': 2, 'hours': 2.0, 'xp': 25
            },
            {
                'name': 'JavaScript Fundamentals',
                'desc': 'Variables, data types, operators, conditionals, loops in JS.',
                'task': 'Build a temperature converter. Build a simple calculator.',
                'url': 'https://javascript.info/',
                'resource': 'JavaScript.info',
                'difficulty': 2, 'hours': 2.5, 'xp': 30
            },
            {
                'name': 'DOM Manipulation',
                'desc': 'querySelector, innerHTML, addEventListener, createElement, classList.',
                'task': 'Build an interactive to-do list with add/delete/complete functionality.',
                'url': 'https://javascript.info/document',
                'resource': 'JavaScript.info DOM',
                'difficulty': 2, 'hours': 2.5, 'xp': 30
            },
            {
                'name': 'JavaScript Functions & Events',
                'desc': 'Arrow functions, callbacks, event propagation, form events.',
                'task': 'Build a quiz app with score tracking and timer.',
                'url': 'https://javascript.info/events',
                'resource': 'JavaScript.info Events',
                'difficulty': 2, 'hours': 2.0, 'xp': 25
            },
            {
                'name': 'Fetch API & AJAX',
                'desc': 'Promises, async/await, fetch(), JSON, REST API consumption.',
                'task': 'Build a weather app using OpenWeatherMap API.',
                'url': 'https://javascript.info/network',
                'resource': 'JavaScript.info Networking',
                'difficulty': 3, 'hours': 2.5, 'xp': 35
            },
            {
                'name': 'Bootstrap 5 Framework',
                'desc': 'Grid system, components, utilities, responsive classes.',
                'task': 'Rebuild your portfolio page using Bootstrap 5.',
                'url': 'https://getbootstrap.com/docs/5.3/',
                'resource': 'Bootstrap 5 Docs',
                'difficulty': 2, 'hours': 2.0, 'xp': 25
            },
            {
                'name': 'Git & Version Control',
                'desc': 'Git init, add, commit, branch, merge, GitHub, pull requests.',
                'task': 'Put all projects on GitHub. Make your first pull request.',
                'url': 'https://learngitbranching.js.org/',
                'resource': 'Learn Git Branching',
                'difficulty': 2, 'hours': 2.0, 'xp': 25
            },
            {
                'name': 'Node.js & npm Basics',
                'desc': 'Node runtime, npm, package.json, modules, Express basics.',
                'task': 'Build a simple Express server with 3 routes.',
                'url': 'https://nodejs.org/en/learn/',
                'resource': 'Node.js Docs',
                'difficulty': 3, 'hours': 2.5, 'xp': 35
            },
            {
                'name': 'Databases — SQL Basics',
                'desc': 'SQL SELECT, INSERT, UPDATE, DELETE, JOIN, with SQLite.',
                'task': 'Design a blog DB schema. Write queries for CRUD operations.',
                'url': 'https://sqliteonline.com/',
                'resource': 'SQLite Online IDE',
                'difficulty': 3, 'hours': 2.5, 'xp': 35
            },
            {
                'name': 'Capstone — Full-Stack Mini App',
                'desc': 'Build and deploy a full-stack web app combining all skills.',
                'task': 'Build a note-taking app with Node.js backend + SQLite + frontend.',
                'url': 'https://vercel.com/',
                'resource': 'Deploy on Vercel',
                'difficulty': 4, 'hours': 4.0, 'xp': 80
            },
        ],
    },
    'aiml': {
        'beginner': [
            {
                'name': 'Python for ML — NumPy',
                'desc': 'Arrays, operations, broadcasting, linear algebra with NumPy.',
                'task': 'Complete NumPy exercises: array creation, slicing, matrix ops.',
                'url': 'https://numpy.org/learn/',
                'resource': 'NumPy Official Learn',
                'difficulty': 2, 'hours': 2.0, 'xp': 25
            },
            {
                'name': 'Data Manipulation with Pandas',
                'desc': 'DataFrames, series, groupby, merge, missing data handling.',
                'task': 'Load the Titanic dataset. Clean, analyze, and extract insights.',
                'url': 'https://pandas.pydata.org/docs/getting_started/',
                'resource': 'Pandas Getting Started',
                'difficulty': 2, 'hours': 2.5, 'xp': 30
            },
            {
                'name': 'Data Visualization — Matplotlib & Seaborn',
                'desc': 'Line plots, bar charts, histograms, scatter plots, heatmaps.',
                'task': 'Create 10 different visualizations from the Titanic dataset.',
                'url': 'https://seaborn.pydata.org/tutorial.html',
                'resource': 'Seaborn Tutorial',
                'difficulty': 2, 'hours': 2.0, 'xp': 25
            },
            {
                'name': 'ML Fundamentals & Scikit-Learn',
                'desc': 'Supervised vs unsupervised, train/test split, cross-validation.',
                'task': 'Run first ML model: predict Titanic survival with Logistic Regression.',
                'url': 'https://scikit-learn.org/stable/getting_started.html',
                'resource': 'Scikit-Learn Getting Started',
                'difficulty': 2, 'hours': 2.5, 'xp': 30
            },
            {
                'name': 'Linear Regression',
                'desc': 'Simple and multiple linear regression, gradient descent, MSE, R².',
                'task': 'Predict house prices using linear regression. Plot the regression line.',
                'url': 'https://scikit-learn.org/stable/modules/linear_model.html',
                'resource': 'Scikit-Learn Linear Models',
                'difficulty': 2, 'hours': 2.0, 'xp': 30
            },
            {
                'name': 'Classification — Logistic Regression',
                'desc': 'Binary classification, sigmoid function, decision boundary, metrics.',
                'task': 'Classify spam emails. Evaluate with precision, recall, F1.',
                'url': 'https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression',
                'resource': 'Scikit-Learn Logistic Regression',
                'difficulty': 3, 'hours': 2.5, 'xp': 35
            },
            {
                'name': 'Decision Trees & Random Forests',
                'desc': 'Decision tree splits, information gain, ensemble methods, bagging.',
                'task': 'Build a random forest classifier. Compare with decision tree.',
                'url': 'https://scikit-learn.org/stable/modules/tree.html',
                'resource': 'Scikit-Learn Decision Trees',
                'difficulty': 3, 'hours': 2.5, 'xp': 35
            },
            {
                'name': 'Clustering — K-Means',
                'desc': 'Unsupervised learning, cluster centroids, elbow method.',
                'task': 'Cluster mall customers by spending behavior. Visualize clusters.',
                'url': 'https://scikit-learn.org/stable/modules/clustering.html',
                'resource': 'Scikit-Learn Clustering',
                'difficulty': 3, 'hours': 2.0, 'xp': 30
            },
            {
                'name': 'Feature Engineering & Selection',
                'desc': 'Encoding categorical vars, scaling, feature importance, PCA.',
                'task': 'Apply feature engineering to improve your previous models by 5%+.',
                'url': 'https://scikit-learn.org/stable/modules/preprocessing.html',
                'resource': 'Scikit-Learn Preprocessing',
                'difficulty': 3, 'hours': 2.5, 'xp': 35
            },
            {
                'name': 'Neural Networks Introduction',
                'desc': 'Perceptron, multilayer networks, activation functions, backprop.',
                'task': 'Build a neural network to classify handwritten digits (MNIST).',
                'url': 'https://www.tensorflow.org/tutorials',
                'resource': 'TensorFlow Tutorials',
                'difficulty': 4, 'hours': 3.0, 'xp': 50
            },
            {
                'name': 'Deep Learning with Keras',
                'desc': 'Sequential model, dense layers, compile, fit, evaluate.',
                'task': 'Build a CNN to classify CIFAR-10 images. Achieve 70%+ accuracy.',
                'url': 'https://keras.io/getting_started/',
                'resource': 'Keras Getting Started',
                'difficulty': 4, 'hours': 3.0, 'xp': 50
            },
            {
                'name': 'Natural Language Processing Basics',
                'desc': 'Tokenization, stemming, TF-IDF, sentiment analysis.',
                'task': 'Build a movie review sentiment classifier using NLP.',
                'url': 'https://www.nltk.org/book/',
                'resource': 'NLTK Book',
                'difficulty': 3, 'hours': 2.5, 'xp': 40
            },
            {
                'name': 'Model Deployment with Flask',
                'desc': 'Pickle model, Flask API endpoint, serve predictions.',
                'task': 'Deploy your best ML model as a REST API.',
                'url': 'https://flask.palletsprojects.com/',
                'resource': 'Flask Documentation',
                'difficulty': 3, 'hours': 2.5, 'xp': 40
            },
            {
                'name': 'ML Project — End to End',
                'desc': 'Complete ML pipeline: data → cleaning → training → evaluation → deploy.',
                'task': 'Build and deploy a complete ML project on Kaggle or Hugging Face.',
                'url': 'https://kaggle.com/',
                'resource': 'Kaggle Platform',
                'difficulty': 4, 'hours': 4.0, 'xp': 80
            },
            {
                'name': 'Review & Portfolio Presentation',
                'desc': 'Document all projects, write README files, publish on GitHub.',
                'task': 'Clean up all projects. Write detailed READMEs. Post on LinkedIn.',
                'url': 'https://github.com/',
                'resource': 'GitHub Portfolio',
                'difficulty': 2, 'hours': 2.0, 'xp': 50
            },
        ],
    },
    'competitive': {
        'beginner': [
            {
                'name': 'Competitive Programming Setup',
                'desc': 'Set up Codeforces, AtCoder. Learn contest rules, input/output format.',
                'task': 'Create accounts on Codeforces and LeetCode. Solve first 5 A-level problems.',
                'url': 'https://codeforces.com/',
                'resource': 'Codeforces Platform',
                'difficulty': 1, 'hours': 1.5, 'xp': 20
            },
            {
                'name': 'Complexity Analysis — Big O',
                'desc': 'Time/space complexity, Big O, Omega, Theta, best/worst/average case.',
                'task': 'Analyze complexity of your previous solutions. Optimize if possible.',
                'url': 'https://www.bigocheatsheet.com/',
                'resource': 'Big O Cheat Sheet',
                'difficulty': 2, 'hours': 2.0, 'xp': 25
            },
            {
                'name': 'Brute Force & Complete Search',
                'desc': 'Generate all possibilities, recursion for combinations/permutations.',
                'task': 'Solve 10 brute force problems on Codeforces (rating 800-1200).',
                'url': 'https://codeforces.com/problemset?tags=brute%20force',
                'resource': 'Codeforces Brute Force',
                'difficulty': 2, 'hours': 2.5, 'xp': 30
            },
            {
                'name': 'Greedy Approach in Contests',
                'desc': 'Greedy strategies, proof by exchange argument, common greedy patterns.',
                'task': 'Solve 10 greedy problems. Learn to prove greedy correctness.',
                'url': 'https://codeforces.com/problemset?tags=greedy',
                'resource': 'Codeforces Greedy',
                'difficulty': 2, 'hours': 2.5, 'xp': 30
            },
            {
                'name': 'Prefix Sums & Difference Arrays',
                'desc': 'Prefix sum arrays for range queries, 2D prefix sums.',
                'task': 'Solve 8 prefix sum problems. Implement 2D prefix sum.',
                'url': 'https://codeforces.com/edu/course/2',
                'resource': 'Codeforces EDU',
                'difficulty': 2, 'hours': 2.0, 'xp': 25
            },
            {
                'name': 'Binary Search in Competitions',
                'desc': 'Binary search on answers, ternary search, parametric binary search.',
                'task': 'Solve 8 binary search problems including "binary search on answer" type.',
                'url': 'https://codeforces.com/problemset?tags=binary+search',
                'resource': 'Codeforces Binary Search',
                'difficulty': 3, 'hours': 2.5, 'xp': 35
            },
            {
                'name': 'Two Pointers in Competitions',
                'desc': 'Same-direction and opposite-direction pointers for array problems.',
                'task': 'Solve 8 two-pointer problems.',
                'url': 'https://codeforces.com/problemset?tags=two+pointers',
                'resource': 'Codeforces Two Pointers',
                'difficulty': 3, 'hours': 2.0, 'xp': 30
            },
            {
                'name': 'Graph Basics in Competitions',
                'desc': 'BFS/DFS in contest context, tree problems, connected components.',
                'task': 'Solve 10 graph problems. Participate in 1 virtual contest.',
                'url': 'https://codeforces.com/problemset?tags=graphs',
                'resource': 'Codeforces Graphs',
                'difficulty': 3, 'hours': 3.0, 'xp': 40
            },
            {
                'name': 'Dynamic Programming in Contests',
                'desc': 'Standard DP patterns for competitions, DP optimization basics.',
                'task': 'Solve 10 DP problems up to Codeforces rating 1600.',
                'url': 'https://codeforces.com/problemset?tags=dp',
                'resource': 'Codeforces DP Problems',
                'difficulty': 4, 'hours': 3.5, 'xp': 55
            },
            {
                'name': 'Math for Competitive Programming',
                'desc': 'Modular arithmetic, GCD, LCM, prime sieve, combinatorics basics.',
                'task': 'Implement Sieve of Eratosthenes. Solve 8 math problems.',
                'url': 'https://cp-algorithms.com/algebra/',
                'resource': 'CP-Algorithms Algebra',
                'difficulty': 3, 'hours': 2.5, 'xp': 35
            },
            {
                'name': 'String Algorithms',
                'desc': 'KMP, Z-function, string hashing for fast pattern matching.',
                'task': 'Implement KMP. Solve 8 string algorithm problems.',
                'url': 'https://cp-algorithms.com/string/kmp.html',
                'resource': 'CP-Algorithms KMP',
                'difficulty': 4, 'hours': 3.0, 'xp': 45
            },
            {
                'name': 'Virtual Contest Practice',
                'desc': 'Simulate real contests using past Codeforces rounds.',
                'task': 'Participate in 3 virtual contests. Analyze each solution after.',
                'url': 'https://codeforces.com/contests',
                'resource': 'Codeforces Virtual Contests',
                'difficulty': 3, 'hours': 3.0, 'xp': 60
            },
            {
                'name': 'Advanced Data Structures',
                'desc': 'Segment tree, BIT, sparse table for competitive use.',
                'task': 'Implement segment tree with lazy propagation. Solve 5 problems.',
                'url': 'https://cp-algorithms.com/data_structures/',
                'resource': 'CP-Algorithms Data Structures',
                'difficulty': 4, 'hours': 3.0, 'xp': 50
            },
            {
                'name': 'Contest Strategy & Time Management',
                'desc': 'How to read problems, choose which to attempt, upsolving strategy.',
                'task': 'Write a reflection on past contests. Make a contest strategy document.',
                'url': 'https://codeforces.com/blog/entry/62730',
                'resource': 'Codeforces Strategy Blog',
                'difficulty': 2, 'hours': 1.5, 'xp': 25
            },
            {
                'name': 'Final Mock Competition',
                'desc': 'Full 2-hour mock competition to test all skills.',
                'task': 'Compete in a live or virtual Codeforces round. Submit as many problems as possible.',
                'url': 'https://codeforces.com/',
                'resource': 'Codeforces Live Contest',
                'difficulty': 4, 'hours': 3.0, 'xp': 100
            },
        ],
    },
    'blockchain': {
        'beginner': [
            {
                'name': 'Blockchain Fundamentals',
                'desc': 'What is blockchain, how it works, mining, and core concepts.',
                'task': 'Watch Bitcoin whitepaper explanation videos. Write notes on blockchain basics.',
                'url': 'https://www.youtube.com/watch?v=bBC-nCj2qjY',
                'resource': 'YouTube Blockchain Explained',
                'difficulty': 1, 'hours': 2.0, 'xp': 25
            },
            {
                'name': 'Cryptography Essentials',
                'desc': 'Hash functions, digital signatures, public key cryptography.',
                'task': 'Understand SHA-256, RSA basics. Use online hash tools to explore hashing.',
                'url': 'https://en.wikipedia.org/wiki/Cryptography',
                'resource': 'Wikipedia Cryptography',
                'difficulty': 2, 'hours': 2.5, 'xp': 30
            },
            {
                'name': 'Bitcoin & Cryptocurrency Basics',
                'desc': 'Bitcoin protocol, wallets, transactions, addresses, and key management.',
                'task': 'Create a test Bitcoin wallet. Send test transactions on testnet.',
                'url': 'https://bitcoin.org/en/',
                'resource': 'Bitcoin.org Official',
                'difficulty': 2, 'hours': 2.0, 'xp': 30
            },
            {
                'name': 'Introduction to Ethereum',
                'desc': 'Ethereum network, accounts, gas fees, transactions, and the EVM.',
                'task': 'Create an Ethereum wallet. Explore block explorers like Etherscan.',
                'url': 'https://ethereum.org/en/',
                'resource': 'Ethereum.org Official',
                'difficulty': 2, 'hours': 2.5, 'xp': 35
            },
            {
                'name': 'Smart Contracts Fundamentals',
                'desc': 'What are smart contracts, Solidity basics, and deployment basics.',
                'task': 'Write your first simple Solidity contract. Deploy on Remix IDE.',
                'url': 'https://remix.ethereum.org/',
                'resource': 'Ethereum Remix IDE',
                'difficulty': 2, 'hours': 2.5, 'xp': 35
            },
            {
                'name': 'Solidity Programming Basics',
                'desc': 'Variables, data types, functions, modifiers, and control flow in Solidity.',
                'task': 'Write 5 simple smart contracts covering basic constructs.',
                'url': 'https://docs.soliditylang.org/',
                'resource': 'Solidity Documentation',
                'difficulty': 2, 'hours': 3.0, 'xp': 40
            },
            {
                'name': 'Web3.js & Interacting with Blockchain',
                'desc': 'Web3.js library, connecting to Ethereum, reading/writing contracts.',
                'task': 'Use Web3.js to interact with a deployed contract. Build a simple dApp.',
                'url': 'https://web3js.org/',
                'resource': 'Web3.js Documentation',
                'difficulty': 2, 'hours': 2.5, 'xp': 35
            },
            {
                'name': 'DeFi Protocols Overview',
                'desc': 'Decentralized finance basics, liquidity pools, AMMs, lending protocols.',
                'task': 'Use Uniswap testnet interface. Research Aave and Compound.',
                'url': 'https://uniswap.org/',
                'resource': 'Uniswap Protocol',
                'difficulty': 2, 'hours': 2.0, 'xp': 30
            },
            {
                'name': 'Security Best Practices',
                'desc': 'Common vulnerabilities, private key management, transaction safety.',
                'task': 'Study contract security checklist. Understand common exploit patterns.',
                'url': 'https://consensys.github.io/smart-contract-best-practices/',
                'resource': 'ConsenSys Security Guide',
                'difficulty': 3, 'hours': 2.5, 'xp': 40
            },
            {
                'name': 'Blockchain Explorer & Wallet Project',
                'desc': 'End-to-end project: explore blockchain, send transactions, track balances.',
                'task': 'Build a mini project using Web3.js to display wallet balance and history.',
                'url': 'https://etherscan.io/',
                'resource': 'Etherscan Block Explorer',
                'difficulty': 2, 'hours': 3.0, 'xp': 50
            },
        ],
        'intermediate': [
            {
                'name': 'Advanced Solidity Patterns',
                'desc': 'Inheritance, interfaces, libraries, and advanced design patterns.',
                'task': 'Implement contracts using inheritance, interfaces, and libraries.',
                'url': 'https://docs.soliditylang.org/en/latest/contracts.html',
                'resource': 'Solidity Contracts Guide',
                'difficulty': 3, 'hours': 3.0, 'xp': 45
            },
            {
                'name': 'Gas Optimization & Efficient Contracts',
                'desc': 'Understanding gas costs, writing efficient contracts, optimization tricks.',
                'task': 'Optimize a contract and reduce gas costs. Measure before and after.',
                'url': 'https://dev.to/shafu0605/solidity-gas-optimization-tips-1kmo',
                'resource': 'Gas Optimization Guide',
                'difficulty': 3, 'hours': 2.5, 'xp': 40
            },
            {
                'name': 'Contract Testing & Hardhat Framework',
                'desc': 'Testing frameworks, Hardhat setup, unit testing smart contracts.',
                'task': 'Set up Hardhat. Write comprehensive tests for a contract.',
                'url': 'https://hardhat.org/',
                'resource': 'Hardhat Framework',
                'difficulty': 3, 'hours': 3.0, 'xp': 45
            },
            {
                'name': 'Cryptocurrency Economics & Tokenomics',
                'desc': 'Token economics, supply/demand, market mechanisms, governance tokens.',
                'task': 'Analyze tokenomics of 3 major projects. Create a tokenomics spreadsheet.',
                'url': 'https://blog.curve.fi/understanding-tokenomics/',
                'resource': 'Curve Finance Tokenomics',
                'difficulty': 3, 'hours': 2.5, 'xp': 35
            },
            {
                'name': 'Building a Token (ERC-20)',
                'desc': 'Create and deploy an ERC-20 token contract with standard functionality.',
                'task': 'Deploy an ERC-20 token. Add features like minting and burning.',
                'url': 'https://docs.openzeppelin.com/contracts/4.x/erc20',
                'resource': 'OpenZeppelin ERC-20',
                'difficulty': 3, 'hours': 2.5, 'xp': 40
            },
            {
                'name': 'NFT Development (ERC-721 & ERC-1155)',
                'desc': 'Non-fungible tokens, NFT contracts, metadata, and IPFS integration.',
                'task': 'Deploy an ERC-721 contract. Create and mint NFTs with metadata.',
                'url': 'https://docs.openzeppelin.com/contracts/4.x/erc721',
                'resource': 'OpenZeppelin ERC-721',
                'difficulty': 3, 'hours': 3.0, 'xp': 45
            },
            {
                'name': 'Building a DeFi Application',
                'desc': 'Create a simple lending protocol, liquidity pool, or automated market maker.',
                'task': 'Build a basic AMM or lending contract. Test with local blockchain.',
                'url': 'https://uniswap.org/docs/v3/',
                'resource': 'Uniswap V3 Docs',
                'difficulty': 4, 'hours': 4.0, 'xp': 60
            },
            {
                'name': 'Security Auditing & Code Review',
                'desc': 'Identify vulnerabilities, conduct code reviews, use analysis tools.',
                'task': 'Audit 3 sample contracts. Use Slither and Mythril for analysis.',
                'url': 'https://slither.readthedocs.io/',
                'resource': 'Slither Security Tool',
                'difficulty': 4, 'hours': 3.5, 'xp': 55
            },
            {
                'name': 'Smart Contract Deployment & Mainnet Interaction',
                'desc': 'Deploy contracts to testnet and mainnet. Use Truffle/Hardhat.',
                'task': 'Deploy contracts to goerli testnet. Interact via Etherscan.',
                'url': 'https://goerlifaucet.com/',
                'resource': 'Goerli Testnet Faucet',
                'difficulty': 3, 'hours': 2.5, 'xp': 40
            },
            {
                'name': 'Building a Full dApp',
                'desc': 'Frontend (React), smart contracts, Web3 integration, and deployment.',
                'task': 'Build a complete dApp with frontend and backend. Deploy to production.',
                'url': 'https://ethereum.org/en/developers/docs/dapps/',
                'resource': 'Ethereum dApp Guide',
                'difficulty': 4, 'hours': 5.0, 'xp': 70
            },
        ],
        'advanced': [
            {
                'name': 'Layer 2 Solutions & Scaling',
                'desc': 'Rollups (Optimistic/ZK), sidechains, plasma, and their trade-offs.',
                'task': 'Deploy contracts on Arbitrum or Polygon. Compare gas costs and speed.',
                'url': 'https://ethereum.org/en/layer-2/',
                'resource': 'Ethereum Layer 2 Guide',
                'difficulty': 4, 'hours': 3.0, 'xp': 50
            },
            {
                'name': 'Smart Contract Architecture & Design Patterns',
                'desc': 'Proxy patterns, upgradeability, delegation, and architectural patterns.',
                'task': 'Implement an upgradeable proxy contract. Study contract architecture.',
                'url': 'https://docs.openzeppelin.com/contracts/4.x/upgradeable',
                'resource': 'OpenZeppelin Upgradeable Contracts',
                'difficulty': 4, 'hours': 3.5, 'xp': 55
            },
            {
                'name': 'Advanced Security: Formal Verification',
                'desc': 'Formal verification, SMT solvers, and mathematical proofs for contracts.',
                'task': 'Study formal verification basics. Use Certora or similar tools.',
                'url': 'https://www.certora.com/',
                'resource': 'Certora Verification',
                'difficulty': 5, 'hours': 4.0, 'xp': 70
            },
            {
                'name': 'Cross-Chain Interoperability',
                'desc': 'Cross-chain bridges, messaging protocols, atomic swaps, and oracles.',
                'task': 'Build a contract using cross-chain messaging or bridge protocols.',
                'url': 'https://axelar.network/',
                'resource': 'Axelar Cross-Chain',
                'difficulty': 4, 'hours': 3.0, 'xp': 55
            },
            {
                'name': 'Building a Custom Blockchain',
                'desc': 'Cosmos SDK, Substrate, or Solana development for custom chains.',
                'task': 'Build a simple chain with Cosmos SDK or explore Solana development.',
                'url': 'https://docs.cosmos.network/',
                'resource': 'Cosmos SDK Documentation',
                'difficulty': 5, 'hours': 5.0, 'xp': 80
            },
            {
                'name': 'Advanced DeFi Strategies & Governance',
                'desc': 'DAO governance, yield farming, automated strategies, and treasury mgmt.',
                'task': 'Propose and vote on DAO governance. Analyze yield farming strategies.',
                'url': 'https://mirror.xyz/',
                'resource': 'Mirror DAO Platform',
                'difficulty': 4, 'hours': 3.0, 'xp': 50
            },
            {
                'name': 'Cryptographic Protocols & Zero-Knowledge Proofs',
                'desc': 'ZK-SNARKs, ZK-STARKs, and their applications in privacy & scaling.',
                'task': 'Understand ZK proof basics. Experiment with ZK circuits.',
                'url': 'https://github.com/zcash/halo2',
                'resource': 'Halo2 ZK Library',
                'difficulty': 5, 'hours': 4.5, 'xp': 75
            },
            {
                'name': 'Consensus Mechanisms & Network Architecture',
                'desc': 'PoW, PoS, Byzantine fault tolerance, validator architecture.',
                'task': 'Study Ethereum 2.0 consensus. Understand validator economics.',
                'url': 'https://ethereum.org/en/developers/docs/consensus-mechanisms/',
                'resource': 'Ethereum Consensus Guide',
                'difficulty': 4, 'hours': 3.5, 'xp': 55
            },
            {
                'name': 'Production Blockchain Development',
                'desc': 'Deploy to production mainnet, monitoring, maintenance, and incident response.',
                'task': 'Deploy a production contract. Set up monitoring and security alerts.',
                'url': 'https://openzeppelin.com/defender/',
                'resource': 'OpenZeppelin Defender',
                'difficulty': 4, 'hours': 3.0, 'xp': 60
            },
            {
                'name': 'Blockchain Research & Innovation',
                'desc': 'Read academic papers, contribute to open-source, and explore cutting edge.',
                'task': 'Read 3 blockchain research papers. Contribute to a blockchain project.',
                'url': 'https://arxiv.org/list/cs.CR/recent',
                'resource': 'ArXiv Cryptography Papers',
                'difficulty': 5, 'hours': 5.0, 'xp': 90
            },
        ],
    },
    'ethical_hacking': {
        'beginner': [
            {
                'name': 'Cybersecurity Fundamentals',
                'desc': 'CIA triad, threat landscape, common vulnerabilities, and defense basics.',
                'task': 'Read OWASP top 10. Watch cybersecurity awareness videos.',
                'url': 'https://owasp.org/www-project-top-ten/',
                'resource': 'OWASP Top 10',
                'difficulty': 1, 'hours': 2.0, 'xp': 25
            },
            {
                'name': 'Networking Basics for Security',
                'desc': 'OSI model, TCP/IP, ports, protocols, and common network tools.',
                'task': 'Learn the OSI model. Use ping, traceroute, netstat, and nmap basics.',
                'url': 'https://www.youtube.com/watch?v=e5DEVMtrZIo',
                'resource': 'OSI Model Explained',
                'difficulty': 2, 'hours': 2.5, 'xp': 30
            },
            {
                'name': 'Command Line & Linux Basics',
                'desc': 'Linux commands, file system, permissions, users, and shell scripting intro.',
                'task': 'Practice Linux commands. Write 3 simple shell scripts.',
                'url': 'https://www.linux.com/training-tutorials/linux-command-line-tips/',
                'resource': 'Linux Command Line',
                'difficulty': 2, 'hours': 3.0, 'xp': 35
            },
            {
                'name': 'Cryptography & Hashing Basics',
                'desc': 'Encryption, decryption, hashing, symmetric & asymmetric crypto.',
                'task': 'Learn AES, RSA, MD5, SHA. Use OpenSSL for encryption tasks.',
                'url': 'https://www.youtube.com/watch?v=NuyzuNBFWxQ',
                'resource': 'Cryptography Basics',
                'difficulty': 2, 'hours': 2.5, 'xp': 30
            },
            {
                'name': 'Penetration Testing Fundamentals',
                'desc': 'Methodology, reconnaissance, scanning, enumeration, and exploitation intro.',
                'task': 'Learn the penetration testing framework. Practice with DVWA.',
                'url': 'http://www.dvwa.co.uk/',
                'resource': 'DVWA Vulnerable App',
                'difficulty': 2, 'hours': 3.0, 'xp': 35
            },
            {
                'name': 'Scanning & Enumeration Tools',
                'desc': 'Nmap, Masscan, Shodan, and other reconnaissance and scanning tools.',
                'task': 'Use nmap on lab networks. Practice network scanning scenarios.',
                'url': 'https://nmap.org/',
                'resource': 'Nmap Documentation',
                'difficulty': 2, 'hours': 2.5, 'xp': 30
            },
            {
                'name': 'Web Application Security Basics',
                'desc': 'HTTP/HTTPS, web vulnerabilities, OWASP top 10 web issues.',
                'task': 'Learn SQL injection, XSS, CSRF. Practice with OWASP WebGoat.',
                'url': 'https://owasp.org/www-project-webgoat/',
                'resource': 'OWASP WebGoat',
                'difficulty': 2, 'hours': 3.0, 'xp': 35
            },
            {
                'name': 'Vulnerability Assessment Introduction',
                'desc': 'Identifying vulnerabilities, severity ratings, and remediation basics.',
                'task': 'Perform vulnerability assessment on DVWA. Create remediation report.',
                'url': 'http://www.dvwa.co.uk/',
                'resource': 'DVWA Assessment Practice',
                'difficulty': 2, 'hours': 2.5, 'xp': 30
            },
            {
                'name': 'Social Engineering & Physical Security',
                'desc': 'Common social engineering tactics, phishing, pretexting, and defense.',
                'task': 'Study social engineering attacks. Practice identifying phishing emails.',
                'url': 'https://www.youtube.com/watch?v=4OknzjV0Uac',
                'resource': 'Social Engineering Demo',
                'difficulty': 1, 'hours': 2.0, 'xp': 25
            },
            {
                'name': 'Security Tools & Lab Setup',
                'desc': 'Setting up ethical hacking labs, using Kali Linux, VM environments.',
                'task': 'Set up Kali Linux. Configure virtual lab with target machines.',
                'url': 'https://www.kali.org/',
                'resource': 'Kali Linux Official',
                'difficulty': 2, 'hours': 2.5, 'xp': 30
            },
        ],
        'intermediate': [
            {
                'name': 'Advanced Network Penetration Testing',
                'desc': 'Man-in-the-middle attacks, sniffing, packet analysis, network exploitation.',
                'task': 'Set up network lab. Practice MITM attacks with Wireshark analysis.',
                'url': 'https://www.wireshark.org/',
                'resource': 'Wireshark Network Analyzer',
                'difficulty': 3, 'hours': 3.5, 'xp': 45
            },
            {
                'name': 'Exploitation Techniques',
                'desc': 'Buffer overflow, shellcode, payload generation, and exploit creation.',
                'task': 'Learn shellcode basics. Create exploits for vulnerable programs.',
                'url': 'https://www.exploit-db.com/',
                'resource': 'Exploit Database',
                'difficulty': 4, 'hours': 4.0, 'xp': 55
            },
            {
                'name': 'Web Application Penetration Testing',
                'desc': 'Advanced web vulnerabilities, API security, authentication bypass, etc.',
                'task': 'Perform full web pentest on a vulnerable application. Create detailed report.',
                'url': 'https://portswigger.net/burp',
                'resource': 'Burp Suite Web Security',
                'difficulty': 3, 'hours': 4.0, 'xp': 50
            },
            {
                'name': 'SQL Injection & Database Attacks',
                'desc': 'SQL injection techniques, union-based, blind, time-based, and bypasses.',
                'task': 'Exploit database using SQL injection. Perform blind and time-based attacks.',
                'url': 'https://sqlmap.org/',
                'resource': 'SQLMap Automated Tool',
                'difficulty': 3, 'hours': 3.0, 'xp': 40
            },
            {
                'name': 'Wireless Security & WiFi Cracking',
                'desc': 'WiFi protocols, WEP, WPA/WPA2, aircrack, and wireless exploitation.',
                'task': 'Capture WPA handshake. Crack passwords using aircrack and hashcat.',
                'url': 'https://www.aircrack-ng.org/',
                'resource': 'Aircrack-ng Wireless',
                'difficulty': 3, 'hours': 3.5, 'xp': 45
            },
            {
                'name': 'Malware Analysis Basics',
                'desc': 'Static & dynamic analysis, reverse engineering, sandbox environments.',
                'task': 'Analyze malware samples in sandbox. Use IDA Free or Ghidra.',
                'url': 'https://www.ghidra-sre.org/',
                'resource': 'Ghidra Reverse Engineering',
                'difficulty': 4, 'hours': 4.0, 'xp': 55
            },
            {
                'name': 'Password Cracking & Hashing',
                'desc': 'Hash cracking, password wordlists, rainbow tables, GPU acceleration.',
                'task': 'Crack hashes using hashcat. Compare cracking performance.',
                'url': 'https://hashcat.net/',
                'resource': 'Hashcat Password Cracking',
                'difficulty': 3, 'hours': 2.5, 'xp': 35
            },
            {
                'name': 'Metasploit Framework Mastery',
                'desc': 'Metasploit modules, payload generation, multi-stage exploitation.',
                'task': 'Build exploits using Metasploit. Create custom modules.',
                'url': 'https://www.metasploit.com/',
                'resource': 'Metasploit Framework',
                'difficulty': 4, 'hours': 3.5, 'xp': 50
            },
            {
                'name': 'Post-Exploitation & Persistence',
                'desc': 'Maintaining access, privilege escalation, lateral movement, and evasion.',
                'task': 'Practice privilege escalation. Set up persistence mechanisms.',
                'url': 'https://gtfobins.github.io/',
                'resource': 'GTFOBins Privilege Escalation',
                'difficulty': 4, 'hours': 3.5, 'xp': 50
            },
            {
                'name': 'Comprehensive Lab Practice',
                'desc': 'End-to-end penetration test in lab environment with full reporting.',
                'task': 'Perform complete pentest. Write professional security report.',
                'url': 'https://www.hackthebox.com/',
                'resource': 'HackTheBox Platform',
                'difficulty': 3, 'hours': 5.0, 'xp': 70
            },
        ],
        'advanced': [
            {
                'name': 'Advanced Exploitation & Vulnerability Research',
                'desc': 'Zero-day research, vulnerability disclosure, exploit development.',
                'task': 'Research and develop exploit for known vulnerability. Document findings.',
                'url': 'https://www.cvedetails.com/',
                'resource': 'CVE Details Database',
                'difficulty': 5, 'hours': 5.0, 'xp': 80
            },
            {
                'name': 'Reverse Engineering & Decompilation',
                'desc': 'Binary analysis, decompilation, IDA Pro, Ghidra advanced usage.',
                'task': 'Reverse engineer binary. Identify and modify functionality.',
                'url': 'https://www.ida.fyi/',
                'resource': 'IDA Pro Advanced',
                'difficulty': 5, 'hours': 4.5, 'xp': 75
            },
            {
                'name': 'Advanced Malware Analysis',
                'desc': 'Malware behavior analysis, polymorphism, packing, and obfuscation.',
                'task': 'Analyze packed and obfuscated malware. Identify C&C communication.',
                'url': 'https://any.run/',
                'resource': 'ANY.RUN Malware Sandbox',
                'difficulty': 5, 'hours': 4.5, 'xp': 75
            },
            {
                'name': 'Advanced Application Security',
                'desc': 'API security, microservices, containerization, and cloud security issues.',
                'task': 'Perform security audit of microservices architecture.',
                'url': 'https://owasp.org/www-project-api-security/',
                'resource': 'OWASP API Security Top 10',
                'difficulty': 4, 'hours': 4.0, 'xp': 60
            },
            {
                'name': 'Red Teaming & Advanced Simulation',
                'desc': 'Full adversary simulation, evasion techniques, and detection bypass.',
                'task': 'Conduct full red team engagement. Present findings to blue team.',
                'url': 'https://www.maltego.com/',
                'resource': 'Maltego Intelligence Platform',
                'difficulty': 5, 'hours': 5.0, 'xp': 85
            },
            {
                'name': 'Incident Response & Forensics',
                'desc': 'Investigating security incidents, gathering evidence, timeline reconstruction.',
                'task': 'Perform forensic investigation of sample systems. Create chain of custody.',
                'url': 'https://www.sleuthkit.org/',
                'resource': 'Sleuth Kit Forensics',
                'difficulty': 4, 'hours': 4.0, 'xp': 65
            },
            {
                'name': 'Threat Intelligence & Cyber Threat Landscape',
                'desc': 'MITRE ATT&CK, threat actors, threat modeling, and defense strategy.',
                'task': 'Map threat actor tactics using MITRE ATT&CK. Create threat model.',
                'url': 'https://attack.mitre.org/',
                'resource': 'MITRE ATT&CK Framework',
                'difficulty': 4, 'hours': 3.5, 'xp': 55
            },
            {
                'name': 'Cloud Security & Infrastructure Penetration Testing',
                'desc': 'AWS, Azure, GCP security, misconfigurations, and cloud exploitation.',
                'task': 'Audit cloud infrastructure. Identify misconfigurations and risks.',
                'url': 'https://about.gitlab.com/blog/2021/01/06/kubernetes-security/',
                'resource': 'Kubernetes Security Best Practices',
                'difficulty': 4, 'hours': 4.5, 'xp': 65
            },
            {
                'name': 'Vulnerability Disclosure Program Management',
                'desc': 'Running bug bounty programs, vulnerability coordination, and reporting.',
                'task': 'Submit vulnerability reports to bug bounty platform. Track outcomes.',
                'url': 'https://www.bugcrowd.com/',
                'resource': 'Bugcrowd Platform',
                'difficulty': 3, 'hours': 2.5, 'xp': 35
            },
            {
                'name': 'Certified Ethical Hacker Preparation',
                'desc': 'CEH exam preparation, comprehensive review, and practice tests.',
                'task': 'Complete CEH practice exams. Review all CEH domains thoroughly.',
                'url': 'https://www.eccouncil.org/programs/certified-ethical-hacker/',
                'resource': 'EC-Council CEH',
                'difficulty': 4, 'hours': 6.0, 'xp': 100
            },
        ],
    },
    'devops': {
        'beginner': [
            {'name': 'Linux Command Line Essentials', 'desc': 'Shell basics, file system, permissions, processes, and pipes — the foundation of every server.', 'task': 'Complete 20 Linux command exercises. Write a shell script that backs up a directory.', 'url': 'https://linuxjourney.com/', 'resource': 'Linux Journey', 'difficulty': 1, 'hours': 2.0, 'xp': 25},
            {'name': 'SSH, Users, and Permissions', 'desc': 'Key-based SSH, sudo, file ownership, chmod, and managing remote servers safely.', 'task': 'Generate an SSH key pair. Configure a remote server for key-only login. Create three users with different permissions.', 'url': 'https://www.digitalocean.com/community/tutorials/ssh-essentials-working-with-ssh-servers-clients-and-keys', 'resource': 'DigitalOcean SSH Guide', 'difficulty': 2, 'hours': 2.0, 'xp': 25},
            {'name': 'Git for Operations', 'desc': 'Branching strategies, rebases, conflict resolution, and trunk-based development for ops workflows.', 'task': 'Practice rebase, cherry-pick, and conflict resolution on a sample repo. Document a branching strategy.', 'url': 'https://learngitbranching.js.org/', 'resource': 'Learn Git Branching', 'difficulty': 2, 'hours': 2.0, 'xp': 25},
            {'name': 'Docker Fundamentals', 'desc': 'Images, containers, volumes, networks, and writing your first Dockerfile.', 'task': 'Containerize a Python or Node app. Push the image to Docker Hub.', 'url': 'https://docs.docker.com/get-started/', 'resource': 'Docker Official Tutorial', 'difficulty': 2, 'hours': 2.5, 'xp': 35},
            {'name': 'Docker Compose for Multi-Service Apps', 'desc': 'Compose files, service dependencies, environment files, and local dev stacks.', 'task': 'Write a compose file with app + Postgres + Redis. Bring it up locally with persistent volumes.', 'url': 'https://docs.docker.com/compose/', 'resource': 'Docker Compose Docs', 'difficulty': 2, 'hours': 2.0, 'xp': 30},
            {'name': 'Networking Basics for DevOps', 'desc': 'TCP/IP, DNS, HTTP, load balancers, NAT, and how requests reach your servers.', 'task': 'Trace a request from browser to server. Configure /etc/hosts and a basic reverse proxy.', 'url': 'https://www.cloudflare.com/learning/network-layer/what-is-the-network-layer/', 'resource': 'Cloudflare Learning Center', 'difficulty': 2, 'hours': 2.5, 'xp': 30},
            {'name': 'Cloud Provider Crash Course (AWS)', 'desc': 'EC2, S3, IAM, VPC basics, and how the AWS billing model works.', 'task': 'Launch a free-tier EC2 instance. Host a static site on S3 with CloudFront.', 'url': 'https://aws.amazon.com/getting-started/', 'resource': 'AWS Getting Started', 'difficulty': 2, 'hours': 3.0, 'xp': 40},
            {'name': 'CI/CD Pipelines with GitHub Actions', 'desc': 'Workflows, jobs, runners, secrets, and matrix builds for automated testing and deploys.', 'task': 'Add a CI workflow to a project that runs tests, lints, and builds a Docker image on every push.', 'url': 'https://docs.github.com/en/actions', 'resource': 'GitHub Actions Docs', 'difficulty': 2, 'hours': 2.5, 'xp': 35},
            {'name': 'Bash & Shell Scripting', 'desc': 'Loops, conditionals, functions, arguments, error handling, and writing maintainable scripts.', 'task': 'Write a deploy script that pulls latest code, runs migrations, and restarts a service with error handling.', 'url': 'https://google.github.io/styleguide/shellguide.html', 'resource': 'Google Shell Style Guide', 'difficulty': 2, 'hours': 2.0, 'xp': 25},
            {'name': 'Monitoring & Logs Basics', 'desc': 'journalctl, systemd services, structured logging, and using a metrics dashboard.', 'task': 'Install a sample service as systemd. Tail its logs. Set up a basic Grafana Cloud free-tier dashboard.', 'url': 'https://grafana.com/tutorials/', 'resource': 'Grafana Tutorials', 'difficulty': 2, 'hours': 2.5, 'xp': 35},
        ],
        'intermediate': [
            {'name': 'Kubernetes Core Concepts', 'desc': 'Pods, ReplicaSets, Deployments, Services, ConfigMaps, and the control plane.', 'task': 'Spin up a local cluster (kind or minikube). Deploy a 2-tier app with Deployments + Services.', 'url': 'https://kubernetes.io/docs/tutorials/', 'resource': 'Kubernetes Tutorials', 'difficulty': 3, 'hours': 3.5, 'xp': 50},
            {'name': 'Kubernetes Ingress, ConfigMaps & Secrets', 'desc': 'Routing external traffic, environment management, and sealed secrets.', 'task': 'Add Ingress with TLS to your app. Move env vars to ConfigMaps and a Secret.', 'url': 'https://kubernetes.io/docs/concepts/services-networking/ingress/', 'resource': 'K8s Ingress Docs', 'difficulty': 3, 'hours': 3.0, 'xp': 45},
            {'name': 'Helm for K8s Templating', 'desc': 'Charts, values files, dependencies, and upgrade strategies.', 'task': 'Convert your raw manifests into a Helm chart. Deploy two envs (staging/prod) from one chart.', 'url': 'https://helm.sh/docs/', 'resource': 'Helm Documentation', 'difficulty': 3, 'hours': 3.0, 'xp': 45},
            {'name': 'Terraform — Infrastructure as Code', 'desc': 'Providers, resources, state, modules, and remote backends.', 'task': 'Provision a VPC + EC2 + RDS stack in AWS via Terraform. Store state in S3 with locking.', 'url': 'https://developer.hashicorp.com/terraform/tutorials', 'resource': 'Terraform Tutorials', 'difficulty': 3, 'hours': 3.5, 'xp': 50},
            {'name': 'AWS in Depth — VPC, IAM, ELB', 'desc': 'Network design, IAM roles vs users, load balancers, and security groups in practice.', 'task': 'Design a 3-tier VPC. Use IAM roles for EC2. Front the app with an ALB.', 'url': 'https://aws.amazon.com/architecture/well-architected/', 'resource': 'AWS Well-Architected Framework', 'difficulty': 3, 'hours': 3.0, 'xp': 50},
            {'name': 'Observability — Logs, Metrics, Traces', 'desc': 'Prometheus, Grafana, OpenTelemetry, and the three pillars of observability.', 'task': 'Instrument an app with OpenTelemetry. Ship metrics to Prometheus and traces to Jaeger.', 'url': 'https://opentelemetry.io/docs/', 'resource': 'OpenTelemetry Docs', 'difficulty': 3, 'hours': 3.0, 'xp': 45},
            {'name': 'Production CI/CD Pipelines', 'desc': 'Multi-stage pipelines, environment promotion, approvals, and rollback strategies.', 'task': 'Build a GitHub Actions pipeline: build → test → push image → deploy to staging → manual approval → prod.', 'url': 'https://docs.github.com/en/actions/deployment/about-deployments', 'resource': 'GitHub Actions Deployments', 'difficulty': 3, 'hours': 3.5, 'xp': 55},
            {'name': 'Container Registries & Image Hardening', 'desc': 'ECR/GHCR, image scanning, distroless images, and minimal attack surface.', 'task': 'Switch a Dockerfile to a distroless base. Add vulnerability scanning to CI (Trivy).', 'url': 'https://github.com/aquasecurity/trivy', 'resource': 'Trivy Scanner', 'difficulty': 3, 'hours': 2.5, 'xp': 40},
            {'name': 'Configuration Management with Ansible', 'desc': 'Inventory, playbooks, roles, idempotency, and managing fleets of servers.', 'task': 'Write an Ansible playbook that provisions Nginx + your app on a fresh server.', 'url': 'https://docs.ansible.com/', 'resource': 'Ansible Documentation', 'difficulty': 3, 'hours': 3.0, 'xp': 45},
            {'name': 'Incident Response & Postmortems', 'desc': 'On-call workflows, runbooks, blameless postmortems, and SLO-driven alerts.', 'task': 'Write a runbook for a service. Author a sample blameless postmortem for a past outage you read about.', 'url': 'https://sre.google/sre-book/postmortem-culture/', 'resource': 'Google SRE Book', 'difficulty': 3, 'hours': 2.5, 'xp': 40},
        ],
        'advanced': [
            {'name': 'Service Mesh — Istio / Linkerd', 'desc': 'Sidecars, mTLS, traffic splitting, and zero-trust networking inside clusters.', 'task': 'Install Linkerd on your cluster. Enable mTLS for one app. Set up a canary split.', 'url': 'https://linkerd.io/2.14/getting-started/', 'resource': 'Linkerd Getting Started', 'difficulty': 4, 'hours': 4.0, 'xp': 65},
            {'name': 'GitOps with ArgoCD / Flux', 'desc': 'Declarative continuous delivery, drift detection, and progressive delivery.', 'task': 'Install ArgoCD. Move one app to a GitOps workflow. Demonstrate auto-sync and rollback.', 'url': 'https://argo-cd.readthedocs.io/', 'resource': 'ArgoCD Documentation', 'difficulty': 4, 'hours': 3.5, 'xp': 60},
            {'name': 'Kubernetes Operators & CRDs', 'desc': 'Custom Resource Definitions, controllers, and the operator pattern.', 'task': 'Write a tiny operator with kubebuilder that reconciles a custom resource.', 'url': 'https://book.kubebuilder.io/', 'resource': 'Kubebuilder Book', 'difficulty': 5, 'hours': 4.5, 'xp': 75},
            {'name': 'Multi-Region & Multi-Cluster Strategy', 'desc': 'Active/active vs active/passive, data replication, DNS failover, and disaster recovery.', 'task': 'Design and document a multi-region DR plan for a sample SaaS, including RPO/RTO targets.', 'url': 'https://aws.amazon.com/blogs/architecture/disaster-recovery-dr-architecture-on-aws-part-i-strategies-for-recovery-in-the-cloud/', 'resource': 'AWS DR Architecture', 'difficulty': 4, 'hours': 3.5, 'xp': 60},
            {'name': 'Cost Optimization & FinOps', 'desc': 'Right-sizing, spot/preemptible, reserved capacity, and tagging discipline.', 'task': 'Audit a real or sample AWS bill. Identify 3 concrete savings worth >20% each.', 'url': 'https://www.finops.org/introduction/what-is-finops/', 'resource': 'FinOps Foundation', 'difficulty': 3, 'hours': 2.5, 'xp': 45},
            {'name': 'Chaos Engineering', 'desc': 'Fault injection, game days, and steady-state hypotheses.', 'task': 'Use LitmusChaos or chaos-mesh to kill pods and inject latency. Document what broke.', 'url': 'https://litmuschaos.io/', 'resource': 'Litmus Chaos', 'difficulty': 4, 'hours': 3.0, 'xp': 55},
            {'name': 'eBPF & Modern Linux Observability', 'desc': 'BPF programs, Cilium, Pixie, and zero-instrumentation observability.', 'task': 'Install Cilium on a cluster. Visualize service-to-service traffic with Hubble.', 'url': 'https://ebpf.io/', 'resource': 'eBPF.io', 'difficulty': 5, 'hours': 4.0, 'xp': 70},
            {'name': 'Secrets Management — Vault', 'desc': 'Dynamic secrets, transit encryption, K8s auth, and short-lived credentials.', 'task': 'Stand up Vault dev mode. Use it to issue dynamic DB credentials to a pod.', 'url': 'https://developer.hashicorp.com/vault/tutorials', 'resource': 'HashiCorp Vault Tutorials', 'difficulty': 4, 'hours': 3.0, 'xp': 55},
            {'name': 'Policy as Code — OPA / Gatekeeper', 'desc': 'Rego, admission control, and enforcing org policy at deploy time.', 'task': 'Write 3 Gatekeeper constraints (e.g. no :latest tag, require resource limits) and enforce on a cluster.', 'url': 'https://www.openpolicyagent.org/docs/', 'resource': 'OPA Documentation', 'difficulty': 4, 'hours': 3.0, 'xp': 55},
            {'name': 'Platform Engineering Capstone', 'desc': 'Design an internal developer platform with golden paths, self-service envs, and SLOs.', 'task': 'Document an IDP for a fictional 50-engineer company: tooling choices, golden path, and ownership model.', 'url': 'https://internaldeveloperplatform.org/', 'resource': 'Internal Developer Platform', 'difficulty': 5, 'hours': 5.0, 'xp': 100},
        ],
    },
    'system_design': {
        'beginner': [
            {'name': 'Client-Server Model & HTTP', 'desc': 'How requests, responses, statelessness, and HTTP verbs work.', 'task': 'Diagram the full path of a GET request from browser to DB and back. Label every hop.', 'url': 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview', 'resource': 'MDN HTTP Overview', 'difficulty': 1, 'hours': 1.5, 'xp': 20},
            {'name': 'Latency, Throughput & Back-of-Envelope', 'desc': 'Numbers every engineer should know — latency at each layer.', 'task': 'Memorize Jeff Dean\'s latency numbers. Estimate QPS for a 1M-user app.', 'url': 'https://gist.github.com/jboner/2841832', 'resource': 'Latency Numbers Gist', 'difficulty': 2, 'hours': 1.5, 'xp': 20},
            {'name': 'Load Balancing Strategies', 'desc': 'L4 vs L7, round-robin, least-connections, sticky sessions, and health checks.', 'task': 'Configure Nginx as an L7 load balancer in front of 2 app servers. Demonstrate failover.', 'url': 'https://www.nginx.com/resources/glossary/load-balancing/', 'resource': 'Nginx Load Balancing Guide', 'difficulty': 2, 'hours': 2.0, 'xp': 30},
            {'name': 'Caching Fundamentals', 'desc': 'Client, CDN, app-layer, and DB caching; cache-aside, write-through, write-behind.', 'task': 'Add Redis cache-aside to a slow endpoint. Measure the latency delta.', 'url': 'https://aws.amazon.com/caching/', 'resource': 'AWS Caching Guide', 'difficulty': 2, 'hours': 2.5, 'xp': 35},
            {'name': 'Databases — SQL vs NoSQL', 'desc': 'When to pick relational, document, key-value, wide-column, or graph.', 'task': 'For 5 sample products (chat, e-commerce, analytics, social, IoT) justify a primary DB choice.', 'url': 'https://www.mongodb.com/nosql-explained/nosql-vs-sql', 'resource': 'MongoDB SQL vs NoSQL', 'difficulty': 2, 'hours': 2.0, 'xp': 30},
            {'name': 'DNS & CDNs', 'desc': 'How DNS lookups, edge caching, and Anycast routing accelerate global apps.', 'task': 'Put a free CloudFront/Cloudflare in front of a static site. Measure TTFB before/after.', 'url': 'https://www.cloudflare.com/learning/cdn/what-is-a-cdn/', 'resource': 'Cloudflare CDN Learning', 'difficulty': 2, 'hours': 1.5, 'xp': 25},
            {'name': 'Message Queues 101', 'desc': 'Producers, consumers, durability, ack modes — using SQS or RabbitMQ.', 'task': 'Add a queue between a web request and a slow worker. Send 1000 jobs and observe behavior.', 'url': 'https://www.rabbitmq.com/tutorials/tutorial-one-python.html', 'resource': 'RabbitMQ Tutorials', 'difficulty': 2, 'hours': 2.0, 'xp': 30},
            {'name': 'Designing a URL Shortener', 'desc': 'The classic warm-up problem — hashing, collisions, base62, and read-heavy patterns.', 'task': 'Sketch the architecture for a 100M-link URL shortener. Justify your DB and caching choices.', 'url': 'https://www.youtube.com/watch?v=JQDHz72OA3c', 'resource': 'System Design Primer — URL Shortener', 'difficulty': 2, 'hours': 2.0, 'xp': 35},
            {'name': 'Reading a System Design Diagram', 'desc': 'Conventions: clients, gateways, services, queues, stores; how to read someone else\'s diagram.', 'task': 'Pick 3 architecture diagrams from public engineering blogs and annotate every component.', 'url': 'https://github.com/donnemartin/system-design-primer', 'resource': 'System Design Primer Repo', 'difficulty': 2, 'hours': 2.0, 'xp': 25},
            {'name': 'CAP, PACELC & Consistency Models', 'desc': 'Strong vs eventual consistency, partition handling, and trade-offs.', 'task': 'Write 1 paragraph each justifying a consistency model for: bank, social feed, cart, leaderboard.', 'url': 'https://en.wikipedia.org/wiki/CAP_theorem', 'resource': 'CAP Theorem Reference', 'difficulty': 2, 'hours': 1.5, 'xp': 25},
        ],
        'intermediate': [
            {'name': 'Sharding & Partitioning', 'desc': 'Range, hash, and directory-based partitioning; resharding; hot keys.', 'task': 'Design a sharding scheme for a 10B-row tweets table. Discuss hot-key mitigation.', 'url': 'https://www.scylladb.com/glossary/database-sharding/', 'resource': 'ScyllaDB Sharding Glossary', 'difficulty': 3, 'hours': 2.5, 'xp': 40},
            {'name': 'Replication & Leader Election', 'desc': 'Sync vs async replication, quorum, Raft/Paxos at a high level.', 'task': 'Diagram a 3-node Raft cluster. Walk through leader failover step by step.', 'url': 'https://raft.github.io/', 'resource': 'Raft Visualization', 'difficulty': 3, 'hours': 2.5, 'xp': 40},
            {'name': 'Database Indexing Deep Dive', 'desc': 'B-trees, hash indexes, covering indexes, write amplification, and EXPLAIN.', 'task': 'Take 3 slow queries from a real app. Add the right index. Document the EXPLAIN before/after.', 'url': 'https://use-the-index-luke.com/', 'resource': 'Use The Index, Luke!', 'difficulty': 3, 'hours': 3.0, 'xp': 45},
            {'name': 'Designing a News Feed', 'desc': 'Fan-out on write vs read, hybrid, ranking, freshness, and feed assembly.', 'task': 'Design a Twitter-style timeline service for 100M DAU. Walk through fan-out trade-offs.', 'url': 'https://highscalability.com/twitter-justin-bieber-the-big-tweet-vs-twitter-the-tweet-rec/', 'resource': 'High Scalability — Twitter Case Study', 'difficulty': 3, 'hours': 3.0, 'xp': 50},
            {'name': 'Designing a Rate Limiter', 'desc': 'Token bucket, leaky bucket, sliding window, and distributed enforcement.', 'task': 'Implement a Redis-backed sliding-window rate limiter. Stress test it.', 'url': 'https://redis.io/learn/howtos/solutions/microservices/rate-limiting', 'resource': 'Redis Rate Limiting', 'difficulty': 3, 'hours': 2.5, 'xp': 45},
            {'name': 'Designing a Chat System', 'desc': 'Websockets vs long-polling, presence, message delivery guarantees, and fan-out.', 'task': 'Design a 1-to-1 + group chat service. Choose a delivery semantic (at-least-once vs exactly-once) and justify.', 'url': 'https://signal.org/blog/', 'resource': 'Signal Engineering Blog', 'difficulty': 3, 'hours': 3.0, 'xp': 50},
            {'name': 'API Gateway & Service Discovery', 'desc': 'Kong/Envoy, service registries, traffic routing, and rate limiting at the edge.', 'task': 'Set up Kong in front of 2 microservices. Add JWT auth and a rate limit at the gateway.', 'url': 'https://docs.konghq.com/', 'resource': 'Kong Documentation', 'difficulty': 3, 'hours': 2.5, 'xp': 40},
            {'name': 'Designing a Notification Service', 'desc': 'Push, email, SMS providers; templating; retries; dedup; user preferences.', 'task': 'Sketch a multichannel notification platform. Include a quiet-hours feature and idempotency.', 'url': 'https://aws.amazon.com/blogs/messaging-and-targeting/', 'resource': 'AWS Messaging Blog', 'difficulty': 3, 'hours': 2.5, 'xp': 45},
            {'name': 'Event-Driven Architecture & Kafka', 'desc': 'Topics, partitions, consumer groups, ordering, and exactly-once semantics.', 'task': 'Run Kafka locally. Build a producer/consumer with a partition key strategy that preserves per-user ordering.', 'url': 'https://kafka.apache.org/documentation/', 'resource': 'Kafka Documentation', 'difficulty': 4, 'hours': 3.5, 'xp': 55},
            {'name': 'Microservices vs Monolith Trade-offs', 'desc': 'When to split, distributed monoliths, and team-shaped boundaries.', 'task': 'Take an existing monolith you know. Identify 3 services to extract and 3 to leave alone, with reasoning.', 'url': 'https://martinfowler.com/articles/microservice-trade-offs.html', 'resource': 'Martin Fowler — Microservice Trade-offs', 'difficulty': 3, 'hours': 2.0, 'xp': 35},
        ],
        'advanced': [
            {'name': 'Designing YouTube / Netflix Streaming', 'desc': 'HLS/DASH, CDN ladder encoding, watch history, recommendations.', 'task': 'Design the architecture for a 1B-user VOD platform. Cover ingest, transcoding, delivery, and personalization.', 'url': 'https://netflixtechblog.com/', 'resource': 'Netflix Tech Blog', 'difficulty': 5, 'hours': 4.0, 'xp': 75},
            {'name': 'Designing a Distributed Cache (Memcached/Redis Cluster)', 'desc': 'Consistent hashing, cluster mode, replication, and failover.', 'task': 'Design a 100-node distributed cache. Walk through key placement and node-failure recovery.', 'url': 'https://redis.io/docs/management/scaling/', 'resource': 'Redis Cluster Docs', 'difficulty': 4, 'hours': 3.0, 'xp': 60},
            {'name': 'Designing Uber / Ride-Sharing', 'desc': 'Geo-indexing (S2/H3), matching, surge pricing, and real-time driver location.', 'task': 'Design the dispatch system. Pick a geo index and justify. Handle high-density city load.', 'url': 'https://www.uber.com/blog/h3/', 'resource': 'Uber H3 Engineering Blog', 'difficulty': 5, 'hours': 4.0, 'xp': 75},
            {'name': 'Designing Google Docs / Real-Time Collab', 'desc': 'CRDTs vs OT, presence, conflict resolution, and offline edits.', 'task': 'Design a collaborative text editor. Pick CRDT or OT, defend the choice, and outline storage.', 'url': 'https://www.figma.com/blog/multiplayer-editing-in-figma/', 'resource': 'Figma Multiplayer Blog', 'difficulty': 5, 'hours': 4.0, 'xp': 70},
            {'name': 'Designing a Payments System', 'desc': 'Idempotency, ledger design, double-entry accounting, reconciliation, PCI scope.', 'task': 'Design a wallet + transfers system. Build the ledger schema. Walk through idempotent retries.', 'url': 'https://stripe.com/blog/idempotency', 'resource': 'Stripe Idempotency Blog', 'difficulty': 4, 'hours': 3.5, 'xp': 65},
            {'name': 'Designing a Search Engine', 'desc': 'Crawling, inverted index, tokenization, ranking (BM25), and incremental indexing.', 'task': 'Design a niche search engine over 100M docs. Cover ingest, index sharding, and query path.', 'url': 'https://lucene.apache.org/', 'resource': 'Apache Lucene', 'difficulty': 5, 'hours': 4.0, 'xp': 70},
            {'name': 'Distributed Transactions & Sagas', 'desc': 'Two-phase commit, sagas, outbox pattern, and dual-write problems.', 'task': 'Implement the outbox pattern in a sample service. Walk through a saga rollback scenario.', 'url': 'https://microservices.io/patterns/data/saga.html', 'resource': 'Microservices.io — Saga Pattern', 'difficulty': 4, 'hours': 3.0, 'xp': 60},
            {'name': 'Multi-Tenant SaaS Architecture', 'desc': 'Shared-DB vs schema-per-tenant vs DB-per-tenant; noisy neighbors.', 'task': 'Design tenancy for a B2B product targeting 10k small tenants + 50 enterprise tenants.', 'url': 'https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/tenancy-models', 'resource': 'Microsoft Multitenancy Guide', 'difficulty': 4, 'hours': 3.0, 'xp': 55},
            {'name': 'Mock System Design Interviews', 'desc': 'Communicating trade-offs under time pressure, capacity planning, and deep-dive prompts.', 'task': 'Do 3 mock interviews (with a peer or yourself) on classic prompts. Record and review.', 'url': 'https://www.exponent.com/courses/system-design-interview', 'resource': 'Exponent System Design', 'difficulty': 4, 'hours': 4.5, 'xp': 80},
            {'name': 'Capstone — End-to-End Architecture Doc', 'desc': 'Write a production-grade architecture doc for a real or imagined product.', 'task': 'Author a full design doc covering scale, data model, APIs, failures, security, and cost.', 'url': 'https://www.industrialempathy.com/posts/design-docs-at-google/', 'resource': 'Design Docs at Google', 'difficulty': 5, 'hours': 5.0, 'xp': 100},
        ],
    },
    'mobile': {
        'beginner': [
            {'name': 'Mobile Development Landscape', 'desc': 'Native vs cross-platform; iOS vs Android lifecycle; choosing your stack.', 'task': 'Write a 1-page comparison of React Native, Flutter, and native. Pick your stack for this track.', 'url': 'https://reactnative.dev/docs/getting-started', 'resource': 'React Native Docs', 'difficulty': 1, 'hours': 1.5, 'xp': 20},
            {'name': 'Setup — Expo / Flutter Toolchain', 'desc': 'Installing SDKs, simulators, and your first "Hello, Mobile".', 'task': 'Set up Expo (or Flutter). Run the starter on a simulator and a real device.', 'url': 'https://docs.expo.dev/get-started/installation/', 'resource': 'Expo Installation Guide', 'difficulty': 1, 'hours': 2.0, 'xp': 25},
            {'name': 'Core Layout & Styling', 'desc': 'Flex layout on mobile, safe areas, scroll views, and responsive sizing.', 'task': 'Build a profile screen with avatar, stats, and a scrollable activity list.', 'url': 'https://reactnative.dev/docs/flexbox', 'resource': 'RN Flexbox Guide', 'difficulty': 2, 'hours': 2.0, 'xp': 25},
            {'name': 'Lists, Touchables & Gestures', 'desc': 'FlatList performance, pressables, and basic gesture handling.', 'task': 'Build an infinite scrolling list with pull-to-refresh and swipe-to-delete.', 'url': 'https://reactnative.dev/docs/flatlist', 'resource': 'RN FlatList Docs', 'difficulty': 2, 'hours': 2.5, 'xp': 30},
            {'name': 'Navigation', 'desc': 'Stack, tab, and drawer navigators; params; deep links.', 'task': 'Build a 3-tab app (Home / Search / Profile) with a detail screen and parameter passing.', 'url': 'https://reactnavigation.org/docs/getting-started', 'resource': 'React Navigation Docs', 'difficulty': 2, 'hours': 2.5, 'xp': 35},
            {'name': 'State Management Basics', 'desc': 'Hooks/Provider for local state; when to reach for Zustand/Riverpod.', 'task': 'Build a cart screen with quantity controls and a running total stored in app-level state.', 'url': 'https://react.dev/learn/managing-state', 'resource': 'React State Guide', 'difficulty': 2, 'hours': 2.5, 'xp': 30},
            {'name': 'Calling REST APIs', 'desc': 'fetch/axios, loading states, errors, and pagination.', 'task': 'Build a movie-search screen that hits a public API with loading/empty/error states.', 'url': 'https://reactnative.dev/docs/network', 'resource': 'RN Networking Docs', 'difficulty': 2, 'hours': 2.0, 'xp': 30},
            {'name': 'Forms & Validation', 'desc': 'Controlled inputs, keyboard handling, and validation libraries.', 'task': 'Build a sign-up form with client-side validation and friendly inline errors.', 'url': 'https://react-hook-form.com/', 'resource': 'React Hook Form', 'difficulty': 2, 'hours': 2.0, 'xp': 25},
            {'name': 'Local Storage & Async Storage', 'desc': 'Persisting prefs and tokens between app launches.', 'task': 'Add "remember me" to your login screen. Survive app restarts.', 'url': 'https://react-native-async-storage.github.io/async-storage/', 'resource': 'AsyncStorage Docs', 'difficulty': 2, 'hours': 1.5, 'xp': 25},
            {'name': 'First End-to-End Mini-App', 'desc': 'Tie navigation + state + API + storage into a small, usable app.', 'task': 'Ship a notes app: list, create, edit, delete, persisted locally, with two screens.', 'url': 'https://reactnative.dev/docs/tutorial', 'resource': 'RN Tutorial', 'difficulty': 3, 'hours': 3.0, 'xp': 50},
        ],
        'intermediate': [
            {'name': 'Authentication Flows', 'desc': 'Token storage, refresh, biometric unlock, OAuth/social login.', 'task': 'Add email + Google login to your notes app. Use secure storage for tokens.', 'url': 'https://docs.expo.dev/guides/authentication/', 'resource': 'Expo Authentication Guide', 'difficulty': 3, 'hours': 3.0, 'xp': 45},
            {'name': 'Offline-First with React Query / Riverpod', 'desc': 'Caching, optimistic updates, background refetch, mutation queues.', 'task': 'Make your app fully usable offline. Sync edits when reconnecting.', 'url': 'https://tanstack.com/query/latest', 'resource': 'TanStack Query Docs', 'difficulty': 3, 'hours': 3.5, 'xp': 55},
            {'name': 'Push Notifications', 'desc': 'APNs/FCM, token registration, foreground vs background handling.', 'task': 'Wire push notifications via Expo / Firebase. Send a notification that deep-links to a screen.', 'url': 'https://docs.expo.dev/push-notifications/overview/', 'resource': 'Expo Push Notifications', 'difficulty': 3, 'hours': 3.0, 'xp': 50},
            {'name': 'Animations & Gestures', 'desc': 'Reanimated, gesture handler, and 60fps interactions.', 'task': 'Build a draggable swipeable card stack (Tinder-style) at 60fps.', 'url': 'https://docs.swmansion.com/react-native-reanimated/', 'resource': 'Reanimated Docs', 'difficulty': 3, 'hours': 3.0, 'xp': 50},
            {'name': 'Camera, Maps & Native APIs', 'desc': 'Permissions, camera capture, geolocation, maps integration.', 'task': 'Build a "report an issue" screen with photo + location pinned on a map.', 'url': 'https://docs.expo.dev/versions/latest/sdk/camera/', 'resource': 'Expo Camera Docs', 'difficulty': 3, 'hours': 3.0, 'xp': 50},
            {'name': 'Performance Profiling', 'desc': 'Flipper / DevTools, dropped frames, bridge cost, and list virtualization.', 'task': 'Profile your app. Find one re-render storm and fix it. Find one slow list and virtualize it.', 'url': 'https://reactnative.dev/docs/performance', 'resource': 'RN Performance Guide', 'difficulty': 3, 'hours': 2.5, 'xp': 40},
            {'name': 'App Theming & Design Systems', 'desc': 'Dark mode, dynamic colors, accessibility scaling.', 'task': 'Add a dark mode that respects system setting and a font-size accessibility control.', 'url': 'https://reactnative.dev/docs/appearance', 'resource': 'RN Appearance API', 'difficulty': 3, 'hours': 2.0, 'xp': 35},
            {'name': 'Testing Mobile Apps', 'desc': 'Jest, React Native Testing Library, and Detox / Maestro for E2E.', 'task': 'Add unit tests for one screen and one E2E test for the auth flow.', 'url': 'https://callstack.github.io/react-native-testing-library/', 'resource': 'RN Testing Library', 'difficulty': 3, 'hours': 2.5, 'xp': 40},
            {'name': 'OTA Updates & Crash Reporting', 'desc': 'EAS Update / CodePush, Sentry, and out-of-band fixes.', 'task': 'Hook up Sentry. Ship a fix via EAS Update without going through the stores.', 'url': 'https://docs.expo.dev/eas-update/introduction/', 'resource': 'EAS Update Docs', 'difficulty': 3, 'hours': 2.5, 'xp': 40},
            {'name': 'Shipping to TestFlight & Google Play Internal', 'desc': 'Signing, provisioning, beta tracks, and review notes.', 'task': 'Push a build to TestFlight and to Google Play internal testing.', 'url': 'https://docs.expo.dev/submit/introduction/', 'resource': 'EAS Submit', 'difficulty': 3, 'hours': 3.0, 'xp': 50},
        ],
        'advanced': [
            {'name': 'Writing Native Modules', 'desc': 'Bridging into Swift/Kotlin when JS isn\'t enough.', 'task': 'Write a tiny native module (e.g. battery info) and call it from JS.', 'url': 'https://reactnative.dev/docs/native-modules-intro', 'resource': 'RN Native Modules', 'difficulty': 4, 'hours': 3.5, 'xp': 60},
            {'name': 'New Architecture — Fabric & TurboModules', 'desc': 'JSI, codegen, and the modern RN runtime.', 'task': 'Migrate a small library to the new architecture. Measure startup and bridge cost.', 'url': 'https://reactnative.dev/docs/new-architecture-intro', 'resource': 'New Architecture Intro', 'difficulty': 5, 'hours': 4.0, 'xp': 70},
            {'name': 'App Performance at Scale', 'desc': 'Cold start, memory, JS thread vs UI thread, list windowing.', 'task': 'Profile cold start; cut it by 30%. Document what you changed.', 'url': 'https://reactnative.dev/docs/profile-hermes', 'resource': 'Profiling Hermes', 'difficulty': 4, 'hours': 3.0, 'xp': 55},
            {'name': 'In-App Purchases & Subscriptions', 'desc': 'StoreKit / Play Billing, server-side validation, restore flow, paywalls.', 'task': 'Add a single subscription product with server-side receipt validation in a sandbox.', 'url': 'https://developer.apple.com/in-app-purchase/', 'resource': 'Apple IAP Docs', 'difficulty': 4, 'hours': 3.5, 'xp': 60},
            {'name': 'Background Tasks & Geofencing', 'desc': 'Background fetch, location updates, and OS limits.', 'task': 'Implement geofence triggers that fire a notification when entering a region.', 'url': 'https://docs.expo.dev/versions/latest/sdk/task-manager/', 'resource': 'Expo TaskManager', 'difficulty': 4, 'hours': 3.0, 'xp': 55},
            {'name': 'Deep Linking & Universal Links', 'desc': 'App associations, branch.io, and routing across cold-start.', 'task': 'Add universal links so a web URL opens the right screen in your app, even from cold start.', 'url': 'https://reactnavigation.org/docs/deep-linking', 'resource': 'RN Navigation Deep Links', 'difficulty': 4, 'hours': 2.5, 'xp': 45},
            {'name': 'Accessibility & Localization', 'desc': 'VoiceOver/TalkBack, dynamic type, RTL, and i18n best practices.', 'task': 'Add full accessibility labels + an RTL language. Audit with VoiceOver.', 'url': 'https://reactnative.dev/docs/accessibility', 'resource': 'RN Accessibility Docs', 'difficulty': 3, 'hours': 2.5, 'xp': 45},
            {'name': 'Mobile Security Hardening', 'desc': 'Cert pinning, jailbreak detection, secure storage, obfuscation.', 'task': 'Add cert pinning and protect sensitive data with the Keychain/Keystore.', 'url': 'https://owasp.org/www-project-mobile-application-security/', 'resource': 'OWASP MAS', 'difficulty': 4, 'hours': 3.0, 'xp': 55},
            {'name': 'CI/CD for Mobile', 'desc': 'EAS / Bitrise / Fastlane, automated screenshots, and store submission.', 'task': 'Automate iOS + Android builds, screenshots, and store metadata on every tag.', 'url': 'https://docs.fastlane.tools/', 'resource': 'Fastlane Documentation', 'difficulty': 4, 'hours': 3.0, 'xp': 55},
            {'name': 'Production-Ready App Capstone', 'desc': 'Polish, analytics, paywall, push, deep links, and store launch.', 'task': 'Ship a complete app to the App Store + Play Store, monetized or free.', 'url': 'https://developer.apple.com/app-store/review/guidelines/', 'resource': 'App Store Review Guidelines', 'difficulty': 5, 'hours': 6.0, 'xp': 100},
        ],
    },
    'gamedev': {
        'beginner': [
            {'name': 'Engine Choice — Unity vs Godot', 'desc': 'Picking your engine, installing it, and shipping a "Hello, Game".', 'task': 'Install Unity or Godot. Build the sample project and run it.', 'url': 'https://docs.godotengine.org/en/stable/getting_started/introduction/index.html', 'resource': 'Godot Getting Started', 'difficulty': 1, 'hours': 1.5, 'xp': 20},
            {'name': 'Scenes, Nodes & GameObjects', 'desc': 'The scene graph, transforms, parent/child, and prefabs.', 'task': 'Build a scene with 3 objects parented under a controller. Animate the parent.', 'url': 'https://docs.godotengine.org/en/stable/getting_started/step_by_step/scenes_and_nodes.html', 'resource': 'Godot Scenes Tutorial', 'difficulty': 1, 'hours': 2.0, 'xp': 25},
            {'name': 'Input & Player Movement', 'desc': 'Reading keyboard/gamepad and translating to character movement.', 'task': 'Make a top-down character that moves with WASD and a gamepad stick.', 'url': 'https://learn.unity.com/tutorial/character-controllers', 'resource': 'Unity Character Controllers', 'difficulty': 2, 'hours': 2.0, 'xp': 30},
            {'name': '2D Physics & Collisions', 'desc': 'Rigidbodies, colliders, layers, and triggers.', 'task': 'Build a brick-breaker prototype with collisions and brick destruction.', 'url': 'https://docs.unity3d.com/Manual/Physics2DReference.html', 'resource': 'Unity 2D Physics', 'difficulty': 2, 'hours': 2.5, 'xp': 35},
            {'name': 'Sprites, Animations & Tilemaps', 'desc': 'Sprite sheets, animation state machines, and tile-based levels.', 'task': 'Animate a sprite character idle/walk/jump. Build a small tilemap level.', 'url': 'https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.html', 'resource': 'Godot Tilemaps', 'difficulty': 2, 'hours': 2.5, 'xp': 35},
            {'name': 'UI in Game Engines', 'desc': 'Canvas / Control nodes, anchors, scaling, and HUD design.', 'task': 'Add a health bar, score counter, and a pause menu to your prototype.', 'url': 'https://docs.unity3d.com/Manual/UISystem.html', 'resource': 'Unity UI Manual', 'difficulty': 2, 'hours': 2.0, 'xp': 30},
            {'name': 'Audio — SFX & Music', 'desc': 'Triggering one-shots, looping music, and basic mixing.', 'task': 'Add jump SFX and a music track that ducks under SFX.', 'url': 'https://docs.unity3d.com/Manual/Audio.html', 'resource': 'Unity Audio Manual', 'difficulty': 2, 'hours': 1.5, 'xp': 25},
            {'name': 'Scene Management & Game Loop', 'desc': 'Title → game → game over → replay; saving state between scenes.', 'task': 'Wire a full loop: title screen → level → death → restart.', 'url': 'https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html', 'resource': 'Godot Autoload (Singletons)', 'difficulty': 2, 'hours': 2.0, 'xp': 30},
            {'name': 'Save / Load Game State', 'desc': 'Local files, JSON saves, and versioning save data.', 'task': 'Persist high score, settings, and current level to disk.', 'url': 'https://docs.unity3d.com/Manual/JSONSerialization.html', 'resource': 'Unity JSON Serialization', 'difficulty': 2, 'hours': 2.0, 'xp': 30},
            {'name': 'First Game — Mini-Jam Prototype', 'desc': 'Take everything above and ship a small playable game.', 'task': 'Make a 5-minute playable game (any genre). Get one friend to playtest.', 'url': 'https://itch.io/jams', 'resource': 'itch.io Game Jams', 'difficulty': 3, 'hours': 4.0, 'xp': 60},
        ],
        'intermediate': [
            {'name': '3D Math — Vectors, Quaternions, Transforms', 'desc': 'Dot/cross, basis vectors, rotations, and the math behind transforms.', 'task': 'Implement look-at, orbit camera, and a tangent-space calc by hand.', 'url': 'https://gamemath.com/book/intro.html', 'resource': '3D Math Primer Online', 'difficulty': 3, 'hours': 3.0, 'xp': 45},
            {'name': '3D Movement & Camera Controllers', 'desc': 'First/third person controllers, camera collision, and smoothing.', 'task': 'Build a 3D third-person controller with a camera that avoids walls.', 'url': 'https://learn.unity.com/tutorial/cinemachine', 'resource': 'Unity Cinemachine', 'difficulty': 3, 'hours': 3.0, 'xp': 45},
            {'name': 'Lighting, Materials & PBR', 'desc': 'Directional/point/spot lights, baked vs realtime GI, PBR materials.', 'task': 'Light a small indoor scene with baked GI. Build a PBR material from textures.', 'url': 'https://learnopengl.com/PBR/Theory', 'resource': 'LearnOpenGL — PBR', 'difficulty': 3, 'hours': 3.0, 'xp': 50},
            {'name': 'Shaders 101', 'desc': 'Vertex/fragment basics, UVs, and writing your first custom shader.', 'task': 'Write a "dissolve" shader and a simple toon shader.', 'url': 'https://thebookofshaders.com/', 'resource': 'The Book of Shaders', 'difficulty': 4, 'hours': 3.5, 'xp': 60},
            {'name': 'AI Basics — State Machines & Pathfinding', 'desc': 'FSMs, behavior trees, NavMesh, and A* fundamentals.', 'task': 'Build a guard that patrols, chases on sight, and gives up after losing the player.', 'url': 'https://docs.unity3d.com/Manual/Navigation.html', 'resource': 'Unity NavMesh', 'difficulty': 3, 'hours': 3.0, 'xp': 50},
            {'name': 'Particles & VFX', 'desc': 'Particle systems for explosions, dust, magic, and weather.', 'task': 'Build 3 reusable VFX: footstep dust, hit explosion, level-up swirl.', 'url': 'https://docs.unity3d.com/Manual/ParticleSystems.html', 'resource': 'Unity Particle Systems', 'difficulty': 3, 'hours': 2.5, 'xp': 40},
            {'name': 'Game Feel — Juice & Polish', 'desc': 'Screen shake, hit pause, easing, and "game feel" multipliers.', 'task': 'Take a basic prototype and add screen shake, hit-pause, and tween easings.', 'url': 'https://www.youtube.com/watch?v=AJdEqssNZ-U', 'resource': 'Game Feel Talk (Jan Willem Nijman)', 'difficulty': 3, 'hours': 2.5, 'xp': 40},
            {'name': 'Performance Profiling', 'desc': 'Frame budget, draw calls, batching, GC spikes, and the profiler.', 'task': 'Hit a stable 60fps on a target device. Document the 3 biggest wins.', 'url': 'https://docs.unity3d.com/Manual/Profiler.html', 'resource': 'Unity Profiler', 'difficulty': 3, 'hours': 2.5, 'xp': 45},
            {'name': 'Build Pipelines — PC, Web, Mobile', 'desc': 'Export targets, asset bundles, and compression.', 'task': 'Export your prototype to WebGL and a desktop build. Get them under a size budget.', 'url': 'https://docs.unity3d.com/Manual/PublishingBuilds.html', 'resource': 'Unity Publishing Builds', 'difficulty': 3, 'hours': 2.0, 'xp': 35},
            {'name': 'Game Jam Project', 'desc': 'Ship a 48-hour jam game; emphasis on scope discipline.', 'task': 'Enter (or simulate) a 48-hour jam. Ship something playable. Write a postmortem.', 'url': 'https://itch.io/jams', 'resource': 'itch.io Game Jams', 'difficulty': 4, 'hours': 6.0, 'xp': 90},
        ],
        'advanced': [
            {'name': 'Custom Render Pipelines (URP/HDRP)', 'desc': 'Render features, post-processing, and pipeline customization.', 'task': 'Add a custom render feature: outline pass or selective bloom.', 'url': 'https://docs.unity3d.com/Manual/srp-universal.html', 'resource': 'Unity URP Manual', 'difficulty': 5, 'hours': 4.0, 'xp': 70},
            {'name': 'Networking for Multiplayer', 'desc': 'Authoritative server, client prediction, interpolation, lag compensation.', 'task': 'Build a 4-player networked prototype using Mirror/Photon/Netcode for Entities.', 'url': 'https://mirror-networking.gitbook.io/docs/', 'resource': 'Mirror Networking Docs', 'difficulty': 5, 'hours': 4.5, 'xp': 80},
            {'name': 'ECS / Data-Oriented Design', 'desc': 'Entity-Component-System, cache locality, and DOTS.', 'task': 'Rewrite a 1000-entity prototype to an ECS pattern. Compare perf.', 'url': 'https://unity.com/dots', 'resource': 'Unity DOTS', 'difficulty': 5, 'hours': 4.0, 'xp': 70},
            {'name': 'Procedural Generation', 'desc': 'Noise, wave function collapse, dungeon generation, and biomes.', 'task': 'Generate a 2D dungeon procedurally with reachable rooms and no dead ends.', 'url': 'https://www.redblobgames.com/', 'resource': 'Red Blob Games', 'difficulty': 4, 'hours': 3.5, 'xp': 65},
            {'name': 'Advanced AI — Behavior Trees & Utility AI', 'desc': 'BTs, utility scoring, and squad AI patterns.', 'task': 'Build a guard squad with role-based behavior (lookout/flanker/medic) using a BT framework.', 'url': 'https://www.gamasutra.com/blogs/ChrisSimpson/20140717/221339/Behavior_trees_for_AI_How_they_work.php', 'resource': 'Behavior Trees Explained', 'difficulty': 4, 'hours': 3.5, 'xp': 65},
            {'name': 'Save Systems & Modding Support', 'desc': 'Robust save formats, versioning, and exposing mod hooks.', 'task': 'Ship a sample mod loader that can override assets and inject scripts.', 'url': 'https://steamcommunity.com/workshop/about/', 'resource': 'Steam Workshop', 'difficulty': 4, 'hours': 3.0, 'xp': 55},
            {'name': 'Analytics & Live Ops', 'desc': 'Funnels, retention, live events, and balance changes after launch.', 'task': 'Instrument a game with 5 key events. Build a funnel from boot → first playthrough complete.', 'url': 'https://docs.unity.com/analytics/', 'resource': 'Unity Analytics', 'difficulty': 4, 'hours': 2.5, 'xp': 45},
            {'name': 'Monetization Models', 'desc': 'Premium, F2P, ads, IAP, season passes — ethics and trade-offs.', 'task': 'Pick a model for your prototype and write a 1-page rationale + projected economics.', 'url': 'https://www.gamedeveloper.com/business', 'resource': 'Game Developer — Business', 'difficulty': 3, 'hours': 2.0, 'xp': 40},
            {'name': 'Console / Steam Release Pipeline', 'desc': 'Steamworks, achievements, cloud saves, and certification basics.', 'task': 'Set up a Steamworks app page draft and a "coming soon" build with achievements.', 'url': 'https://partner.steamgames.com/doc/sdk', 'resource': 'Steamworks Documentation', 'difficulty': 4, 'hours': 3.0, 'xp': 60},
            {'name': 'Shippable Game Capstone', 'desc': 'Take a prototype, polish it, ship it on itch.io or Steam.', 'task': 'Release a complete small game publicly. Collect feedback and patch once.', 'url': 'https://itch.io/', 'resource': 'itch.io Publishing', 'difficulty': 5, 'hours': 8.0, 'xp': 120},
        ],
    },
    'data_engineering': {
        'beginner': [
            {'name': 'What Is Data Engineering?', 'desc': 'Pipelines, warehouses, lakes, and how data teams are organized.', 'task': 'Write a 1-page glossary covering OLTP vs OLAP, lake vs warehouse, batch vs stream.', 'url': 'https://www.databricks.com/glossary/data-engineering', 'resource': 'Databricks DE Glossary', 'difficulty': 1, 'hours': 1.5, 'xp': 20},
            {'name': 'SQL Fundamentals', 'desc': 'SELECT, JOIN, GROUP BY, window functions, and CTEs.', 'task': 'Solve 30 SQL exercises on a public dataset (e.g. Mode SQL Tutorial).', 'url': 'https://mode.com/sql-tutorial/', 'resource': 'Mode SQL Tutorial', 'difficulty': 2, 'hours': 3.0, 'xp': 40},
            {'name': 'Data Modeling Basics', 'desc': 'Normalization, star/snowflake schemas, slowly changing dimensions.', 'task': 'Model a small e-commerce warehouse: orders, customers, products as a star schema.', 'url': 'https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/', 'resource': 'Kimball Group Techniques', 'difficulty': 2, 'hours': 2.5, 'xp': 35},
            {'name': 'Postgres Deep Dive for DE', 'desc': 'EXPLAIN, indexes, partitioning, and bulk-load patterns.', 'task': 'Bulk-load 1M rows into Postgres. Speed up a slow query by 10x using an index.', 'url': 'https://www.postgresql.org/docs/current/', 'resource': 'PostgreSQL Documentation', 'difficulty': 2, 'hours': 3.0, 'xp': 40},
            {'name': 'Python for ETL', 'desc': 'pandas, requests, file I/O, and structured pipelines.', 'task': 'Build a script that pulls a public API daily, transforms it, and writes Parquet to disk.', 'url': 'https://pandas.pydata.org/docs/', 'resource': 'pandas Documentation', 'difficulty': 2, 'hours': 2.5, 'xp': 35},
            {'name': 'File Formats — CSV, JSON, Parquet, Avro', 'desc': 'When each format wins; columnar vs row; compression.', 'task': 'Convert the same dataset to all 4 formats. Compare size and read speed.', 'url': 'https://parquet.apache.org/docs/', 'resource': 'Apache Parquet Docs', 'difficulty': 2, 'hours': 2.0, 'xp': 30},
            {'name': 'Object Storage — S3 Basics', 'desc': 'Buckets, keys, lifecycle policies, and the lakehouse foundation.', 'task': 'Build a daily "raw → bronze" pipeline writing partitioned Parquet to S3.', 'url': 'https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html', 'resource': 'AWS S3 User Guide', 'difficulty': 2, 'hours': 2.0, 'xp': 35},
            {'name': 'Cron & Simple Scheduling', 'desc': 'Cron expressions, idempotency, and lightweight DAGs.', 'task': 'Schedule your ETL with cron. Make it idempotent on re-runs.', 'url': 'https://crontab.guru/', 'resource': 'Crontab Guru', 'difficulty': 2, 'hours': 1.5, 'xp': 25},
            {'name': 'Data Quality Checks', 'desc': 'Row counts, schema checks, freshness, and uniqueness.', 'task': 'Add 5 data quality assertions to your pipeline. Fail loudly when broken.', 'url': 'https://greatexpectations.io/', 'resource': 'Great Expectations', 'difficulty': 2, 'hours': 2.0, 'xp': 35},
            {'name': 'First End-to-End Pipeline', 'desc': 'Tie ingest, storage, transform, and validation into one repeatable flow.', 'task': 'Build raw → cleaned → analytics layers for one dataset, with daily refresh and tests.', 'url': 'https://airbyte.com/blog/data-engineering-lifecycle', 'resource': 'Data Engineering Lifecycle', 'difficulty': 3, 'hours': 3.5, 'xp': 60},
        ],
        'intermediate': [
            {'name': 'Airflow — DAGs, Operators, XComs', 'desc': 'Authoring production DAGs, sensors, retries, SLAs.', 'task': 'Convert your cron pipeline to Airflow. Add retries, alerts, and an SLA.', 'url': 'https://airflow.apache.org/docs/', 'resource': 'Airflow Documentation', 'difficulty': 3, 'hours': 3.5, 'xp': 55},
            {'name': 'dbt — Transformation Workflows', 'desc': 'Models, tests, snapshots, exposures, and software-engineering for SQL.', 'task': 'Build a small dbt project with staging + marts layers and 10 tests.', 'url': 'https://docs.getdbt.com/', 'resource': 'dbt Documentation', 'difficulty': 3, 'hours': 3.5, 'xp': 55},
            {'name': 'Spark — Distributed Compute', 'desc': 'DataFrames, partitions, shuffle, broadcast joins, and the catalyst optimizer.', 'task': 'Run a multi-GB join locally with PySpark. Tune partitions for runtime.', 'url': 'https://spark.apache.org/docs/latest/', 'resource': 'Apache Spark Docs', 'difficulty': 3, 'hours': 4.0, 'xp': 65},
            {'name': 'Kafka — Streaming Basics', 'desc': 'Topics, partitions, consumer groups, offsets.', 'task': 'Stream a clickstream into Kafka. Consume with Spark Structured Streaming.', 'url': 'https://kafka.apache.org/documentation/streams/', 'resource': 'Kafka Streams Docs', 'difficulty': 3, 'hours': 3.5, 'xp': 55},
            {'name': 'Warehouses — Snowflake / BigQuery', 'desc': 'Compute/storage separation, micro-partitions, clustering.', 'task': 'Load a dataset into a free-tier warehouse. Tune one query with clustering keys.', 'url': 'https://docs.snowflake.com/', 'resource': 'Snowflake Documentation', 'difficulty': 3, 'hours': 2.5, 'xp': 45},
            {'name': 'CDC — Change Data Capture', 'desc': 'Debezium, log-based CDC, idempotent sinks.', 'task': 'Set up Debezium to stream Postgres changes into Kafka and land them in S3.', 'url': 'https://debezium.io/', 'resource': 'Debezium Documentation', 'difficulty': 4, 'hours': 3.5, 'xp': 60},
            {'name': 'Lakehouse — Iceberg / Delta', 'desc': 'ACID on object storage, time travel, schema evolution.', 'task': 'Convert your S3 Parquet tables to Iceberg. Time-travel to a past snapshot.', 'url': 'https://iceberg.apache.org/docs/latest/', 'resource': 'Apache Iceberg Docs', 'difficulty': 4, 'hours': 3.5, 'xp': 60},
            {'name': 'Orchestration Patterns', 'desc': 'Backfills, partitioned runs, conditional branches, sensors.', 'task': 'Add a backfill workflow that re-runs the last 30 days of data idempotently.', 'url': 'https://www.astronomer.io/guides/airflow-decorators', 'resource': 'Astronomer Airflow Guides', 'difficulty': 3, 'hours': 2.5, 'xp': 45},
            {'name': 'Observability for Pipelines', 'desc': 'Lineage, freshness alerts, anomaly detection.', 'task': 'Add OpenLineage emitters to your DAGs. Visualize lineage in Marquez.', 'url': 'https://openlineage.io/', 'resource': 'OpenLineage', 'difficulty': 3, 'hours': 2.5, 'xp': 45},
            {'name': 'Cost-Aware Data Pipelines', 'desc': 'Cluster sizing, partition pruning, and avoiding the $10k query.', 'task': 'Audit a workload. Cut one query\'s cost by 50% using partition pruning or clustering.', 'url': 'https://cloud.google.com/bigquery/docs/best-practices-costs', 'resource': 'BigQuery Cost Best Practices', 'difficulty': 3, 'hours': 2.5, 'xp': 45},
        ],
        'advanced': [
            {'name': 'Streaming Architectures — Lambda vs Kappa', 'desc': 'Choosing batch+stream vs streaming-only; reprocessing strategies.', 'task': 'Diagram and justify a Kappa architecture for an e-commerce events pipeline.', 'url': 'https://www.confluent.io/learn/streaming-architecture/', 'resource': 'Confluent Streaming Guide', 'difficulty': 4, 'hours': 3.0, 'xp': 55},
            {'name': 'Exactly-Once Semantics', 'desc': 'Idempotent producers, transactional sinks, and end-to-end EOS.', 'task': 'Build a Kafka → Iceberg pipeline with end-to-end exactly-once guarantees.', 'url': 'https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/', 'resource': 'Confluent EOS Blog', 'difficulty': 5, 'hours': 4.0, 'xp': 75},
            {'name': 'Real-Time Analytics — ClickHouse / Pinot / Druid', 'desc': 'Sub-second analytics over event streams.', 'task': 'Stand up ClickHouse. Ingest events and serve a sub-100ms dashboard query.', 'url': 'https://clickhouse.com/docs', 'resource': 'ClickHouse Documentation', 'difficulty': 4, 'hours': 3.5, 'xp': 65},
            {'name': 'Data Contracts & Schemas', 'desc': 'Producer/consumer contracts, Avro/Protobuf schemas, breaking-change policy.', 'task': 'Author a data contract for one source. Enforce it in CI with a schema registry.', 'url': 'https://www.datamesh-architecture.com/', 'resource': 'Data Mesh Architecture', 'difficulty': 4, 'hours': 3.0, 'xp': 55},
            {'name': 'Data Mesh & Domain Ownership', 'desc': 'Decentralized data ownership, federated governance, and discoverability.', 'task': 'Design a data mesh for a 200-person company. Define domains and a global catalog.', 'url': 'https://martinfowler.com/articles/data-mesh-principles.html', 'resource': 'Martin Fowler — Data Mesh', 'difficulty': 4, 'hours': 3.0, 'xp': 55},
            {'name': 'ML / Feature Store Pipelines', 'desc': 'Offline vs online features, point-in-time joins, and feature freshness.', 'task': 'Build offline + online feature serving for a churn model using Feast.', 'url': 'https://docs.feast.dev/', 'resource': 'Feast Feature Store', 'difficulty': 4, 'hours': 3.5, 'xp': 65},
            {'name': 'Privacy, GDPR & Right-to-Erasure', 'desc': 'PII handling, tokenization, deletion across lakes, and access controls.', 'task': 'Implement right-to-erasure across raw → curated layers for one dataset.', 'url': 'https://gdpr.eu/right-to-be-forgotten/', 'resource': 'GDPR Right to Erasure', 'difficulty': 4, 'hours': 2.5, 'xp': 50},
            {'name': 'Performance Tuning Spark Jobs', 'desc': 'Skew, shuffle, broadcast, AQE, and reading Spark UI.', 'task': 'Take a job that takes 60 min. Get it under 15 min and document each win.', 'url': 'https://spark.apache.org/docs/latest/sql-performance-tuning.html', 'resource': 'Spark Perf Tuning Docs', 'difficulty': 4, 'hours': 3.5, 'xp': 65},
            {'name': 'Disaster Recovery & Backfills', 'desc': 'Snapshots, retention, and replaying weeks of data without corrupting downstream.', 'task': 'Design a DR plan with RPO/RTO. Practice a 7-day backfill.', 'url': 'https://docs.databricks.com/en/disaster-recovery/index.html', 'resource': 'Databricks DR Guide', 'difficulty': 4, 'hours': 3.0, 'xp': 55},
            {'name': 'Production Platform Capstone', 'desc': 'Author a production data platform doc — stack, SLAs, lineage, governance.', 'task': 'Write a 5-page platform doc as if onboarding a new DE team to your design.', 'url': 'https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/', 'resource': 'Fundamentals of Data Engineering (O\'Reilly)', 'difficulty': 5, 'hours': 5.0, 'xp': 100},
        ],
    },
    'java_spring': {
        'beginner': [
            {'name': 'Modern Java Setup (17+)', 'desc': 'JDK install, IntelliJ, Maven/Gradle, and "Hello, Java".', 'task': 'Install JDK 21. Create a Maven project. Run a Hello World.', 'url': 'https://docs.oracle.com/en/java/javase/21/', 'resource': 'Java SE 21 Documentation', 'difficulty': 1, 'hours': 1.5, 'xp': 20},
            {'name': 'Java Language Essentials', 'desc': 'Types, control flow, classes, records, sealed types, pattern matching.', 'task': 'Build 5 small console apps using records, switch patterns, and var.', 'url': 'https://dev.java/learn/', 'resource': 'dev.java Tutorials', 'difficulty': 2, 'hours': 2.5, 'xp': 30},
            {'name': 'Collections & Streams', 'desc': 'List/Map/Set, Optional, and the Streams API.', 'task': 'Re-solve 10 problems using only Streams. Compare readability to imperative loops.', 'url': 'https://docs.oracle.com/en/java/javase/21/core/streams.html', 'resource': 'Java Streams Guide', 'difficulty': 2, 'hours': 2.5, 'xp': 35},
            {'name': 'Maven / Gradle Build Tools', 'desc': 'POM/build.gradle, dependencies, plugins, multi-module projects.', 'task': 'Split a project into 2 modules with a shared library module.', 'url': 'https://maven.apache.org/guides/', 'resource': 'Maven Guides', 'difficulty': 2, 'hours': 2.0, 'xp': 30},
            {'name': 'Spring Boot — Your First REST API', 'desc': 'Starter, auto-config, @RestController, @GetMapping, and Spring DevTools.', 'task': 'Build a /hello and /health endpoint. Run it with `mvn spring-boot:run`.', 'url': 'https://spring.io/guides/gs/spring-boot/', 'resource': 'Spring Boot Getting Started', 'difficulty': 2, 'hours': 2.5, 'xp': 35},
            {'name': 'Dependency Injection in Spring', 'desc': 'Beans, components, configuration classes, profiles.', 'task': 'Refactor a class with 3 hard-coded dependencies into Spring-managed beans.', 'url': 'https://docs.spring.io/spring-framework/reference/core/beans.html', 'resource': 'Spring Beans Documentation', 'difficulty': 2, 'hours': 2.0, 'xp': 30},
            {'name': 'Spring Data JPA', 'desc': 'Entities, repositories, derived queries, and pagination.', 'task': 'Add a Book entity + repository. Persist and list books from Postgres.', 'url': 'https://spring.io/projects/spring-data-jpa', 'resource': 'Spring Data JPA', 'difficulty': 2, 'hours': 3.0, 'xp': 40},
            {'name': 'Validation & Error Handling', 'desc': 'Bean Validation (Jakarta), @ControllerAdvice, problem+json responses.', 'task': 'Add input validation and a global exception handler that returns RFC7807 errors.', 'url': 'https://docs.spring.io/spring-framework/reference/web/webmvc.html', 'resource': 'Spring Web MVC Docs', 'difficulty': 2, 'hours': 2.0, 'xp': 35},
            {'name': 'Configuration & Profiles', 'desc': 'application.yml, env-driven config, profiles, secrets.', 'task': 'Externalize DB credentials. Run the same app under dev and prod profiles.', 'url': 'https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#features.external-config', 'resource': 'Spring Boot External Config', 'difficulty': 2, 'hours': 1.5, 'xp': 30},
            {'name': 'First CRUD Service', 'desc': 'Tie controller + service + repository + DB into a clean layered app.', 'task': 'Ship a Books CRUD service with validation, error handling, and a Postgres DB.', 'url': 'https://spring.io/guides/tutorials/rest/', 'resource': 'Spring REST Tutorial', 'difficulty': 3, 'hours': 3.0, 'xp': 55},
        ],
        'intermediate': [
            {'name': 'Spring Security Fundamentals', 'desc': 'Filter chains, authentication, authorization, password encoding.', 'task': 'Secure your Books API with basic auth and role-based access.', 'url': 'https://docs.spring.io/spring-security/reference/', 'resource': 'Spring Security Reference', 'difficulty': 3, 'hours': 3.0, 'xp': 50},
            {'name': 'JWT-Based Auth', 'desc': 'Issuing JWTs, validation, refresh tokens, stateless APIs.', 'task': 'Replace basic auth with JWTs. Add a refresh endpoint.', 'url': 'https://www.baeldung.com/spring-security-oauth-jwt', 'resource': 'Baeldung Spring + JWT', 'difficulty': 3, 'hours': 3.0, 'xp': 50},
            {'name': 'Database Migrations with Flyway', 'desc': 'Versioned SQL migrations, repeatable migrations, and rollbacks.', 'task': 'Add Flyway. Version every schema change and run a backfill migration.', 'url': 'https://flywaydb.org/documentation/', 'resource': 'Flyway Documentation', 'difficulty': 3, 'hours': 2.5, 'xp': 45},
            {'name': 'Caching with Spring + Redis', 'desc': '@Cacheable, cache eviction, and Redis as a cache backend.', 'task': 'Add caching to a hot read endpoint. Measure throughput before/after.', 'url': 'https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#io.caching', 'resource': 'Spring Boot Caching', 'difficulty': 3, 'hours': 2.5, 'xp': 45},
            {'name': 'Testing — JUnit 5 + MockMvc', 'desc': 'Slice tests, @WebMvcTest, Testcontainers for DB.', 'task': 'Reach 80% coverage on your service. Use Testcontainers for repository tests.', 'url': 'https://testcontainers.com/', 'resource': 'Testcontainers', 'difficulty': 3, 'hours': 3.0, 'xp': 50},
            {'name': 'Observability — Actuator, Micrometer', 'desc': 'Health, metrics, traces, and exposing Prometheus endpoints.', 'task': 'Expose /actuator/prometheus. Scrape it from a local Prometheus + Grafana.', 'url': 'https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#actuator', 'resource': 'Spring Boot Actuator', 'difficulty': 3, 'hours': 2.5, 'xp': 40},
            {'name': 'Async, Scheduling & Retry', 'desc': '@Async, @Scheduled, Resilience4j retries and circuit breakers.', 'task': 'Add a nightly job + a flaky downstream call with retries and a circuit breaker.', 'url': 'https://resilience4j.readme.io/', 'resource': 'Resilience4j', 'difficulty': 3, 'hours': 2.5, 'xp': 45},
            {'name': 'REST API Best Practices', 'desc': 'HATEOAS, versioning, pagination, content negotiation, OpenAPI.', 'task': 'Generate an OpenAPI spec from your service. Add pagination + versioning.', 'url': 'https://springdoc.org/', 'resource': 'springdoc-openapi', 'difficulty': 3, 'hours': 2.5, 'xp': 40},
            {'name': 'Containerizing Spring Boot', 'desc': 'Jib, layered jars, multi-stage Dockerfiles, JVM flags for containers.', 'task': 'Containerize your service with Jib. Run it with Postgres via docker-compose.', 'url': 'https://github.com/GoogleContainerTools/jib', 'resource': 'Jib Container Builder', 'difficulty': 3, 'hours': 2.0, 'xp': 40},
            {'name': 'Messaging with RabbitMQ / Kafka', 'desc': 'Spring AMQP / Spring Kafka, producers, consumers, error topics.', 'task': 'Add an async order-processing flow over Kafka. Handle poison messages.', 'url': 'https://docs.spring.io/spring-kafka/reference/', 'resource': 'Spring for Apache Kafka', 'difficulty': 4, 'hours': 3.0, 'xp': 55},
        ],
        'advanced': [
            {'name': 'Reactive Spring — WebFlux & Project Reactor', 'desc': 'Non-blocking I/O, backpressure, Mono/Flux, R2DBC.', 'task': 'Rewrite a hot endpoint with WebFlux. Compare throughput vs MVC.', 'url': 'https://projectreactor.io/docs/core/release/reference/', 'resource': 'Project Reactor Reference', 'difficulty': 4, 'hours': 4.0, 'xp': 65},
            {'name': 'GraalVM Native Image', 'desc': 'AOT compilation, reflection config, and sub-100ms cold start.', 'task': 'Build a native image of your service. Measure startup and memory delta.', 'url': 'https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#native-image', 'resource': 'Spring Boot Native Image', 'difficulty': 5, 'hours': 4.0, 'xp': 70},
            {'name': 'Spring Cloud — Service Discovery & Config', 'desc': 'Eureka/Consul, Spring Cloud Config, retries, distributed tracing.', 'task': 'Run 3 services with Eureka + Config Server. Verify service-to-service calls.', 'url': 'https://spring.io/projects/spring-cloud', 'resource': 'Spring Cloud', 'difficulty': 4, 'hours': 3.5, 'xp': 60},
            {'name': 'CQRS & Event Sourcing in Spring', 'desc': 'Commands/queries, event store, projections, and rebuilds.', 'task': 'Implement a small CQRS sample with an event store and a read projection.', 'url': 'https://martinfowler.com/bliki/CQRS.html', 'resource': 'Martin Fowler — CQRS', 'difficulty': 5, 'hours': 4.0, 'xp': 70},
            {'name': 'OAuth2 / OIDC with Spring Authorization Server', 'desc': 'Authorization code flow, PKCE, OIDC scopes, JWKS.', 'task': 'Stand up Spring Authorization Server. Authenticate an SPA against it.', 'url': 'https://docs.spring.io/spring-authorization-server/reference/', 'resource': 'Spring Authorization Server', 'difficulty': 4, 'hours': 3.5, 'xp': 65},
            {'name': 'Hexagonal / Clean Architecture in Spring', 'desc': 'Ports & adapters, decoupling Spring from your domain.', 'task': 'Refactor a service to hexagonal layout. Show the domain has zero Spring imports.', 'url': 'https://reflectoring.io/spring-hexagonal/', 'resource': 'Reflectoring — Hexagonal Spring', 'difficulty': 4, 'hours': 3.0, 'xp': 55},
            {'name': 'Performance Tuning the JVM', 'desc': 'GC choice (G1/ZGC), heap sizing, JFR, async-profiler.', 'task': 'Profile a slow service with async-profiler. Fix one allocation hot spot.', 'url': 'https://github.com/jvm-profiling-tools/async-profiler', 'resource': 'async-profiler', 'difficulty': 4, 'hours': 3.5, 'xp': 60},
            {'name': 'Production Observability', 'desc': 'Distributed tracing with OpenTelemetry, log correlation, RED metrics.', 'task': 'Add OpenTelemetry traces. Correlate logs with trace IDs across 2 services.', 'url': 'https://opentelemetry.io/docs/instrumentation/java/', 'resource': 'OpenTelemetry Java', 'difficulty': 4, 'hours': 3.0, 'xp': 55},
            {'name': 'Kubernetes for Spring Boot', 'desc': 'Manifests, readiness/liveness probes, graceful shutdown, secrets.', 'task': 'Deploy your service to a local K8s cluster with proper probes and a HorizontalPodAutoscaler.', 'url': 'https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#deployment.cloud.kubernetes', 'resource': 'Spring Boot on Kubernetes', 'difficulty': 4, 'hours': 3.0, 'xp': 55},
            {'name': 'Production-Ready Microservice Capstone', 'desc': 'Full pipeline: code, tests, OpenAPI, container, K8s, observability.', 'task': 'Ship a small microservice to a public K8s cluster with CI/CD, tracing, and alerts.', 'url': 'https://12factor.net/', 'resource': 'The Twelve-Factor App', 'difficulty': 5, 'hours': 5.0, 'xp': 100},
        ],
    },
}

# Fallback topics for any skill/level combination not explicitly defined
FALLBACK_TOPICS = [
    {'name': 'Foundations & Setup', 'desc': 'Set up environment and understand core concepts.', 'task': 'Complete setup and read through key documentation.', 'url': 'https://docs.python.org/', 'resource': 'Official Documentation', 'difficulty': 1, 'hours': 1.5, 'xp': 20},
    {'name': 'Core Concepts Review', 'desc': 'Review and solidify fundamental concepts.', 'task': 'Take notes and implement 3 examples.', 'url': 'https://www.youtube.com/', 'resource': 'YouTube Tutorials', 'difficulty': 2, 'hours': 2.0, 'xp': 25},
    {'name': 'Hands-on Practice', 'desc': 'Apply concepts with hands-on exercises.', 'task': 'Complete practice exercises.', 'url': 'https://exercism.org/', 'resource': 'Exercism Platform', 'difficulty': 2, 'hours': 2.0, 'xp': 25},
    {'name': 'Advanced Techniques', 'desc': 'Explore advanced patterns and techniques.', 'task': 'Study and implement 2 advanced patterns.', 'url': 'https://www.coursera.org/', 'resource': 'Coursera Courses', 'difficulty': 3, 'hours': 2.5, 'xp': 35},
    {'name': 'Project Application', 'desc': 'Build a mini-project applying learned concepts.', 'task': 'Complete a small project from scratch.', 'url': 'https://github.com/', 'resource': 'GitHub Projects', 'difficulty': 3, 'hours': 3.0, 'xp': 50},
]


def get_skill_key(skill_name: str) -> str:
    """Map skill name to our internal key"""
    name = skill_name.lower()
    explicit = [
        ('devops & cloud', 'devops'),
        ('devops', 'devops'),
        ('system design', 'system_design'),
        ('mobile development', 'mobile'),
        ('mobile', 'mobile'),
        ('game development', 'gamedev'),
        ('game dev', 'gamedev'),
        ('data engineering', 'data_engineering'),
        ('java & spring boot', 'java_spring'),
        ('java spring', 'java_spring'),
        ('spring boot', 'java_spring'),
        ('java', 'java_spring'),
        ('data structures & algorithms', 'dsa'),
        ('dsa', 'dsa'),
        ('python programming', 'python'),
        ('python', 'python'),
        ('web development', 'webdev'),
        ('artificial intelligence / machine learning', 'aiml'),
        ('machine learning', 'aiml'),
        ('ai / ml', 'aiml'),
        ('ai/ml', 'aiml'),
        ('competitive programming', 'competitive'),
        ('blockchain & web3', 'blockchain'),
        ('blockchain', 'blockchain'),
        ('ethical hacking & security', 'ethical_hacking'),
        ('ethical hacking', 'ethical_hacking'),
    ]
    for needle, key in explicit:
        if needle in name:
            return key
    return 'dsa'  # default


def get_topics_for_skill_level(skill_name: str, level: str) -> list:
    """Retrieve relevant topics for skill + level combo"""
    skill_key = get_skill_key(skill_name)
    skill_data = SKILL_TOPICS.get(skill_key, {})
    topics = skill_data.get(level, [])

    if not topics:
        # Try beginner as fallback
        topics = skill_data.get('beginner', FALLBACK_TOPICS)

    return topics if topics else FALLBACK_TOPICS


def generate_roadmap(user, skill, level: str, daily_hours: float, duration_days: int) -> Roadmap:
    """
    Main roadmap generator function.
    Creates a Roadmap and RoadmapTask objects for a given user.
    """
    from datetime import date, timedelta

    # Create the roadmap record
    roadmap = Roadmap.objects.create(
        user=user,
        skill=skill,
        title=f"{skill.name} — {level.title()} Path ({duration_days} Days)",
        level=level,
        daily_hours=daily_hours,
        duration_days=duration_days,
        target_end_date=date.today() + timedelta(days=duration_days),
    )

    topics = get_topics_for_skill_level(skill.name, level)

    # Calculate workload scaling
    base_hours = 1.0
    workload_factor = daily_hours / base_hours  # >1 means more content per day

    # Topics per day based on hours
    # With 1hr: 1 topic per day; with 2hrs: can do 1.5 topics; with 4hrs: 2-3 topics
    topics_per_day = max(1, round(daily_hours / 1.5))

    # Total topic slots available
    total_slots = duration_days * topics_per_day

    # Stretch or compress topic list to fit duration
    if len(topics) < total_slots:
        # Repeat topics with variation if needed (or add review days)
        scheduled = []
        while len(scheduled) < total_slots:
            scheduled.extend(topics)
        scheduled = scheduled[:total_slots]
    else:
        # Compress: skip some intermediate topics
        step = len(topics) / total_slots
        scheduled = [topics[int(i * step)] for i in range(total_slots)]

    # Group topics by day
    day_topics = {}
    for i, topic_data in enumerate(scheduled):
        day = (i // topics_per_day) + 1
        if day > duration_days:
            break
        if day not in day_topics:
            day_topics[day] = []
        day_topics[day].append(topic_data)

    # Create RoadmapTask for each day
    for day_num in range(1, duration_days + 1):
        day_topic_list = day_topics.get(day_num, [topics[day_num % len(topics)]])
        primary = day_topic_list[0]

        # Scale XP with workload
        xp = int(primary['xp'] * workload_factor)

        # Combine descriptions if multiple topics in a day
        if len(day_topic_list) > 1:
            secondary = day_topic_list[1]
            combined_title = f"{primary['name']} + {secondary['name']}"
            combined_task = f"Part 1: {primary['task']}\n\nPart 2: {secondary['task']}"
            combined_desc = f"{primary['desc']}\n\nAlso covers: {secondary['desc']}"
            xp = int((primary['xp'] + secondary['xp'] * 0.5) * workload_factor)
        else:
            combined_title = primary['name']
            combined_task = primary['task']
            combined_desc = primary['desc']

        est_minutes = int(daily_hours * 60)

        RoadmapTask.objects.create(
            roadmap=roadmap,
            day_number=day_num,
            title=combined_title,
            description=combined_desc,
            task_details=combined_task,
            resource_url=primary['url'],
            resource_title=primary['resource'],
            difficulty=primary['difficulty'],
            estimated_minutes=est_minutes,
            xp_reward=xp,
        )

    return roadmap
