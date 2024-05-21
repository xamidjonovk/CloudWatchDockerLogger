import argparse
import logging
import time
from cloudwatch_logger import CloudWatchLogger
from docker_runner import DockerRunner

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Run a Docker container and stream logs to AWS CloudWatch")
    parser.add_argument('--docker-image', required=True, help='Name of the Docker image')
    parser.add_argument('--bash-command', required=True, help='Bash command to run inside the Docker container')
    parser.add_argument('--aws-cloudwatch-group', required=True, help='AWS CloudWatch log group name')
    parser.add_argument('--aws-cloudwatch-stream', required=True, help='AWS CloudWatch log stream name')
    parser.add_argument('--aws-access-key-id', required=True, help='AWS access key ID')
    parser.add_argument('--aws-secret-access-key', required=True, help='AWS secret access key')
    parser.add_argument('--aws-region', required=True, help='AWS region name')

    args = parser.parse_args()

    # Initialize AWS CloudWatch client with provided credentials
    cloudwatch_logger = CloudWatchLogger(
        access_key_id=args.aws_access_key_id,
        secret_access_key=args.aws_secret_access_key,
        region=args.aws_region
    )

    # Ensure log group and stream exist
    cloudwatch_logger.create_log_group(args.aws_cloudwatch_group)
    cloudwatch_logger.create_log_stream(args.aws_cloudwatch_group, args.aws_cloudwatch_stream)

    # Run the Docker command and stream logs
    docker_runner = DockerRunner()
    try:
        container_id = docker_runner.run_docker_command(args.docker_image, args.bash_command)
    except Exception as e:
        logger.error(f"Failed to run the Docker container. Exiting. Error: {e}")
        return

    try:
        docker_runner.stream_docker_logs_to_cloudwatch(container_id, cloudwatch_logger, args.aws_cloudwatch_group,
                                                       args.aws_cloudwatch_stream)
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
    finally:
        docker_runner.stop_and_remove_container(container_id)


if __name__ == "__main__":
    main()
