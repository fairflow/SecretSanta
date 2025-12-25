import random

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

    # Generate a proper Secret Santa assignment:
    # - Everyone gives exactly one gift
    # - Everyone receives exactly one gift
    # - Nobody gives to themselves
    # We do this by generating a random derangement: a random permutation of
    # participants where no one is assigned to themselves.
    rng = random.Random(seed)

    participants = list(range(1, n + 1))
    recipients = participants[:]

    # Rejection-sample shuffles until there are no fixed points.
    # Expected number of shuffles is ~e (~2.7), so this is fast for typical n.
    while True:
        rng.shuffle(recipients)
        if all(giver != recipient for giver, recipient in zip(participants, recipients)):
            break

    assignments = dict(zip(participants, recipients))

    return assignments


# Example usage
if __name__ == "__main__":
    result = secret_santa_imperative(6)
    print("Secret Santa Assignments (Python Imperative):")
    for giver, recipient in sorted(result.items()):
        print(f"  {giver} → {recipient}")
