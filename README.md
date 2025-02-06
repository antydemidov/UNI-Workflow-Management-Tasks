# Camunda Worker Application

This application implements a Camunda worker that handles various tasks in a workflow process. It's built with Python and uses Docker for containerization.

## Project Structure

The worker implementation can be found in the following locations:
- `camunda/` - Core worker implementation
  - `tasks/` - Individual task handlers
  - `client.py` - Zeebe client configuration
  - `constants.py` - Configuration constants
- `database/` - Database integration

## Prerequisites

- Docker and Docker Compose
- Python 3.11 or higher (for local development)
- Access to Camunda Platform 8 (Zeebe)

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### Zeebe Connection

The application connects to Zeebe API. This can be configured in:
- `docker-compose.yml` for Docker deployment
- `camunda/constants.py` for local development

## Starting the Application

### Using Docker (Recommended)

1. Make sure Docker is running
2. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

The worker will be available at port 8082.

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the worker:
   ```bash
   python run_camunda.py
   ```

## Starting a Process

To start a new process instance:

```bash
python run_camunda_process.py
```

## Monitoring

The worker logs task registrations and executions to the console. You can monitor the process execution through:
- Console logs
- Camunda Operate interface
- Docker logs (when running in container)

## Troubleshooting

1. If the worker can't connect to Zeebe:
   - Verify the ZEEBE_ADDRESS in both docker-compose.yml and constants.py
   - Check if the Zeebe broker is accessible

2. If database operations fail:
   - Verify your Supabase credentials in the .env file
   - Check if the Supabase service is accessible

3. For Docker-related issues:
   - Ensure all required environment variables are set
   - Check Docker logs: `docker-compose logs camunda-worker`