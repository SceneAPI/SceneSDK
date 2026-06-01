import scenesdk


def test_import_exposes_version() -> None:
    assert isinstance(scenesdk.__version__, str)
