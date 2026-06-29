from issuescout.utils.issue_file_parser import (
    extract_file_mentions,
)


def test_python_file():

    files = extract_file_mentions("See Lib/test/test_json.py")

    assert files == {
        "Lib/test/test_json.py",
    }


def test_multiple_files():

    files = extract_file_mentions(
        """
        Lib/test/test_json.py
        Lib/json/__init__.py
        README.md
        """
    )

    assert files == {
        "Lib/test/test_json.py",
        "Lib/json/__init__.py",
        "README.md",
    }


def test_duplicate_files():

    files = extract_file_mentions(
        """
        README.md
        README.md
        """
    )

    assert files == {
        "README.md",
    }


def test_no_files():

    files = extract_file_mentions("This issue has no filenames.")

    assert files == set()


def test_nested_paths():

    files = extract_file_mentions("Modules/_io/textio.c")

    assert files == {
        "Modules/_io/textio.c",
    }


def test_windows_path_not_detected():

    files = extract_file_mentions(r"C:\Users\milan\test.py")

    assert files == set()


def test_markdown_code_block():

    files = extract_file_mentions(
        """
            ```python
            Lib/test/test_json.py
        """
    )
    assert "Lib/test/test_json.py" in files
