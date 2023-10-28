askcq_prompt = {
    'zero_shot': [
        {'role': 'system',
         'content': 'You will be given a user requirement and its candidate solutions. '
                    'The user requirement is not clear, leading developers to interpret it differently. '
                    'Thus, the candidate solutions writtent by these developers have different functionalities, and some of them are wrong.'
                    '\nYour task is to clarify this requirement by asking clarifying questions. '
                    'Specifically, you first analyze how each developer understands the requirement. '
                    'Then, by comparing their different understandings of the requirement, '
                    'you can determine which statements in the requirement are not clear, and ask clarification questions for those statements.',
    }],

    'one_shot': [
        {'role': 'system',
         'content': 'You will be given a user requirement and its candidate solutions. '
                    'The user requirement is not clear, leading developers to interpret it differently. '
                    'Thus, the candidate solutions writtent by these developers have different functionalities, and some of them are wrong.'
                    '\nYour task is to clarify this requirement by asking clarifying questions. '
                    'Specifically, you first analyze how each developer understands the requirement. '
                    'Then, by comparing their different understandings of the requirement, '
                    'you can determine which statements in the requirement are not clear, and ask clarification questions for those statements.',

         },
        {'role': 'user',
         'content': "User Requirement:\nfrom typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    \"\"\" Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups('( ) (( )) (( )( ))')\n    ['()', '(())', '(()())']\n    \"\"\""
                    "\nSolution 0:\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    result = []\n    stack = []\n    current_group = \"\"\n    \n    for char in paren_string:\n        if char == \"(\":\n            stack.append(char)\n        elif char == \")\":\n            stack.pop()\n        \n        current_group += char\n        \n        if not stack:\n            result.append(current_group.replace(\" \", \"\"))\n            current_group = \"\"\n    \n    return result"
                    "\nSolution 1:\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    result = []\n    stack = []\n    current_group = ''\n    for char in paren_string:\n        if char == '(':\n            stack.append(char)\n            current_group += char\n        elif char == ')':\n            stack.pop()\n            current_group += char\n            if not stack:\n                result.append(current_group)\n                current_group = ''\n    return result"
                    "\nSolution 2:\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    stack = []\n    result = []\n    current_group = ''\n    for char in paren_string:\n        if char == '(':\n            stack.append(char)\n        elif char == ')':\n            stack.pop()\n        if not stack:\n            current_group += char\n            result.append(current_group)\n            current_group = ''\n        else:\n            current_group += char\n    return result"
         },
        {'role': 'assistant',
         'content': 'Solution 0:\n- Solution 0 maintains a stack to keep track of open and close parentheses.\n- It accumulates characters into current_group until the stack becomes empty, indicating the completion of a balanced group.\n- However, it appends spaces to the current_group, and removes spaces from the current_group before appending it to the result, which seems to deviate from the requirement to ignore spaces.'
                    '\nSolution 1:\n- Solution 1 also maintains a stack to track balanced parentheses.\n- It accumulates characters into current_group and appends to result when a balanced group is encountered.\n- This solution seems to properly handle the nested structure of parentheses and the requirement to ignore spaces.'
                    '\nSolution 2:\n- Solution 2 is similar to Solution 0, also maintaining a stack and updating current_group.\n- It adds current_group to result when the stack becomes empty, indicating a balanced group.\n- However, it appends the current_group to the result without removing spaces.'
                    '\nClarifying Questions:\n1. Should the function remove spaces from the input string before processing it, or should it handle spaces within the groups of parentheses?'
                    '\n2. Should the final output in the result list include spaces?'
         },
    ],

    'two_shot': [
        {'role': 'system',
         'content': "You will be given a user requirement and its code solutions. However, these solutions have different functionalities, and at most only one of them is correct. This problem is due to one of two reasons:"
                    "\nR1. The requirement is unclear, resulting in some solutions misunderstanding the user's intention."
                    "\nR2. The requirement is clear, but some solutions ignore specific information provided in the requirement."
                    "\nYour task is to clarify this requirement through the following steps:"
                    "\n1. Analyze these solutions, and compare their differences in comprehending the requirement."
                    "\n2. Determine which reason (R1 or R2) causes these solutions to have different understandings. "
                    "If it is due to R1, raise clarifying questions for the requirement and wait for user feedback. If it is due to R2, provide the ignored information for clarification."
                    "\nNote that some (may be all) of the given solutions are wrong, please strictly follow the above steps to find the reason, and reply with \"### Analysis\" and \"### Conclusion\".",
        },
        {'role': 'user',
         'content': 'User Requirement:\ndef below_zero(operations):\n    """ You\'re given a list of deposit and withdrawal operations on a bank account that starts with\n    zero balance. Your task is to detect if the balance of account will fall below zero.\n    """'
                    '\nSolution 0:\ndef below_zero(operations):\n    if sum(operations) < 0:\n        return True\n    else:\n        return False'
                    '\nSolution 1:\ndef below_zero(operations):\n    balance = 0\n    for operation in operations:\n        balance += operation\n        if balance < 0:\n            return True\n    return False'
                    '\nSolution 2:\ndef below_zero(operations):\n    balance = 0\n    for idx, operation in enumerate(operations):\n        balance += operation\n        if balance < 0:\n            return idx\n    return -1'},
        {'role': 'assistant',
         'content': '### Analysis:'
                    '\nSolution 0:\n- Solution 0 calculates the total balance by summing up all the operations.\n- If the total balance is less than zero, it returns True, indicating that the balance fell below zero. Otherwise, it returns False.\nSolution 1:\n- Solution 1 uses a variable balance to keep track of the account balance.\n- It iterates through the operations, adding each operation to the balance. If at any point the balance falls below zero, it returns True.\nSolution 2:\n- Similar to Solution 1, it iterates through the operations and keeps track of the balance.\n- However, it returns the index where the balance goes below zero (if it does), and -1 if it never goes below zero.'
                    '\n\n### Conclusion:\nThe different understandings in these solutions arise from reason R1 (the requirement is unclear). Specifically, it is unclear whether the requirement is aimed at detecting account balances at any point or at the final point. Also, the expected return value is not mentioned in the requirement. To clarify this requirement, we need to raise clarifying questions to obtain additional information:'
                    '\n1. Is the requirement intended to detect if the balance falls below zero at any point during the operations, or is it intended to detect if the balance falls below zero at the final point only?'
                    '\n2. Should the function return a boolean value to indicate whether the balance goes below zero or not?'
         },
        {'role': 'user',
         'content': "User Requirement:\nfrom typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    \"\"\" Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups('( ) (( )) (( )( ))')\n    ['()', '(())', '(()())']\n    \"\"\""
                    "\nSolution 0:\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    result = []\n    stack = []\n    current_group = \"\"\n    \n    for char in paren_string:\n        if char == \"(\":\n            stack.append(char)\n        elif char == \")\":\n            stack.pop()\n        \n        current_group += char\n        \n        if not stack:\n            result.append(current_group.replace(\" \", \"\"))\n            current_group = \"\"\n    \n    return result"
                    "\nSolution 1:\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    result = []\n    stack = []\n    current_group = ''\n    for char in paren_string:\n        if char == '(':\n            stack.append(char)\n            current_group += char\n        elif char == ')':\n            stack.pop()\n            current_group += char\n            if not stack:\n                result.append(current_group)\n                current_group = ''\n    return result"
                    "\nSolution 2:\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    stack = []\n    result = []\n    current_group = ''\n    for char in paren_string:\n        if char == '(':\n            stack.append(char)\n        elif char == ')':\n            stack.pop()\n        if not stack:\n            current_group += char\n            result.append(current_group)\n            current_group = ''\n        else:\n            current_group += char\n    return result"
         },
        {'role': 'assistant',
         'content': '### Analysis:'
                    '\nSolution 0:\n- Solution 0 maintains a stack to keep track of open and close parentheses.\n- It accumulates characters into current_group until the stack becomes empty, indicating the completion of a balanced group.\n- However, it appends spaces to the current_group, and removes spaces from the current_group before appending it to the result, which seems to deviate from the requirement to ignore spaces.\nSolution 1:\n- Solution 1 also maintains a stack to track balanced parentheses.\n- It accumulates characters into current_group and appends to result when a balanced group is encountered.\n- This solution seems to properly handle the nested structure of parentheses and the requirement to ignore spaces.\nSolution 2:\n- Solution 2 is similar to Solution 0, also maintaining a stack and updating current_group.\n- It adds current_group to result when the stack becomes empty, indicating a balanced group.\n- However, it appends the current_group to the result without removing spaces.'
                    '\n\n### Conclusion:\nThe different understandings in these solutions arise from reason R2 (some solutions ignore specific information provided in the requirement). Therefore, we need to provide information that has been ignored in the requirement:'
                    '\n1. The function should ignore any spaces in the input string.'
                    '\n2. The result list should not include spaces.'
         },
    ],

    'three_shot': [
        {'role': 'system',
         'content': "You will receive a user requirement and some solutions written by different developers. "
                    "However, the functionality of these solutions is different. The reason behind this is that the requirement is unclear, leading the developers to understand the requirement differently. "
                    "Your task is to clarify this requirement by asking clarifying questions. "
                    "Specifically, you first analyze how each developer understands the requirement. "
                    "Then, by comparing their different understandings of the requirement, you can determine which statements in the requirement are not clear, "
                    "and ask clarification questions for those statements."
         },

        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    """ Check if in given list of numbers, are any two numbers closer to each other than\n    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    """'
                    '\nSolution 0:\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    for i in range(len(numbers)):\n        for j in range(i + 1, len(numbers)):\n            if abs(numbers[i] - numbers[j]) < threshold:\n                return True\n    return False'
                    '\nSolution 1:\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    flag = True\n    for i in range(len(numbers)):\n        for j in range(i + 1, len(numbers)):\n            if abs(numbers[i] - numbers[j]) >= threshold:\n                flag = False\n    return flag'
         },
        {'role': 'assistant',
         'content': "Solution 0:\n- Solution 0 iterates through all possible pairs of numbers and checks if the absolute difference between them is less than the threshold.\n- It returns True as soon as it finds such a pair.\n- This solution checks if any two numbers are closer than the threshold."
                    "\nSolution 1:\n- Solution 1 seems to assume that initially, the flag is set to True, and it checks if any pair of numbers violates the threshold condition. If a pair is found that doesn't satisfy the condition, the flag is set to False.\n- After checking all pairs, it returns the value of the flag.\n- This solution checks if all pairs of numbers satisfy the threshold condition, and if any pair doesn't, it returns False."
                    "\nClarifying Questions:"
                    "\n1. Is the requirement intended to check if there is any pair of numbers in the list whose absolute difference is less than a given threshold?"
         },

        {'role': 'user',
         'content': "User Requirement:\nfrom typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    \"\"\" Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups('( ) (( )) (( )( ))')\n    ['()', '(())', '(()())']\n    \"\"\""
                    "\nSolution 0:\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    result = []\n    stack = []\n    current_group = \"\"\n    \n    for char in paren_string:\n        if char == \"(\":\n            stack.append(char)\n        elif char == \")\":\n            stack.pop()\n        \n        current_group += char\n        \n        if not stack:\n            result.append(current_group.replace(\" \", \"\"))\n            current_group = \"\"\n    \n    return result"
                    "\nSolution 1:\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    result = []\n    stack = []\n    current_group = ''\n    for char in paren_string:\n        if char == '(':\n            stack.append(char)\n            current_group += char\n        elif char == ')':\n            stack.pop()\n            current_group += char\n            if not stack:\n                result.append(current_group)\n                current_group = ''\n    return result"
                    "\nSolution 2:\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    stack = []\n    result = []\n    current_group = ''\n    for char in paren_string:\n        if char == '(':\n            stack.append(char)\n        elif char == ')':\n            stack.pop()\n        if not stack:\n            current_group += char\n            result.append(current_group)\n            current_group = ''\n        else:\n            current_group += char\n    return result"
         },
        {'role': 'assistant',
         'content': 'Solution 0:\n- Solution 0 maintains a stack to keep track of open and close parentheses.\n- It accumulates characters into current_group until the stack becomes empty, indicating the completion of a balanced group.\n- However, it appends spaces to the current_group, and removes spaces from the current_group before appending it to the result, which seems to deviate from the requirement to ignore spaces.'
                    '\nSolution 1:\n- Solution 1 also maintains a stack to track balanced parentheses.\n- It accumulates characters into current_group and appends to result when a balanced group is encountered.\n- This solution seems to properly handle the nested structure of parentheses and the requirement to ignore spaces.'
                    '\nSolution 2:\n- Solution 2 is similar to Solution 0, also maintaining a stack and updating current_group.\n- It adds current_group to result when the stack becomes empty, indicating a balanced group.\n- However, it appends the current_group to the result without removing spaces.'
                    '\nClarifying Questions:'
                    '\n1. What does it mean for groups to be "not nested within each other"? Are we allowed to have groups that are partially overlapping, or should they be completely separate?'
                    '\n2. Should the function remove spaces from the input string before processing it, or should it handle spaces within the groups of parentheses?'
                    '\n3. Should the final output in the result list include spaces?'
         },

        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef below_zero(operations: List[int]) -> bool:\n    """ You\'re given a list of deposit and withdrawal operations on a bank account that starts with\n    zero balance. Your task is to detect if at any point the balance of account fallls below zero, and\n    at that point function should return True. Otherwise it should return False.\n    >>> below_zero([1, 2, 3])\n    False\n    >>> below_zero([1, 2, -4, 5])\n    True\n    """'
                    '\nSolution 0:\ndef below_zero(operations: List[int]) -> bool:\n    if sum(operations) < 0:\n        return True\n    else:\n        return False'
                    '\nSolution 1:\ndef below_zero(operations: List[int]) -> bool:\n    balance = 0\n    for operation in operations:\n        balance += operation\n        if balance < 0:\n            return True\n    return False'
         },
        {'role': 'assistant',
         'content': 'Solution 0:\n- Solution 0 calculates the total balance by summing up all the operations.\n- If the total balance is less than zero, it returns True, indicating that the balance fell below zero. Otherwise, it returns False.\n- This solution seems to be interpreting the requirement as checking if the overall balance change is negative.'
                    '\nSolution 1:\n- Solution 1 uses a variable balance to keep track of the account balance.\n- It iterates through the operations, adding each operation to the balance. If at any point the balance falls below zero, it returns True.\n- This solution appears to be interpreting the requirement as checking if the balance becomes negative at any point during the operations.'
                    '\nClarifying Questions:'
                    '\n1. Should the function detect if the balance falls below zero at any point during the operations, or is it intended to detect if the balance falls below zero at the final point only?'
                    '\n2. If the balance drops to zero exactly, is that also considered "the balance falls below zero"?'
         },
    ],

    'four_shot': [
        {'role': 'system',
         'content': "You will receive a user requirement and some solutions written by different developers. "
                    "However, the functionality of these solutions is different. The reason behind this is that the requirement is unclear, leading the developers to understand the requirement differently. "
                    "Your task is to clarify this requirement by asking clarifying questions. "
                    "Specifically, you first analyze how each developer understands the requirement. "
                    "Then, by comparing their different understandings of the requirement, you can determine which statements in the requirement are not clear, "
                    "and ask clarification questions for those statements. "
                    "Do not judge the correctness of these solutions, just analyze the unclear parts of this requirement and ask clarifying questions."
         },
        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    """ Check if in given list of numbers, are any two numbers closer to each other than\n    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    """'
                    '\nSolution 0:\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    for i in range(len(numbers)):\n        for j in range(i + 1, len(numbers)):\n            if abs(numbers[i] - numbers[j]) < threshold:\n                return True\n    return False'
                    '\nSolution 1:\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    flag = True\n    for i in range(len(numbers)):\n        for j in range(i + 1, len(numbers)):\n            if abs(numbers[i] - numbers[j]) >= threshold:\n                flag = False\n    return flag'
         },
        {'role': 'assistant',
         'content': "Solution 0:\n- Solution 0 iterates through all possible pairs of numbers and checks if the absolute difference between them is less than the threshold.\n- It returns True as soon as it finds such a pair.\n- This solution checks if any two numbers are closer than the threshold."
                    "\nSolution 1:\n- Solution 1 seems to assume that initially, the flag is set to True, and it checks if any pair of numbers violates the threshold condition. If a pair is found that doesn't satisfy the condition, the flag is set to False.\n- After checking all pairs, it returns the value of the flag.\n- This solution checks if all pairs of numbers satisfy the threshold condition, and if any pair doesn't, it returns False."
                    "\nClarifying Questions:\n1. Is the requirement intended to check if there is any pair of numbers in the list whose absolute difference is less than a given threshold?"
         },

        {'role': 'user',
         'content': "User Requirement:\nfrom typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    \"\"\" Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups('( ) (( )) (( )( ))')\n    ['()', '(())', '(()())']\n    \"\"\""
                    "\nSolution 0:\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    result = []\n    stack = []\n    current_group = \"\"\n    \n    for char in paren_string:\n        if char == \"(\":\n            stack.append(char)\n        elif char == \")\":\n            stack.pop()\n        \n        current_group += char\n        \n        if not stack:\n            result.append(current_group.replace(\" \", \"\"))\n            current_group = \"\"\n    \n    return result"
                    "\nSolution 1:\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    result = []\n    stack = []\n    current_group = ''\n    for char in paren_string:\n        if char == '(':\n            stack.append(char)\n            current_group += char\n        elif char == ')':\n            stack.pop()\n            current_group += char\n            if not stack:\n                result.append(current_group)\n                current_group = ''\n    return result"
                    "\nSolution 2:\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    stack = []\n    result = []\n    current_group = ''\n    for char in paren_string:\n        if char == '(':\n            stack.append(char)\n        elif char == ')':\n            stack.pop()\n        if not stack:\n            current_group += char\n            result.append(current_group)\n            current_group = ''\n        else:\n            current_group += char\n    return result"
         },
        {'role': 'assistant',
         'content': 'Solution 0:\n- Solution 0 maintains a stack to keep track of open and close parentheses.\n- It accumulates characters into current_group until the stack becomes empty, indicating the completion of a balanced group.\n- However, it appends spaces to the current_group, and removes spaces from the current_group before appending it to the result, which seems to deviate from the requirement to ignore spaces.'
                    '\nSolution 1:\n- Solution 1 also maintains a stack to track balanced parentheses.\n- It accumulates characters into current_group and appends to result when a balanced group is encountered.\n- This solution seems to properly handle the nested structure of parentheses and the requirement to ignore spaces.'
                    '\nSolution 2:\n- Solution 2 is similar to Solution 0, also maintaining a stack and updating current_group.\n- It adds current_group to result when the stack becomes empty, indicating a balanced group.\n- However, it appends the current_group to the result without removing spaces.'
                    '\nClarifying Questions:\n1. Should the function remove spaces from the input string before processing it, or should it handle spaces within the groups of parentheses?'
                    '\n2. Should the final output in the result list include spaces?'
         },

        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef below_zero(operations: List[int]) -> bool:\n    """ You\'re given a list of deposit and withdrawal operations on a bank account that starts with\n    zero balance. Your task is to detect if at any point the balance of account fallls below zero, and\n    at that point function should return True. Otherwise it should return False.\n    >>> below_zero([1, 2, 3])\n    False\n    >>> below_zero([1, 2, -4, 5])\n    True\n    """'
                    '\nSolution 0:\ndef below_zero(operations: List[int]) -> bool:\n    if sum(operations) < 0:\n        return True\n    else:\n        return False'
                    '\nSolution 1:\ndef below_zero(operations: List[int]) -> bool:\n    balance = 0\n    for operation in operations:\n        balance += operation\n        if balance < 0:\n            return True\n    return False'
         },
        {'role': 'assistant',
         'content': 'Solution 0:\n- Solution 0 calculates the total balance by summing up all the operations.\n- If the total balance is less than zero, it returns True, indicating that the balance fell below zero. Otherwise, it returns False.\n- This solution seems to be interpreting the requirement as checking if the overall balance change is negative.'
                    '\nSolution 1:\n- Solution 1 uses a variable balance to keep track of the account balance.\n- It iterates through the operations, adding each operation to the balance. If at any point the balance falls below zero, it returns True.\n- This solution appears to be interpreting the requirement as checking if the balance becomes negative at any point during the operations.'
                    '\nClarifying Questions:'
                    '\n1. Should the function detect if the balance falls below zero at any point during the operations, or is it intended to detect if the balance falls below zero at the final point only?'
                    '\n2. If the balance drops to zero exactly, is that also considered "the balance falls below zero"?'
         },

        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef mean_absolute_deviation(numbers: List[float]) -> float:\n    """ For a given list of input numbers, calculate Mean Absolute Deviation\n    around the mean of this dataset.\n    Mean Absolute Deviation is the average absolute difference between each\n    element and a centerpoint (mean in this case):\n    MAD = average | x - x_mean |\n    >>> mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])\n    1.0\n    """'
                    '\nSolution 0:\ndef mean_absolute_deviation(numbers: List[float]) -> float:\n    mean = sum(numbers) / len(numbers)\n    return sum(x - mean for x in numbers) / len(numbers)'
                    '\nSolution 1:\ndef mean_absolute_deviation(numbers: List[float]) -> float:\n    mean = sum(numbers) / len(numbers)\n    avg_list = [abs(x - mean) for x in numbers]\n    return sum(avg_list)'
                    '\nSolution 2:\ndef mean_absolute_deviation(numbers: List[float]) -> float:\n    mean = sum(numbers) / len(numbers)\n    return sum(abs(x - mean) for x in numbers) / len(numbers)'
         },
        {'role': 'assistant',
         'content': 'Solution 0:\n- Solution 0 first calculates the mean of the input numbers.\n- It then calculates the sum of the differences between each element and the mean, instead of the absolute differences as required by the Mean Absolute Deviation formula.'
                    '\nSolution 1:\n- Solution 1 first calculates the mean of the input numbers.\n- It then calculates the absolute differences between each element and the mean, stores them in the avg_list.\n- However, it returns the sum of the absolute differences, which seems to deviate from the requirement to calculate mean the absolute deviation.'
                    '\nSolution 2:\n- Solution 2 calculates the mean of the input numbers.\n- It then calculates the sum of the absolute differences between each element and the mean, and returns the average of these absolute differences.'
                    '\nClarifying Questions:'
                    '\n1. Is the centerpoint referred to in the requirement the same as the mean of the input numbers?'
                    '\n2. Should the function calculate the absolute differences between each element and the mean? Or just the differences between each element and the mean?'
                    '\n3. Should the function return the average of the absolute differences or the sum of the absolute differences?'
         },
    ],
}

