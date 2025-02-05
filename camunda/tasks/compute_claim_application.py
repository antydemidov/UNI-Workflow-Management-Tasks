import random
from pyzeebe import Job

from . import router

TASK_TYPE = 'ComputeClaimApplication'  # name of the task


def get_claim_type():
    claim_types = [
        'Animal Collision',  # Damage caused by hitting an animal, such as a deer
        'Brake Failure Accident',  # Accidents caused by malfunctioning brakes
        'Collision Accident',  # Two or more vehicles colliding
        'Fire or Explosion',  # Damage due to fire, engine explosion, or external causes
        'Flood or Water Damage',  # Vehicle damage caused by floods or water-related incidents
        'Hail or Storm Damage',  # Damage due to hailstorms, falling branches, or severe storms
        'Hit-and-Run',  # Unidentified driver causes damage and leaves the scene
        'Mechanical Failure Accident',  # Caused by brake failure, tire blowouts, or other mechanical issues
        'Multi-Vehicle Pileup',  # Accidents involving multiple vehicles, often on highways
        'Parked Car Accident',  # Damage to a parked vehicle from another vehicle or object
        'Pothole Damage',  # Damage caused by hitting deep potholes
        'Rear-End Collision',  # One vehicle hitting another from behind
        'Road Debris Damage',  # Accidents or damage caused by debris on the road
        'Rollover Accident',  # Vehicle flipping over due to impact or sharp turns
        'Side-Impact (T-Bone) Collision',  # A vehicle being hit on its side
        'Single-Vehicle Accident',  # Damage from hitting an object, rollover, etc.
        'Theft or Vandalism',  # Vehicle stolen or damaged due to break-ins or malicious intent
        'Tire Blowout Accident',  # Loss of control due to a sudden tire burst
        'Weather-Related Accident',  # Slippery roads, reduced visibility, hydroplaning, etc.
    ]

    return random.choice(claim_types)


@router.task(task_type=TASK_TYPE)
async def save_invoice(job: Job):
    """
    Inserts invoice data into the database.
    """

    print(f'Task \'{TASK_TYPE}\' is started for instance {job.process_instance_key}')

    data = job.variables
    claim_data = data['bvis_message']

    claim_data['type'] = get_claim_type()

    return {'claim': claim_data}
