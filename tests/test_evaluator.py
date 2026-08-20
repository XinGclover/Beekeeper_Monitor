from rule_engine.evaluator import is_rule_matched


def test_greater_than():
    assert is_rule_matched(10, ">", 5) is True
    assert is_rule_matched(3, ">", 5) is False


def test_less_than():
    assert is_rule_matched(3, "<", 5) is True
    assert is_rule_matched(10, "<", 5) is False


def test_greater_or_equal():
    assert is_rule_matched(5, ">=", 5) is True
    assert is_rule_matched(4, ">=", 5) is False


def test_less_or_equal():
    assert is_rule_matched(5, "<=", 5) is True
    assert is_rule_matched(6, "<=", 5) is False


def test_equal():
    assert is_rule_matched(5, "=", 5) is True
    assert is_rule_matched(4, "=", 5) is False


def test_invalid_operator():
    assert is_rule_matched(5, "!=", 5) is False
