import pytest
from aws_cdk import core
from sameer_repo.sameer_repo_stack import SameerRepoStack

#This unit test is to check wheter I have two lambda functions or not
def test_lambda():
    
    app = core.App()
    SameerRepoStack(app, "teststacksameer")
    template = app.synth().get_stack_by_name('teststacksameer').template
    functions = [resource for resource in template['Resources'].values() if resource['Type'] == 'AWS::Lambda::Function']
    
    assert len(functions) == 2
    

    
    