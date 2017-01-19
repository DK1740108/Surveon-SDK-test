# Surveon SDK, AutoTest Plan.
# Dreizehn.Wei
# Fun(): param_General

import os, sys, time, webbrowser, re
import cfg
import pyping, requests

g_File    = "../report/param.cgi.list.General.txt"
g_iniFile = "../setting.ini"
g_CAM_IP  = ""
g_URL     = ""
g_USER    = cfg.cfg_GetKey(g_iniFile, "CAM_UserInfo", "USER")
g_PWD     = cfg.cfg_GetKey(g_iniFile, "CAM_UserInfo", "PWD")

def check_error(out_page):
	ret1 = re.search("error", out_page, re.IGNORECASE)
	ret2 = re.search("failed", out_page, re.IGNORECASE)
	if bool(ret1) | bool(ret2):
		return "Failed"
	else:
		return "Success"

def set_Report(FileName, rURL, page):
	file = open(FileName, "a+")
	file.write("[URL]: " + rURL + "\n")
	file.write("[Ret]: " + check_error(page) + "\n")
	file.write(page + "\n")
	file.close()

def get_param_list(CAM_IP):
	global g_CAM_IP
	global g_URL
	g_CAM_IP = CAM_IP
	g_URL = "http://" + str(CAM_IP) + "/surveon-cgi/param.cgi"
	payload = {"action":"list"}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	file = open("../report/param.cgi.list.txt", "w")
	file.write(the_page)
	file.close()
	file = open("../report/param.cgi.list.txt", "r")
	for line in file.readlines():
		ret = line.find("root.Brand.ProdShortName")
		if ret == 0:
			line = line.strip('\n')
			line = line.strip(' ')
			filedata = line.split("=")
			cfg.cfg_SetKey(g_iniFile, "Basic", "HostName", filedata[1]+"aa")
			cfg.cfg_SetKey(g_iniFile, "Basic", "CameraName", filedata[1]+"bb")
			break
	file.close()

def p_update_Lang():
	Lang = cfg.cfg_GetKey(g_iniFile, "Properties", "Language")
	global g_URL
	global g_USER
	global g_PWD
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Properties.System.Language":Lang}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	file = open(g_File, "w")
	file.write("[URL]: " + response.url + "\n")
	file.write("[Ret]: " + check_error(the_page) + "\n")
	file.write(the_page + "\n")
	file.close()

def p_list_Brand():
	global g_URL
	groupArray = ["Brand.Brand", "Brand.ProdFullName", "Brand.ProdNbr", "Brand.ProdShortName", "Brand.ProdType",
	              "Brand.WebURL", "Brand.plat_type/camtype/OEM_model_name"]
	file = open(g_File, "a")
	for group_T in groupArray:
		payload = {"action":"list", "group":group_T}
		response = requests.get(g_URL, params=payload)
		the_page = response.text
		file.write("[URL]: " + response.url + "\n")
		file.write("[Ret]: " + check_error(the_page) + "\n")
		file.write(the_page + "\n")
	file.close()

def p_update_Basic_HName():
	Name = cfg.cfg_GetKey(g_iniFile, "Basic", "HostName")
	global g_URL
	global g_USER
	global g_PWD
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.HostName":Name}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)

def p_update_Basic_CName():
	Name = cfg.cfg_GetKey(g_iniFile, "Basic", "CameraName")
	global g_URL
	global g_USER
	global g_PWD
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.CameraName":Name}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)

def p_list_AccessLogin():
	global g_URL
	payload = {"action":"list", "group":"Layout.FreeLiveview"}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)

def p_list_UserAccount():
	global g_CAM_IP
	g_URL = "http://" + str(g_CAM_IP) + "/surveon-cgi/pwdgrp.cgi"
	payload = {"action":"get"}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)

def p_update_UserAccount():
	global g_CAM_IP
	g_URL = "http://" + str(g_CAM_IP) + "/surveon-cgi/pwdgrp.cgi"
	user = cfg.cfg_GetKey(g_iniFile, "User", "admin_act")
	pwd = cfg.cfg_GetKey(g_iniFile, "User", "admin_pwd")
	payload = {"action":"add", "user":user, "pwd":pwd, "grp":"Administrator"}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	user = cfg.cfg_GetKey(g_iniFile, "User", "operator_act")
	pwd = cfg.cfg_GetKey(g_iniFile, "User", "operator_pwd")
	payload = {"action":"add", "user":user, "pwd":pwd, "grp":"Operator"}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	user = cfg.cfg_GetKey(g_iniFile, "User", "operator_act")
	pwd = cfg.cfg_GetKey(g_iniFile, "User", "operator_pwd")
	payload = {"action":"remove", "user":user, "pwd":pwd, "grp":"Operator"}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)

def p_list_Date():
	global g_CAM_IP
	g_URL = "http://" + str(g_CAM_IP) + "/surveon-cgi/date.cgi"
	payload = {"action":"get"}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)

def p_update_Date():
	global g_CAM_IP
	global g_USER
	global g_PWD
	g_URL = "http://" + str(g_CAM_IP) + "/surveon-cgi/date.cgi"
	payload = {"action":"set", "USER":g_USER, "PWD":g_PWD, "year":"2008", "month":"5", "day":"10", "hour":"10", "minute":"10", "second":"10"}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)

def p_update_TimeZone():
	Zone = cfg.cfg_GetKey(g_iniFile, "Time", "TimeZone")
	global g_URL
	global g_USER
	global g_PWD
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Time.TimeZone":Zone}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)

def p_update_NTPSource():
	Source = cfg.cfg_GetKey(g_iniFile, "Time", "SyncSource")
	global g_URL
	global g_USER
	global g_PWD
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Time.SyncSource":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)

def p_update_NTPServer():
	Source = cfg.cfg_GetKey(g_iniFile, "Time", "NTPServer")
	global g_URL
	global g_USER
	global g_PWD
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Time.NTP.Server":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
