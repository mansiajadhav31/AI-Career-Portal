import json

CODING_QUESTIONS = [
    {
        'id': 1,
        'title': 'Two Sum',
        'difficulty': 'Easy',
        'description': 'Given an array of integers nums and an integer target, return indices of the two numbers that add up to target.',
        'examples': [
            {'input': 'nums = [2,7,11,15], target = 9', 'output': '[0,1]'},
            {'input': 'nums = [3,2,4], target = 6', 'output': '[1,2]'}
        ],
        'constraints': '2 <= nums.length <= 10^4, -10^9 <= nums[i] <= 10^9',
        'starter_code': {
            'python': 'def two_sum(nums, target):\n    # Write your solution here\n    pass',
            'javascript': 'function twoSum(nums, target) {\n    // Write your solution here\n}',
            'java': 'public int[] twoSum(int[] nums, int target) {\n    // Write your solution here\n    return new int[0];\n}'
        },
        'test_cases': [
            {'input': [2, 7, 11, 15], 'target': 9, 'expected': [0, 1]},
            {'input': [3, 2, 4], 'target': 6, 'expected': [1, 2]},
            {'input': [3, 3], 'target': 6, 'expected': [0, 1]}
        ]
    },
    {
        'id': 2,
        'title': 'Reverse String',
        'difficulty': 'Easy',
        'description': 'Write a function that reverses a string. The input string is given as an array of characters.',
        'examples': [
            {'input': '["h","e","l","l","o"]', 'output': '["o","l","l","e","h"]'},
            {'input': '["H","a","n","n","a","h"]', 'output': '["h","a","n","n","a","H"]'}
        ],
        'constraints': '1 <= s.length <= 10^5',
        'starter_code': {
            'python': 'def reverse_string(s):\n    # Write your solution here\n    pass',
            'javascript': 'function reverseString(s) {\n    // Write your solution here\n}',
            'java': 'public void reverseString(char[] s) {\n    // Write your solution here\n}'
        },
        'test_cases': [
            {'input': ['h','e','l','l','o'], 'expected': ['o','l','l','e','h']},
            {'input': ['H','a','n','n','a','h'], 'expected': ['h','a','n','n','a','H']}
        ]
    },
    {
        'id': 3,
        'title': 'Fizz Buzz',
        'difficulty': 'Easy',
        'description': 'Write a program that outputs the string representation of numbers from 1 to n. But for multiples of three it should output "Fizz" instead of the number and for the multiples of five output "Buzz". For numbers which are multiples of both three and five output "FizzBuzz".',
        'examples': [
            {'input': 'n = 3', 'output': '["1","2","Fizz"]'},
            {'input': 'n = 5', 'output': '["1","2","Fizz","4","Buzz"]'}
        ],
        'constraints': '1 <= n <= 10^4',
        'starter_code': {
            'python': 'def fizz_buzz(n):\n    result = []\n    # Write your solution here\n    return result',
            'javascript': 'function fizzBuzz(n) {\n    let result = [];\n    // Write your solution here\n    return result;\n}',
            'java': 'public List<String> fizzBuzz(int n) {\n    List<String> result = new ArrayList<>();\n    // Write your solution here\n    return result;\n}'
        },
        'test_cases': [
            {'input': 3, 'expected': ["1","2","Fizz"]},
            {'input': 5, 'expected': ["1","2","Fizz","4","Buzz"]}
        ]
    },
    {
        'id': 4,
        'title': 'Valid Parentheses',
        'difficulty': 'Medium',
        'description': 'Given a string s containing just the characters "(", ")", "{", "}", "[" and "]", determine if the input string is valid.',
        'examples': [
            {'input': 's = "()"', 'output': 'true'},
            {'input': 's = "()[]{}"', 'output': 'true'},
            {'input': 's = "(]"', 'output': 'false'}
        ],
        'constraints': '1 <= s.length <= 10^4',
        'starter_code': {
            'python': 'def is_valid(s):\n    stack = []\n    # Write your solution here\n    return False',
            'javascript': 'function isValid(s) {\n    let stack = [];\n    // Write your solution here\n    return false;\n}',
            'java': 'public boolean isValid(String s) {\n    Stack<Character> stack = new Stack<>();\n    // Write your solution here\n    return false;\n}'
        },
        'test_cases': [
            {'input': '()', 'expected': True},
            {'input': '()[]{}', 'expected': True},
            {'input': '(]', 'expected': False},
            {'input': '([)]', 'expected': False}
        ]
    },
    {
        'id': 5,
        'title': 'Maximum Subarray',
        'difficulty': 'Hard',
        'description': 'Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.',
        'examples': [
            {'input': 'nums = [-2,1,-3,4,-1,2,1,-5,4]', 'output': '6 (subarray: [4,-1,2,1])'},
            {'input': 'nums = [1]', 'output': '1'}
        ],
        'constraints': '1 <= nums.length <= 10^5',
        'starter_code': {
            'python': 'def max_subarray(nums):\n    # Write your solution using Kadane\'s algorithm\n    pass',
            'javascript': 'function maxSubArray(nums) {\n    // Write your solution using Kadane\'s algorithm\n}',
            'java': 'public int maxSubArray(int[] nums) {\n    // Write your solution using Kadane\'s algorithm\n    return 0;\n}'
        },
        'test_cases': [
            {'input': [-2,1,-3,4,-1,2,1,-5,4], 'expected': 6},
            {'input': [1], 'expected': 1},
            {'input': [5,4,-1,7,8], 'expected': 23}
        ]
    }
]

