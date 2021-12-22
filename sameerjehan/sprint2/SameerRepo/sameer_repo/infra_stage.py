from aws_cdk import core

from sameer_repo.sameer_repo_stack import SameerRepoStack 
#from sameer_repo.sameer_repo import SameerRepoStack as InfraStack

class InfraStage(core.Stage): #here core.Stack is super class from which MyPipelineStack is inheriting
    def __init__(self, scope: core.Construct, id:str, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        sameer_stack = SameerRepoStack(self,'sameerStack')