class MidiProtocol:
    NON_REAL_TIME_HEADER = 0x7E

    GENERAL_SYSTEM_INFORMATION = 0x06
    DEVICE_IDENTITY_REQUEST = 0x01

    @staticmethod
    def device_identify_request(target=0x00):

        TARGET_ID = target
        SUB_ID_1 = MidiProtocol.GENERAL_SYSTEM_INFORMATION
        SUB_ID_2 = MidiProtocol.DEVICE_IDENTITY_REQUEST

        return [MidiProtocol.NON_REAL_TIME_HEADER, TARGET_ID, SUB_ID_1, SUB_ID_2]

    @staticmethod
    def device_identity_reply_decode(data):
        '''
        F0 7E 00 06 02 52 5A 00 00 00 32 2E 31 30 F7

        F0 7E	Universal Non Real Time Sys Ex header
        id	ID of target device   (default = 7F = All devices)
        06	Sub ID#1 = General System Information
        02	Sub ID#2 = Device Identity message
        mm	Manufacturers System Exclusive ID code.
        If mm = 00, then the message is extended by 2 bytes to accomodate the additional manufacturers ID code.
        ff ff	Device family code (14 bits, LSB first)
        dd dd	Device family member code (14 bits, LSB first)
        ss ss ss ss	Software revision level (the format is device specific)
        F7	EOX
        '''
        # 7e id 06 02 mm ff ff dd dd ss ss ss ss EOX
        return {
            'id': data[1],
            'manufacturer': data[4],
            'device family code': data[5:7],
            'device family member code': data[7:11],
        }
