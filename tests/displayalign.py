import os
import sys
import inspect
import RPi.GPIO as GPIO
import subprocess

from time import sleep
from PIL import Image

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import config
import utils

display_config = config.conf["atm"]["display"]
display = getattr(__import__("displays", fromlist=[display_config]), display_config)

print(display)

utils.check_epd_size()

#systemctl is-active LightningATM.service -> 0 = active 768 = inactive
#sudo systemctl stop LightningATM.service -> inactive

# os.system will return 0 for service is active else inactive.
status = os.system('systemctl is-active --quiet LightningATM.service')

startService = 0

if status == 0:
    print("LightningATM.service is started and will be stopped now.")
    os.system('sudo systemctl stop LightningATM.service')
    startService = 1
else:
    print("LightningATM.service is not started, display test starts now.")

display.update_startup_screen()
time.sleep(3)
display.update_qr_request()
time.sleep(3)
display.update_qr_failed()
time.sleep(3)
display.update_payout_screen()
time.sleep(3)
display.update_payment_failed()
time.sleep(3)
display.update_thankyou_screen()
time.sleep(3)
display.update_nocoin_screen()
time.sleep(3)
display.update_lnurl_generation()
time.sleep(3)
display.update_shutdown_screen()
time.sleep(3)
display.update_wallet_scan()
time.sleep(3)
display.update_lntxbot_balance(123)
time.sleep(3)
display.update_btcpay_lnd()
time.sleep(3)

qrImage = Image.new('1', (122, 122), 255)
display.draw_lnurl_qr(qrImage)
time.sleep(3)
display.update_amount_screen()
time.sleep(3)
display.update_lnurl_cancel_notice()
time.sleep(3)
display.update_blank_screen()
time.sleep(3)
display.init_screen(0)
time.sleep(3)

if startService == 1:
    print("LightningATM.service will be started now.")
    os.system('sudo systemctl start LightningATM.service')