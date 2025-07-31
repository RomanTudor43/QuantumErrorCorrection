def correct(result_string):
    result_string = list(result_string)

    for i in range(0, 28, 2):
        left = result_string[i - 1]
        right = result_string[(i + 1) % 28]
        parity = result_string[i]

        # XOR check: 1 if bits are different, 0 if the same
        expected_parity = '1' if left != right else '0'

        if parity != expected_parity:
            return "WRONG"
    
    for i in range(1, 28, 2):
        if result_string[i] == '1':
            if result_string[(i + 1) % 28] == '0' and result_string[(i + 2) % 28] == '0':
                return "WRONG"
            
            if result_string[i - 1] == '0' and result_string[i - 2] == '0':
                return "WRONG"

    return "CORRECT"


#####################################################################################################

import csv

def read_and_correct(filename="split_surface_from_0.csv"):
    """
    Reads state strings from the CSV file and checks them using the 'correct' function.
    
    Args:
        filename (str): The CSV file to read from.
    
    Returns:
        results (list of tuples): Each tuple contains (job_id, state, count, result)
    """
    results = []
    current_job_id = None

    correct_states = 0

    with open(filename, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if not row:
                continue  # Skip empty lines

            if len(row) == 1:
                # This is a job ID line
                current_job_id = row[0]
            elif len(row) == 2:
                state, count = row
                verdict = correct(state)
                if verdict == "CORRECT":
                    correct_states += int(count)

    return correct_states


# Example usage:
results = read_and_correct()

print(f"{results/3}/10,000")


#####################################################################################################
