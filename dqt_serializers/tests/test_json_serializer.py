from dqt_serializers.dqt_serializers.json_serializer import JsonSerializer


def test_json_roundtrip(tmp_path):
    json_ser = JsonSerializer()
    data = {"key": "value"}
    path = tmp_path / "test.json"

    json_ser.serialize(data, path)
    loaded = json_ser.deserialize(path)

    assert loaded == data
