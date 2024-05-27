# Jain's fairness index
# Equals 1 when all vehicles have the same delay
def jains_fairness_index(d):
    if len(d) > 1:
        return sum(d) ** 2 / (len(d) * sum([i ** 2 for i in d]))
    return 1
