def convert_stat_to_mod(stat: int) -> int:
    """
    Convert the stat of a creature to the corresponding modifier.

    :param stat: (int) The original stat.
    :return: (int) The modifier.
    """
    result = (stat - 10) // 2
    return result
