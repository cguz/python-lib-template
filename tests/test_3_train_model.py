from mlspace import train_model

from mlspace.helpers.configuration import PATH_TRAIN_TO_PKL

def test_train_all_steps():
    prepare = train_model.TrainModel(PATH_TRAIN_TO_PKL)
    prepare.train()
    assert prepare.model