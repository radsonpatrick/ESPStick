from utime import sleep
from fonts import vga1_16x32 as font
import webrepl
import network 
from config  import WEBREPL_PASS,WIFI_SSID,WIFI_PASS
class Device:
    def __init__(self,gpio):
        self.pin = gpio
    
    def toggle(self):
        if self.pin.value() == 0 :
            self.pin.value(1)
        else:
            self.pin.value(0)
        
    def stat(self):
        if self.pin.value() :
            status = False
        else:
            status = True
        return status

class Wifi: 
    def __init__(self):
        from config import DISPLAY
        self.display = DISPLAY
        self.wifi_ap = network.WLAN(network.AP_IF)
        self.wifi_sta = network.WLAN(network.STA_IF)

    def ip(self):
        if self.mode() == 0:
            return '192.168.4.1'
        else:
            return self.wifi_sta.ifconfig()[0]
    
    def status(self):
        if self.wifi_sta.isconnected() : 
            return 'Connected'
        else: 
            return 'Disconnected'
    
    def mode(self,set_mode=None):
        self.set_mode = set_mode
        
        if self.set_mode == 'AP':
            self.to_ap()
        
        elif self.set_mode =='CLIENT':
            self.to_client()
        
        if not self.set_mode :
            if self.wifi_ap.active():
                return 0
        
            elif self.wifi_sta.active():
                return 1
    
    def scan(self):
        
        print('start_scanning')
        a = []
        security_dict = {
            0:'Open',
            1:'WEP',
            2:'WPA-PSK',
            3:'WPA2-PSK',
            4:'WPA/WPA2-PSK',
        }
        self.mode_status = 'AP' if self.mode() == 0 else 'STA'

        self.wifi_ap.active(False)
        self.wifi_sta.active(True)
        for result in self.wifi_sta.scan() :
            a.append({
                result[0].decode('utf-8')[:11]:
                {
                 'rssi':result[3],
                 'ch':result[2],
                 'type':security_dict.get(result[4]),
                 'hidden':'yes' if result[5] else 'no'
                }
             })
        if self.mode_status == 'AP':
            self.wifi_sta.active(False)
            self.wifi_ap.active(True)
            self.wifi_ap.config(essid='ESP32', password='12345678')
        return a 
        
    def to_ap(self):
        print('ap_mode starting')
        self.wifi_sta.active(False)
        self.wifi_ap.active(True)
        self.wifi_ap.config(essid='ESP32', password='12345678')
        webrepl.start(password=WEBREPL_PASS)
        self.display.fill(0)
        text_y = abs(int((self.display.height()/2)-((2*font.HEIGHT)/2)))
        self.display.text(font,'Started AP Mode',int((self.display.width()/2)-((len('Started AP Mode')*font.WIDTH)/2)),text_y)
        sleep(2)
        self.display.fill(0)
    def to_client(self):
        self.status = False
        for i in range(0,5):
            
            self.wifi_sta.active(True)
            self.display.fill(0)
            text_y = abs(int((self.display.height()/2)-((2*font.HEIGHT)/2)))
            self.display.text(font,'Connecting to :',int((self.display.width()/2)-((len('Connecting to :')*font.WIDTH)/2)),text_y)
            self.display.text(font,WIFI_SSID,int((self.display.width()/2)-((len(WIFI_SSID)*font.WIDTH)/2)),
                                        text_y+font.HEIGHT)
            print(f'tentando_conectar no wifi:{WIFI_SSID}')
            self.wifi_sta.connect(WIFI_SSID,WIFI_PASS)
            sleep(2)
            if self.wifi_sta.isconnected():
                text_y = abs(int((self.display.height()/2)-((1*font.HEIGHT)/2)))
                self.display.fill(0)
                print('connectou')
                webrepl.start(password=WEBREPL_PASS)
                #sleep(1)
                self.display.fill_rect(40, 78, 160, 80, 0x07E0)
                self.display.text(font,'Connected',int((self.display.width()/2)-((len('Connected')*font.WIDTH)/2)),text_y,0,0x07E0)
                sleep(2)
                self.display.fill(0)
                self.status = True
                break
            self.wifi_sta.active(False)
        if self.status == False:
            self.to_ap()
