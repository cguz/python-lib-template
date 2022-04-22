from mlspace import create_dataset

def test_create_download():
    prepare = create_dataset.PrepareData('test')
    prepare.skip_test_download = True
    assert prepare.download()

def test_create_all_steps():
    prepare = create_dataset.PrepareData('test')
    prepare.load_data()
    prepare.analyze_data()
    prepare.check_quality_gate()
    prepare.save_to_file()
    assert prepare.all_cols[0] == 'sa'