import pytest
from subprocess import Popen, PIPE

CLI_COMMAND = "dowhen"
MODULE_NAME = "dowhen"


def no_error(output):
    return (
        b"ERROR" not in output
        and b"CRITICAL" not in output
        and b"Exception" not in output
    )


def execute_command_assert_no_error_success(cmd):
    """ Execute a shell command and assert there's no error and return code
    shows success
    """
    assert type(cmd) == list
    list_proc = Popen(cmd, stdout=PIPE)
    list_output = list_proc.stdout.read()
    assert no_error(list_output), list_output
    list_proc.wait()
    if list_proc.returncode is None:
        list_proc.terminate()
    try:
        assert (
            list_proc.returncode == 0
        ), "Invalid return code from command. Expected 0 but saw {}".format(
            list_proc.returncode
        )
    except AssertionError as err:
        print("--------------------------------------------------------")
        print("Command failed: {}".format(" ".join(cmd)))
        raise err
    return list_output


@pytest.mark.parametrize("cmd", [[CLI_COMMAND], ["python", "-m", MODULE_NAME],])
def test_cli_integration(cmd):
    """ Test the CLI as a whole """

    # Test help
    execute_command_assert_no_error_success([*cmd, "-h"])
    execute_command_assert_no_error_success([*cmd, "--help"])
