from pyzeebe import Job

from database.database import supabase
from database.validators import EligibilityValidator

from . import router

TASK_TYPE = 'SaveEligibility'  # name of the task


@router.task(task_type=TASK_TYPE)
async def save_eligibility(job: Job):
    """
    Updates eligibility data in the database.
    """

    print(f'Task \'{TASK_TYPE}\' is started for instance {job.process_instance_key}')

    data = job.variables
    eligibility_data = data['eligibility']
    eligibility = EligibilityValidator(**eligibility_data)
    application_id = data['application']['application_id']

    (supabase.table('applications')
     .update({'driver_risk': eligibility.driver_risk})
     .eq('application_id', application_id).execute())
    for item in eligibility.vehicle_risk:
        (supabase.table('vehicles')
         .update({'vehicle_risk': item.final_score})
         .eq('vehicle_id', item.vehicle_id).execute())
