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
  #  aws_stepfunctions_tasks as tasks_,
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
            constants.BUCKET_NAME = "newsameerbucketsprint2"
       #     sameerBucket = s3.Bucket(self, id = "sameerbucketnews3sprint2", bucket_name = constants.BUCKET_NAME)
       #     firstDeploy = s3_deploy.BucketDeployment(self, "FirstDeployBucket",sources=[s3_deploy.Source.asset("./files")], destination_bucket = sameerBucket)
            # constants.BUCKET_NAME_MODIFIED = constants.BUCKET_NAME
            
        except:
            print("Bucket Already Exists")
            
        # try:
        #     self.create_table("newTableSameer", "SameerTableTwoSprintTwo")
        # except:
        #     print("Table Already Created")
       
   
        
        s3_lambda = self.create_lambda("S3Lambda", "./resources", "s3lambda.lambda_handler", lambda_role)
        lambda_target_two = targets_.LambdaFunction(handler=s3_lambda)
        
        
        
        
        #HLambda = self.create_lambda("HelloLambda", "./resources", "lambda.lambda_handler")
        HLambda = self.create_lambda("WebHealthCheck", "./resources", "webhealth_lambda.lambda_handler", lambda_role)
        dynamodb_lambda = self.create_lambda("DyamoDBLambda", "./resources", "dynamoDB.lambda_handler", lambda_role)
       
        
        lambda_schedule = events_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_target = targets_.LambdaFunction(handler=HLambda)
        lambda_target_one = targets_.LambdaFunction(handler=dynamodb_lambda)
       
        rule = events_.Rule(self, "WebHealth_Check",description = "Periodic Lambda", enabled = True, schedule = lambda_schedule, targets = 
        [lambda_target, lambda_target_one
        ])
    
        topic = sns.Topic(self, "SameerWebHealthTopicSNS")
        topic.add_subscription(subscriptions_.EmailSubscription('sameer.jehan.s@skipq.org'))
        # print(topic)
        topic.add_subscription(subscriptions_.LambdaSubscription(fn=dynamodb_lambda))
        
        constants.URL_TO_MONITOR_LIST = ["https://www.espn.com/","https://www.dawn.com/","https://www.facebook.com/","https://www.messenger.com/"]
        
        for i in range(len(constants.URL_TO_MONITOR_LIST)):
            
            dimensions = {"URL" :constants.URL_TO_MONITOR_LIST[i]}
            ##comment period below
            availability_metric = cloudwatch_.Metric(
                namespace=constants.URL_TO_MONITOR_NAMESPACE,
                #metric_name=constants.URL_MONITOR_AVAILABILITY,
                metric_name =  "Sameer" + constants.URL_MONITOR_AVAILABILITY+constants.URL_TO_MONITOR_LIST[i],
                dimensions_map=dimensions, 
                period = cdk.Duration.minutes(1), 
                label = "SameerNew" + "_" + "Availability Metric" + "_" + constants.URL_TO_MONITOR_LIST[i]
            )
        
            availability_alarm = cloudwatch_.Alarm(
                self, 
                id = "SameerNew" + "_" + constants.URL_TO_MONITOR_LIST[i] + "_" + 'AvailabilityAlarm', 
                metric = availability_metric, 
                comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                datapoints_to_alarm = 1,
                evaluation_periods = 1,
                threshold = 1 #if site goes down than 1 so raise alarm
            )
            
            dimensions = {"URL" : constants.URL_TO_MONITOR_LIST[i]}
        
            latency_metric = cloudwatch_.Metric(
                namespace=constants.URL_TO_MONITOR_NAMESPACE,
                #metric_name=constants.URL_MONITOR_LATENCY,
                metric_name = "Sameer" + constants.URL_MONITOR_LATENCY+constants.URL_TO_MONITOR_LIST[i],
                dimensions_map=dimensions,
                period = cdk.Duration.minutes(1),
                label = "SameerNew" + "_" + "Latency Metric" + "_" + constants.URL_TO_MONITOR_LIST[i]
                )
        
            latency_alarm = cloudwatch_.Alarm(
                self, 
                id = "SameerNew" + "_" + constants.URL_TO_MONITOR_LIST[i] + "_" + 'LatencyAlarm', 
                metric = latency_metric, 
                comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                datapoints_to_alarm = 1,
                evaluation_periods = 1,
                threshold = constants.THRESHOLDS[i] #if site goes down than 1 so raise alarm
                )
        
            availability_alarm.add_alarm_action(actions_.SnsAction(topic))
            latency_alarm.add_alarm_action(actions_.SnsAction(topic))
    
   
    def create_lambda_role(self):
        lambdaRole = aws_iam.Role(self, "lambda-role",
        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
        managed_policies = [
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess"),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
          #  aws_iam.ManagedPolicy.from_aws_managed_policy_name
            
            ])
            
        return lambdaRole
        
    def create_lambda(self, newid, asset, handler, role):
        return lambda_.Function(self, id = newid,
        runtime=lambda_.Runtime.PYTHON_3_6,
        handler=handler,
        code=lambda_.Code.from_asset(asset),
        role = role,
        timeout= cdk.Duration.minutes(5)
        
) #Filhal commenting it as table is made

    def create_table(self, newid,tablename):
        return db.Table(self, 
        id = newid,
        table_name = tablename,
        partition_key=db.Attribute(name="Name", type=db.AttributeType.STRING),
        sort_key=db.Attribute(name="CreationDate", type=db.AttributeType.STRING)
        )
       