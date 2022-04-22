from mlspace import build_model

from mlspace.helpers.configuration import PATH_TRAIN_TO_PKL

def test_build_all_steps():
    prepare = build_model.BuildModel(PATH_TRAIN_TO_PKL, "RandomForest")
    prepare.build()
    assert prepare.check_continue == True