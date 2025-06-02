from dqt_serializers.dqt_serializers.csv_serializer import CsvSerializer

def test_csv_serialization(tmp_path):
    csv = CsvSerializer()
    data = [{"col1": 1, "col2": "A"}, {"col1": 2, "col2": "B"}]
    path = tmp_path / "test.csv"

    csv.serialize(data, path)
    df = csv.deserialize(path)

    assert df.shape == (2, 2)
    assert df.iloc[0]["col1"] == 1