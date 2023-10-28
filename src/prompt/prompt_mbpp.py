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
         'content': "User Requirement:"
                    "\nimport collections as ct\ndef merge_dictionaries_three(dict1,dict2, dict3):\n    '''\n    Write a function to merge three dictionaries into a single dictionary.\n    '''"
                    "\nSolution 0:\ndef merge_dictionaries_three(dict1,dict2, dict3):\n    merged_dict = ct.ChainMap(dict1, dict2, dict3)\n    return dict(merged_dict)"
                    "\nSolution 1:\ndef merge_dictionaries_three(dict1,dict2, dict3):\n    return ct.ChainMap(dict1, dict2, dict3)"
                    "\nSolution 2:\ndef merge_dictionaries_three(dict1, dict2, dict3):\n    return {**dict1, **dict2, **dict3}"
         },
        {'role': 'assistant',
         'content': '### Analysis:'
                    '\nThe requirement is to merge three dictionaries into a single dictionary.'
                    '\n\nSolution 0:\n- Solution 0 uses the `ChainMap` class from the `collections` module to merge the dictionaries.\n- It creates a `ChainMap` object with the three input dictionaries and then converts it to a regular dictionary using the `dict()` function.'
                    '\n\nSolution 1:\n- Solution 1 also uses the `ChainMap` class from the `collections` module to merge the dictionaries.\n- It directly returns the `ChainMap` object without converting it to a regular dictionary.'
                    '\n\nSolution 2:\n- Solution 2 merges the dictionaries using the dictionary unpacking operator (`**`).\n- It creates a new dictionary by unpacking the three input dictionaries.'
                    '\n\n### Clarifying Questions:'
                    '\n1. What should be the type of the output? `ChainMap` object or a regular dictionary?'
                    '\n2. Should the merged dictionary contain all key-value pairs from all three input dictionaries, and what should happen if there are overlapping keys?'
                    '\n3. Can you provide an input-output example to help us better understand your requirement?'
         },
    ],

    'two_shot': [
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
         'content': "User Requirement:"
                    "\ndef lateralsuface_cylinder(r,h):\n    '''\n    Write a function to find the lateral surface area of a cylinder.\n    '''"
                    "\nSolution 0:\ndef lateralsuface_cylinder(r,h):\n    return 2 * 3.1415 * r * h"
                    "\nSolution 1:\nimport math\ndef lateralsuface_cylinder(r,h):\n    return 2 * math.pi * r * h"
         },
        {'role': 'assistant',
         'content': '### Analysis:'
                    '\nThe requirement is to write a function to find the lateral surface area of a cylinder.'
                    '\n\nSolution 0:\n- Solution 0 calculates the lateral surface area of a cylinder using an approximation of the value of π (approximately 3.1415).\n- It calculates the lateral surface area of a cylinder using the formula: 2 * 3.1415 * r * h.'
                    '\n\nSolution 1:\n- Solution 1 imports the math module and uses the precise value of π from the math module to calculate the lateral surface area of the cylinder.\n- It calculates the lateral surface area of a cylinder using the formula: 2 * π * r * h.'
                    '\n\n### Clarifying Questions:'
                    '\n1. What do the input parameters `r` and `h` mean respectively?'
                    '\n2. Is it acceptable to use an approximation for the value of π, or should the exact value be used?'
         },
        {'role': 'user',
         'content': "User Requirement:"
                    "\nimport collections as ct\ndef merge_dictionaries_three(dict1,dict2, dict3):\n    '''\n    Write a function to merge three dictionaries into a single dictionary.\n    '''"
                    "\nSolution 0:\ndef merge_dictionaries_three(dict1,dict2, dict3):\n    merged_dict = ct.ChainMap(dict1, dict2, dict3)\n    return dict(merged_dict)"
                    "\nSolution 1:\ndef merge_dictionaries_three(dict1,dict2, dict3):\n    return ct.ChainMap(dict1, dict2, dict3)"
                    "\nSolution 2:\ndef merge_dictionaries_three(dict1, dict2, dict3):\n    return {**dict1, **dict2, **dict3}"
         },
        {'role': 'assistant',
         'content': '### Analysis:'
                    '\nThe requirement is to merge three dictionaries into a single dictionary.'
                    '\n\nSolution 0:\n- Solution 0 uses the `ChainMap` class from the `collections` module to merge the dictionaries.\n- It creates a `ChainMap` object with the three input dictionaries and then converts it to a regular dictionary using the `dict()` function.'
                    '\n\nSolution 1:\n- Solution 1 also uses the `ChainMap` class from the `collections` module to merge the dictionaries.\n- It directly returns the `ChainMap` object without converting it to a regular dictionary.'
                    '\n\nSolution 2:\n- Solution 2 merges the dictionaries using the dictionary unpacking operator (`**`).\n- It creates a new dictionary by unpacking the three input dictionaries.'
                    '\n\n### Clarifying Questions:'
                    '\n1. What should be the type of the output? `ChainMap` object or a regular dictionary?'
                    '\n2. Should the merged dictionary contain all key-value pairs from all three input dictionaries, and what should happen if there are overlapping keys?'
                    '\n3. Can you provide an input-output example to help us better understand your requirement?'
         },
    ],

    'three_shot': [
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
         'content': "User Requirement:"
                    "\ndef lateralsuface_cylinder(r,h):\n    '''\n    Write a function to find the lateral surface area of a cylinder.\n    '''"
                    "\nSolution 0:\ndef lateralsuface_cylinder(r,h):\n    return 2 * 3.1415 * r * h"
                    "\nSolution 1:\nimport math\ndef lateralsuface_cylinder(r,h):\n    return 2 * math.pi * r * h"
         },
        {'role': 'assistant',
         'content': '### Analysis:'
                    '\nThe requirement is to write a function to find the lateral surface area of a cylinder.'
                    '\n\nSolution 0:\n- Solution 0 calculates the lateral surface area of a cylinder using an approximation of the value of π (approximately 3.1415).\n- It calculates the lateral surface area of a cylinder using the formula: 2 * 3.1415 * r * h.'
                    '\n\nSolution 1:\n- Solution 1 imports the math module and uses the precise value of π from the math module to calculate the lateral surface area of the cylinder.\n- It calculates the lateral surface area of a cylinder using the formula: 2 * π * r * h.'
                    '\n\n### Clarifying Questions:'
                    '\n1. What do the input parameters `r` and `h` mean respectively?'
                    '\n2. Is it acceptable to use an approximation for the value of π, or should the exact value be used?'
         },
        {'role': 'user',
         'content': "User Requirement:"
                    "\ndef max_val(listval):\n    '''\n    Write a function to find the maximum value in a given heterogeneous list.\n    '''"
                    "\nSolution 0:\ndef max_val(listval):\n    return max(listval)"
                    "\nSolution 1:\ndef max_val(listval):\n    return max(listval)"
         },
        {'role': 'assistant',
         'content': '### Analysis:'
                    '\nThe requirement is to write a function to find the maximum value in a given heterogeneous list.'
                    '\n\nSolution 0:\n- Solution 0 uses the built-in `max()` function to find the maximum value in the given list.\n- It directly returns the result of the `max()` function.'
                    '\n\nSolution 1:\n- Solution 1 also uses the built-in `max()` function to find the maximum value in the given list.\n- It also directly returns the result of the `max()` function.'
                    '\n\n### Clarifying Questions:'
                    '\n1. What do you mean by a "heterogeneous list"? Does it mean that the list can contain elements of different types (e.g., integers, strings, etc.)?'
                    '\n2. If the list can contain different types of elements, does the function only need to focus on the int elements and return the maximum interger in these int elements?'
                    '\n3. Can you provide an example of a heterogeneous list and its expected maximum value?'
         },
        {'role': 'user',
         'content': "User Requirement:"
                    "\nimport collections as ct\ndef merge_dictionaries_three(dict1,dict2, dict3):\n    '''\n    Write a function to merge three dictionaries into a single dictionary.\n    '''"
                    "\nSolution 0:\ndef merge_dictionaries_three(dict1,dict2, dict3):\n    merged_dict = ct.ChainMap(dict1, dict2, dict3)\n    return dict(merged_dict)"
                    "\nSolution 1:\ndef merge_dictionaries_three(dict1,dict2, dict3):\n    return ct.ChainMap(dict1, dict2, dict3)"
                    "\nSolution 2:\ndef merge_dictionaries_three(dict1, dict2, dict3):\n    return {**dict1, **dict2, **dict3}"
         },
        {'role': 'assistant',
         'content': '### Analysis:'
                    '\nThe requirement is to merge three dictionaries into a single dictionary.'
                    '\n\nSolution 0:\n- Solution 0 uses the `ChainMap` class from the `collections` module to merge the dictionaries.\n- It creates a `ChainMap` object with the three input dictionaries and then converts it to a regular dictionary using the `dict()` function.'
                    '\n\nSolution 1:\n- Solution 1 also uses the `ChainMap` class from the `collections` module to merge the dictionaries.\n- It directly returns the `ChainMap` object without converting it to a regular dictionary.'
                    '\n\nSolution 2:\n- Solution 2 merges the dictionaries using the dictionary unpacking operator (`**`).\n- It creates a new dictionary by unpacking the three input dictionaries.'
                    '\n\n### Clarifying Questions:'
                    '\n1. What should be the type of the output? `ChainMap` object or a regular dictionary?'
                    '\n2. Should the merged dictionary contain all key-value pairs from all three input dictionaries, and what should happen if there are overlapping keys?'
                    '\n3. Can you provide an input-output example to help us better understand your requirement?'
         },
    ],
}

