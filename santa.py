from derangement import pool_derangement

def secret_santa_imperative(n, seed=None):
    """
    Imperative implementation of Secret Santa algorithm.
    
    Args:
        n: Number of people (index 1 to n)
        seed: Optional random seed for reproducible assignments
    
    Returns:
        Dictionary mapping giver -> recipient
    """
    if n < 2:
        raise ValueError("n must be greater than 1")

    return pool_derangement(n, seed=seed)


# Example usage
if __name__ == "__main__":
    result = secret_santa_imperative(6)
    print("Secret Santa Assignments (Python Imperative):")
    for giver, recipient in sorted(result.items()):
        print(f"  {giver} → {recipient}")
