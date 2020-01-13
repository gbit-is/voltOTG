import serial
import time 
import serial.tools.list_ports


class voltOTG():


    def __init__(self):
        self.data = [ ]

    def findDevice(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            try:
                pid = hex(port.pid)
                vid = hex(port.vid)
                if pid == "0x5523" and vid == "0x1a86":
                    return port.device
            except:
                pass
        return "Device not found"


    def connectDevice(self,path):
        ser = serial.Serial()
        ser.baudrate = 9600
        ser.port = path
        ser.open()
        self.ser = ser
        return True


    def autoConnect(self):
        device = self.findDevice()
        self.connectDevice(device)

        test = self.bcom("ReadVolt")

        if test == "":
            return False
        else:
            return True




    def bcom(self,msg):
        self.ser.write(msg.encode())
        self.ser.timeout = 0.1

        x = ""
        while True:
            y = self.ser.read()
            y = y.decode()

            if y == "":
                data = x.rstrip()
                return data
            else:
                x = x + y



    def scom(self,msg,**kwargs):

        retryCount = kwargs.get('retryCount',0)
        maxRetries = kwargs.get('maxRetries',3)

        response = self.bcom(msg)
        if response == "":
            retryCount = retryCount + 1
            if retryCount <= maxRetries:
                status = self.scom(msg,retryCount=retryCount,maxRetries=maxRetries)
                return(status)
            else:
                return "Did not recieve a repsonse from device"
        else:
            return response

    def getVersion(self,**kwargs):

        list = kwargs.get('list',False)
        version = kwargs.get('version',False)
        name = kwargs.get('name',False)

        unparsed = self.scom("ReadVersion")

        try:
            data = unparsed.split(":")[1][:-1].split("_")
            dname = data[0]
            dver = data[1][1:]
            if list:
                return dname,dver
            elif version:
                return dver
            elif name:
                return dname
            else:
                return dver

        except Exception as e:
            return "unable to parse: ' " + str(unparsed) + " ' as a version"

    def readVolt(self,**kwargs):

        list = kwargs.get('list',False)
        voltage = kwargs.get('voltage',False)
        pga = kwargs.get('pga',False)
        info = kwargs.get('info',False)
        raw = kwargs.get('raw',False)

        if info:
            message = '''readVolt() by default returns the value from the VoltOTG in millivolts (mv)\nuse the boolean arguments list,voltage,pga,raw,info to refine the output'''
            return message

        unparsed = self.scom("ReadVolt")

        if raw:
            return unparsed
        try:
            unparsed = unparsed[:-1].split(",")
            dvoltage = unparsed[0].split(":")[1][:-2]
            dpga = unparsed[1].split("=")[1]

            if list:
                l = [dvoltage,dpga]
                return l
            elif voltage:
                return dvoltage
            elif pga:
                return dpga
            else:
                return dvoltage

        except:
            return "unable to parse: ' " + str(unparsed) + " ' as voltage "

    def readScale(self,**kwargs):

        list = kwargs.get('list',False)
        scale = kwargs.get('scale',False)
        calib = kwargs.get('calib',False)
        raw = kwargs.get('raw',False)

        unparsed = self.scom("ReadScale")

        if raw:
            return unparsed

        try:
            unparsed = unparsed[:-1].split(",")

            dscale = unparsed[0].split(":")[1]
            dcalib = unparsed[1].split(":")[1]


            if list:
                l = [ dscale,dcalib]
                return l
            elif scale:
                return dscale
            elif calib:
                return dcalib
            else:
                return dscale


        except:
            return "unable to parse: ' " + str(unparsed) + " ' as scale "

    def setScale(self,scale,calib):

        try:
            scale = float(scale)
            calib = int(calib)
        except:
            print("arg 0 must be float and arg 1 int")
            return "arg 0 must be float and arg 1 int" 


        command = "SetScale:%s,%s>"%(str(scale),str(calib))
        reply = self.scom(command)

        try:
            data = reply.split(",")

            if data[0] == "OK" and data[1] == "OK" and data[2] == "SetScale<":
                return True
            else:
                dscale = "Scale:" + str(data[0])
                dcalib = "Calib:" + str(data[1])
                report = [ dscale,dcalib ]
                return report

        except:
            return "unable to parse: ' " + str(reply) + " ' as a SetScale reply "
    
    def readPga(self):

        unparsed = self.scom("ReadPga")

        try:
            pga = unparsed[-2]
            pga = int(pga)
            return pga
        except:
            return "unable to parse: ' " + str(unparsed) + " ' as a PGA Value "



    def setPga(self,pga):

        try:
            pga = int(pga)
        except:
            return "pga must be integer"

        if pga not in [1,2,4,8]:
            return  "pga can only be one of: 1,2,4,8"


    
        command = "SetPga:%s>"%pga
        unparsed = self.scom(command)
        reply = unparsed.split(",")[0] 



        if reply == "OK":
            return True
        elif reply == "ERR":
            return False
        else:
            return "Unknown Error, setPga reply was: " + str(unparsed)

    def readMode(self):

        unparsed = self.scom("ReadMode")

        try:
            mode = unparsed[-2]
            mode = int(mode)
            return mode
        except:
            return "Unknown Error, Mode reply was : " + str(unparsed)



    def setMode(self,mode):

        try:
            mode = int(mode)
        except:
            return "Mode must be 0 or 1"

        if mode not in [ 0,1 ]:
            return "Mode must be 0 or 1"


        command = "SetMode:%s>"%str(mode)
        unparsed = self.scom(command)
        reply = unparsed.split(",")[0]

        if reply == "OK":
            return True
        elif reply == "ERR":
            return False
        else:
            return "Unknown Error, Mode reply was : " + str(unparsed)



