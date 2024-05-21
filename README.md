# DockerCloudWatchLogger

DockerCloudWatchLogger is a Python project designed to stream logs from Docker containers directly to AWS CloudWatch. This tool helps in managing, monitoring, and analyzing the logs from your Docker applications by leveraging AWS CloudWatch.

## About

This project provides the following functionalities:
- Creation and management of AWS CloudWatch log groups and streams.
- Running Docker containers with specified commands.
- Streaming logs from Docker containers to AWS CloudWatch in real-time.
- Continuously monitoring Docker container logs and updating CloudWatch logs incrementally.

## Installation

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.6 or higher
- Docker
- AWS CLI (configured with appropriate access)

### Steps

1. **Clone the Repository**

   Clone the repository to your local machine:

   ```sh
   git clone https://github.com/yourusername/DockerCloudWatchLogger.git
   cd DockerCloudWatchLogger

2. **Create and Activate a Virtual Environment (Optional but recommended)**
python3 -m venv venv
source venv/bin/activate

3. **Clone the Repository**
    ```sh
    pip install -r requirements.txt

### Usage
    ```sh
    python main.py --docker-image python --bash-command $'pip install pip -U && pip install tqdm && python3 -c "import time\ncounter = 0\nwhile True:\n\tprint(counter)\n\tcounter += 1\n\ttime.sleep(0.1)"' --aws-cloudwatch-group test-task-group-1 --aws-cloudwatch-stream test-task-stream-1 --aws-access-key-id YOUR_AWS_ACCESS_KEY_ID --aws-secret-access-key YOUR_AWS_SECRET_ACCESS_KEY --aws-region YOUR_AWS_REGION

**Arguments**
--docker-image: The name of the Docker image to run.
--bash-command: The command to execute inside the Docker container.
--aws-cloudwatch-group: The AWS CloudWatch log group name.
--aws-cloudwatch-stream: The AWS CloudWatch log stream name.
--aws-access-key-id: Your AWS access key ID.
--aws-secret-access-key: Your AWS secret access key.
--aws-region: The AWS region (e.g., us-west-2).

