from mlspace import create_dataset

def test_rmse():
    assert create_dataset.rmse() == 1.0

def test_download():
    prepare = create_dataset.PrepareData('test')
    assert prepare.download()