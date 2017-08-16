
class Common():
    def get_api(self):
        return 'common api -->'

class Speaker(Common):
    def get_api(self):
        api = super().get_api()
        return '{} regular speaker api -->'.format(api)

class Headset(Common):
    def get_api(self):
        api = super().get_api()
        return '{} regular headset api -->'.format(api)

class SpecialSpeaker(Common):
    def get_api(self):
        api = super().get_api()
        return '{} special speaker api -->'.format(api)

class SpecialHeadset(Common):
    def get_api(self):
        api = super().get_api()
        return '{} special headset api -->'.format(api)

class Dut(Speaker, SpecialSpeaker):
    def __init__(self):
        for c in Dut.__mro__:
            print(c)


d = Dut()
print(d.get_api())