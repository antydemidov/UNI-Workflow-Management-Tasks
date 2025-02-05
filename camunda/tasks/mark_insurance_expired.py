from pyzeebe import Job

from database.database import supabase
from database.validators import InsuranceValidator

from . import router

TASK_TYPE = 'MarkInsuranceExpired'  # name of the task


@router.task(task_type=TASK_TYPE)
async def mark_insurance_expired(job: Job):
    """
    Formats the invoice.
    """

    print(f'Task \'{TASK_TYPE}\' is started for instance {job.process_instance_key}')

    data = job.variables
    insurance = InsuranceValidator.model_validate(data['insurance'])

    (supabase.table('insurances')
     .update({'status': 'Expired'})
     .eq('insurance_id', insurance.insurance_id)
     .execute())
    insurance.status = 'Expired'

    return {'insurance': insurance.model_dump()}
