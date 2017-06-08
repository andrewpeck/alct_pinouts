
from alct_pinouts    import *
from name_translator import *
from led_lut         import *


# export netlist as  MultiWire

def parse_netlist():
    filename = 'FPGA_IO.NET'
    f = open(filename, 'r')

    netlist = {}

    for line in f:

        if (line[0]!='-'):
            (net,part,pin) = line.split()
            if (part=='U1' and net[0]!='+' and net!='GND'):
                netlist.update({net: pin})

#    for key in netlist:
#        print netlist[key]

    return netlist

def check_ios (io_list, netlist):
    for key in io_list:
        value = io_list [key]
        #print value[0:2]

        if (not pin_needs_ucf(value)):
            pass

        if (value[0:2] == "tp"):
            a = netlist.get(value, "not found")
            if (a=="not found"):
                print key + "\t\t" + "\t\t" + value + "\t\t" +  a
        else:
            a = netlist.get(key, "not found")
            if (a=="not found"):
                print key + "\t\t" + "\t\t" + value + "\t\t" +  a

    print ''
    print ''
    print ''


def pin_needs_ucf (io_signal):
    if (io_signal=='GND'):
        return False
    elif (io_signal[0:3]=='3v3'):
        return False
    elif (io_signal[0:3]=='1v8'):
        return False
    elif (io_signal[0]=='+'):
        return False
    elif (io_signal[0:2] == "NC"):
        return False
    elif (io_signal[4:9] == "prgrm"):
        return False
    elif (io_signal == '/hard_rst'):
        return False

    return True


def gen_constraints (filename, samtec_io, base_led, netlist):

    f = open(filename, 'w')

    # loop over ALCT Baseboard Samtec IOs (XPXX_YY)

    for io in samtec_io:

        # io       = XPXX_YY
        # signal   = lct2_8  (for example)
        # ucf_name = lct2<8> (for example)

        signal    = samtec_io [io]

        # power and ground and etc pins etc don't need to be added to the ucf
        if (pin_needs_ucf(signal)):

            ucf_name = name_lut    [signal];

            if   (signal[0:2] == "tp" and signal[2]!='_'):
                pin = netlist.get(signal, "not found")
            elif (signal=="clock"):
                pin = netlist.get("mez_clock", "not found")
            elif (base_led.get(signal, "not found")!='not found'):
                pin = netlist.get(base_led.get(signal), "not found")
            else:
                pin = netlist.get (io, "not found");

            #print '{:20s}  {:20s}  {:20s}  {:20s}'.format(io, signal, ucf_name, pin)
            constraint = 'NET {:20s} LOC = {:10s} # {:10s} {:20s}'.format('"' + ucf_name + '"', '"'+pin+'";' , io, signal);
            print constraint
            f.write(constraint + "\n")
            #print 'NET ' + '{:20s}'.format(ucf_name) + '"' + '     LOC = '

    f.write ('#------------------------------------------------------------------------\n')
    f.write ('# IOB Modifiers                                                          \n')
    f.write ('#------------------------------------------------------------------------\n')
    f.write ('NET "clk80<*>"            SLEW=FAST | DRIVE=12;                          \n')
    f.write ('                                                                         \n')
    f.write ('NET "rsrvd_out<*>"        SLEW=SLOW | DRIVE=12;                          \n')
    f.write ('NET "ext_inject_trig"     SLEW=SLOW | DRIVE=12;                          \n')
    f.write ('NET "activeFeb_cfgDone"   SLEW=SLOW | DRIVE=12;                          \n')
    f.write ('NET "valid"               SLEW=SLOW | DRIVE=12;                          \n')
    f.write ('NET "keyp<*>"             SLEW=SLOW | DRIVE=12;                          \n')
    f.write ('NET "quality<*>"          SLEW=SLOW | DRIVE=12;                          \n')
    f.write ('NET "amu"                 SLEW=SLOW | DRIVE=12;                          \n')
    f.write ('NET "bxn_wrFifo<*>"       SLEW=SLOW | DRIVE=12;                          \n')
    f.write ('NET "L1A_SyncAdb"         SLEW=SLOW | DRIVE=12;                          \n')
    f.write ('NET "daqData<*>"          SLEW=SLOW | DRIVE=12;                          \n')
    f.write ('NET "lctSpec_FirstFr"     SLEW=SLOW | DRIVE=12;                          \n')
    f.write ('NET "dduSpec_LastFr"      SLEW=SLOW | DRIVE=12;                          \n')
    f.write ('NET "seq_seu<*>"          SLEW=SLOW | DRIVE=12;                          \n')
    f.write ('                                                                         \n')
    f.write ('#------------------------------------------------------------------------\n')
    f.write ('# Time Specs                                                             \n')
    f.write ('#------------------------------------------------------------------------\n')
    f.write ('NET "tck2" TNM_NET = "tck2";                                             \n')
    f.write ('TIMESPEC "TS_tck2" = PERIOD "tck2" 21 ns HIGH 50 %;                      \n')
    f.write ('NET "clkp" TNM_NET = "clkp";                                             \n')
    f.write ('TIMESPEC "TS_clkp" = PERIOD "clkp" 21 ns HIGH 50 %;                      \n')
    f.write ('                                                                         \n')
    f.write ('NET "tck2" CLOCK_DEDICATED_ROUTE = FALSE;                                \n')

#for led in base_led:
#
#
#    if (signal != 'nc'):
#
#        ucf_name = name_lut    [signal];
#        pin      = netlist.get (led, "not found");
#        print '{:20s}  {:20s}  {:20s}  {:20s}'.format(io, signal, ucf_name, pin)



#check_ios(a288_io, netlist);
#check_ios(a384_io, netlist);
#check_ios(a672_io, netlist);

netlist = parse_netlist()

gen_constraints ("alct288.ucf", a288_io, led_288, netlist);
gen_constraints ("alct384.ucf", a384_io, led_384, netlist);
gen_constraints ("alct672.ucf", a672_io, led_672, netlist);

