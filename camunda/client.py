from pyzeebe import ZeebeWorker, create_insecure_channel

from .constants import ZEEBE_ADDRESS
from .tasks import router

__all__ = [
    'get_worker'
]


def get_worker():
    channel = create_insecure_channel(grpc_address=ZEEBE_ADDRESS)
    zeebe_worker = ZeebeWorker(channel)
    zeebe_worker.include_router(router)
    task_types = ', '.join([task.type for task in zeebe_worker.tasks])
    print(f'Registered tasks: {task_types}')
    return zeebe_worker
