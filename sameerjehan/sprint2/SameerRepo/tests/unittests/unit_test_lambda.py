import pytest
from aws_cdk import core
from sameer_repo.pipeline_stack import PipelineStack

#This unit test is to check wheter I have two lambda functions or not
def test_lambda():
    
    app = core.App()
    PipelineStack(app, "NewSameerSkipqQPipelineSprint2")
    template = app.synth().get_stack_by_name('NewSameerSkipqQPipelineSprint2').template
    functions = [resource for resource in template['Resources'].values() if resource['Type'] == 'AWS::Lambda::Function']
    
    assert len(functions) == 2
    

    
    