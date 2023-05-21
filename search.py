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
    ids = []
    # Loop through the list of strings
    r = range(len(lst) - 1, -1, -1) if reverse else range(len(lst))
    for i in r:
        if not case_sensitive:
            distance = damerau_levenshtein_distance(query.lower(),
                                                    lst[i].lower())
        else:
            distance = damerau_levenshtein_distance(query, lst[i])
        if distance < max_distance:
            ids.append(i)
        if k_matches and len(ids) == k_matches:
            return ids
    return ids
