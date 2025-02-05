from pyzeebe import Job

from database.database import supabase
from database.validators import InvoiceValidator

from . import router

TASK_TYPE = 'SaveInvoice'  # name of the task


@router.task(task_type=TASK_TYPE)
async def save_invoice(job: Job):
    """
    Inserts invoice data into the database.
    """

    print(f'Task \'{TASK_TYPE}\' is started for instance {job.process_instance_key}')

    data = job.variables
    invoice_data = data['invoice']

    invoice = InvoiceValidator(**invoice_data)

    response = supabase.table('invoices').insert(
        invoice.model_dump(exclude=['invoice_id'])).execute()

    invoice.invoice_id = response.data[0]['invoice_id']

    return {'invoice': invoice.model_dump()}