answercq_prompt = {
    'zero_shot': [
        {'role': 'system',
         'content': 'You will receive a user requirement and its clarifying questions. '
                    'Your task is to answer these clarifying questions using the information provided in the given requirement. '
                    'In cases where the requirement does not contain specific information required to answer certain questions, '
                    'you should provide reasonable answers based your own understanding or knowledge. '
                    'Reply only with the answers, do not repeat the requirement and questions.'
         }],

    'one_shot': [
        {'role': 'system',
         'content': 'You will receive a user requirement and its clarifying questions. '
                    'Your task is to answer these clarifying questions using the information provided in the given requirement. '
                    'In cases where the requirement does not contain specific information required to answer certain questions, '
                    'you should provide reasonable answers based your own understanding or knowledge. '
                    'Reply only with the answers, do not repeat the requirement and questions.'
         },
        {'role': 'user',
         'content': "User Requirement:"
                    "\nimport collections as ct\ndef merge_dictionaries_three(dict1,dict2, dict3):\n    '''\n    Write a function to merge three dictionaries into a single dictionary.\n    '''"
                    "\n\n### Clarifying Questions:"
                    "\n1. What should be the type of the output? `ChainMap` object or a regular dictionary?"
                    "\n2. Should the merged dictionary contain all key-value pairs from all three input dictionaries, and what should happen if there are overlapping keys?"
                    "\n3. Can you provide an input-output example to help us better understand your requirement?"
                    "\n\n### Answers:\n{insert answers here}"
         },
        {'role': 'assistant',
         'content': "### Answers:"
                    "\n1. The merged dictionaries should be a regular dictionary."
                    "\n2. Yes, the merged dictionary should contain all key-value pairs from all three input dictionaries, and when there are overlapping keys, the value from the first dictionary in the input sequence should take precedence."
                    "\n3. Yes, here is an input-output example: assert merge_dictionaries_three({\"R\": \"Red\", \"B\": \"Black\", \"P\": \"Pink\" }, {\"L\": \"lavender\", \"B\": \"Blue\"}, {\"G\": \"Green\", \"W\": \"White\"}) == {'B': 'Black', 'P': 'Pink', 'R': 'Red', 'G': 'Green', 'L': 'lavender', 'W': 'White'}"
         },
    ],

    'one_shot_w_test': [
            {'role': 'system',
             'content': 'You will receive a Python function and its test cases. '
                        'Your task is to answer some clarifying questions using the information provided in the given function and tests. '
                        'Reply only with the answers, do not repeat the code and questions.'
             },
            {'role': 'user',
             'content': "Python Function:"
                        "\n'''\nWrite a function to merge three dictionaries into a single dictionary.\n'''"
                        "\nimport collections as ct\ndef merge_dictionaries_three(dict1,dict2, dict3):\n    merged_dict = ct.ChainMap(dict1, dict2, dict3)\n    return dict(merged_dict)"
                        "\nTest Cases:"
                        "\nassert merge_dictionaries_three({ \"R\": \"Red\", \"B\": \"Black\", \"P\": \"Pink\" }, { \"G\": \"Green\", \"W\": \"White\" },{ \"O\": \"Orange\", \"W\": \"White\", \"B\": \"Black\" })=={'B': 'Black', 'R': 'Red', 'P': 'Pink', 'G': 'Green', 'W': 'White', 'O': 'Orange'}"
                        "\nassert merge_dictionaries_three({ \"R\": \"Red\", \"B\": \"Black\", \"P\": \"Pink\" }, { \"G\": \"Green\", \"W\": \"White\" },{\"L\":\"lavender\",\"B\":\"Blue\"})=={'W': 'White', 'P': 'Pink', 'B': 'Black', 'R': 'Red', 'G': 'Green', 'L': 'lavender'}"
                        "\nassert merge_dictionaries_three({ \"R\": \"Red\", \"B\": \"Black\", \"P\": \"Pink\" },{\"L\":\"lavender\",\"B\":\"Blue\"},{ \"G\": \"Green\", \"W\": \"White\" })=={'B': 'Black', 'P': 'Pink', 'R': 'Red', 'G': 'Green', 'L': 'lavender', 'W': 'White'}"
                        "\n\n### Clarifying Questions:"
                        "\n1. What should be the type of the output? `ChainMap` object or a regular dictionary?"
                        "\n2. Should the merged dictionary contain all key-value pairs from all three input dictionaries, and what should happen if there are overlapping keys?"
                        "\n3. Can you provide an input-output example to help us better understand your requirement?"
                        "\n\n### Answers:\n{insert answers here}"
             },
            {'role': 'assistant',
             'content': "### Answers:"
                        "\n1. The merged dictionaries should be a regular dictionary."
                        "\n2. Yes, the merged dictionary should contain all key-value pairs from all three input dictionaries, and when there are overlapping keys, the value from the first dictionary in the input sequence should take precedence."
                        "\n3. Yes, here is an input-output example: assert merge_dictionaries_three({\"R\": \"Red\", \"B\": \"Black\", \"P\": \"Pink\" }, {\"L\": \"lavender\", \"B\": \"Blue\"}, {\"G\": \"Green\", \"W\": \"White\"}) == {'B': 'Black', 'P': 'Pink', 'R': 'Red', 'G': 'Green', 'L': 'lavender', 'W': 'White'}"
             },
        ],

    'two_shot': [
        {'role': 'system',
         'content': 'You will receive a user requirement and its clarifying questions. '
                    'Your task is to answer these clarifying questions using the information provided in the given requirement. '
                    'In cases where the requirement does not contain specific information required to answer certain questions, '
                    'you should provide reasonable answers based your own understanding or knowledge. '
                    'Reply only with the answers, do not repeat the requirement and questions.'
         },
        {'role': 'user',
         'content': "User Requirement:"
                    "\ndef lateralsuface_cylinder(r,h):\n    '''\n    Write a function to find the lateral surface area of a cylinder.\n    '''"
                    "\n\n### Clarifying Questions:"
                    "\n1. What do the input parameters `r` and `h` mean respectively?"
                    "\n2. Is it acceptable to use an approximation for the value of π, or should the exact value be used?"
                    "\n\n### Answers:\n{insert answers here}"
         },
        {'role': 'assistant',
         'content': '### Answers:'
                    '\n1. The input parameter `r` represents the radius of the cylinder, `h` represents the height of the cylinder.'
                    '\n2. Of course, it is acceptable to use an approximation for the value of π, like 3.1415.'
         },
        {'role': 'user',
         'content': "User Requirement:"
                    "\nimport collections as ct\ndef merge_dictionaries_three(dict1,dict2, dict3):\n    '''\n    Write a function to merge three dictionaries into a single dictionary.\n    '''"
                    "\n\n### Clarifying Questions:"
                    "\n1. What should be the type of the output? `ChainMap` object or a regular dictionary?"
                    "\n2. Should the merged dictionary contain all key-value pairs from all three input dictionaries, and what should happen if there are overlapping keys?"
                    "\n3. Can you provide an input-output example to help us better understand your requirement?"
                    "\n\n### Answers:\n{insert answers here}"
         },
        {'role': 'assistant',
         'content': "### Answers:"
                    "\n1. The merged dictionaries should be a regular dictionary."
                    "\n2. Yes, the merged dictionary should contain all key-value pairs from all three input dictionaries, and when there are overlapping keys, the value from the first dictionary in the input sequence should take precedence."
                    "\n3. Yes, here is an input-output example: assert merge_dictionaries_three({\"R\": \"Red\", \"B\": \"Black\", \"P\": \"Pink\" }, {\"L\": \"lavender\", \"B\": \"Blue\"}, {\"G\": \"Green\", \"W\": \"White\"}) == {'B': 'Black', 'P': 'Pink', 'R': 'Red', 'G': 'Green', 'L': 'lavender', 'W': 'White'}"
         },
    ],

    'two_shot_w_test': [
            {'role': 'system',
             'content': 'You will receive a Python function and its test cases. '
                        'Your task is to answer some clarifying questions using the information provided in the given function and tests. '
                        'Reply only with the answers, do not repeat the code and questions.'
             },
            {'role': 'user',
             'content': "Python Function:"
                        "\n'''\nWrite a function to find the lateral surface area of a cylinder.\n'''"
                        "\ndef lateralsuface_cylinder(r,h):\n    return 2 * 3.1415 * r * h"
                        "\nTest Cases:"
                        "\nassert math.isclose(lateralsuface_cylinder(10,5), 314.15000000000003, rel_tol=0.001)"
                        "\nassert math.isclose(lateralsuface_cylinder(4,5), 125.66000000000001, rel_tol=0.001)"
                        "\nassert math.isclose(lateralsuface_cylinder(4,10), 251.32000000000002, rel_tol=0.001)"
                        "\n\n### Clarifying Questions:"
                        "\n1. What do the input parameters `r` and `h` mean respectively?"
                        "\n2. Is it acceptable to use an approximation for the value of π, or should the exact value be used?"
                        "\n\n### Answers:\n{insert answers here}"
             },
            {'role': 'assistant',
             'content': '### Answers:'
                        '\n1. The input parameter `r` represents the radius of the cylinder, `h` represents the height of the cylinder.'
                        '\n2. Of course, it is acceptable to use an approximation for the value of π, like 3.1415.'
             },
            {'role': 'user',
             'content': "Python Function:"
                        "\n'''\nWrite a function to merge three dictionaries into a single dictionary.\n'''"
                        "\nimport collections as ct\ndef merge_dictionaries_three(dict1,dict2, dict3):\n    merged_dict = ct.ChainMap(dict1, dict2, dict3)\n    return dict(merged_dict)"
                        "\nTest Cases:"
                        "\nassert merge_dictionaries_three({ \"R\": \"Red\", \"B\": \"Black\", \"P\": \"Pink\" }, { \"G\": \"Green\", \"W\": \"White\" },{ \"O\": \"Orange\", \"W\": \"White\", \"B\": \"Black\" })=={'B': 'Black', 'R': 'Red', 'P': 'Pink', 'G': 'Green', 'W': 'White', 'O': 'Orange'}"
                        "\nassert merge_dictionaries_three({ \"R\": \"Red\", \"B\": \"Black\", \"P\": \"Pink\" }, { \"G\": \"Green\", \"W\": \"White\" },{\"L\":\"lavender\",\"B\":\"Blue\"})=={'W': 'White', 'P': 'Pink', 'B': 'Black', 'R': 'Red', 'G': 'Green', 'L': 'lavender'}"
                        "\nassert merge_dictionaries_three({ \"R\": \"Red\", \"B\": \"Black\", \"P\": \"Pink\" },{\"L\":\"lavender\",\"B\":\"Blue\"},{ \"G\": \"Green\", \"W\": \"White\" })=={'B': 'Black', 'P': 'Pink', 'R': 'Red', 'G': 'Green', 'L': 'lavender', 'W': 'White'}"
                        "\n\n### Clarifying Questions:"
                        "\n1. What should be the type of the output? `ChainMap` object or a regular dictionary?"
                        "\n2. Should the merged dictionary contain all key-value pairs from all three input dictionaries, and what should happen if there are overlapping keys?"
                        "\n3. Can you provide an input-output example to help us better understand your requirement?"
                        "\n\n### Answers:\n{insert answers here}"
             },
            {'role': 'assistant',
             'content': "### Answers:"
                        "\n1. The merged dictionaries should be a regular dictionary."
                        "\n2. Yes, the merged dictionary should contain all key-value pairs from all three input dictionaries, and when there are overlapping keys, the value from the first dictionary in the input sequence should take precedence."
                        "\n3. Yes, here is an input-output example: assert merge_dictionaries_three({\"R\": \"Red\", \"B\": \"Black\", \"P\": \"Pink\" }, {\"L\": \"lavender\", \"B\": \"Blue\"}, {\"G\": \"Green\", \"W\": \"White\"}) == {'B': 'Black', 'P': 'Pink', 'R': 'Red', 'G': 'Green', 'L': 'lavender', 'W': 'White'}"
             },
        ],

    'three_shot': [
        {'role': 'system',
         'content': 'You will receive a user requirement and its clarifying questions. '
                    'Your task is to answer these clarifying questions using the information provided in the given requirement. '
                    'In cases where the requirement does not contain specific information required to answer certain questions, '
                    'you should provide reasonable answers based your own understanding or knowledge. '
                    'Reply only with the answers, do not repeat the requirement and questions.'
         },
        {'role': 'user',
         'content': "User Requirement:"
                    "\ndef lateralsuface_cylinder(r,h):\n    '''\n    Write a function to find the lateral surface area of a cylinder.\n    '''"
                    "\n\n### Clarifying Questions:"
                    "\n1. What do the input parameters `r` and `h` mean respectively?"
                    "\n2. Is it acceptable to use an approximation for the value of π, or should the exact value be used?"
                    "\n\n### Answers:\n{insert answers here}"
         },
        {'role': 'assistant',
         'content': '### Answers:'
                    '\n1. The input parameter `r` represents the radius of the cylinder, `h` represents the height of the cylinder.'
                    '\n2. Of course, it is acceptable to use an approximation for the value of π, like 3.1415.'
         },
        {'role': 'user',
         'content': "User Requirement:"
                    "\ndef max_val(listval):\n    '''\n    Write a function to find the maximum value in a given heterogeneous list.\n    '''"
                    "\n\n### Clarifying Questions:"
                    "\n1. What do you mean by a \"heterogeneous list\"? Does it mean that the list can contain elements of different types (e.g., integers, strings, etc.)?"
                    "\n2. If the list can contain different types of elements, does the function only need to focus on the int elements and return the maximum interger in these int elements?"
                    "\n3. Can you provide an example of a heterogeneous list and its expected maximum value?"
                    "\n\n### Answers:\n{insert answers here}"
         },
        {'role': 'assistant',
         'content': "### Answers:"
                    "\n1. A \"heterogeneous list\" means that the list can contain elements of different types, such as integers, strings, etc."
                    "\n2. Yes, the function should focus on the int elements and return the maximum interger in these int elements."
                    "\n3. Yes, here is an example: Input:['Python', 30, 20, 40, 50, 'version'], Output:50."
         },
        {'role': 'user',
         'content': "User Requirement:"
                    "\nimport collections as ct\ndef merge_dictionaries_three(dict1,dict2, dict3):\n    '''\n    Write a function to merge three dictionaries into a single dictionary.\n    '''"
                    "\n\n### Clarifying Questions:"
                    "\n1. What should be the type of the output? `ChainMap` object or a regular dictionary?"
                    "\n2. Should the merged dictionary contain all key-value pairs from all three input dictionaries, and what should happen if there are overlapping keys?"
                    "\n3. Can you provide an input-output example to help us better understand your requirement?"
                    "\n\n### Answers:\n{insert answers here}"
         },
        {'role': 'assistant',
         'content': "### Answers:"
                    "\n1. The merged dictionaries should be a regular dictionary."
                    "\n2. Yes, the merged dictionary should contain all key-value pairs from all three input dictionaries, and when there are overlapping keys, the value from the first dictionary in the input sequence should take precedence."
                    "\n3. Yes, here is an input-output example: assert merge_dictionaries_three({\"R\": \"Red\", \"B\": \"Black\", \"P\": \"Pink\" }, {\"L\": \"lavender\", \"B\": \"Blue\"}, {\"G\": \"Green\", \"W\": \"White\"}) == {'B': 'Black', 'P': 'Pink', 'R': 'Red', 'G': 'Green', 'L': 'lavender', 'W': 'White'}"
         },
    ],

    'three_shot_w_test': [
            {'role': 'system',
             'content': 'You will receive a Python function and its test cases. '
                        'Your task is to answer some clarifying questions using the information provided in the given function and tests. '
                        'Reply only with the answers, do not repeat the code and questions.'
             },
            {'role': 'user',
             'content': "Python Function:"
                        "\n'''\nWrite a function to find the lateral surface area of a cylinder.\n'''"
                        "\ndef lateralsuface_cylinder(r,h):\n    return 2 * 3.1415 * r * h"
                        "\nTest Cases:"
                        "\nassert math.isclose(lateralsuface_cylinder(10,5), 314.15000000000003, rel_tol=0.001)"
                        "\nassert math.isclose(lateralsuface_cylinder(4,5), 125.66000000000001, rel_tol=0.001)"
                        "\nassert math.isclose(lateralsuface_cylinder(4,10), 251.32000000000002, rel_tol=0.001)"
                        "\n\n### Clarifying Questions:"
                        "\n1. What do the input parameters `r` and `h` mean respectively?"
                        "\n2. Is it acceptable to use an approximation for the value of π, or should the exact value be used?"
                        "\n\n### Answers:\n{insert answers here}"
             },
            {'role': 'assistant',
             'content': '### Answers:'
                        '\n1. The input parameter `r` represents the radius of the cylinder, `h` represents the height of the cylinder.'
                        '\n2. Of course, it is acceptable to use an approximation for the value of π, like 3.1415.'
             },
            {'role': 'user',
             'content': "Python Function:"
                        "\n'''\nWrite a function to find the maximum value in a given heterogeneous list.\n'''"
                        "\ndef max_val(listval):\n     max_val = max(i for i in listval if isinstance(i, int)) \n     return(max_val)"
                        "\nTest Cases:"
                        "\nassert max_val(['Python', 3, 2, 4, 5, 'version'])==5"
                        "\nassert max_val(['Python', 15, 20, 25])==25"
                        "\nassert max_val(['Python', 30, 20, 40, 50, 'version'])==50"
                        "\n\n### Clarifying Questions:"
                        "\n1. What do you mean by a \"heterogeneous list\"? Does it mean that the list can contain elements of different types (e.g., integers, strings, etc.)?"
                        "\n2. If the list can contain different types of elements, does the function only need to focus on the int elements and return the maximum interger in these int elements?"
                        "\n3. Can you provide an example of a heterogeneous list and its expected maximum value?"
                        "\n\n### Answers:\n{insert answers here}"
             },
            {'role': 'assistant',
             'content': "### Answers:"
                        "\n1. A \"heterogeneous list\" means that the list can contain elements of different types, such as integers, strings, etc."
                        "\n2. Yes, the function should focus on the int elements and return the maximum interger in these int elements."
                        "\n3. Yes, here is an example: Input:['Python', 30, 20, 40, 50, 'version'], Output:50."
             },
            {'role': 'user',
             'content': "Python Function:"
                        "\n'''\nWrite a function to merge three dictionaries into a single dictionary.\n'''"
                        "\nimport collections as ct\ndef merge_dictionaries_three(dict1,dict2, dict3):\n    merged_dict = ct.ChainMap(dict1, dict2, dict3)\n    return dict(merged_dict)"
                        "\nTest Cases:"
                        "\nassert merge_dictionaries_three({ \"R\": \"Red\", \"B\": \"Black\", \"P\": \"Pink\" }, { \"G\": \"Green\", \"W\": \"White\" },{ \"O\": \"Orange\", \"W\": \"White\", \"B\": \"Black\" })=={'B': 'Black', 'R': 'Red', 'P': 'Pink', 'G': 'Green', 'W': 'White', 'O': 'Orange'}"
                        "\nassert merge_dictionaries_three({ \"R\": \"Red\", \"B\": \"Black\", \"P\": \"Pink\" }, { \"G\": \"Green\", \"W\": \"White\" },{\"L\":\"lavender\",\"B\":\"Blue\"})=={'W': 'White', 'P': 'Pink', 'B': 'Black', 'R': 'Red', 'G': 'Green', 'L': 'lavender'}"
                        "\nassert merge_dictionaries_three({ \"R\": \"Red\", \"B\": \"Black\", \"P\": \"Pink\" },{\"L\":\"lavender\",\"B\":\"Blue\"},{ \"G\": \"Green\", \"W\": \"White\" })=={'B': 'Black', 'P': 'Pink', 'R': 'Red', 'G': 'Green', 'L': 'lavender', 'W': 'White'}"
                        "\n\n### Clarifying Questions:"
                        "\n1. What should be the type of the output? `ChainMap` object or a regular dictionary?"
                        "\n2. Should the merged dictionary contain all key-value pairs from all three input dictionaries, and what should happen if there are overlapping keys?"
                        "\n3. Can you provide an input-output example to help us better understand your requirement?"
                        "\n\n### Answers:\n{insert answers here}"
             },
            {'role': 'assistant',
             'content': "### Answers:"
                        "\n1. The merged dictionaries should be a regular dictionary."
                        "\n2. Yes, the merged dictionary should contain all key-value pairs from all three input dictionaries, and when there are overlapping keys, the value from the first dictionary in the input sequence should take precedence."
                        "\n3. Yes, here is an input-output example: assert merge_dictionaries_three({\"R\": \"Red\", \"B\": \"Black\", \"P\": \"Pink\" }, {\"L\": \"lavender\", \"B\": \"Blue\"}, {\"G\": \"Green\", \"W\": \"White\"}) == {'B': 'Black', 'P': 'Pink', 'R': 'Red', 'G': 'Green', 'L': 'lavender', 'W': 'White'}"
             },
        ],
}


