import random

from pyzeebe import Job

from database.database import supabase
from database.validators import ApplicationValidator

from . import router

TASK_TYPE = 'SaveApplication'  # name of the task


def get_accident_severity():
    return random.randint(1, 5)

def get_accident_recency():
    return random.randint(1, 5)

def get_co2_emissions(fuel_type: str):
    if not fuel_type or fuel_type.lower() == 'electric':
        return 0
    if fuel_type.lower() == 'diesel':
        return random.randint(120, 200)
    return random.randint(95, 165)

def get_expected_mileage():
    return random.randint(10000, 100000)


@router.task(task_type=TASK_TYPE)
async def save_application(job: Job):
    """
    Computes and inserts data of the application into the database.
    """

    instance_id = job.process_instance_key

    print(f'Task \'{TASK_TYPE}\' is started for instance {instance_id}')

    data = job.variables
    application_data: dict = data['application']
    application_object = ApplicationValidator(**application_data)

    if len(application_object.available_cars) == 1:
        application_object.request_type = 'individual'
    else:
        application_object.request_type = 'fleet'

    application_object.number_of_accidents = random.randint(0, 10)
    application_object.accident_recency = get_accident_recency()
    application_object.accident_severity = get_accident_severity()

    application_data = application_object.model_dump(exclude=['application_id', 'available_cars'])
    response = supabase.table('applications').insert(application_data).execute()
    application_id = response.data[0]['application_id']
    application_object.application_id = application_id

    vehicles = application_object.available_cars
    for vehicle in vehicles:
        vehicle.application_id = application_id
        vehicle.co2_emission = get_co2_emissions(vehicle.fuel_type)
        vehicle.expected_mileage = get_expected_mileage()
        vehicle_data = vehicle.model_dump(exclude=['vehicle_id'])
        response = supabase.table('vehicles').insert(vehicle_data).execute()

    output = application_object.model_dump()

    print(f'Task \'{TASK_TYPE}\' is finished for instance {instance_id}')

    return {
        'application': output,
        'application_id': application_id
    }
