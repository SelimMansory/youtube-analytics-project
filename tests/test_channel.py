from src.channel import Channel


def test_channel():
    """Тестируем класс Channel"""
    ch = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
    assert ch.channel_id == 'UC-OVMPlMA3-YCIeg4z5z23A'
    assert ch.url == 'https://www.youtube.com/channel/UC-OVMPlMA3-YCIeg4z5z23A'
    ch.print_info()
    ch.to_json('test.json')