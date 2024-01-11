
import pyinsim


def message_out(insim, mso):
    # Print out the MSO message.
    # Note: ^L means Latin character, ^J japanese etc... ^0-^9 refer to colors.
    print(mso.Msg)


def insim_state(insim, sta):
    '''
    # SMALL_LCS Flags
LCS_SET_SIGNALS = 1		# bit 0
LCS_SET_FLASH = 2		# bit 1
LCS_SET_HEADLIGHTS = 4	# bit 2
LCS_SET_HORN = 8		# bit 3
LCS_SET_SIREN = 0x10	# bit 4

LCS_Mask_Signals = 0x0300       # bits  8-9   (Switches & 0x0300) - Signal    (0 off / 1 left / 2 right / 3 hazard)
LCS_Mask_Flash = 0x0400         # bit   10    (Switches & 0x0400) - Flash
LCS_Mask_Headlights = 0x0800    # bit	11    (Switches & 0x0800) - Headlights
LCS_Mask_Horn = 0x070000        # bits  16-18 (Switches & 0x070000) - Horn    (0 off / 1 to 5 horn type)
LCS_Mask_Siren = 0x300000       # bits  20-21 (Switches & 0x300000) - Siren   (0 off / 1 fast / 2 slow)

    '''
    # turn on
    insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_EXTRA | pyinsim.LCL_Mask_Extra)
    # turn off
    insim.send(pyinsim.ISP_SMALL, SubT=pyinsim.SMALL_LCL, UVal=pyinsim.LCL_SET_EXTRA)

# Init new InSim object.
insim = pyinsim.insim(b'127.0.0.1', 29999, Admin=b'')

# Bind ISP_MSO packet to message out method.
insim.bind(pyinsim.ISP_MSO, message_out)
# Bind ISP_STA packet to insim state method.
insim.bind(pyinsim.ISP_STA, insim_state)

# Start pyinsim.
pyinsim.run()