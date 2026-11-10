from ledgerly import cache


def test_cache_round_trip(tmp_path):
    target = tmp_path / "report.cache"
    cache.save({"a": [1, 2, 3]}, target)
    assert cache.load(target) == {"a": [1, 2, 3]}


def test_scratch_file_suffix():
    assert cache.scratch_file().endswith(".cache")
