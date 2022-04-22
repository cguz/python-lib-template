from mlspace import evaluate

from mlspace.helpers.configuration import PATH_TRAIN_TO_PKL

def test_evaluate_all_steps():
    prepare = evaluate.EvaluateModel(PATH_TRAIN_TO_PKL)
    prepare.evaluate()
    assert prepare.check_finish  == True