synthesize_prompt = {
    'zero_shot': [
        {'role': 'system',
         'content': 'You will be given a user requirement and its clarification. '
                    'The clarification aims to enhance the clarity of the requirement and should be duly noted. '
                    'Strictly follow the function signature provided in the requirement, '
                    'respond only with a correct, efficient Python function. '
                    'Do not write explanations or assertions; simply provide only the code.'
         }],

    'one_shot': [
        {'role': 'system',
         'content': 'You will be given a user requirement containing a function signature and a docstring. '
                    'Please read the docstring, understand the user\'s intention, and respond only with a correct, efficient Python function. '
                    'Do not import libraries other than those provided in the function signature; '
                    'do not write explanations or assertions; simply provide only the code.'
         },
        {'role': 'user',
         'content': 'User Requirement:'
                    '\nimport collections as ct\ndef merge_dictionaries_three(dict1,dict2, dict3):\n    \'\'\'\n    Write a function to merge three dictionaries into a single dictionary.'
                    '\n    Clarification:'
                    '\n    1. What should be the type of the output? `ChainMap` object or a regular dictionary?'
                    '\n    - The merged dictionaries should be a regular dictionary.'
                    '\n    2. Should the merged dictionary contain all key-value pairs from all three input dictionaries, and what should happen if there are overlapping keys?'
                    '\n    - Yes, the merged dictionary should contain all key-value pairs from all three input dictionaries, and when there are overlapping keys, the value from the first dictionary in the input sequence should take precedence.'
                    '\n    3. Can you provide an input-output example to help us better understand your requirement?'
                    '\n    - Yes, here is an input-output example: assert merge_dictionaries_three({"R": "Red", "B": "Black", "P": "Pink"}, {"L": "lavender", "B": "Blue"}, {"G": "Green", "W": "White"}) == {\'B\': \'Black\', \'P\': \'Pink\', \'R\': \'Red\', \'G\': \'Green\', \'L\': \'lavender\', \'W\': \'White\'}\n    \'\'\'\n'
         },
        {'role': 'assistant',
         'content': 'def merge_dictionaries_three(dict1,dict2, dict3):\n    merged_dict = ct.ChainMap(dict1, dict2, dict3)\n    return dict(merged_dict)'
         },
    ],

    'two_shot': [
        {'role': 'system',
         'content': 'You will be given a user requirement containing a function signature and a docstring. '
                    'Please read the docstring, understand the user\'s intention, and respond only with a correct, efficient Python function. '
                    'Do not import libraries other than those provided in the function signature; '
                    'do not write explanations or assertions; simply provide only the code.'
         },
        {'role': 'user',
         'content': "User Requirement:"
                    "\ndef lateralsuface_cylinder(r,h):\n    '''\n    Write a function to find the lateral surface area of a cylinder."
                    "\n    Clarification:"
                    "\n    1. What do the input parameters `r` and `h` mean respectively?"
                    "\n    - The input parameter `r` represents the radius of the cylinder, `h` represents the height of the cylinder."
                    "\n    2. Is it acceptable to use an approximation for the value of π, or should the exact value be used?"
                    "\n    - Of course, it is acceptable to use an approximation for the value of π, like 3.1415.\n    '''"
         },
        {'role': 'assistant',
         'content': "def lateralsuface_cylinder(r,h):\n    return 2 * 3.1415 * r * h"
         },
        {'role': 'user',
         'content': 'User Requirement:'
                    '\nimport collections as ct\ndef merge_dictionaries_three(dict1,dict2, dict3):\n    \'\'\'\n    Write a function to merge three dictionaries into a single dictionary.'
                    '\n    Clarification:'
                    '\n    1. What should be the type of the output? `ChainMap` object or a regular dictionary?'
                    '\n    - The merged dictionaries should be a regular dictionary.'
                    '\n    2. Should the merged dictionary contain all key-value pairs from all three input dictionaries, and what should happen if there are overlapping keys?'
                    '\n    - Yes, the merged dictionary should contain all key-value pairs from all three input dictionaries, and when there are overlapping keys, the value from the first dictionary in the input sequence should take precedence.'
                    '\n    3. Can you provide an input-output example to help us better understand your requirement?'
                    '\n    - Yes, here is an input-output example: assert merge_dictionaries_three({"R": "Red", "B": "Black", "P": "Pink"}, {"L": "lavender", "B": "Blue"}, {"G": "Green", "W": "White"}) == {\'B\': \'Black\', \'P\': \'Pink\', \'R\': \'Red\', \'G\': \'Green\', \'L\': \'lavender\', \'W\': \'White\'}\n    \'\'\''
         },
        {'role': 'assistant',
         'content': 'def merge_dictionaries_three(dict1,dict2, dict3):\n    merged_dict = ct.ChainMap(dict1, dict2, dict3)\n    return dict(merged_dict)'
         },
    ],

    'three_shot': [
        {'role': 'system',
         'content': 'You will be given a user requirement containing a function signature and a docstring. '
                    'Please read the docstring, understand the user\'s intention, and respond only with a correct, efficient Python function. '
                    'Do not import libraries other than those provided in the function signature; '
                    'do not write explanations or assertions; simply provide only the code.'
         },
        {'role': 'user',
         'content': "User Requirement:"
                    "\ndef lateralsuface_cylinder(r,h):\n    '''\n    Write a function to find the lateral surface area of a cylinder."
                    "\n    Clarification:"
                    "\n    1. What do the input parameters `r` and `h` mean respectively?"
                    "\n    - The input parameter `r` represents the radius of the cylinder, `h` represents the height of the cylinder."
                    "\n    2. Is it acceptable to use an approximation for the value of π, or should the exact value be used?"
                    "\n    - Of course, it is acceptable to use an approximation for the value of π, like 3.1415.\n    '''"},
        {'role': 'assistant',
         'content': "def lateralsuface_cylinder(r,h):\n    return 2 * 3.1415 * r * h"
         },
        {'role': 'user',
         'content': 'User Requirement:'
                    '\ndef max_val(listval):\n    \'\'\'\n    Write a function to find the maximum value in a given heterogeneous list.'
                    '\n    Clarification:'
                    '\n    1. What do you mean by a "heterogeneous list"? Does it mean that the list can contain elements of different types (e.g., integers, strings, etc.)?'
                    '\n    - A "heterogeneous list" means that the list can contain elements of different types, such as integers, strings, etc.'
                    '\n    2. If the list can contain different types of elements, does the function only need to focus on the int elements and return the maximum interger in these int elements?'
                    '\n    - Yes, the function should focus on the int elements and return the maximum interger in these int elements.'
                    '\n    3. Can you provide an example of a heterogeneous list and its expected maximum value?'
                    '\n    - Yes, here is an example: Input:[\'Python\', 30, 20, 40, 50, \'version\'], Output:50.\n    \'\'\''
         },
        {'role': 'assistant',
         'content': 'def max_val(listval):\n     max_val = max(i for i in listval if isinstance(i, int)) \n     return(max_val)'
         },
        {'role': 'user',
         'content': 'User Requirement:'
                    '\nimport collections as ct\ndef merge_dictionaries_three(dict1,dict2, dict3):\n    \'\'\'\n    Write a function to merge three dictionaries into a single dictionary.'
                    '\n    Clarification:'
                    '\n    1. What should be the type of the output? `ChainMap` object or a regular dictionary?'
                    '\n    - The merged dictionaries should be a regular dictionary.'
                    '\n    2. Should the merged dictionary contain all key-value pairs from all three input dictionaries, and what should happen if there are overlapping keys?'
                    '\n    - Yes, the merged dictionary should contain all key-value pairs from all three input dictionaries, and when there are overlapping keys, the value from the first dictionary in the input sequence should take precedence.'
                    '\n    3. Can you provide an input-output example to help us better understand your requirement?'
                    '\n    - Yes, here is an input-output example: assert merge_dictionaries_three({"R": "Red", "B": "Black", "P": "Pink"}, {"L": "lavender", "B": "Blue"}, {"G": "Green", "W": "White"}) == {\'B\': \'Black\', \'P\': \'Pink\', \'R\': \'Red\', \'G\': \'Green\', \'L\': \'lavender\', \'W\': \'White\'}\n    \'\'\''
         },
        {'role': 'assistant',
         'content': 'def merge_dictionaries_three(dict1,dict2, dict3):\n    merged_dict = ct.ChainMap(dict1, dict2, dict3)\n    return dict(merged_dict)'
         },
    ],
}