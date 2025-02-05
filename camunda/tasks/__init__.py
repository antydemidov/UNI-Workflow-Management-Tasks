from pyzeebe import ZeebeTaskRouter


router = ZeebeTaskRouter()

# # Imports of all the tasks
from . import (
    activate_insurance,
    format_invoice,
    mark_insurance_expired,
    prepare_insurance_certificate,
    save_application,
    save_invoice,
    save_eligibility,
    save_insurance,
    validation_application,
    messages
)
