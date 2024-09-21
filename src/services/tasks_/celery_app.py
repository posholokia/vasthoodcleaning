from pathlib import Path

from celery import (
    bootsteps,
    Celery,
)
from celery.signals import (
    worker_ready,
    worker_shutdown,
)


"""------------------------------------------------------------------"""
"""-------------ПРОБЫ ПРОВЕРКИ ЦЕЛОСТНОСТИ CELERY WORKER-------------"""
"""------------------------------------------------------------------"""

HEARTBEAT_FILE = Path("/tmp/celery_heartbeat")
READINESS_FILE = Path("/tmp/celery_ready")


class LivenessProbe(bootsteps.StartStopStep):
    requires = {"celery.worker.components:Timer"}

    def __init__(self, worker, **kwargs):  # noqa
        self.requests = []
        self.tref = None

    def start(self, worker):
        self.tref = worker.timer.call_repeatedly(
            1.0,
            self.update_heartbeat_file,
            (worker,),
            priority=10,
        )

    def stop(self, worker):
        HEARTBEAT_FILE.unlink(missing_ok=True)

    def update_heartbeat_file(self, worker):
        HEARTBEAT_FILE.touch()


@worker_ready.connect
def worker_ready(**_):
    READINESS_FILE.touch()


@worker_shutdown.connect
def worker_shutdown(**_):
    READINESS_FILE.unlink(missing_ok=True)


"""------------------------------------------------------------------"""
"""--------------------НАСТРОЙКИ ПРИЛОЖЕНИЯ CELERY-------------------"""
"""------------------------------------------------------------------"""


app = Celery("quiz")
app.steps["worker"].add(LivenessProbe)

app.config_from_object("services.tasks_.celery_config")

app.autodiscover_tasks(packages=["services.tasks_"])


"""------------------------------------------------------------------"""
"""-----------------------ПЕРИОДИЧЕСКИЕ ТАСКИ------------------------"""
"""------------------------------------------------------------------"""
