#!/usr/bin/python
import datetime, sys
sys.path.append('/home/pi/Pigrow/scripts/')
import pigrow_defs

for argu in sys.argv[1:]:
    if argu == '-h' or argu == '--help':
        print("Pigrow Lamp switch")
        print("")
        print("This turns the Lamp OFF")
        print("To use this program you must have the devices GPIO and wiring direction")
        print("set in the pigrow configuration file /config/pigrow_config.txt")
        print("use the setup tool /scripts/config/setup.py or the remote gui")
        sys.exit()

def lamp_off(set_dic, switch_log):
    script = 'lamp_off.py'
    msg =("\n")
    msg +=("      #############################################\n")
    msg +=("      ##         Turning the lamp - OFF        ##\n")
    if 'gpio_lamp' in set_dic and not str(set_dic['gpio_lamp']).strip() == '':
        gpio_pin = int(set_dic['gpio_lamp'])
        gpio_pin_on = set_dic['gpio_lamp_on']
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(gpio_pin, GPIO.OUT)
        if gpio_pin_on == "low":
            GPIO.output(gpio_pin, GPIO.HIGH)
            gpio_pin_dir = 'high'
        elif gpio_pin_on == "high":
            gpio_pin_dir = 'low'
            GPIO.output(gpio_pin, GPIO.LOW)
        else:
            msg +=("      !!       CAN'T DETERMINE GPIO DIRECTION   !!\n")
            msg +=("      !!  run config program or edit config.txt !!\n")
            msg +=("      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
            pigrow_defs.write_log(script, 'Failed - no direction set in config', switch_log)
            return msg
    else:
        msg +=("      !!               NO lamp SET            !!\n")
        msg +=("      !!  run config program or edit config.txt !!\n")
        msg +=("      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        pigrow_defs.write_log(script, 'Failed - due to none set in config', switch_log)
        return msg

    msg +=("      ##            by switching GPIO "+str(gpio_pin)+" to "+gpio_pin_dir+"  ##\n")
    msg +=("      #############################################\n")
    pigrow_defs.write_log(script, 'lamp turned off', switch_log)
    return msg

if __name__ == '__main__':

    ### default settings
    loc_dic = pigrow_defs.load_locs("/home/pi/Pigrow/config/dirlocs.txt")
    set_dic = pigrow_defs.load_settings(loc_dic['loc_settings'], err_log=loc_dic['err_log'],)
    msg = lamp_off(set_dic, loc_dic['loc_switchlog'])
    print msg
