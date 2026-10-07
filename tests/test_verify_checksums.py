"""The eval-integrity gate must work after a Windows Git checkout."""

import importlib.util
from pathlib import Path


def test_checksum_ignores_line_endings_but_detects_content_edits(tmp_path):
    source = Path(__file__).resolve().parents[1] / "scripts" / "verify.py"
    spec = importlib.util.spec_from_file_location("lab_verify", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    dataset = tmp_path / "eval.jsonl"
    dataset.write_bytes(b'{"label":"a"}\n{"label":"b"}\n')
    expected = module._sha(dataset)

    dataset.write_bytes(b'{"label":"a"}\r\n{"label":"b"}\r\n')
    assert module._sha(dataset) == expected

    dataset.write_bytes(b'{"label":"a"}\r\n{"label":"c"}\r\n')
    assert module._sha(dataset) != expected
