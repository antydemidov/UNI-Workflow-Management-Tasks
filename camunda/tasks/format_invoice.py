from pyzeebe import Job

from database.validators import ApplicationValidator, InvoiceValidator

from . import router

TASK_TYPE = 'FormatInvoice'  # name of the task


@router.task(task_type=TASK_TYPE)
async def format_invoice(job: Job):
    """
    Formats the invoice.
    """

    instance_id = job.process_instance_key

    print(f'Task \'{TASK_TYPE}\' is started for instance {instance_id}')

    data = job.variables
    application_object = ApplicationValidator.model_validate(data['application'])

    invoice = InvoiceValidator(
        application_id=application_object.application_id,
        date_start=application_object.rental_start_date,
        date_end=application_object.rental_end_date,
        total_amount=data['insurance_cost'],
        payment_method='Debit',
        iban='DE89370400440532013000'
    )

    return {'invoice': invoice.model_dump(exclude=['invoice_id'])}
