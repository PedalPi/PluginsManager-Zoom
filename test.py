import time

from zoom.observer.zoom_host import ZoomHost
from zoom.zoomg3v2 import ZoomG3v2

zoom = ZoomG3v2()
zoom.connect(ZoomHost())

zoom.load_data()
print('ok')
time.sleep(2)


#pedalboard = zoom.current_pedalboard

# Change pedalboard
#zoom.next_pedalboard()
#zoom.previous_pedalboard()

#equipment.current_pedalboard = pedalboard

# Previous pedalboard
#print(len(zoom.current_pedalboard.effects))
#print(zoom.current_pedalboard.effects)

#for effect in zoom.current_pedalboard.effects:
#    effect.active = True

'''
equipment.register(host)

observer = ZoomGSeriesObserver()

equipment.register(observer)

bank = Bank('Zoom G3')
equipment.append(bank)

with observer:
    for i in range(0, 100):
        pedalboard = Pedalboard(str(i) + ' - ')
        bank.append(pedalboard)

        for i in range(0, 5):
            pedalboard.append(ZoomGSeriesBuilder().build('MS 1959'))

pedalboard = equipment.banks[0].pedalboards[0]
effect = pedalboard.effects[0]
effect.toggle()
effect.params[2].value = 75

print(bank)
'''
