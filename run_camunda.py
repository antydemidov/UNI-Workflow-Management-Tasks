import asyncio

from camunda.client import get_worker


async def main():
    """Starts the Zeebe worker and handles graceful shutdown."""
    print('Starting Zeebe worker...')

    try:
        zeebe_worker = get_worker()
        await zeebe_worker.work()
    except asyncio.CancelledError:
        print('Worker cancelled. Shutting down...')
    finally:
        print('Zeebe worker stopped.')
        await zeebe_worker.stop()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Program terminated by user')
