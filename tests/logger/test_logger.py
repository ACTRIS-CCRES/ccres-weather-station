import logging

from ccres_weather_station.logger import (
    LOG_FORMAT,
    LogLevels,
    get_log_level_from_count,
    init_logger,
)


def test_log_level_from_count():
    assert LogLevels.ERROR == get_log_level_from_count(0)
    assert LogLevels.INFO == get_log_level_from_count(1)
    assert LogLevels.DEBUG == get_log_level_from_count(2)
    assert LogLevels.DEBUG == get_log_level_from_count(1000)


def test_init_logger():
    init_logger(level=LogLevels.INFO)
    lgr = logging.getLogger("ccres_weather_station")
    print(lgr.handlers)
    assert logging.getLevelName(lgr.handlers[0].level) == "INFO"
    assert LOG_FORMAT in logging.getLevelName(lgr.handlers[0].formatter._fmt)
