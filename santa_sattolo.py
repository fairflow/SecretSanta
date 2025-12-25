import random


def secret_santa_imperative(n):
    """Generate Secret Santa assignments using Sattolo's algorithm.

    This produces a single cycle of length n (an n-cycle), which is always a
    valid Secret Santa assignment for n >= 2:
    - Everyone gives exactly one gift
    - Everyone receives exactly one gift
    - Nobody gives to themselves

    Args:
        n: Number of people (index 1 to n)

    Returns:
        Dictionary mapping giver -> recipient
    """
    if n < 2:
        raise ValueError("n must be greater than 1")

    # Sattolo's algorithm: uniform over n-cycles.
    participants = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = random.randrange(i)  # 0 <= j < i
        participants[i], participants[j] = participants[j], participants[i]

    assignments = {}
    for i in range(n):
        giver = participants[i]
        recipient = participants[(i + 1) % n]
        assignments[giver] = recipient

    return assignments


# Example usage
if __name__ == "__main__":
    result = secret_santa_imperative(6)
    print("Secret Santa Assignments (Sattolo / single cycle):")
    for giver, recipient in sorted(result.items()):
        print(f"  {giver}  {recipient}")
