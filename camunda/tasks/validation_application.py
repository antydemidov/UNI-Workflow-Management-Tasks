from pydantic import ValidationError
from pyzeebe import Job

from database.validators import ApplicationValidator

from . import router

TASK_TYPE = 'ApplicationValidation'


@router.task(task_type=TASK_TYPE)
async def application_validation(job: Job):
    """
    Validates a dictionary against a given schema.
    """

    instance_id = job.process_instance_key
    print(f'Task \'{TASK_TYPE}\' is started for instance {instance_id}')

    application_data: dict | None = job.variables.get('bvis_message')

    if not application_data:
        return {'is_application_validated': False}

    try:
        application = ApplicationValidator(**application_data)
    except ValidationError as e:
        print(f'Validation error: {e}')
        return {'is_application_validated': False}

    return {
        'is_application_validated': True,
        'application': application.model_dump()
    }
