from pyzeebe import create_insecure_channel, ZeebeClient, Job

from camunda.constants import ZEEBE_ADDRESS_BVIS

from . import router


def get_client_bvis():
    channel = create_insecure_channel(grpc_address=ZEEBE_ADDRESS_BVIS)
    return ZeebeClient(channel)


@router.task(task_type='send_feedback')
async def send_feedback(job: Job):
    pid = job.variables['bvis_message']['pid']
    no_issues_with_terms = job.variables['message_settings']
    issues_with_terms = not no_issues_with_terms

    client = get_client_bvis()
    await client.publish_message(
        name='receive_capitol_feedback',
        correlation_key=str(pid),
        variables={
            'application_id_capitol': pid,
            'issues_with_terms': issues_with_terms,
            'no_issues_with_terms': no_issues_with_terms
        }
    )


@router.task(task_type='send_eligibility_assessment')
async def send_eligibility_assessment(job: Job):
    pid = job.variables['application']['pid']
    not_blacklisted = job.variables['message_settings']
    blacklisted = not not_blacklisted
    client = get_client_bvis()
    await client.publish_message(
        name='receive_eligibility',
        correlation_key=str(pid),
        variables={
            'not_blacklisted': not_blacklisted,
            'blacklisted': blacklisted
        },
    )


@router.task(task_type='receive_plan_confirmation')
async def receive_plan_confirmation(job: Job):
    plan_confirmed = True
    plan_not_confirmed = not plan_confirmed
    insurance_cost_from_capitol = job.variables['insurance_cost']
    pid = job.variables['application']['pid']
    client = get_client_bvis()
    await client.publish_message(
        name='receive_plan_confirmation',
        correlation_key=str(pid),
        variables={
            'plan_confirmed': plan_confirmed,
            'plan_not_confirmed': plan_not_confirmed,
            'insurance_cost_from_capitol': insurance_cost_from_capitol
        }
    )


@router.task(task_type='receive_insurance_confirmation')
async def receive_insurance_confirmation(job: Job):
    insurance_confirmed = job.variables['message_settings']
    pid = job.variables['application']['pid']
    client = get_client_bvis()
    await client.publish_message(
        name='receive_insurance_confirmation',
        correlation_key=str(pid),
        variables={
            'insurance_confirmed': insurance_confirmed
        }
    )


@router.task(task_type='receive_capitol_response')
async def receive_capitol_response(job: Job):
    fraud_and_liability_assessment = job.variables['fraud_and_liability_assessment']
    insurance_cover_exists = fraud_and_liability_assessment['result']['valid']
    insurance_cover_does_not_exist = not insurance_cover_exists
    capitol_pays_amount = bool(
        fraud_and_liability_assessment['result']['payout'])
    capitol_does_not_pay_amount = not capitol_pays_amount
    pid = job.variables['application']['pid']
    client = get_client_bvis()
    await client.publish_message(
        name='receive_capitol_response',
        correlation_key=str(pid),
        variables={
            'insurance_cover_does_not_exist': insurance_cover_does_not_exist,
            'insurance_cover_exists': insurance_cover_exists,
            'capitol_does_not_pay_amount': capitol_does_not_pay_amount,
            'capitol_pays_amount': capitol_pays_amount,
            'payout': fraud_and_liability_assessment['result']['payout']
        }
    )


@router.task(task_type='receive_message_insurance_case_solved')
async def receive_message_insurance_case_solved(job: Job):
    insurance_case_solved = True
    pid = job.variables['application']['pid']
    client = get_client_bvis()
    await client.publish_message(
        name='receive_message_insurance_case_solved',
        correlation_key=str(pid),
        variables={
            'insurance_case_solved': insurance_case_solved
        }
    )