def get_coding_questions(difficulty=None):
    """Get coding questions, optionally filtered by difficulty"""
    if difficulty:
        return [q for q in CODING_QUESTIONS if q['difficulty'] == difficulty]
    return CODING_QUESTIONS

def evaluate_code(code, language, question_id):
    """Evaluate submitted code"""
    
    # Find the question
    question = None
    for q in CODING_QUESTIONS:
        if q['id'] == question_id:
            question = q
            break
    
    if not question:
        return {'score': 0, 'feedback': 'Question not found', 'passed': False}
    
    # Basic evaluation (In production, you'd actually run the code)
    # Here we do a simple analysis
    
    score = 50  # Base score
    feedback = []
    
    # Check code length (more code doesn't mean better, but very short might be incomplete)
    code_length = len(code.strip())
    if code_length < 50:
        score -= 20
        feedback.append("Code seems incomplete. Try to write a complete solution.")
    elif code_length > 200:
        score -= 10
        feedback.append("Try to write more concise code.")
    
    # Check for function definition
    if language == 'python' and 'def ' not in code:
        score -= 30
        feedback.append("No function defined. Define the required function.")
    
    if language == 'javascript' and 'function' not in code and 'const ' not in code:
        score -= 30
        feedback.append("No function defined. Define the required function.")
    
    # Check for return statement
    if 'return' not in code.lower():
        score -= 20
        feedback.append("Missing return statement.")
    
    # Check for basic syntax patterns
    if 'for' in code or 'while' in code:
        score += 10
    
    if 'if' in code:
        score += 5
    
    # Additional checks for specific questions
    if question_id == 1:  # Two Sum
        if 'dict' in code or 'map' in code or 'hash' in code:
            score += 15
            feedback.append("Good use of hash map for O(n) solution!")
    
    if question_id == 2:  # Reverse String
        if 'reverse' in code.lower() or 'while' in code or 'for' in code:
            score += 10
    
    if question_id == 3:  # Fizz Buzz
        if 'Fizz' in code and 'Buzz' in code:
            score += 10
    
    if question_id == 4:  # Valid Parentheses
        if 'stack' in code.lower():
            score += 15
            feedback.append("Good use of stack data structure!")
    
    if question_id == 5:  # Maximum Subarray
        if 'kadane' in code.lower() or 'max' in code:
            score += 15
            feedback.append("Kadane's algorithm is the efficient approach here!")
    
    # Cap score between 0 and 100
    score = max(0, min(100, score))
    
    if score >= 70:
        feedback.insert(0, "Good attempt! Your code shows understanding of the problem.")
    elif score >= 40:
        feedback.insert(0, "Your code is on the right track. Review the logic and try again.")
    else:
        feedback.insert(0, "Your solution needs improvement. Study the problem and try a different approach.")
    
    return {
        'score': score,
        'feedback': '\n'.join(feedback),
        'passed': score >= 70
    }