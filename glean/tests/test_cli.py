import tempfile
import pytest
from click.testing import CliRunner
import glean.cli
import glean.api


@pytest.yield_fixture
def tempfl():
    """Create a temp file, needed for CLI args that check that file exists"""
    with tempfile.NamedTemporaryFile() as fl:
        yield fl


@pytest.mark.parametrize(
    "subcmd",
    [None, "single", "quantiles"],
    ids=("--help", "single --help", "quantiles --help"),
)
def test_cli_helpflags(subcmd):
    """Test that CLI commands don't throw Error if given --help flag"""
    runner = CliRunner()

    # Setup CLI args
    cli_args = ["--help"]
    if subcmd is not None:
        cli_args = [subcmd, "--help"]

    result = runner.invoke(glean.cli.glean_cli, cli_args)
    assert "Error:" not in result.output


def test_single_nofile(mocker):
    """Ensure that 'single' gives error output if input file doesn't exist"""
    mocker.patch.object(glean.api, "single")
    tempfile_name = "doesntexist.foobar"

    runner = CliRunner()

    result = runner.invoke(glean.cli.glean_cli, ["single", tempfile_name])
    assert "Error:" in result.output and "does not exist" in result.output


@pytest.mark.parametrize(
    "addargs,expected",
    [
        (None, {}),
        (["-c", "region=CAN.1.2.28"], {"region": "CAN.1.2.28"}),
        (["--conf", "region=CAN.1.2.28"], {"region": "CAN.1.2.28"}),
        (
            ["-c", "region=CAN.1.2.28", "-c", "yearsets=yes"],
            {"region": "CAN.1.2.28", "yearsets": "yes"},
        ),
    ],
)
def test_single_argpass(mocker, tempfl, addargs, expected):
    """Whitebox test that 'single' subcommand correctly passes args to API"""
    mocker.patch.object(glean.api, "single")
    cli_args = ["single"]

    # Assemble CLI args
    tempfile_name = str(tempfl.name)
    cli_args.append(tempfile_name)
    if addargs is not None:
        addargs = list(addargs)
        cli_args += addargs

    runner = CliRunner()

    runner.invoke(glean.cli.glean_cli, cli_args)
    glean.api.single.assert_called_once_with([tempfile_name], expected)


def test_quantiles_nofile(mocker):
    """Ensure that 'quantiles' gives error output if input file doesn't exist"""
    mocker.patch.object(glean.api, "quantiles")
    tempfile_name = "doesntexist.foobar"

    runner = CliRunner()

    result = runner.invoke(glean.cli.glean_cli, ["quantiles", tempfile_name])
    assert "Error:" in result.output and "does not exist" in result.output


@pytest.mark.parametrize(
    "addargs,expected_argv,expected_config",
    [
        (["basefilename"], ("basefilename",), {"abc": 123}),
        (
            ["basefilename", "basefilename2"],
            ("basefilename", "basefilename2"),
            {"abc": 123},
        ),
        (
            ["basefilename", "--", "-basefilename2"],
            ("basefilename", "-basefilename2"),
            {"abc": 123},
        ),
        (
            ["-c", "region=CAN.1.2.28", "basefilename"],
            ("basefilename",),
            {"abc": 123, "region": "CAN.1.2.28"},
        ),
        (
            ["-c", "region=CAN.1.2.28", "--", "basefilename", "-basefilename2"],
            ("basefilename", "-basefilename2"),
            {"abc": 123, "region": "CAN.1.2.28"},
        ),
    ],
)
def test_quantiles_argpass(mocker, tempfl, addargs, expected_argv, expected_config):
    """Whitebox test that 'quantiles' subcommand correctly passes args to API"""
    mocker.patch.object(glean.api, "quantiles")
    mocker.patch.object(glean.cli.core, "read_config", return_value={"abc": 123})

    cli_args = ["quantiles"]

    # Assemble CLI args
    tempfile_name = str(tempfl.name)
    cli_args.append(tempfile_name)
    if addargs is not None:
        addargs = list(addargs)
        cli_args += addargs

    runner = CliRunner()

    runner.invoke(glean.cli.glean_cli, cli_args)
    glean.api.quantiles.assert_called_once_with(expected_argv, expected_config)
