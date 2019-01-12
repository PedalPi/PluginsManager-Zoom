from pluginsmanager.banks_manager import BanksManager
from pluginsmanager.model.bank import Bank
from pluginsmanager.model.pedalboard import Pedalboard

from zoomgseries.zoomgseries_builder import ZoomGSeriesBuilder
from zoomgseries.zoomgseries_manager import ZoomGSeriesObserver

ZoomG3 = BanksManager()
observer = ZoomGSeriesObserver()

ZoomG3.register(observer)

bank = Bank('Zoom G3')
ZoomG3.append(bank)

with observer:
    for i in range(0, 100):
        pedalboard = Pedalboard(str(i) + ' - ')
        bank.append(pedalboard)

        for i in range(0, 5):
            pedalboard.append(ZoomGSeriesBuilder().build('MS 1959'))

pedalboard = ZoomG3.banks[0].pedalboards[0]
effect = pedalboard.effects[0]
effect.toggle()
effect.params[2].value = 75

print(bank)
