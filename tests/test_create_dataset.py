from mlspace import create_dataset

def test_rmse():
    assert create_dataset.rmse() == 1.0

def test_download():
    prepare = create_dataset.PrepareData('test')
    assert prepare.download()

def test_load_data():
    prepare = create_dataset.PrepareData('test')
    prepare.load_data()
    assert prepare.all_cols[0] == 'sa'