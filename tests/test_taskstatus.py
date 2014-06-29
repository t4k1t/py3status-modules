"""Tests for the taskstatus module."""

import pytest
import os.path
from subprocess import CalledProcessError
from taskstatus import taskstatus
from taskstatus.taskstatus import Data, Py3status, TaskstatusException
# TODO: Test actual py3status response.


class TestData:

    """Test Data functions."""

    def test_no_open_tasks(self, monkeypatch):
        """Test taskwarrior without any open tasks."""
        def mockreturn(*args, **kwargs):
            if args == (['task', 'stats'],):
                output = b"""
                Category Data
                -------- ----
                Pending 0
                Waiting 0"""
                return output
            elif args == (['task', 'overdue'],):
                output = 'No matches.'
                e = CalledProcessError(1, 'task')
                e.output = output
                raise e
        monkeypatch.setattr(taskstatus, 'check_output', mockreturn)
        data = Data()
        tasks = data.get_tasks()
        assert tasks == (0, 0)

    def test_overdue_tasks(self, monkeypatch):
        """Test taskwarrior with one open and one overdue task."""
        def mockreturn(*args, **kwargs):
            if args == (['task', 'stats'],):
                output = b"""
                Category Data
                -------- ----
                Pending 1
                Waiting 0"""
                return output
            elif args == (['task', 'overdue'],):
                output = b"""
                ID Project Pri Due Active Age Description
                -- ------- --- --- ------ --- -----------
                1  project L              1m  test stuff

                1 task"""
                return output
        monkeypatch.setattr(taskstatus, 'check_output', mockreturn)
        data = Data()
        tasks = data.get_tasks()
        assert tasks == (1, 1)


class TestResponse:

    """Test Py3status class."""

    def test_empty_config(self, monkeypatch, empty_config):
        """Test config without taskstatus section."""
        def mockreturn(path):
            path_string = (empty_config.dirname + "/" +
                           empty_config.basename + "/modules.ini")
            return path_string
        monkeypatch.setattr(os.path, 'expanduser', mockreturn)
        with pytest.raises(TaskstatusException) as e:
            Py3status()
        assert "no taskstatus section" in str(e)

    def test_no_taskwarrior(self, monkeypatch, valid_config):
        """Test missing installation of taskwarrior."""
        def mock_config(path):
            path_string = (valid_config.dirname + "/" +
                           valid_config.basename + "/modules.ini")
            return path_string

        def mock_check_output(*args, **kwargs):
            if args == (['task', '--version'],):
                raise OSError
        monkeypatch.setattr(taskstatus, 'check_output', mock_check_output)
        monkeypatch.setattr(os.path, 'expanduser', mock_config)
        with pytest.raises(TaskstatusException) as e:
            py3 = Py3status()
            py3.data.get_tasks()
        assert "failed to execute" in str(e)
