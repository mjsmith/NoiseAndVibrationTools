from shapely.geometry import Point
import logging, sys
import numpy as np

class ISO9613:

    def __init__(self,temp=20,humidity=70):
        self.temp = temp
        self.humidity=humidity
    
    def __str__(self):
        return "ISO9613 calculator: temp={0}, humidity={1}".format(self.temp, self.humidity)
    
    def calc(self, source, path, receiver):
       
       dist = source.location.distance(receiver.location)
       logging.debug("Distance = {0}".format(dist))
       
       
       # divergance
       A_div = 20*np.log10(dist) - 11
       
       #air abs
       A_abs = np.zeros([8,1])
       
       #ground abs
       A_gr = np.zeros([8,1])
       
       
       # barrier
       A_bar = np.zeros([8,1])
       
       receiver.addPressure(Spectrum(source.power.linear \
                                     + A_div + A_gr + A_abs + A_bar ))
       
       
    def _isoAirAbsPerMetre(self):
       
       
       
       
       pass
   
    
    def _ISO_GroundAbsorption(dp, Gs, Gm, Gr, hs, hr):
      
        if dp <= 30 * (hs + hr):
             q = 0
        else:
             q = 1 - ((30 * (hs + hr)) / dp) 
     
        A_s = np.zeros([8,1])
        A_r = np.zeros([8,1])
        A_m = np.zeros([8,1])
           
    
    #     Case 63
        A_s[0] = -1.5
        A_r[0] = -1.5
        A_m[0] = -3 * q ^ 2
    #     Case 125
        A_s[1] = -1.5 + Gs * ISO9613._Ground_a(hs, dp)
        A_r[1] = -1.5 + Gr * _Ground_a(hr, dp)
        A_m[1] = -3 * q * (1 - Gm)
    #     Case 250
        A_s[2] = -1.5 + Gs * _Ground_b(hs, dp)
        A_r[2] = -1.5 + Gr * _Ground_b(hr, dp)
        A_m[2] = -3 * q * (1 - Gm)
    #     Case 500
        A_s[3] = -1.5 + Gs * _Ground_c(hs, dp)
        A_r[3] = -1.5 + Gr * _Ground_c(hr, dp)
        A_m[3] = -3 * q * (1 - Gm)
    #     Case 1000
        A_s[4] = -1.5 + Gs * _Ground_d(hs, dp)
        A_r[4] = -1.5 + Gr * _Ground_d(hr, dp)
        A_m[4] = -3 * q * (1 - Gm)
    #    Case 2000, 4000, 8000
        A_s[5:7] = -1.5 * (1 - Gs)
        A_r[5:7] = -1.5 * (1 - Gr)
        A_m[5:7] = -3 * q * (1 - Gm)
            
    
        return  A_s + A_m + A_r
     
    
    
    def _Ground_a(h, dp):
         return 1.5 + 3 * np.exp(-0.12 * (h - 5) ^ 2) * (1 - np.exp(-dp / 50)) \
                 + 5.7 * np.exp(-0.09 * h ^ 2) * (1 - np.exp(-2.8 * 10 ^ (-6) * dp ^ 2))
    
    def _Ground_b(h, dp):
         return 1.5 + 8.6 * np.exp(-0.09 * h ^ 2) * (1 - np.exp(-dp / 50))
    
    def _Ground_c(h, dp):
        return 1.5 + 14 * np.exp(-0.46 * h ^ 2) * (1 - np.exp(-dp / 50))
    
    def _Ground_d(h, dp):
        return 1.5 + 5 * np.exp(-0.9 * h ^ 2) * (1 - np.exp(-dp / 50))
    

class Spectrum:

    linear = np.zeros([8,1])

    def __init__(self,linear):
        self.linear = linear


    def A(self):
        a_weighting = np.array([-26.2, -16.1, -8.6, -3.2, 0, 1.2, 1, -1.1])
        A = self.linear + a_weighting
        return np.log10(np.sum( np.power(A,10) ) )
    

class NoiseSource:
     
    
    def __init__(self,location):
        self.location = location
        self.power = Spectrum
        
    def setPower(self,power):
        self.power = power
    
    def setPressure(self, pressure, dist, sphere):
        self.power.linear = pressure.linear + 20*np.log10(dist) - 10*np.log10(sphere) + 11
         
    def __str__(self):
        return "SRC: location={0}, power={1}".format(self.location, self.power.linear)



class NoiseReceiver:
     
    
    def __init__(self,location):
        self.location = location
        self.pressure = Spectrum(np.zeros([8,1]))
        
    def __str__(self):
        return "RCV: location={0}, pressure={1}".format(self.location, self.pressure.linear)

       
    def clear(self):
        self.pressure = Spectrum(np.zeros([8,1]))
    
    
    # possibly should add each contribution as a list to get partial levels
    def addPressure(self, pressure):
        
        if self.pressure.linear[0] == 0:
            self.pressure = pressure
        else:
            self.pressure.linear = 10*np.log10( np.power( self.pressure.linear/10, 10) \
                                               + np.power(pressure.linear/10, 10 ) )


class Path:
    absorption = []
    barrier = 0
    propagation_height = []



if __name__ == "__main__":
    
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    iso = ISO9613() # create new ISO instance
    
    logging.debug(iso)
    
    # create a source
    s_loc = Point(0,0,1.5)
    s_spec = Spectrum(np.array([60,60,60,60,60,60,60,60]))
    
    source = NoiseSource(location=s_loc)
    source.setPressure(pressure=s_spec,dist=10,sphere=0.5)
    print(source)
#    print("Source sound power. Should be 94 dB: {0}".format(source.power.A()))
    

    # create a receiver
    r_loc = Point(100,0,1.5)
    receiver = NoiseReceiver(r_loc)
    receiver.clear()

    print("")
    print("Before calc")
    print(receiver)

    iso.calc(source,None,receiver)

    print("")
    print("After calc")
    print(receiver)
    print(receiver.pressure.A())
        




