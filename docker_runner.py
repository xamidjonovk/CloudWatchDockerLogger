import docker
import logging
import time

logger = logging.getLogger(__name__)


class DockerRunner:
    def __init__(self):
        try:
            self.client = docker.from_env()
            self.client.ping()  # Check if the Docker client can communicate with the Docker daemon
        except docker.errors.DockerException as e:
            logger.error(f"Error connecting to Docker: {e}")
            raise

    def run_docker_command(self, image_name, bash_command):
        """Run a Docker container with the specified image and command."""
        try:
            logger.info(f"Running docker image {image_name} with command: {bash_command}")
            container = self.client.containers.run(
                image_name,
                command=["/bin/sh", "-c", bash_command],
                detach=True,
                stdout=True,
                stderr=True
            )
            logger.info(f"Docker container started with ID: {container.id}")
            return container
        except Exception as e:
            logger.error(f"Exception occurred: {e}")
            raise

    @staticmethod
    def stream_docker_logs_to_cloudwatch(container, cloudwatch_logger, log_group_name, log_stream_name):
        """Stream Docker container logs to CloudWatch."""
        import time

        log_events = []
        try:
            for line in container.logs(stream=True):
                timestamp = int(time.time() * 1000)
                message = line.decode('utf-8').strip()
                if message:
                    log_events.append({
                        'timestamp': timestamp,
                        'message': message
                    })

                if log_events:
                    cloudwatch_logger.send_logs_to_cloudwatch(log_group_name, log_stream_name, log_events)
                    log_events = []

                time.sleep(1)  # Adjust the sleep interval for real-time logging

        except Exception as e:
            logger.error(f"Exception occurred while streaming logs: {e}")

    @staticmethod
    def stop_and_remove_container(container):
        """Stop and remove the Docker container."""
        container.stop()
        container.remove()
        logger.info(f"Stopped and removed Docker container with ID: {container.id}")
