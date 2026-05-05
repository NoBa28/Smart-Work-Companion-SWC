import json

from storage.json_storage import JsonStorage


def test_init_creates_empty_file(tmp_path):
    file_path = tmp_path / "data" / "test.json"

    storage = JsonStorage(str(file_path))

    assert file_path.exists()

    assert storage.load() == []


def test_load_returns_empty_list_for_new_file(tmp_path):
    file_path = tmp_path / "new.json"

    storage = JsonStorage(str(file_path))

    assert storage.load() == []


def test_save_writes_data_to_file(tmp_path):
    file_path = tmp_path / "save_test.json"
    storage = JsonStorage(str(file_path))

    data = [{"id": 1, "title": "Task"}]

    storage.save(data)

    with open(file_path) as f:
        loaded_raw = json.load(f)

    assert loaded_raw == data


def test_load_returns_saved_data(tmp_path):
    file_path = tmp_path / "load_test.json"
    storage = JsonStorage(str(file_path))

    data = [{"name": "Noah"}, {"name": "Python"}]

    storage.save(data)

    assert storage.load() == data


def test_save_overwrites_existing_data(tmp_path):
    file_path = tmp_path / "overwrite.json"
    storage = JsonStorage(str(file_path))

    storage.save([{"old": True}])
    storage.save([{"new": True}])

    assert storage.load() == [{"new": True}]


def test_empty_file_returns_empty_list(tmp_path):
    file_path = tmp_path / "empty.json"

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("")

    storage = JsonStorage(str(file_path))

    assert storage.load() == []


def test_nested_directories_are_created(tmp_path):
    file_path = tmp_path / "deep" / "nested" / "folder" / "file.json"

    storage = JsonStorage(str(file_path))

    assert file_path.exists()
    assert file_path.parent.exists()
    assert storage.load() == []
