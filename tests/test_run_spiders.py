from unittest.mock import MagicMock, patch
from run_spiders import run_spiders


@patch("run_spiders.CrawlerProcess")
def test_run_spiders_all(mock_crawler_class):
    mock_process = MagicMock()
    mock_crawler_class.return_value = mock_process

    run_spiders()
    mock_crawler_class.assert_called_once()

    assert mock_process.crawl.call_count == 3
    assert mock_process.start.call_count == 1


@patch("run_spiders.run_spiders")
@patch("run_spiders.save_to_db")
@patch("run_spiders.stats_storage")
def test_main_execution(mock_storage, mock_save, mock_run):
    mock_storage.data = {"junior": {"python": 1}}
    mock_run()
    mock_save(data=mock_storage.data)
    mock_run.assert_called_once()
    mock_save.assert_called_once_with(data=mock_storage.data)
