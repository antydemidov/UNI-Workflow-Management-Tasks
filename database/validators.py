"""Pydantic validation of data objects."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class InvoiceValidator(BaseModel):
    model_config = ConfigDict(extra='ignore')

    invoice_id: int
    application_id: int
    date_start: str
    date_end: str
    currency: str = 'EUR'
    total_amount: float = 0.0
    payment_method: str | None = None
    iban: str | None = None


class InsuranceValidator(BaseModel):
    model_config = ConfigDict(extra='ignore')

    insurance_id: int
    application_id: int
    insurance_type: str
    policy_number: str
    date_start: str
    date_end: str
    amount: float = 0.0
    currency: str = 'EUR'
    maximum_coverage: float = 0.0
    deductible: float = 0.0
    status: str = 'Not approved'


class EligibilityInternalValidator(BaseModel):
    model_config = ConfigDict(extra='ignore')
    vehicle_id: int
    final_score: float = 0.0


class EligibilityValidator(BaseModel):
    driver_risk: float = 0.0
    vehicle_risk: list[EligibilityInternalValidator]
    total_risk: float = 0.0
    eligibility: str | None = None


class VehicleValidator(BaseModel):

    vehicle_id: int
    vehicle_manufacturer: str
    vehicle_model: str
    vehicle_type: str
    construction_year: int
    fuel_type: str = 'petrol'

    application_id: int | None = None
    vehicle_risk: float = 0.5
    co2_emission: int = 0
    expected_mileage: int = 0

    # MISSING FIELDS
    accident_history: str = 'clean'
    maintenance_status: str = 'valid'


class ApplicationValidator(BaseModel):

    application_id: int | None = None
    pid: int
    first_name: str
    last_name: str
    age: int
    driver_license_valid: bool
    street_number: int = 0
    phone_number: int
    email_address: str
    child_seat: bool = False
    additional_services: str = 'No'
    extra_insurance: bool = False
    lashing_strap: bool = False
    gps: bool = False
    customer_type: str = 'individual'
    data_privacy_accepted: Any = None
    rental_start_date: str
    rental_end_date: str
    days_of_rental: int = 1
    insurance_type: str = 'liability_insurance'
    available_cars: list[VehicleValidator]
    request_type: str | None = None
    driver_risk: float = 0.0

    # MISSING FIELDS
    number_of_accidents: int = 0
    accident_severity: int = 0
    accident_recency: int = 0
