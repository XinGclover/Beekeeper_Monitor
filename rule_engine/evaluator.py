import operator

OPS = {
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
    "=": operator.eq,
}


def is_rule_matched(value: float, condition_type: str, threshold: float) -> bool:
    op = OPS.get(condition_type)
    if op is None:
        return False
    return op(value, threshold)