answercq_prompt = {
    'zero_shot': [
        {'role': 'system',
         'content': 'You will receive a user requirement and its clarifying questions. '
                    'Your task is to answer these clarifying questions drawing on the information provided in the given requirement. '
                    'For certain questions, if the requirement does not provide the relevant information, you can make assumptions to answer them. '
                    'Reply only with the answers, do not repeat the requirement and questions.'
         }],

    'one_shot': [
        {'role': 'system',
         'content': 'You will receive a user requirement and its clarifying questions. '
                    'Your task is to answer these clarifying questions drawing on the information provided in the given requirement. '
                    'For certain questions, if the requirement does not provide the relevant information, you can make assumptions to answer them. '
                    'Reply only with the answers, do not repeat the requirement and questions.'
         },
        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups(\'( ) (( )) (( )( ))\')\n    [\'()\', \'(())\', \'(()())\']\n    """'
                    '\n\nClarifying Questions:\n1. Should the function remove spaces from the input string before processing it, or should it handle spaces within the groups of parentheses?'
                    '\n2. Should the final output in the result list include spaces?'
                    '\n\nAnswers:\n{insert your answers here}'
         },
        {'role': 'assistant',
         'content': '1. The requirement mentions that "Ignore any spaces in the input string", '
                    'so you can remove spaces from the input string directly or ignore spaces when processing the input string.'
                    '\n2. No, the final output in the result list should not include spaces.'
         },
    ],

    'two_shot': [
        {'role': 'system',
         'content': 'You will receive a user requirement and some clarifying questions for the requirement. '
                    'Your task is to answer these clarifying questions '
                    'drawing on the information provided in the given requirement. '
                    'Reply only with the answers, do not repeat the requirement and questions.'
         },
        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    """ Check if in given list of numbers, are any two numbers closer to each other than\n    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    """'
                    '\n\nClarifying Questions:\n1. Is the requirement intended to check if there is any pair of numbers in the list whose absolute difference is less than a given threshold?'
                    '\n\nAnswers:\n{insert your answers here}'
         },
        {'role': 'assistant',
         'content': '1. Yes, the requirement aims to check if there is any pair of numbers in the list whose absolute difference is less than a given threshold.'
         },
        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups(\'( ) (( )) (( )( ))\')\n    [\'()\', \'(())\', \'(()())\']\n    """'
                    '\n\nClarifying Questions:\n1. Should the function remove spaces from the input string before processing it, or should it handle spaces within the groups of parentheses?'
                    '\n2. Should the final output in the result list include spaces?'
                    '\n\nAnswers:\n{insert your answers here}'
         },
        {'role': 'assistant',
         'content': '1. The requirement mentions that "Ignore any spaces in the input string", '
                    'so you can remove spaces from the input string directly or ignore spaces when processing the input string.'
                    '\n2. No, the final output in the result list should not include spaces.'
         },
    ],

    'three_shot': [
        {'role': 'system',
         'content': 'You will receive a user requirement and some clarifying questions for the requirement. '
                    'Your task is to answer these clarifying questions '
                    'drawing on the information provided in the given requirement. '
                    'Reply only with the answers, do not repeat the requirement and questions.'
         },

        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    """ Check if in given list of numbers, are any two numbers closer to each other than\n    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    """'
                    '\n\nClarifying Questions:\n1. Is the requirement intended to check if there is any pair of numbers in the list whose absolute difference is less than a given threshold?'
                    '\n\nAnswers:\n{insert your answers here}'
         },
        {'role': 'assistant',
         'content': '1. Yes, the requirement aims to check if there is any pair of numbers in the list whose absolute difference is less than a given threshold.'
         },

        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups(\'( ) (( )) (( )( ))\')\n    [\'()\', \'(())\', \'(()())\']\n    """'
                    '\n\nClarifying Questions:'
                    '\n1. What does it mean for groups to be "not nested within each other"? Are we allowed to have groups that are partially overlapping, or should they be completely separate?'
                    '\n2. Should the function remove spaces from the input string before processing it, or should it handle spaces within the groups of parentheses?'
                    '\n3. Should the final output in the result list include spaces?'
                    '\n\nAnswers:\n{insert your answers here}'
         },
        {'role': 'assistant',
         'content': '1. It means that a group of parentheses should not be completely enclosed within another group of parentheses. Each group should be a distinct and separate entity.'
                    '\n2. The requirement mentions that "Ignore any spaces in the input string", '
                    'so you can remove spaces from the input string directly or ignore spaces when processing the input string.'
                    '\n3. No, the final output in the result list should not include spaces.'
         },

        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef below_zero(operations: List[int]) -> bool:\n    """ You\'re given a list of deposit and withdrawal operations on a bank account that starts with\n    zero balance. Your task is to detect if at any point the balance of account fallls below zero, and\n    at that point function should return True. Otherwise it should return False.\n    >>> below_zero([1, 2, 3])\n    False\n    >>> below_zero([1, 2, -4, 5])\n    True\n    """'
                    '\n\nClarifying Questions:'
                    '\n1. Should the function detect if the balance falls below zero at any point during the operations, or is it intended to detect if the balance falls below zero at the final point only?'
                    '\n2. If the balance drops to zero exactly, is that also considered "the balance falls below zero"?'
                    '\n\nAnswers:\n{insert your answers here}'
         },
        {'role': 'assistant',
         'content': '1. The function should detect if the balance falls below zero at any point.'
                    '\n2. No, the requirement specifically states that the function should detect when the balance becomes negative. Therefore, if the balance drops to exactly zero, it is not considered as "the balance falls below zero."'
         },
    ],

    'one_shot_w_test': [
        {'role': 'system',
         'content': 'You will receive a Python function and its test cases. '
                        'Your task is to answer some clarifying questions using the information provided in the given function and tests. '
                        'Reply only with the answers, do not repeat the code and questions.'
        },
        {'role': 'user',
         'content': 'Python Function:'
                    '\nfrom typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups(\'( ) (( )) (( )( ))\')\n    [\'()\', \'(())\', \'(()())\']\n    """\n    result = []\n    current_string = []\n    current_depth = 0\n\n    for c in paren_string:\n        if c == \'(\':\n            current_depth += 1\n            current_string.append(c)\n        elif c == \')\':\n            current_depth -= 1\n            current_string.append(c)\n\n            if current_depth == 0:\n                result.append(\'\'.join(current_string))\n                current_string.clear()\n\n    return result'
                    '\nTest Cases:'
                    '\ndef check(candidate):\n    assert candidate(\'(()()) ((())) () ((())()())\') == [\n        \'(()())\', \'((()))\', \'()\', \'((())()())\'\n    ]\n    assert candidate(\'() (()) ((())) (((())))\') == [\n        \'()\', \'(())\', \'((()))\', \'(((())))\'\n    ]\n    assert candidate(\'(()(())((())))\') == [\n        \'(()(())((())))\'\n    ]\n    assert candidate(\'( ) (( )) (( )( ))\') == [\'()\', \'(())\', \'(()())\']'
                    '\n\nClarifying Questions:\n1. Should the function remove spaces from the input string before processing it, or should it handle spaces within the groups of parentheses?'
                    '\n2. Should the final output in the result list include spaces?'
                    '\n\nAnswers:\n{insert your answers here}'
         },
        {'role': 'assistant',
         'content': '1. The requirement mentions that "Ignore any spaces in the input string", '
                    'so you can remove spaces from the input string directly or ignore spaces when processing the input string.'
                    '\n2. No, the final output in the result list should not include spaces.'
         },
    ],

    'two_shot_w_test': [
        {'role': 'system',
         'content': 'You will receive a Python function and its test cases. '
                    'Your task is to answer some clarifying questions using the information provided in the given function and tests. '
                    'Reply only with the answers, do not repeat the code and questions.'
         },
        {'role': 'user',
         'content': 'Python Function:'
                    '\nfrom typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    """ Check if in given list of numbers, are any two numbers closer to each other than\n    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    """\n    for idx, elem in enumerate(numbers):\n        for idx2, elem2 in enumerate(numbers):\n            if idx != idx2:\n                distance = abs(elem - elem2)\n                if distance < threshold:\n                    return True\n\n    return False'
                    '\nTest Cases:'
                    '\ndef check(candidate):\n    assert candidate([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) == True\n    assert candidate([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05) == False\n    assert candidate([1.0, 2.0, 5.9, 4.0, 5.0], 0.95) == True\n    assert candidate([1.0, 2.0, 5.9, 4.0, 5.0], 0.8) == False\n    assert candidate([1.0, 2.0, 3.0, 4.0, 5.0, 2.0], 0.1) == True\n    assert candidate([1.1, 2.2, 3.1, 4.1, 5.1], 1.0) == True\n    assert candidate([1.1, 2.2, 3.1, 4.1, 5.1], 0.5) == False'
                    '\n\nClarifying Questions:\n1. Is the requirement intended to check if there is any pair of numbers in the list whose absolute difference is less than a given threshold?'
                    '\n\nAnswers:\n{insert your answers here}'
         },
        {'role': 'assistant',
         'content': '1. Yes, the requirement aims to check if there is any pair of numbers in the list whose absolute difference is less than a given threshold.'
         },
        {'role': 'user',
         'content': 'Python Function:'
                    '\nfrom typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups(\'( ) (( )) (( )( ))\')\n    [\'()\', \'(())\', \'(()())\']\n    """\n    result = []\n    current_string = []\n    current_depth = 0\n\n    for c in paren_string:\n        if c == \'(\':\n            current_depth += 1\n            current_string.append(c)\n        elif c == \')\':\n            current_depth -= 1\n            current_string.append(c)\n\n            if current_depth == 0:\n                result.append(\'\'.join(current_string))\n                current_string.clear()\n\n    return result'
                    '\nTest Cases:'
                    '\ndef check(candidate):\n    assert candidate(\'(()()) ((())) () ((())()())\') == [\n        \'(()())\', \'((()))\', \'()\', \'((())()())\'\n    ]\n    assert candidate(\'() (()) ((())) (((())))\') == [\n        \'()\', \'(())\', \'((()))\', \'(((())))\'\n    ]\n    assert candidate(\'(()(())((())))\') == [\n        \'(()(())((())))\'\n    ]\n    assert candidate(\'( ) (( )) (( )( ))\') == [\'()\', \'(())\', \'(()())\']'
                    '\n\nClarifying Questions:\n1. Should the function remove spaces from the input string before processing it, or should it handle spaces within the groups of parentheses?'
                    '\n2. Should the final output in the result list include spaces?'
                    '\n\nAnswers:\n{insert your answers here}'
         },
        {'role': 'assistant',
         'content': '1. The requirement mentions that "Ignore any spaces in the input string", '
                    'so you can remove spaces from the input string directly or ignore spaces when processing the input string.'
                    '\n2. No, the final output in the result list should not include spaces.'
         },
    ],

    'three_shot_w_test': [
        {'role': 'system',
         'content': 'You will receive a Python function and its test cases. '
                    'Your task is to answer some clarifying questions using the information provided in the given function and tests. '
                    'Reply only with the answers, do not repeat the code and questions.'
         },

        {'role': 'user',
         'content': 'Python Function:'
                    '\nfrom typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    """ Check if in given list of numbers, are any two numbers closer to each other than\n    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    """\n    for idx, elem in enumerate(numbers):\n        for idx2, elem2 in enumerate(numbers):\n            if idx != idx2:\n                distance = abs(elem - elem2)\n                if distance < threshold:\n                    return True\n\n    return False'
                    '\nTest Cases:'
                    '\ndef check(candidate):\n    assert candidate([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) == True\n    assert candidate([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05) == False\n    assert candidate([1.0, 2.0, 5.9, 4.0, 5.0], 0.95) == True\n    assert candidate([1.0, 2.0, 5.9, 4.0, 5.0], 0.8) == False\n    assert candidate([1.0, 2.0, 3.0, 4.0, 5.0, 2.0], 0.1) == True\n    assert candidate([1.1, 2.2, 3.1, 4.1, 5.1], 1.0) == True\n    assert candidate([1.1, 2.2, 3.1, 4.1, 5.1], 0.5) == False'
                    '\n\nClarifying Questions:\n1. Is the requirement intended to check if there is any pair of numbers in the list whose absolute difference is less than a given threshold?'
                    '\n\nAnswers:\n{insert your answers here}'
         },
        {'role': 'assistant',
         'content': '1. Yes, the requirement aims to check if there is any pair of numbers in the list whose absolute difference is less than a given threshold.'
         },

        {'role': 'user',
         'content': 'Python Function:'
                    '\nfrom typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups(\'( ) (( )) (( )( ))\')\n    [\'()\', \'(())\', \'(()())\']\n    """\n    result = []\n    current_string = []\n    current_depth = 0\n\n    for c in paren_string:\n        if c == \'(\':\n            current_depth += 1\n            current_string.append(c)\n        elif c == \')\':\n            current_depth -= 1\n            current_string.append(c)\n\n            if current_depth == 0:\n                result.append(\'\'.join(current_string))\n                current_string.clear()\n\n    return result'
                    '\nTest Cases:'
                    '\ndef check(candidate):\n    assert candidate(\'(()()) ((())) () ((())()())\') == [\n        \'(()())\', \'((()))\', \'()\', \'((())()())\'\n    ]\n    assert candidate(\'() (()) ((())) (((())))\') == [\n        \'()\', \'(())\', \'((()))\', \'(((())))\'\n    ]\n    assert candidate(\'(()(())((())))\') == [\n        \'(()(())((())))\'\n    ]\n    assert candidate(\'( ) (( )) (( )( ))\') == [\'()\', \'(())\', \'(()())\']'
                    '\n\nClarifying Questions:\n1. Should the function remove spaces from the input string before processing it, or should it handle spaces within the groups of parentheses?'
                    '\n2. Should the final output in the result list include spaces?'
                    '\n\nAnswers:\n{insert your answers here}'
         },
        {'role': 'assistant',
         'content': '1. The requirement mentions that "Ignore any spaces in the input string", '
                    'so you can remove spaces from the input string directly or ignore spaces when processing the input string.'
                    '\n2. No, the final output in the result list should not include spaces.'
         },

        {'role': 'user',
         'content': 'Python Function:'
                    '\nfrom typing import List\n\n\ndef below_zero(operations: List[int]) -> bool:\n    """ You\'re given a list of deposit and withdrawal operations on a bank account that starts with\n    zero balance. Your task is to detect if at any point the balance of account fallls below zero, and\n    at that point function should return True. Otherwise it should return False.\n    >>> below_zero([1, 2, 3])\n    False\n    >>> below_zero([1, 2, -4, 5])\n    True\n    """\n    balance = 0\n\n    for op in operations:\n        balance += op\n        if balance < 0:\n            return True\n\n    return False'
                    '\nTest Cases:'
                    '\ndef check(candidate):\n    assert candidate([]) == False\n    assert candidate([1, 2, -3, 1, 2, -3]) == False\n    assert candidate([1, 2, -4, 5, 6]) == True\n    assert candidate([1, -1, 2, -2, 5, -5, 4, -4]) == False\n    assert candidate([1, -1, 2, -2, 5, -5, 4, -5]) == True\n    assert candidate([1, -2, 2, -2, 5, -5, 4, -4]) == True'
                    '\n\nClarifying Questions:'
                    '\n1. Should the function detect if the balance falls below zero at any point during the operations, or is it intended to detect if the balance falls below zero at the final point only?'
                    '\n2. If the balance drops to zero exactly, is that also considered "the balance falls below zero"?'
                    '\n\nAnswers:\n{insert your answers here}'
         },
        {'role': 'assistant',
         'content': '1. The function should detect if the balance falls below zero at any point.'
                    '\n2. No, the requirement specifically states that the function should detect when the balance becomes negative. Therefore, if the balance drops to exactly zero, it is not considered as "the balance falls below zero."'
         },
    ],

    'four_shot': [
        {'role': 'system',
         'content': 'You will receive a user requirement and some clarifying questions for the requirement. '
                    'Your task is to answer these clarifying questions '
                    'drawing on the information provided in the given requirement. '
                    'Reply only with the answers, do not repeat the requirement and questions.'
         },

        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    """ Check if in given list of numbers, are any two numbers closer to each other than\n    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    """'
                    '\n\nClarifying Questions:\n1. Is the requirement intended to check if there is any pair of numbers in the list whose absolute difference is less than a given threshold?'
                    '\n\nAnswers:\n{insert your answers here}'
         },
        {'role': 'assistant',
         'content': '1. Yes, the requirement aims to check if there is any pair of numbers in the list whose absolute difference is less than a given threshold.'
         },

        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups(\'( ) (( )) (( )( ))\')\n    [\'()\', \'(())\', \'(()())\']\n    """'
                    '\n\nClarifying Questions:\n1. Should the function remove spaces from the input string before processing it, or should it handle spaces within the groups of parentheses?'
                    '\n2. Should the final output in the result list include spaces?'
                    '\n\nAnswers:\n{insert your answers here}'
         },
        {'role': 'assistant',
         'content': '1. The requirement mentions that "Ignore any spaces in the input string", '
                    'so you can remove spaces from the input string directly or ignore spaces when processing the input string.'
                    '\n2. No, the final output in the result list should not include spaces.'
         },

        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef below_zero(operations: List[int]) -> bool:\n    """ You\'re given a list of deposit and withdrawal operations on a bank account that starts with\n    zero balance. Your task is to detect if at any point the balance of account fallls below zero, and\n    at that point function should return True. Otherwise it should return False.\n    >>> below_zero([1, 2, 3])\n    False\n    >>> below_zero([1, 2, -4, 5])\n    True\n    """'
                    '\n\nClarifying Questions:'
                    '\n1. Should the function detect if the balance falls below zero at any point during the operations, or is it intended to detect if the balance falls below zero at the final point only?'
                    '\n2. If the balance drops to zero exactly, is that also considered "the balance falls below zero"?'
                    '\n\nAnswers:\n{insert your answers here}'
         },
        {'role': 'assistant',
         'content': '1. The function should detect if the balance falls below zero at any point.'
                    '\n2. No, the requirement specifically states that the function should detect when the balance becomes negative. Therefore, if the balance drops to exactly zero, it is not considered as "the balance falls below zero."'
         },

        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef mean_absolute_deviation(numbers: List[float]) -> float:\n    """ For a given list of input numbers, calculate Mean Absolute Deviation\n    around the mean of this dataset.\n    Mean Absolute Deviation is the average absolute difference between each\n    element and a centerpoint (mean in this case):\n    MAD = average | x - x_mean |\n    >>> mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])\n    1.0\n    """'
                    '\n\nClarifying Questions:'
                    '\n1. Is the centerpoint referred to in the requirement the same as the mean of the input numbers?'
                    '\n2. Should the function calculate the absolute differences between each element and the mean? Or just the differences between each element and the mean?'
                    '\n3. Should the function return the average of the absolute differences or the sum of the absolute differences?'
                    '\n\nAnswers:\n{insert your answers here}'
         },
        {'role': 'assistant',
         'content': '1. Yes, the requirement specifically states that the centerpoint is the mean of the input numbers.'
                    '\n2. The function should calculate the absolute differences between each element and the mean, not just the differences.'
                    '\n3. The requirement mentions that "Mean Absolute Deviation is the average absolute difference", so the function should return the average of the absolute differences.'
         },
    ],
}


