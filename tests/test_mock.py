from unittest.mock import MagicMock
from pytest_mock import MockerFixture
from pytesting import app
import pytest

def test_slack_fails():
    app.send_slack_message("prod")

def test_slack_mocked(mocker: MockerFixture):

    # prod sí envía msj
    mocked_slack = mocker.MagicMock()
    mocker.patch("pytesting.app.connect_slack", return_value=mocked_slack)
    app.send_slack_message("prod")
    mocked_slack.send_message.assert_called_once()

    # dev no debería enviar mensaje
    mocked_slack = mocker.MagicMock()
    mocker.patch("pytesting.app.connect_slack", return_value=mocked_slack)
    app.send_slack_message("dev")
    mocked_slack.send_message.assert_not_called()