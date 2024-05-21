import subprocess
import logging
import time
logger = logging.getLogger(__name__)


class DockerRunner:
    @staticmethod
    def run_docker_command(image_name, bash_command):
        """Run a Docker container with the specified image and command."""
        try:
            logger.info(f"Running docker image {image_name} with command: {bash_command}")
            result = subprocess.run(['docker', 'run', '-d', image_name, '/bin/sh', '-c', bash_command],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                logger.error(f"Error running Docker container: {result.stderr}")
                raise Exception(f"Error running Docker container: {result.stderr}")
            container_id = result.stdout.strip()
            logger.info(f"Docker container started with ID: {container_id}")
            return container_id
        except Exception as e:
            logger.error(f"Exception occurred: {e}")
            raise

    @staticmethod
    def stream_docker_logs_to_cloudwatch(container_id, cloudwatch_logger, log_group_name, log_stream_name):
        """Stream Docker container logs to CloudWatch."""
        log_events = []
        try:
            while True:
                result = subprocess.run(['docker', 'logs', '--tail', '10', container_id],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode != 0:
                    break

                lines = result.stdout.strip().split('\n')
                timestamp = int(time.time() * 1000)
                for line in lines:
                    if line:  # Filter out empty lines
                        log_events.append({
                            'timestamp': timestamp,
                            'message': line
                        })

                if log_events:
                    cloudwatch_logger.send_logs_to_cloudwatch(log_group_name, log_stream_name, log_events)
                    log_events = []

                time.sleep(2)

        except Exception as e:
            logger.error(f"Exception occurred while streaming logs: {e}")

    @staticmethod
    def stop_and_remove_container(container_id):
        """Stop and remove the Docker container."""
        subprocess.run(['docker', 'stop', container_id], check=True)
        subprocess.run(['docker', 'rm', container_id], check=True)
        logger.info(f"Stopped and removed Docker container with ID: {container_id}")
