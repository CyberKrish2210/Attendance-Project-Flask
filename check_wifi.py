import pywifi
import time
def get_signal_strength(ssid_to_check):
    try:
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        iface.scan()
        time.sleep(2)
        scan_results = iface.scan_results()

        for result in scan_results:
            if result.ssid == ssid_to_check:
                return result.signal
        return None
    except pywifi.PyWiFiException as e:
        return str(e)

ssid_to_check = "iPhone"
signal_strength = get_signal_strength(ssid_to_check)
print((signal_strength))