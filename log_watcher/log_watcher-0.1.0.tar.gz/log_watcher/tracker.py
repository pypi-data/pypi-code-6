from log_watcher import settings
from boto.ec2 import cloudwatch

from datetime import timedelta, datetime

import logging

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------

class Tracker(object):
    def __init__(self, name, period=60):
        self.name = name
        self.period = period
        self.current_count = 0
        self.last_date = datetime.now()

    def track(self, count=0):
        date = datetime.now()
        self.current_count += count

        if date - timedelta(seconds=self.period) > self.last_date:
            logger.info('Push events to cloudwatch (%s)' % self.current_count)
            self.send_data()
            self.current_count = 0
            self.last_date = date

    def send_data(self):
        raise NotImplementedError

# -----

class CloudwatchTracker(Tracker):
    NAMESPACE = 'log_watcher'

    def get_connection(self):
        # Cache connection
        if not hasattr(self, 'conn'):
            self.conn = cloudwatch.connect_to_region(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION)

            # Create or update alarm
            self.conn.put_metric_alarm(cloudwatch.alarm.MetricAlarm(
                name='%s_%s_critical' % (self.NAMESPACE, self.name),
                metric=self.name,
                namespace=self.NAMESPACE,
                statistic='Maximum',
                comparison='>',
                threshold=0,
                period=60,
                evaluation_periods=1,
                unit='Count',
                alarm_actions=settings.CLOUDWATCH_NOTIFICATION_ARNS,
                insufficient_data_actions=settings.CLOUDWATCH_NOTIFICATION_ARNS,
                ok_actions=settings.CLOUDWATCH_NOTIFICATION_ARNS))
        return self.conn

    def send_data(self):
        # Send data to cloudwatch
        conn = self.get_connection()
        conn.put_metric_data(
            namespace=self.NAMESPACE,
            name=self.name,
            value=self.current_count,
            unit='Count')
