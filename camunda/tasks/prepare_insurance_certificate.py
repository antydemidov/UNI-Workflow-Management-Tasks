from datetime import datetime
import uuid
from pyzeebe import Job

from database.validators import ApplicationValidator

from . import router

TASK_TYPE = 'PrepareInsuranceCertificate'  # name of the task


def calculate_insurance_details(application: ApplicationValidator):

    def categorize_vehicle(brand: str):
        luxury_keywords = ['Mercedes', 'BMW', 'Audi', 'Porsche']
        sports_keywords = ['Mustang', 'Corvette', 'Ferrari', 'Lamborghini',
                           'Camaro', 'Challenger', 'GT-R', 'Supra']

        if any(keyword.lower() == brand.lower() for keyword in luxury_keywords):
            return 'luxury'

        if any(keyword.lower() == brand.lower() for keyword in sports_keywords):
            return 'sports'

        return 'standard'

    def estimate_vehicle_value(brand: str, vehicle_age: int):

        base_values = {
            'luxury': 80000,
            'sports': 60000,
            'standard': 20000
        }

        depreciation_factor = max(0.3, 1 - (vehicle_age * 0.15))

        vehicle_category = categorize_vehicle(brand)
        base_value = base_values.get(vehicle_category, 20000)

        estimated_value = base_value * depreciation_factor
        return round(estimated_value, 2)

    def calculate_base_coverage(vehicle_value, insurance_type: str, request_type: str):

        base_coverage = {
            'liability_insurance': {
                # Minimum €500k or 50% of vehicle value
                'individual': max(500000, vehicle_value * 0.5),
                # Minimum €300k or 40% of vehicle value
                'fleet': max(300000, vehicle_value * 0.4)
            },
            'partial_coverage': {
                # Minimum €20k or 40% of vehicle value
                'individual': max(20000, vehicle_value * 0.4),
                # Minimum €15k or 30% of vehicle value
                'fleet': max(15000, vehicle_value * 0.3)
            },
            'comprehensive_coverage': {
                # Minimum €40k or 60% of vehicle value
                'individual': max(40000, vehicle_value * 0.6),
                # Minimum €30k or 50% of vehicle value
                'fleet': max(30000, vehicle_value * 0.5)
            }
        }

        coverage = base_coverage[insurance_type][request_type]
        return round(coverage, 2)

    def calculate_coverage_and_deductible(insurance_type: str, brand: str, total_risk,
                                          rental_days: int, vehicle_age: int, request_type: str):

        vehicle_category = categorize_vehicle(brand)

        vehicle_value = estimate_vehicle_value(brand, vehicle_age)

        base_coverage = calculate_base_coverage(
            vehicle_value, insurance_type, request_type)

        # Base deductible values
        base_deductible = {
            'liability_insurance': 0,
            'partial_coverage': 500,
            'comprehensive_coverage': 1000
        }

        risk_factor = max(0.5, 1 - total_risk)
        max_coverage = base_coverage * risk_factor
        deductible = base_deductible[insurance_type] * (1 + total_risk)

        if vehicle_category == 'luxury':
            max_coverage *= 0.8  # Reduce coverage for luxury vehicles
            deductible *= 1.2    # Increase deductible for luxury vehicles
        elif vehicle_category == 'sports':
            max_coverage *= 0.7  # Further reduction for sports vehicles
            deductible *= 1.3    # Higher deductible for sports vehicles

        # Reduce coverage for longer rentals
        rental_factor = min(1.0, 1.0 - (rental_days / 30))
        max_coverage *= rental_factor
        # Increase deductible for longer rentals
        deductible *= (1 + rental_days / 30)

        return round(max_coverage, 2), round(deductible, 2)

    vehicles = application.available_cars
    total_max_coverage = 0
    total_deductible = 0

    for vehicle in vehicles:

        max_coverage, deductible = calculate_coverage_and_deductible(
            insurance_type=application.insurance_type,
            brand=vehicle.vehicle_manufacturer,
            total_risk=vehicle.vehicle_risk,
            rental_days=application.days_of_rental,
            vehicle_age=datetime.now().year - vehicle.construction_year,
            request_type=application.request_type
        )
        total_max_coverage += max_coverage
        total_deductible += deductible

    results = {
        'max_coverage': round(total_max_coverage, 2),
        'deductible': round(total_deductible, 2)
    }

    return results


@router.task(task_type=TASK_TYPE)
async def prepare_insurance_certificate(job: Job):
    """
    Prepares the insurance certificate.
    """

    instance_id = job.process_instance_key

    print(f'Task \'{TASK_TYPE}\' is started for instance {instance_id}')

    data = job.variables
    application = ApplicationValidator.model_validate(data['application'])

    insurance_details = calculate_insurance_details(application)

    certificate = {
        'rental_company': {
            'name': 'BVIS Mobility Solutions Ltd.',
            'address': 'Zentralpl. 2, 56068 Koblenz',
            'contact': 'Phone: (123) 456-7890, Email: 123@example.com'
        },
        'customer': {
            'first_name': application.first_name,
            'last_name': application.last_name,
            'phone_number': application.phone_number,
            'email': application.email_address
        },
        'vehicles': [
            {
                'vehicle_manufacturer': vehicle.vehicle_manufacturer,
                'vehicle_model': vehicle.vehicle_model,
                'vehicle_type': vehicle.vehicle_type,
                'construction_year': vehicle.construction_year,
                'fuel_type': vehicle.fuel_type
            } for vehicle in application.available_cars
        ],
        'insurance_details': {
            'insurance_type': application.insurance_type,
            'date_start': application.rental_start_date,
            'date_end': application.rental_end_date,
            'rental_agreement_number': application.pid,
            'policy_number': str(uuid.uuid4()),
            'max_coverage': insurance_details['max_coverage'],
            'deductible': insurance_details['deductible']
        },
        'insurer': {
            'name': 'Capitol for People Inc.',
            'address': 'Zentralpl. 2, 56068 Koblenz',
            'contact': 'Phone: (123) 456-7890, Email: 123@example.com'
        }
    }
    return {'insurance_certificate': certificate}
