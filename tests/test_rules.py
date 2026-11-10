from ledgerly import rules


def test_rules_surcharge():
    loaded = rules.load_rules("- {when: 'weight > 10', add: 5}\n- {when: 'express', add: 20}\n")
    assert rules.surcharge_for(loaded, {"weight": 12, "express": False}) == 5
    assert rules.surcharge_for(loaded, {"weight": 12, "express": True}) == 25
    assert rules.surcharge_for([], {}) == 0
