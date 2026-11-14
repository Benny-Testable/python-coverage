from ledgerly import utils


def test_utils():
    assert utils.slugify("Hello, World!") == "hello-world"
    assert utils.chunked([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
