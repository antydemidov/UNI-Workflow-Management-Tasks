from pyzeebe import ZeebeTaskRouter


router = ZeebeTaskRouter()

# # Imports of all the tasks
from . import (
    activate_insurance,
    compute_claim_application,
    format_invoice,
    mark_insurance_expired,
    prepare_insurance_certificate,
    save_application,
    save_eligibility,
    save_insurance,
    save_invoice,
    validation_application,
    messages
)
