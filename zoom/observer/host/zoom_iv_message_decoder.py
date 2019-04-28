from zoom.model.zoom_pedalboard import ZoomPedalboard
from zoom.zoom_builder import ZoomBuilder


class ZoomIVMessageDecoder:
    def decode(self, message):
        if message.type == 'program_change':
            print('Current patch is', "'" + str(+message.program) + "'")

        elif len(message) == 110:
            print('Current patch', message)

        elif len(message) == 120:
            return self.decode_specific_path(message)

        elif len(message) == 15:
            print('Device info', message)

        else:
            print(message, '\n', message.hex())
            print('Size', len(message))

    def decode_specific_path(self, message):
        builder = ZoomBuilder(None)
        print('Specified patch', message.hex())

        manufacturing_id = message.data[0]
        device_id = message.data[1]
        model_number = message.data[2]

        name = bytes(message.data[0x65:0x69] + message.data[0x6A:0x70]).decode()
        pedalboard = ZoomPedalboard(name=name)
        pedalboard_number = x

        for i in range(0, 6):
            effect = builder.build()
            for param in range(9):
                effect.params[i] =

            effect.active =
            pedalboard.append(effect)

        print(pedalboard)

        zoom.pedalboards[pedalboard_number] = pedalboard

        '''
        # Read the first four characters of the name
        for i in range(4):
            name += message[count + 0x66]); // Add ascii character to the SP.Label String
        }
        for (uint8_t count = 4; count < 10; count++) { // Read the last six characters of the name
        SP[Current_switch].Label[count] = static_cast < char > (sxdata[count + 0x67]); // Add ascii character to the SP.Label String
        }
        '''
