import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class CloudWatchLogger:
    def __init__(self, access_key_id, secret_access_key, region):
        self.client = boto3.client(
            'logs',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region
        )

    def create_log_group(self, log_group_name):
        """Create a CloudWatch log group if it doesn't exist."""
        try:
            self.client.create_log_group(logGroupName=log_group_name)
            logger.info(f"Created log group: {log_group_name}")
        except self.client.exceptions.ResourceAlreadyExistsException:
            logger.info(f"Log group {log_group_name} already exists")

    def create_log_stream(self, log_group_name, log_stream_name):
        """Create a CloudWatch log stream if it doesn't exist."""
        try:
            self.client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
            logger.info(f"Created log stream: {log_stream_name} in group: {log_group_name}")
        except self.client.exceptions.ResourceAlreadyExistsException:
            logger.info(f"Log stream {log_stream_name} already exists in group: {log_group_name}")

    def get_log_sequence_token(self, log_group_name, log_stream_name):
        """Retrieve the sequence token for the log stream."""
        response = self.client.describe_log_streams(
            logGroupName=log_group_name,
            logStreamNamePrefix=log_stream_name
        )
        log_streams = response['logStreams']
        if log_streams and 'uploadSequenceToken' in log_streams[0]:
            return log_streams[0]['uploadSequenceToken']
        return None

    def send_logs_to_cloudwatch(self, log_group_name, log_stream_name, log_events):
        """Send log events to CloudWatch."""
        sequence_token = self.get_log_sequence_token(log_group_name, log_stream_name)
        try:
            if sequence_token:
                self.client.put_log_events(
                    logGroupName=log_group_name,
                    logStreamName=log_stream_name,
                    logEvents=log_events,
                    sequenceToken=sequence_token
                )
            else:
                self.client.put_log_events(
                    logGroupName=log_group_name,
                    logStreamName=log_stream_name,
                    logEvents=log_events
                )
        except ClientError as e:
            logger.error(f"Failed to send logs to CloudWatch: {e}")
