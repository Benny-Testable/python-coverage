from ledgerly import shell_tools


def test_batch_script_exit_codes():
    assert shell_tools.run_batch_script("exit 0") == 0
    assert shell_tools.run_batch_script("exit 3") == 3
