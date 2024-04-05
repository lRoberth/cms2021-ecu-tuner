'''
Made by
https://github.com/lRoberth
https://steamcommunity.com/id/MrlRoberth/
for free for the community
'''

from collections import deque
import os

def normalize(number):
    """Normalize a number to be within the range [-2, 6]."""
    if(number > 6):
        return -2
    if(number < -2):
        return 6
    return number

def apply_operation(array, idx, operation):
    """Apply an operation (sum or reduce) to the number at the given index."""
    new_array = array.copy()
    if operation == 'sum':
        new_array[idx] = normalize(new_array[idx] + 1)
        for i in range(len(new_array)):
            if i != idx:
                new_array[i] = normalize(new_array[i] - 1)
    elif operation == 'reduce':
        new_array[idx] = normalize(new_array[idx] - 1)
        for i in range(len(new_array)):
            if i != idx:
                new_array[i] = normalize(new_array[i] + 1)
    return new_array

def get_user_input(prompt, min_val=-2, max_val=6):
    """Get user input within a specified range."""
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Value must be between {min_val} and {max_val}. Please try again.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def find_solution(initial_array):
    """Find the most efficient steps to reach array[6, 6, 6, 6, 6] from the initial array."""
    visited = set()
    queue = deque([(initial_array, [])])

    while queue:
        current_array, steps = queue.popleft()
        if tuple(current_array) in visited:
            continue
        visited.add(tuple(current_array))

        if all(num == 6 for num in current_array):
            return steps

        for idx in range(len(current_array)):
            for operation in ['sum', 'reduce']:
                new_array = apply_operation(current_array, idx, operation)
                if(operation == 'sum'):
                    operation_str = 'Add'
                else:
                    operation_str = 'Subtract'
                new_steps = steps + [f"Step {len(steps) + 1}: {operation_str} to graph {idx + 1} ({current_array[idx]} to {new_array[idx]}). Graph should look like: {new_array}"]
                queue.append((new_array, new_steps))

    return None

print("Please describe your current ECU graph values")
initial_array = []
for i in range(5):
    initial_array.append(get_user_input(f"Enter value for graph {i + 1}: "))

os.system('cls')

print(f"Starting graph: {initial_array}")
current_array = initial_array[:]
steps = find_solution(initial_array)
if steps:
    for step in steps:
        print(step)
        # Update current_array for the next step
        parts = step.split()
        if parts[3] == 'sum':
            current_array[int(parts[5])] = normalize(current_array[int(parts[5])] + 1)
            for i in range(len(current_array)):
                if i != int(parts[5]):
                    current_array[i] = normalize(current_array[i] - 1)
        elif parts[3] == 'reduce':
            current_array[int(parts[5])] = normalize(current_array[int(parts[5])] - 1)
            for i in range(len(current_array)):
                if i != int(parts[5]):
                    current_array[i] = normalize(current_array[i] + 1)
else:
    print("No solution found, please check your input.")
