import pathlib

import pytest

from asciinema_automation.cli import cli

path_to_example_folder = pathlib.Path("examples")
if not path_to_example_folder.is_dir():
    raise ValueError(
        "input-folder argument from command line must be a valid path to a folder."
    )


@pytest.fixture(autouse=True)
def change_test_directory(tmp_path, monkeypatch) -> None:
    pathlib.Path.mkdir(pathlib.Path(tmp_path / "tmp"), exist_ok=True)
    monkeypatch.chdir(tmp_path / "tmp")


# path_to_example_folder.iterdir()
@pytest.mark.parametrize(
    "inputfile",
    path_to_example_folder.iterdir(),
    ids=[example.name for example in path_to_example_folder.iterdir()],
)
def test_regression(tmp_path, request, inputfile: pathlib.Path):
    example_folder = request.config.invocation_params.dir / "examples"
    reference_folder = (
        request.config.invocation_params.dir / "tests" / "reference_output"
    )
    output_folder = tmp_path
    output_file_name = inputfile.stem + ".cast"
    print(pathlib.Path().cwd())
    cli(
        [
            "--debug",
            "--asciinema-arguments",
            """--raw --overwrite -c 'env -i TERM=xterm-256color HOME=~ PS1="$ " PATH=/usr/bin:/usr/local/bin/ bash --noprofile --norc'""",
            str(example_folder / inputfile.name),
            str(output_folder / output_file_name),
        ]
    )

    with open(output_folder / output_file_name, "r") as output_file:
        with pathlib.Path(reference_folder / output_file_name).open() as reference_file:
            assert output_file.readlines() == reference_file.readlines()
