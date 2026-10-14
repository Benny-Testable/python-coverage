from ledgerly.ledger import net_balance, scale


def test_net_balance():
    assert net_balance(10, 4) == 6
    assert net_balance(0, 3) == -3


def test_scale():
    assert scale(4) == 4
    assert scale(4, 3) == 12
