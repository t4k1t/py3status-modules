"""Tests for the taskstatus module."""

from subprocess import CalledProcessError
from taskstatus import taskstatus
from taskstatus.taskstatus import Data


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
                output = b'No matches.'
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
