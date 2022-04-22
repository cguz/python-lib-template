from mlspace import deployment

from mlspace.helpers.configuration import PATH_TRAIN_TO_PKL

def test_deployment_all_steps():
    prepare = deployment.DeploymentModel()
    prepare.check_quality_gate()
    assert prepare.pass_quality_check == True