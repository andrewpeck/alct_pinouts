from alct_pinouts import *


def parse_netlist():
    filename = 'FPGA_IO.NET'
    f = open(filename, 'r')

    netlist = {}

    for line in f:

        if (line[0]!='-'):
            (net,part,pin) = line.split()
            netlist.update({net: pin})

#    for key in netlist:
#        print netlist[key]

    return netlist

def check_ios (io_list, netlist):
    for key in io_list:
        value = io_list [key]
        #print value[0:2]
        if (value=='GND'):
            #print "Ground"
            pass
        elif (value[0:2]=='3v3'[0:2]):
            #print "3.3v"
            pass
        elif (value[0:2]=='1v8'[0:2]):
            #print "3.3v"
            pass
        elif (value[0]=='+'[0]):
            #print "3.3v"
            pass
        elif (value[0:1] == "NC"[0:1]):
            #print "no connect"
            pass
        elif (value[0:1] == "tp"[0:1]):
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

netlist = parse_netlist()

check_ios(a288_io, netlist);
check_ios(a384_io, netlist);
check_ios(a672_io, netlist);

