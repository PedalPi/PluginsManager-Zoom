from zoom.model.zoom_pedalboard import ZoomPedalboard
from zoom.zoom_builder import ZoomBuilder


class ZoomIVMessageDecoder:
    def decode(self, message):
        # Commands (F0 52 00 5A xx)
        # 08: Specific path
        # 28: Current path / Foot switch expression
        # 31: Global info: Tempo / Signal path / Auto save / Foot switch (min, max)
        # 31: Patch info: Patch name / Patch volume / Ctrl switch assignment
        # 31: Effect param value:
        # 32: Patch saved
        print(message.hex())

        if message.type == 'program_change':
            print('Current patch is', "'" + str(+message.program) + "'")

        elif len(message) == 110:
            print('Current patch', message)

        elif len(message) == 120:
            return self.decode_specific_path(message)

        elif len(message) == 15:
            print('Device info', message.hex())

        else:
            # Path saved in x position
            # F0 52 00 5A 32 01 00 00 xx 00 00 00 00 00 F7
            # Swap xx <--> yy
            # F0 52 00 5A 32 02 00 00 xx 00 00 yy 00 00 F7
            print(message, '\n', message.hex())
            print('Size', len(message))

    def decode_specific_path(self, message):
        builder = ZoomBuilder(None)
        print('Specified patch', message.hex())

        manufacturing_id = message.data[0]
        device_id = message.data[1]
        model_number = message.data[2]

        command_number = message.data[3]  # 08

        name = bytes(message.data[0x65:0x69] + message.data[0x6A:0x70]).decode()
        pedalboard = ZoomPedalboard(name=name)
        print(message.data[6+4] & 0b00000001)
        print(message.data[19+4] & 0b00000001)
        print(message.data[33+4] & 0b00000001)
        print(message.data[47+4] & 0b00000001)
        print(message.data[60+4] & 0b00000001)
        print(message.data[74+4] & 0b00000001)
        '''
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

        '''
        # Read the first four characters of the name
        for i in range(4):
            name += message[count + 0x66]); // Add ascii character to the SP.Label String
        }
        for (uint8_t count = 4; count < 10; count++) { // Read the last six characters of the name
        SP[Current_switch].Label[count] = static_cast < char > (sxdata[count + 0x67]); // Add ascii character to the SP.Label String
        }
        '''
