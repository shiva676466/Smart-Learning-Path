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
    mapping = {
        'Data Structures & Algorithms': 'dsa',
        'Python Programming': 'python',
        'Web Development': 'webdev',
        'Artificial Intelligence / Machine Learning': 'aiml',
        'Competitive Programming': 'competitive',
    }
    for key, val in mapping.items():
        if key.lower() in skill_name.lower() or val in skill_name.lower():
            return val
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
