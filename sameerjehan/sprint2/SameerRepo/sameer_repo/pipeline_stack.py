from aws_cdk import core
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines
from sameer_repo.sameer_repo_stack import SameerRepoStack
from sameer_repo.infra_stage import InfraStage

class PipelineStack(core.Stack): #here core.Stack is super class from which MyPipelineStack is inheriting
    def __init__(self, scope: core.Construct, id:str, **kwargs):
        super().__init__(scope, id, **kwargs)

        source = pipelines.CodePipelineSource.git_hub(repo_string = 'sameer2021skipq/ProximaCentauri', branch='main',
                authentication=core.SecretValue.secrets_manager('github/token/sameer'),
                trigger = cpactions.GitHubTrigger.POLL
                
            )
        
        synth=pipelines.ShellStep("synth",input=source,
     
        commands=["cd sameerjehan/sprint2/SameerRepo","pip install -r requirements.txt",
        "pip install -r requirements-dev.txt -t ./SameerRepo/resources/dependencies",
        "npm install -g aws-cdk",
        "cdk synth"
        
        ], 
        primary_output_directory = "sameerjehan/sprint2/SameerRepo/cdk.out"
        ##the above til source and build is done
        )
        #now you have to do staging which is to deploy in test environment
        pipeline = pipelines.CodePipeline(self, 'newPipeline', synth = synth)
        
        beta = InfraStage(self, "Beta", 
        env={
            'account': "315997497220",
            'region':'us-east-2'
        })
        
        prod = InfraStage(self, "Prod", 
        env={
            'account': "315997497220",
            'region':'us-east-2'
        })
        
        unit_test=pipelines.ShellStep("unit_test",
     
        commands=["cd sameerjehan/sprint2/SameerRepo","pip install -r requirements-dev.txt",
        "pytest unittests pytest integrationtests"
        
        ]), 
        
        pipeline.add_stage(beta, pre = [unit_test])
        
        pipeline.add_stage(prod ,
        pre = [pipelines.ManualApprovalStep("PromoteToProd")])
        
     
            
           
              