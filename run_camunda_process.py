import asyncio

from pyzeebe import ZeebeClient, create_insecure_channel

from camunda.constants import PROCESS_ID, ZEEBE_ADDRESS


async def start_work_process(client: ZeebeClient):
    # variables = {}
    await client.run_process(PROCESS_ID)


async def main():
    channel = create_insecure_channel(grpc_address=ZEEBE_ADDRESS)
    zeebe_client = ZeebeClient(channel)
    await start_work_process(zeebe_client)


if __name__ == '__main__':
    asyncio.run(main())
