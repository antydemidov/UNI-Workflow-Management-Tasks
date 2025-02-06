from pyzeebe import Job

from database.validators import ApplicationValidator, InsuranceValidator
from database.database import supabase

from . import router

TASK_TYPE = 'SaveInsurance'  # name of the task


@router.task(task_type=TASK_TYPE)
async def save_insurance(job: Job):
    """
    Prepares the insurance certificate.
    """

    instance_id = job.process_instance_key

    print(f'Task \'{TASK_TYPE}\' is started for instance {instance_id}')

    data = job.variables
    insurance_certificate = data['insurance_certificate']
    application = ApplicationValidator.model_validate(data['application'])

    insurance = InsuranceValidator(
        application_id=application.application_id,
        insurance_type=application.insurance_type,
        policy_number=insurance_certificate['insurance_details']['policy_number'],
        date_start=application.rental_start_date,
        date_end=application.rental_end_date,
        amount=data['insurance_cost'],
        maximum_coverage=insurance_certificate['insurance_details']['max_coverage'],
        deductible=insurance_certificate['insurance_details']['deductible'],
        status='Not approved'
    )

    response = supabase.table('insurances').insert(
        insurance.model_dump(exclude=['insurance_id'])).execute()

    insurance.insurance_id = response.data[0]['insurance_id']

    return {'insurance': insurance.model_dump()}
