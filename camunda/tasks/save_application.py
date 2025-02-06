import random

from pyzeebe import Job

from database.database import supabase
from database.validators import ApplicationValidator

from . import router

TASK_TYPE = 'SaveApplication'  # name of the task


def get_co2_emissions(fuel_type: str):
    if not fuel_type or fuel_type.lower() == 'electric':
        return 0
    if fuel_type.lower() == 'diesel':
        return random.randint(120, 200)
    return random.randint(95, 165)


@router.task(task_type=TASK_TYPE)
async def save_application(job: Job):
    """
    Computes and inserts data of the application into the database.
    """

    instance_id = job.process_instance_key

    print(f'Task \'{TASK_TYPE}\' is started for instance {instance_id}')

    data = job.variables
    application_data: dict = data['application']
    application = ApplicationValidator(**application_data)

    if len(application.available_cars) == 1:
        application.request_type = 'individual'
    else:
        application.request_type = 'fleet'

    application.number_of_accidents = random.randint(0, 10)
    application.accident_recency = random.randint(1, 5)
    application.accident_severity = random.randint(1, 5)

    application_data = application.model_dump(exclude=['application_id', 'available_cars'])
    try:
        response = (
            supabase.table('applications')
            .insert(application_data)
            .execute()
        )
    except Exception:
        response = (
            supabase.table('applications')
            .update(application_data)
            .eq('pid', application.pid)
            .execute()
        )
    application_id = response.data[0]['application_id']
    application.application_id = application_id

    vehicles = application.available_cars
    (supabase.table('vehicles')
     .delete()
     .eq('application_id', application_id)
     .execute())
    for vehicle in vehicles:
        vehicle.application_id = application_id
        vehicle.co2_emission = get_co2_emissions(vehicle.fuel_type)
        vehicle.expected_mileage = random.randint(10000, 100000)
        vehicle_data = vehicle.model_dump(exclude=['vehicle_id'])
        response = (
            supabase.table('vehicles')
            .insert(vehicle_data)
            .execute()
        )
        vehicle.vehicle_id = response.data[0]['vehicle_id']

    output = application.model_dump()

    print(f'Task \'{TASK_TYPE}\' is finished for instance {instance_id}')

    return {
        'application': output,
        'application_id': application_id
    }
