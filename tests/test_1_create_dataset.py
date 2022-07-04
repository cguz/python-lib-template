from mlspace import create_dataset

def test_create_download():
    prepare = create_dataset.PrepareData('NPWD2401')
    prepare.skip_test_download = True
    assert prepare.download()

def test_create_all_steps():
    prepare = create_dataset.PrepareData('NPWD2401')
    prepare.load_data()
    prepare.analyze_data()
    prepare.check_quality_gate()
    prepare.save()
    assert prepare.all_cols[0] == 'sa'