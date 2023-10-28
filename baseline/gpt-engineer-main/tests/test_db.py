import pytest

from gpt_engineer.db import DB, DBs


def test_DB_operations(tmp_path):
    # Test initialization
    db = DB(tmp_path)

    # Test __setitem__
    db["test_key"] = "test_value"

    assert (tmp_path / "test_key").is_file()

    # Test __getitem__
    val = db["test_key"]

    assert val == "test_value"

    # Test error on getting non-existent key
    with pytest.raises(KeyError):
        db["non_existent"]

    # Test error on setting non-str or non-bytes value
    with pytest.raises(TypeError):
        db["key"] = ["Invalid", "value"]


def test_DBs_initialization(tmp_path):
    dir_names = ["memory", "logs", "preprompts", "input", "workspace"]
    directories = [tmp_path / name for name in dir_names]

    # Create DB objects
    dbs = [DB(dir) for dir in directories]

    # Create DB instance
    dbs_instance = DBs(*dbs)

    assert isinstance(dbs_instance.memory, DB)
    assert isinstance(dbs_instance.logs, DB)
    assert isinstance(dbs_instance.preprompts, DB)
    assert isinstance(dbs_instance.input, DB)
    assert isinstance(dbs_instance.workspace, DB)


def test_invalid_path():
    with pytest.raises((PermissionError, OSError)):
        # Test with a path that will raise a permission error
        DB("/root/test")


def test_large_files(tmp_path):
    db = DB(tmp_path)
    large_content = "a" * (10**6)  # 1MB of data

    # Test write large files
    db["large_file"] = large_content

    # Test read large files
    assert db["large_file"] == large_content


def test_concurrent_access(tmp_path):
    import threading

    db = DB(tmp_path)

    num_threads = 10
    num_writes = 1000

    def write_to_db(thread_id):
        for i in range(num_writes):
            key = f"thread{thread_id}_write{i}"
            db[key] = str(i)

    threads = []
    for thread_id in range(num_threads):
        t = threading.Thread(target=write_to_db, args=(thread_id,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # Verify that all expected data was written
    for thread_id in range(num_threads):
        for i in range(num_writes):
            key = f"thread{thread_id}_write{i}"
            assert key in db  # using __contains__ now
            assert db[key] == str(i)


def test_error_messages(tmp_path):
    db = DB(tmp_path)

    with pytest.raises(TypeError) as e:
        db["key"] = ["Invalid", "value"]

    assert str(e.value) == "val must be either a str or bytes"


def test_DBs_instantiation_with_wrong_number_of_arguments(tmp_path):
    db = DB(tmp_path)

    with pytest.raises(TypeError):
        DBs(db, db, db)

    with pytest.raises(TypeError):
        DBs(db, db, db, db, db, db)


def test_DBs_dataclass_attributes(tmp_path):
    dir_names = ["memory", "logs", "preprompts", "input", "workspace"]
    directories = [tmp_path / name for name in dir_names]

    # Create DB objects
    dbs = [DB(dir) for dir in directories]

    # Create DBs instance
    dbs_instance = DBs(*dbs)

    assert dbs_instance.memory == dbs[0]
    assert dbs_instance.logs == dbs[1]
    assert dbs_instance.preprompts == dbs[2]
    assert dbs_instance.input == dbs[3]
    assert dbs_instance.workspace == dbs[4]
