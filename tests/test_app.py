import pytest

import app as app_module
from app import app as flask_app


@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setattr(app_module, "initial_directory", str(tmp_path))
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


def test_file_serves_files_within_base(client, tmp_path):
    (tmp_path / "hello.txt").write_text("deck asset", encoding="utf-8")
    resp = client.get("/file/hello.txt")
    assert resp.status_code == 200
    assert b"deck asset" in resp.data


def test_file_blocks_path_traversal(client, tmp_path):
    secret = tmp_path.parent / "secret.txt"
    secret.write_text("s", encoding="utf-8")
    try:
        resp = client.get("/file/../secret.txt")
        assert resp.status_code == 403
    finally:
        secret.unlink()


def test_file_returns_404_for_missing_files(client):
    assert client.get("/file/nope.bin").status_code == 404


def test_save_writes_into_work_dir(client, tmp_path):
    (tmp_path / "deck").mkdir()
    resp = client.post(
        "/save",
        json={"text": "# hi", "filename": "a.md", "work_dir": "deck"},
    )
    assert resp.status_code == 200
    assert (tmp_path / "deck" / "a.md").read_text(encoding="utf-8") == "# hi"


def test_save_blocks_path_traversal(client):
    resp = client.post(
        "/save",
        json={"text": "x", "filename": "evil.md", "work_dir": ".."},
    )
    assert resp.status_code == 403


def test_save_requires_filename(client):
    resp = client.post("/save", json={"text": "x", "filename": ""})
    assert resp.status_code == 400


def test_render_reports_work_dir_and_prefixes_urls(client):
    resp = client.post(
        "/render",
        json={"text": "work-dir: decks/t\n\n![a](/file/i.png)", "view": "slide-view list"},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["work_dir"] == "decks/t"
    assert "/file/decks/t/i.png" in data["html"]
