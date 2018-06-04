#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import datetime
import logging
import sys
import os
import ConfigParser

#          UTILES

def dateNow():
    return str(datetime.datetime.now())

def ConfigSectionMap(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            print ("skip: %s" % option)
        except:
            logWarning("exception on %s!" % option)
            dict1[option] = None
    return dict1

logging.basicConfig(filename='pythsappErrorLog.log',level=logging.DEBUG)
    #filename='pythsappErrorLog' + dateNow().replace(' ', '')+ '.log',level=logging.DEBUG)
    #

def logInfo(string):
    logging.info(dateNow() + ' - ' + string)

def logWarning(string):
    logging.warning(dateNow() + ' - ' + string)





#   PROGRAMA
def sendMessageOn(number , text ,driver):
    url = ('https://api.whatsapp.com/send?phone=54'+ str(number) +'&text=' + text.replace(" ", "%20"))
    driver.get(url)
    driver.find_element_by_id("action-button").click()

    time.sleep(15)

    driver.find_element_by_xpath("//div[@id='main']/footer/div/div[2]/div/div[2]").send_keys(Keys.RETURN)

    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                    'Timed out waiting for PA creation ' +
                                    'confirmation popup to appear.')

        alert = driver.switch_to.alert
        alert.accept()
        logInfo("alert accepted")
    except TimeoutException:
        print("no alert")

def sendImagenOn(number , imagePath ,driver):
    url = ('https://api.whatsapp.com/send?phone=54'+ str(number) +'&text=' + ' ')
    driver.get(url)
    driver.find_element_by_id("action-button").click()

    time.sleep(15)
    print imagePath
    try:
        driver.find_element_by_xpath("//div[@id='main']/header/div[3]/div/div[2]/div/span").click()
        time.sleep(5)
        driver.find_element_by_xpath("//div[@id='main']/header/div[3]/div/div[2]/span/div/div/ul/li/button").click()
        time.sleep(5)
        
        iPath = (str(os.getcwd()) + '\\' + imagePath) 
        print iPath
        driver.find_element_by_xpath("(//input[@type='file'])[2]").send_keys(iPath)
        time.sleep(5)
        driver.find_element_by_xpath("//div[@id='app']/div/div/div/div[2]/span/div/span/div/div/div[2]/span[2]/div/div").click()
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                    'Timed out waiting for PA creation ' +
                                    'confirmation popup to appear.')

        alert = driver.switch_to.alert
        alert.accept()
        logInfo("alert accepted")
    except TimeoutException:
        print("no alert")

def sendOn( number , text , driver):
    sendPicture = ConfigSectionMap("Picture") ["send"] 
    picture = ConfigSectionMap("Picture") ["picturename"]
    print picture

    if (sendPicture == 'True'):
        sendImagenOn(number, picture , driver)
    else:
        sendMessageOn(number, text, driver)


def closeLog():
    handlers = list(logging._handlerList)
    for handler in handlers:
	    logging._removeHandlerRef(handler)
	    handler.flush()
	    handler.close()

logInfo('Inicio de ejecución')

try:
  
    try:
        file = open('Enviar.txt','r') 
    except Exception:
        raise Exception ('Ocurrio un error en la apertura del archivo Enviar.txt. Verifique la existencia del archivo en el directorio raiz.') 

    try:
        config = ConfigParser.ConfigParser()
        config.read('Conf.ini') 
    except Exception:
        raise Exception ('Ocurrio un error en la apertura del archivo Config.txt. Verifique la existencia del archivo en el directorio raiz.') 

    text = file.readline()

    location = r'numeros.xlsx'


    try:
        df = pd.read_excel(location)
    except Exception:
        raise Exception ('Ocurrio un error en la apertura del archivo '+ location +'. Verifique la existencia del archivo en el directorio raiz.') 

    try:
        driver = webdriver.Chrome('.\\drivers\\chromedriver')
    except Exception:
        raise Exception ('Ocurrio un error en la apertura del archivo chromedriver. Verifique la existencia del archivo en el directorio raiz.')
    
    for number in (df['numeros']):
        try:
            sendOn( number, text, driver)      
        except Exception as espectedError:
            logWarning('Ocurrio un error en el envio del mnsaje al numero: ' + str(number) + '. Mas información en la siguiente linea:')
            logWarning(espectedError.args[0])
    driver.quit()
    closeLog()

except Exception as error:
    logWarning(error.args[0])
except:
    unexpectedException = sys.exc_info()[0]
    logWarning(str(unexpectedException))

logInfo('Fin de Ejecución')






    