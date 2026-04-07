from scraper.collector import StatsCollector, stats_storage


def test_add_skill_normalization():
    collector = StatsCollector()
    collector.add_skill("junior", "js")
    assert collector.data["junior"]["javascript"] == 1

    collector.add_skill("junior", "javascript")
    assert collector.data["junior"]["javascript"] == 2

    collector.add_skill("junior", "django")
    assert collector.data["junior"]["javascript"] == 2
    assert collector.data["junior"]["django"] == 1


def test_exclude_words():
    collector = StatsCollector()

    collector.add_skill("junior", "agile")
    assert "agile" not in collector.data["junior"]
    assert len(collector.data["junior"]) == 0


def test_levels_separation():
    collector = StatsCollector()

    collector.add_skill("junior", "django")
    collector.add_skill("middle", "js")

    assert collector.data["junior"]["django"] == 1
    assert collector.data["middle"]["javascript"] == 1
    assert len(collector.data["junior"]) == 1
    assert len(collector.data["junior"]) == 1


def test_stats_storage():
    stats_storage.data = {k: {} for k in stats_storage.data}
    stats_storage.add_skill("junior", "python")
    stats_storage.add_skill("middle", "javascript")
    assert stats_storage.data["junior"]["python"] == 1
    assert stats_storage.data["middle"]["javascript"] == 1
