from derangement import pool_derangement


def secret_santa_imperative(n, seed=None):
    """Compatibility wrapper for experimenting with the pool derangement."""
    return pool_derangement(n, seed=seed)

if __name__ == "__main__":
    a = secret_santa_imperative(8)
    print(sorted(a.items()))
