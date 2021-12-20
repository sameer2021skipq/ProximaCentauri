from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as actions_,
    aws_dynamodb as db,
    aws_s3 as s3,
    aws_stepfunctions_tasks as tasks_,
    aws_s3_deployment as s3_deploy
    # aws_sqs as sqs,
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from resources import constants as constants
#from resources import cloudwatch_putMetric as cw


class SameerRepoStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        lambda_role = self.create_lambda_role()
        
        try:
            constants.BUCKET_NAME = "sameerbucketnew"
            sameerBucket = s3.Bucket(self, id = "sameerbuckets3", bucket_name = constants.BUCKET_NAME)
            firstDeploy = s3_deploy.BucketDeployment(self, "FirstDeploy",sources=[s3_deploy.Source.asset("./files")], destination_bucket = sameerBucket)
            # constants.BUCKET_NAME_MODIFIED = constants.BUCKET_NAME
            
        except:
            print("Bucket Already Exists")
            
        try:
            self.create_table("newTable", "SameerTableTwo")
        except:
            print("Table Already Created")
       
            
        
        #dynamodb_lambda = self.create_lambda("DyamoDBLambda", "./resources", "dynamoDB.lambda_handler", lambda_role)
        
        s3_lambda = self.create_lambda("S3Lambda", "./resources", "s3lambda.lambda_handler", lambda_role)
        lambda_target_two = targets_.LambdaFunction(handler=s3_lambda)
        
        #HLambda = self.create_lambda("HelloLambda", "./resources", "lambda.lambda_handler")
        HLambda = self.create_lambda("WebHealthCheck", "./resources", "webhealth_lambda.lambda_handler", lambda_role)
        dynamodb_lambda = self.create_lambda("DyamoDBLambda", "./resources", "dynamoDB.lambda_handler", lambda_role)
       
        
        
       #check below that is lambda_target_one working without targest =
        
        lambda_schedule = events_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_target = targets_.LambdaFunction(handler=HLambda)
        lambda_target_one = targets_.LambdaFunction(handler=dynamodb_lambda)
       
        
        # rule = events_.Rule(self, "WebHealth_Check",description = "Periodic Lambda", enabled = True, schedule = lambda_schedule, targets = 
        # [lambda_target#, lambda_target_one
        # ])
        
        rule = events_.Rule(self, "WebHealth_Check",description = "Periodic Lambda", enabled = True, schedule = lambda_schedule, targets = 
        [lambda_target, lambda_target_one
        ])
        
        
        
        
        
        
        topic = sns.Topic(self, "SameerWebHealthTopic")
        topic.add_subscription(subscriptions_.EmailSubscription('sameer.jehan.s@skipq.org'))
        # print(topic)
        topic.add_subscription(subscriptions_.LambdaSubscription(fn=dynamodb_lambda))
        

        
      #  dimensions = {"URL1" : constants.URL_TO_MONITOR_ONE, "URL2":constants.URL_TO_MONITOR_TWO, "URL3":constants.URL_TO_MONITOR_THREE, "URL4":constants.URL_TO_MONITOR_FOUR}
      
        
        
        #First we set the metric on metric name of which is url availability and url latency
      #  dimensions = {"URL" : constants.URL_TO_MONITOR}
      
      #####FIRST URL############
        
        dimensions = {"URL" : constants.URL_TO_MONITOR}
        # dimensions_2 = {"URL" : constants.URL_TO_MONITOR_TWO}
        # dimensions_3 = {"URL" : constants.URL_TO_MONITOR_THREE}
        # dimensions_4 = {"URL" : constants.URL_TO_MONITOR_FOUR}
      
        
        ##comment period below
        availability_metric = cloudwatch_.Metric(
            namespace=constants.URL_MONITOR_NAMESPACE,
            metric_name=constants.URL_MONITOR_AVAILABILITY,
            dimensions_map=dimensions, 
          #  period = cdk.Duration.minutes(1), 
            label = "Availability Metric"
        )
        
        availability_alarm = cloudwatch_.Alarm(
            self, 
            id = 'AvailabilityAlarm', 
            metric = availability_metric, 
            comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
            datapoints_to_alarm = 1,
            evaluation_periods = 1,
            threshold = 1 #if site goes down than 1 so raise alarm
            )
            
        dimensions = {"URL" : constants.URL_TO_MONITOR}
        
        latency_metric = cloudwatch_.Metric(
            namespace=constants.URL_MONITOR_NAMESPACE,
            metric_name=constants.URL_MONITOR_LATENCY,
            dimensions_map=dimensions,
      #     period = cdk.Duration.minutes(1),
            label = "Latency Metric"
        )
        
        latency_alarm = cloudwatch_.Alarm(
            self, 
            id = 'LatencyAlarm', 
            metric = latency_metric, 
            comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            datapoints_to_alarm = 1,
            evaluation_periods = 1,
            threshold = constants.THRESHOLD #if site goes down than 1 so raise alarm
            )
        
        availability_alarm.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm.add_alarm_action(actions_.SnsAction(topic))
        
        
    ######second url########################
         
        
        dimensions = {"URL" : constants.URL_TO_MONITOR_TWO}
      
        
        ##comment period below
        availability_metric_two = cloudwatch_.Metric(
            namespace=constants.URL_MONITOR_NAMESPACE,
            metric_name=constants.URL_MONITOR_TWO_AVAILABILITY,
            dimensions_map=dimensions,  
            period = cdk.Duration.minutes(1), 
            label = "Second URL Availability Metric"
        )
        
        availability_alarm_two = cloudwatch_.Alarm(
            self, 
            id = 'SecondURLAvailabilityAlarm', 
            metric = availability_metric_two, 
            comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
            datapoints_to_alarm = 1,
            evaluation_periods = 1,
            threshold = 1 #if site goes down than 1 so raise alarm
            )
            
        dimensions = {"URL" : constants.URL_TO_MONITOR_TWO}
        
        latency_metric_two = cloudwatch_.Metric(
            namespace=constants.URL_MONITOR_NAMESPACE,
            metric_name=constants.URL_MONITOR_TWO_LATENCY,
            dimensions_map=dimensions,
            period = cdk.Duration.minutes(1),
            label = "Second URL Latency Metric"
        )
        
        latency_alarm_two = cloudwatch_.Alarm(
            self, 
            id = 'SecondURLLatencyAlarm', 
            metric = latency_metric_two, 
            comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            datapoints_to_alarm = 1,
            evaluation_periods = 1,
            threshold = constants.THRESHOLD_TWO #if site goes down than 1 so raise alarm
            )
        
        availability_alarm_two.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm_two.add_alarm_action(actions_.SnsAction(topic))
        
        #THIRD URL##
        
        dimensions = {"URL" : constants.URL_TO_MONITOR_THREE}
      
        
        ##comment period below
        availability_metric_three = cloudwatch_.Metric(
            namespace=constants.URL_MONITOR_NAMESPACE,
            metric_name=constants.URL_MONITOR_THREE_AVAILABILITY,
            dimensions_map=dimensions,  
            period = cdk.Duration.minutes(1), 
            label = "Third URL Availability Metric"
        )
        
        availability_alarm_three = cloudwatch_.Alarm(
            self, 
            id = 'ThirdURLAvailabilityAlarm', 
            metric = availability_metric_three, 
            comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
            datapoints_to_alarm = 1,
            evaluation_periods = 1,
            threshold = 1 #if site goes down than 1 so raise alarm
            )
            
        dimensions = {"URL" : constants.URL_TO_MONITOR_THREE}
        
        latency_metric_three = cloudwatch_.Metric(
            namespace=constants.URL_MONITOR_NAMESPACE,
            metric_name=constants.URL_MONITOR_THREE_LATENCY,
            dimensions_map=dimensions,
            period = cdk.Duration.minutes(1),
            label = "Third URL Latency Metric"
        )
        
        latency_alarm_three = cloudwatch_.Alarm(
            self, 
            id = 'ThirdURLLatencyAlarm', 
            metric = latency_metric_three, 
            comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            datapoints_to_alarm = 1,
            evaluation_periods = 1,
            threshold = constants.THRESHOLD_THREE #if site goes down than 1 so raise alarm
            )
        
        availability_alarm_three.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm_three.add_alarm_action(actions_.SnsAction(topic))
        
           
        #FOURTH URL##
        
        dimensions = {"URL" : constants.URL_TO_MONITOR_FOUR}
      
        
        ##comment period below
        availability_metric_four = cloudwatch_.Metric(
            namespace=constants.URL_MONITOR_NAMESPACE,
            metric_name=constants.URL_MONITOR_FOUR_AVAILABILITY,
            dimensions_map=dimensions,  
            period = cdk.Duration.minutes(1), 
            label = "Fourth URL Availability Metric"
        )
        
        availability_alarm_four = cloudwatch_.Alarm(
            self, 
            id = 'FourthURLAvailabilityAlarm', 
            metric = availability_metric_four, 
            comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
            datapoints_to_alarm = 1,
            evaluation_periods = 1,
            threshold = 1 #if site goes down than 1 so raise alarm
            )
            
        dimensions = {"URL" : constants.URL_TO_MONITOR_FOUR}
        
        latency_metric_four = cloudwatch_.Metric(
            namespace=constants.URL_MONITOR_NAMESPACE,
            metric_name=constants.URL_MONITOR_FOUR_LATENCY,
            dimensions_map=dimensions,
            period = cdk.Duration.minutes(1),
            label = "Fourth URL Latency Metric"
        )
        
        latency_alarm_four = cloudwatch_.Alarm(
            self, 
            id = 'FourthLatencyAlarm', 
            metric = latency_metric_four, 
            comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            datapoints_to_alarm = 1,
            evaluation_periods = 1,
            threshold = constants.THRESHOLD_FOUR
            #if site goes down than 1 so raise alarm
            )
        
        availability_alarm_four.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm_four.add_alarm_action(actions_.SnsAction(topic))
        
   
    def create_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role",
        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
        managed_policies = [
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess')
          #  aws_iam.ManagedPolicy.from_aws_managed_policy_name
            
            ])
            
        return lambdaRole
        
    def create_lambda(self, newid, asset, handler, role):
        return lambda_.Function(self, id = newid,
        runtime=lambda_.Runtime.PYTHON_3_6,
        handler=handler,
        code=lambda_.Code.from_asset(asset),
        role = role
        
) #Filhal commenting it as table is made

    def create_table(self, newid,tablename):
        return db.Table(self, 
        id = newid,
        table_name = tablename,
        partition_key=db.Attribute(name="Name", type=db.AttributeType.STRING),
        sort_key=db.Attribute(name="CreationDate", type=db.AttributeType.STRING)
        )
       

        # example resource
        # queue = sqs.Queue(
        #     self, "SameerRepoQueue",
        #     visibility_timeout=cdk.Duration.seconds(300),
        # )
