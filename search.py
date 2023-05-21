# Define a function to calculate the Damerau-Levenshtein distance
# between two strings
def damerau_levenshtein_distance(s1, s2):
    # Initialize a matrix of size (len(s1)+1) x (len(s2)+1)
    matrix = [[0 for j in range(len(s2)+1)] for i in range(len(s1)+1)]
    # Fill the first row and column with the index values
    for i in range(len(s1)+1):
        matrix[i][0] = i
    for j in range(len(s2)+1):
        matrix[0][j] = j
    # Loop through the rest of the matrix
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            # If the characters match, the cost is 0, otherwise 1
            cost = 0 if s1[i-1] == s2[j-1] else 1
            # Find the minimum of the three possible operations:
            # deletion, insertion, or substitution
            matrix[i][j] = min(matrix[i-1][j] + 1, matrix[i][j-1] + 1,
                               matrix[i-1][j-1] + cost)
            # Check for a transposition and update the matrix if needed
            if i > 1 and j > 1 and s1[i-1] == s2[j-2] and s1[i-2] == s2[j-1]:
                matrix[i][j] = min(matrix[i][j], matrix[i-2][j-2] + cost)
    # Return the bottom-right value of the matrix as the distance
    return matrix[-1][-1]


def search(query, lst, case_sensitive=True, max_distance=2, k_matches=None,
           reverse=False):
    # Initialize a variable to store the minimum distance and the
    # matching string
    if reverse:
        lst.reverse()
    match = []
    # Loop through the list of strings
    for string in lst:
        # If case sensitivity is False, convert both query and
        # string to lower case
        if not case_sensitive:
            distance = damerau_levenshtein_distance(query.lower(),
                                                    string.lower())
        # Calculate the distance between the query and the string
        else:
            distance = damerau_levenshtein_distance(query, string)
        # If the distance is smaller than the current minimum, update
        # the minimum and the match
        if distance < max_distance:
            match.append(string)
        if k_matches and len(match) == k_matches:
            return match
    # Return the match and the minimum distance
    return match


def main():
    lst = ["Apple", "Banana", "Orange", "Pear", "Pineapple", "apple"]
    query = "aple"
    match = search(query, lst, case_sensitive=False, k_matches=1, reverse=True)
    print(f"The closest match to {query} is {match}")


if __name__ == "__main__":
    main()
