
import tempfile
import pathlib


def get_temp_file():
    # Define temporary file
    return tempfile.NamedTemporaryFile(
        mode="w+t", prefix="GC_", suffix=".html", delete=False)


def load_web_page(GC, temp_file):
    GC.webpage(pathlib.Path(temp_file.name).as_uri())
