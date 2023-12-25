import pathlib
import re

import pytest
from pytest import FixtureRequest, MonkeyPatch

from asciinema_automation.cli import cli

path_to_example_folder = pathlib.Path("examples")
if not path_to_example_folder.is_dir():
    raise ValueError(
        "input-folder argument from command line must be a valid path to a folder."
    )


@pytest.fixture(autouse=True)
def change_test_directory(tmp_path: pathlib.Path, monkeypatch: MonkeyPatch) -> None:
    pathlib.Path.mkdir(pathlib.Path(tmp_path / "tmp"), exist_ok=True)
    monkeypatch.chdir(tmp_path / "tmp")


# path_to_example_folder.iterdir()
@pytest.mark.parametrize(
    "inputfile",
    path_to_example_folder.iterdir(),
    ids=[example.name for example in path_to_example_folder.iterdir()],
)
def test_regression(
    tmp_path: pathlib.Path, request: FixtureRequest, inputfile: pathlib.Path
) -> None:
    example_folder = request.config.invocation_params.dir / "examples"
    reference_folder = (
        request.config.invocation_params.dir / "tests" / "reference_output"
    )
    custom_rc_file = (
        request.config.invocation_params.dir / "tests" / "custom_rc_file_dumb_term"
    )
    output_folder = tmp_path
    output_file_name = inputfile.stem + ".cast"
    print(pathlib.Path().cwd())

    if inputfile.name in ["backward_search.sh", "history.sh", "man_page.sh"]:
        custom_rc_file = (
            request.config.invocation_params.dir / "tests" / "custom_rc_file_xterm_term"
        )
    cli(
        [
            "--debug",
            "--asciinema-arguments",
            """--raw --overwrite -c 'env -i bash --noprofile --rcfile """
            + str(custom_rc_file)
            + """'""",
            str(example_folder / inputfile.name),
            str(output_folder / output_file_name),
        ]
    )

    with open(output_folder / output_file_name) as output_file, pathlib.Path(
        reference_folder / output_file_name
    ).open() as reference_file:
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", re.VERBOSE)
        output_text = output_file.read()
        cleaned_output_text = ansi_escape.sub("", output_text)
        assert cleaned_output_text == reference_file.read()
