import random
from typing import Dict, Optional


def pool_derangement(n: int, seed: Optional[object] = None) -> Dict[int, int]:
    """Generate a derangement (no fixed points) as a 1..n -> 1..n mapping.

    This is based on the pool-based algorithm currently prototyped in
    `santa_better.py`: maintain a set of remaining givers and a recipient pool
    that evolves to ensure everyone is eventually assigned exactly once as a
    recipient.

    Notes:
    - This does *not* claim to sample derangements uniformly.
    - It is single-pass and avoids rejection-sampling full permutations.

    Args:
        n: number of participants (labelled 1..n)
        seed: optional seed for reproducible results

    Returns:
        dict mapping giver -> recipient
    """
    if n < 2:
        raise ValueError("n must be greater than 1")

    rng = random.Random(seed)

    def _attempt_once() -> Dict[int, int]:
        people = list(range(1, n + 1))
        givers = set(people)
        recipients = set(people)

        assignments: Dict[int, int] = {}
        assigned_as_recipient = set()

        current_giver = sorted(givers)[rng.randrange(len(givers))]
        givers.remove(current_giver)

        while True:
            candidates = sorted(recipients - {current_giver})
            if not candidates:
                raise RuntimeError("Algorithm reached a dead-end")

            # Endgame lookahead: when only one giver remains after this step
            # and there are exactly two recipients left right now, avoid a
            # choice that would force the last giver to draw themself.
            if len(givers) == 1 and len(recipients) == 2:
                last_giver = next(iter(givers))
                safe_candidates = []
                for candidate_recipient in candidates:
                    recipients_after = set(recipients)
                    recipients_after.remove(candidate_recipient)

                    assigned_after = assigned_as_recipient | {candidate_recipient}
                    if current_giver not in assigned_after:
                        recipients_after.add(current_giver)

                    if not (len(recipients_after) == 1 and last_giver in recipients_after):
                        safe_candidates.append(candidate_recipient)

                if safe_candidates:
                    candidates = safe_candidates

            recipient = candidates[rng.randrange(len(candidates))]

            assignments[current_giver] = recipient
            recipients.remove(recipient)
            assigned_as_recipient.add(recipient)

            if current_giver not in assigned_as_recipient:
                recipients.add(current_giver)

            if not recipients:
                break

            if not givers:
                raise RuntimeError("Algorithm reached a dead-end")

            current_giver = sorted(givers)[rng.randrange(len(givers))]
            givers.remove(current_giver)

        if set(assignments.keys()) != set(people):
            raise RuntimeError("Not all givers assigned")
        if set(assignments.values()) != set(people):
            raise RuntimeError("Not all recipients assigned")
        if any(g == r for g, r in assignments.items()):
            raise RuntimeError("Fixed point detected")

        return assignments

    # The pool-based approach can still hit a dead-end depending on random
    # choices (though the endgame lookahead above prevents a common one).
    # Retry from scratch; this remains deterministic for a given seed because
    # we continue consuming from the same RNG stream.
    for _ in range(200):
        try:
            return _attempt_once()
        except RuntimeError:
            continue

    raise RuntimeError("Failed to generate derangement after many attempts")