synthesize_prompt = {
    'zero_shot': [
        {'role': 'system',
         'content': 'You will be given a user requirement and its clarification. '
                    'The clarification aims to enhance the clarity of the requirement and should be duly noted. '
                    'Respond only with a correct, efficient Python function that meets the requirement. '
                    'Do not write explanations or assertions; simply provide only the code.'
         }],

    'one_shot': [
        {'role': 'system',
         'content': 'You will be given a user requirement and its clarification. '
                    'The clarification aims to enhance the clarity of the requirement and should be duly noted. '
                    'Respond only with a correct, efficient Python function that meets the requirement. '
                    'Do not write explanations or assertions; simply provide only the code.'
         },
        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups(\'( ) (( )) (( )( ))\')\n    [\'()\', \'(())\', \'(()())\']\n    """'
                    '\nClarification:\n1. Should the function remove spaces from the input string before processing it, or should it handle spaces within the groups of parentheses?'
                    '\n- The requirement mentions that "Ignore any spaces in the input string", so you can remove spaces from the input string directly or ignore spaces when processing the input string.'
                    '\n2. Should the final output in the result list include spaces?'
                    '\n- No, the final output in the result list should not include spaces.'
         },
        {'role': 'assistant',
         'content': "def separate_paren_groups(paren_string: str) -> List[str]:\n    result = []\n    current_string = []\n    current_depth = 0\n\n    for c in paren_string:\n        if c == '(':\n            current_depth += 1\n            current_string.append(c)\n        elif c == ')':\n            current_depth -= 1\n            current_string.append(c)\n\n            if current_depth == 0:\n                result.append(''.join(current_string))\n                current_string.clear()\n\n    return result"
         },
    ],

    'two_shot': [
        {'role': 'system',
         'content': 'You will be given a user requirement and its clarification. '
                    'The clarification aims to enhance the clarity of the requirement and should be duly noted. '
                    'Respond only with a correct, efficient Python function that meets the requirement. '
                    'Do not write explanations or assertions; simply provide only the code.'
         },
        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    """ Check if in given list of numbers, are any two numbers closer to each other than\n    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    """'
                    '\nClarification:\n1. Is the requirement intended to check if there is any pair of numbers in the list whose absolute difference is less than a given threshold?'
                    '\n- Yes, the requirement aims to check if there is any pair of numbers in the list whose absolute difference is less than a given threshold.'
         },
        {'role': 'assistant',
         'content': 'def has_close_elements(numbers: List[float], threshold: float) -> bool:\n    for idx, elem in enumerate(numbers):\n        for idx2, elem2 in enumerate(numbers):\n            if idx != idx2:\n                distance = abs(elem - elem2)\n                if distance < threshold:\n                    return True\n\n    return False'
         },

        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups(\'( ) (( )) (( )( ))\')\n    [\'()\', \'(())\', \'(()())\']\n    """'
                    '\nClarification:\n1. Should the function remove spaces from the input string before processing it, or should it handle spaces within the groups of parentheses?'
                    '\n- The requirement mentions that "Ignore any spaces in the input string", so you can remove spaces from the input string directly or ignore spaces when processing the input string.'
                    '\n2. Should the final output in the result list include spaces?'
                    '\n- No, the final output in the result list should not include spaces.'
         },
        {'role': 'assistant',
         'content': "def separate_paren_groups(paren_string: str) -> List[str]:\n    result = []\n    current_string = []\n    current_depth = 0\n\n    for c in paren_string:\n        if c == '(':\n            current_depth += 1\n            current_string.append(c)\n        elif c == ')':\n            current_depth -= 1\n            current_string.append(c)\n\n            if current_depth == 0:\n                result.append(''.join(current_string))\n                current_string.clear()\n\n    return result"
         },
    ],

    'three_shot': [
        {'role': 'system',
         'content': 'You will be given a user requirement and its clarification. '
                    'The clarification aims to enhance the clarity of the requirement and should be duly noted. '
                    'Respond only with a correct, efficient Python function that meets the requirement. '
                    'Do not write explanations or assertions; simply provide only the code.'
         },

        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    """ Check if in given list of numbers, are any two numbers closer to each other than\n    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    """'
                    '\nClarification:\n1. Is the requirement intended to check if there is any pair of numbers in the list whose absolute difference is less than a given threshold?'
                    '\n- Yes, the requirement aims to check if there is any pair of numbers in the list whose absolute difference is less than a given threshold.'
         },
        {'role': 'assistant',
         'content': 'def has_close_elements(numbers: List[float], threshold: float) -> bool:\n    for idx, elem in enumerate(numbers):\n        for idx2, elem2 in enumerate(numbers):\n            if idx != idx2:\n                distance = abs(elem - elem2)\n                if distance < threshold:\n                    return True\n\n    return False'
         },

        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups(\'( ) (( )) (( )( ))\')\n    [\'()\', \'(())\', \'(()())\']\n    """'
                    '\nClarification:'
                    '\n1. What does it mean for groups to be "not nested within each other"? Are we allowed to have groups that are partially overlapping, or should they be completely separate?'
                    '\n- It means that a group of parentheses should not be completely enclosed within another group of parentheses. Each group should be a distinct and separate entity.'
                    '\n2. Should the function remove spaces from the input string before processing it, or should it handle spaces within the groups of parentheses?'
                    '\n- The requirement mentions that "Ignore any spaces in the input string", so you can remove spaces from the input string directly or ignore spaces when processing the input string.'
                    '\n3. Should the final output in the result list include spaces?'
                    '\n- No, the final output in the result list should not include spaces.'
         },
        {'role': 'assistant',
         'content': "def separate_paren_groups(paren_string: str) -> List[str]:\n    result = []\n    current_string = []\n    current_depth = 0\n\n    for c in paren_string:\n        if c == '(':\n            current_depth += 1\n            current_string.append(c)\n        elif c == ')':\n            current_depth -= 1\n            current_string.append(c)\n\n            if current_depth == 0:\n                result.append(''.join(current_string))\n                current_string.clear()\n\n    return result"
         },

        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef below_zero(operations: List[int]) -> bool:\n    """ You\'re given a list of deposit and withdrawal operations on a bank account that starts with\n    zero balance. Your task is to detect if at any point the balance of account fallls below zero, and\n    at that point function should return True. Otherwise it should return False.\n    >>> below_zero([1, 2, 3])\n    False\n    >>> below_zero([1, 2, -4, 5])\n    True\n    """'
                    '\nClarification:'
                    '\n1. Should the function detect if the balance falls below zero at any point during the operations, or is it intended to detect if the balance falls below zero at the final point only?'
                    '\n- The function should detect if the balance falls below zero at any point.'
                    '\n2. If the balance drops to zero exactly, is that also considered "the balance falls below zero"?'
                    '\n- No, the requirement specifically states that the function should detect when the balance becomes negative. Therefore, if the balance drops to exactly zero, it is not considered as "the balance falls below zero."'
         },
        {'role': 'assistant',
         'content': 'def below_zero(operations: List[int]) -> bool:\n    balance = 0\n    for op in operations:\n        balance += op\n        if balance < 0:\n            return True\n\n    return False'
         },
    ],

    'four_shot': [
        {'role': 'system',
         'content': 'You will be given a user requirement and its clarification. '
                    'The clarification aims to enhance the clarity of the requirement and should be duly noted. '
                    'Respond only with a correct, efficient Python function that meets the requirement. '
                    'Do not write explanations or assertions; simply provide only the code.'
         },

        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    """ Check if in given list of numbers, are any two numbers closer to each other than\n    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    """'
                    '\nClarification:\n1. Is the requirement intended to check if there is any pair of numbers in the list whose absolute difference is less than a given threshold?'
                    '\n- Yes, the requirement aims to check if there is any pair of numbers in the list whose absolute difference is less than a given threshold.'
         },
        {'role': 'assistant',
         'content': 'def has_close_elements(numbers: List[float], threshold: float) -> bool:\n    for idx, elem in enumerate(numbers):\n        for idx2, elem2 in enumerate(numbers):\n            if idx != idx2:\n                distance = abs(elem - elem2)\n                if distance < threshold:\n                    return True\n\n    return False'
         },

        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups(\'( ) (( )) (( )( ))\')\n    [\'()\', \'(())\', \'(()())\']\n    """'
                    '\nClarification:\n1. Should the function remove spaces from the input string before processing it, or should it handle spaces within the groups of parentheses?'
                    '\n- The requirement mentions that "Ignore any spaces in the input string", so you can remove spaces from the input string directly or ignore spaces when processing the input string.'
                    '\n2. Should the final output in the result list include spaces?'
                    '\n- No, the final output in the result list should not include spaces.'
         },
        {'role': 'assistant',
         'content': "def separate_paren_groups(paren_string: str) -> List[str]:\n    result = []\n    current_string = []\n    current_depth = 0\n\n    for c in paren_string:\n        if c == '(':\n            current_depth += 1\n            current_string.append(c)\n        elif c == ')':\n            current_depth -= 1\n            current_string.append(c)\n\n            if current_depth == 0:\n                result.append(''.join(current_string))\n                current_string.clear()\n\n    return result"
         },

        {'role': 'user',
         'content': 'User Requirement:\nfrom typing import List\n\n\ndef below_zero(operations: List[int]) -> bool:\n    """ You\'re given a list of deposit and withdrawal operations on a bank account that starts with\n    zero balance. Your task is to detect if at any point the balance of account fallls below zero, and\n    at that point function should return True. Otherwise it should return False.\n    >>> below_zero([1, 2, 3])\n    False\n    >>> below_zero([1, 2, -4, 5])\n    True\n    """'
                    '\nClarification:'
                    '\n1. Should the function detect if the balance falls below zero at any point during the operations, or is it intended to detect if the balance falls below zero at the final point only?'
                    '\n- The function should detect if the balance falls below zero at any point.'
                    '\n2. If the balance drops to zero exactly, is that also considered "the balance falls below zero"?'
                    '\n- No, the requirement specifically states that the function should detect when the balance becomes negative. Therefore, if the balance drops to exactly zero, it is not considered as "the balance falls below zero."'
         },
        {'role': 'assistant',
         'content': 'def below_zero(operations: List[int]) -> bool:\n    balance = 0\n    for op in operations:\n        balance += op\n        if balance < 0:\n            return True\n\n    return False'
         },

        {'role': 'user',
         'content': 'User Requirement:\nUser Requirement:\nfrom typing import List\n\n\ndef mean_absolute_deviation(numbers: List[float]) -> float:\n    """ For a given list of input numbers, calculate Mean Absolute Deviation\n    around the mean of this dataset.\n    Mean Absolute Deviation is the average absolute difference between each\n    element and a centerpoint (mean in this case):\n    MAD = average | x - x_mean |\n    >>> mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])\n    1.0\n    """'
                    '\nClarification:'
                    '\n1. Is the centerpoint referred to in the requirement the same as the mean of the input numbers?'
                    '\n- Yes, the requirement specifically states that the centerpoint is the mean of the input numbers.'
                    '\n2. Should the function calculate the absolute differences between each element and the mean? Or just the differences between each element and the mean?'
                    '\n- The function should calculate the absolute differences between each element and the mean, not just the differences.'
                    '\n3. Should the function return the average of the absolute differences or the sum of the absolute differences?'
                    '\n- The requirement mentions that "Mean Absolute Deviation is the average absolute difference", so the function should return the average of the absolute differences.'
         },
        {'role': 'assistant',
         'content': 'def mean_absolute_deviation(numbers: List[float]) -> float:\n    mean = sum(numbers) / len(numbers)\n    return sum(abs(x - mean) for x in numbers) / len(numbers)'
         },
    ],
}