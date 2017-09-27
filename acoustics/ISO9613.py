from shapely.geometry import Point
import logging, sys
import numpy as np

class ISO9613:

    def __init__(self,temp=20,humidity=70):
        self.temp = temp
        self.humidity=humidity
    
    def printEnvironment(self):
        return "temp={0}, humidity={1}".format(self.temp, self.humidity)
    
    def calc(Source, Path, Receiver):
       print("hello")

class Spectrum:

    linear = np.zeros([8,1])

    def __init__(self,linear):
        self.linear = linear


    def A():
        pass

class NoiseSource:
     
    
    def __init__(self,location):
        self.location = location
        self.power = Spectrum
        
    def setPower(self,power):
        self.power = power
    
    def setPressure(self, pressure, dist, sphere):
        self.power.linear = pressure.linear + 20*np.log10(dist) - np.log10(sphere)
         
    def print(self):
        return "location={0}, power={1}".format(self.location, self.power.linear)



class NoiseReceiver:
     
    
    def __init__(self,location):
        self.location = location
        self.pressure = Spectrum
        
    def clear(self):
        self.pressure = Spectrum
    
    
    # possibly should add each contribution as a list to get partial levels
    def addPressure(self, pressure):
        
        if self.pressure.linear[0] == 0:
            self.pressure = pressure
        else:
            self.pressure.linear = 10*np.log10( np.power( self.pressure.linear/10, 10) \
                                               + np.power(pressure.linear/10, 10 ) )
         
    def print(self):
        return "location={0}, pressure={1}".format(self.location, self.pressure.linear)

        
    

class Path:
    absorption = []
    barrier = 0
    propagation_height = []



if __name__ == "__main__":
    
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    iso = ISO9613() # create new ISO instance
    
    logging.debug(iso.printEnvironment())
    
    # create a source
    s_loc = Point(0,0,1.5)
    s_spec = Spectrum(np.array([60,60,60,60,60,60,60]))
    
    source = NoiseSource(location=s_loc)
    source.setPressure(pressure=s_spec,dist=20,sphere=0.5)
    print(source.print())
    
    
    
    # create a receiver
    r_loc = Point(100,0,1.5)
    receiver = NoiseReceiver(r_loc)
    
    
    #s = NoiseSource(point=Point(0,0,0),power=Spectrum([50 50 50 50 50 50 50 50])
    
    
    
    # create new source
    
    # create receiver
        


# Public Function ISO_GroundAbsorption(F As String, dp As Double, Gs As Double, Gm As Double, Gr As Double, hs As Double, hr As Double) As Double
# ' Table 3

# Dim q As Double
# Dim A_s As Double, A_m As Double, A_r As Double

# On Error GoTo ErrorHandler

# If dp <= 30 * (hs + hr) Then
    # q = 0
# Else
    # q = 1 - ((30 * (hs + hr)) / dp)
# End If

# Select Case F

    # Case 63
        # A_s = -1.5
        # A_r = -1.5
        # A_m = -3 * q ^ 2
    # Case 125
        # A_s = -1.5 + Gs * Ground_a(hs, dp)
        # A_r = -1.5 + Gr * Ground_a(hr, dp)
        # A_m = -3 * q * (1 - Gm)
    # Case 250
        # A_s = -1.5 + Gs * Ground_b(hs, dp)
        # A_r = -1.5 + Gr * Ground_b(hr, dp)
        # A_m = -3 * q * (1 - Gm)
    # Case 500
        # A_s = -1.5 + Gs * Ground_c(hs, dp)
        # A_r = -1.5 + Gr * Ground_c(hr, dp)
        # A_m = -3 * q * (1 - Gm)
    # Case 1000
        # A_s = -1.5 + Gs * Ground_d(hs, dp)
        # A_r = -1.5 + Gr * Ground_d(hr, dp)
        # A_m = -3 * q * (1 - Gm)
    # Case 2000, 4000, 8000
        # A_s = -1.5 * (1 - Gs)
        # A_r = -1.5 * (1 - Gr)
        # A_m = -3 * q * (1 - Gm)
    # Case Else
        # MsgBox (F & " is not a valid frequency")
        # Error (1)
        
# End Select

# ISO_GroundAbsorption = A_s + A_m + A_r
# Exit Function

# ErrorHandler:
# MsgBox (Err.Description)

# End Function

# Public Function Ground_a(h, dp)

    # Ground_a = 1.5 + 3 * Exp(-0.12 * (h - 5) ^ 2) * (1 - Exp(-dp / 50)) + 5.7 * Exp(-0.09 * h ^ 2) * (1 - Exp(-2.8 * 10 ^ (-6) * dp ^ 2))

# End Function
# Public Function Ground_b(h, dp)

    # Ground_b = 1.5 + 8.6 * Exp(-0.09 * h ^ 2) * (1 - Exp(-dp / 50))

# End Function

# Public Function Ground_c(h, dp)

# Ground_c = 1.5 + 14 * Exp(-0.46 * h ^ 2) * (1 - Exp(-dp / 50))

# End Function

# Public Function Ground_d(h, dp)

# Ground_d = 1.5 + 5# * Exp(-0.9 * h ^ 2) * (1 - Exp(-dp / 50))

# End Function

