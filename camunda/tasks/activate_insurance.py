from pyzeebe import Job

from database.validators import InsuranceValidator
from database.database import supabase

from . import router

TASK_TYPE = 'ActivateInsurance'  # name of the task


@router.task(task_type=TASK_TYPE)
async def save_insurance(job: Job):
    """
    Prepares the insurance certificate.
    """

    instance_id = job.process_instance_key

    print(f'Task \'{TASK_TYPE}\' is started for instance {instance_id}')

    data = job.variables
    insurance = InsuranceValidator.model_validate(data['insurance'])
    (supabase.table('insurances')
     .update({'status': 'Activated'})
     .eq('insurance_id', insurance.insurance_id)
     .execute())
    insurance.status = 'Activated'

    return {'insurance': insurance.model_dump()}
