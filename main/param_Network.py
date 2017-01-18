# Surveon SDK, AutoTest Plan.
# Dreizehn.Wei
# Fun(): param_Network

import os, sys, time, webbrowser, re
import cfg
import pyping, requests

g_File    = "../report/param.cgi.list.Network.txt"
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

def p_list_NetInterface(CAM_IP):
	global g_CAM_IP
	global g_URL
	g_CAM_IP = CAM_IP
	g_URL = "http://" + str(CAM_IP) + "/surveon-cgi/param.cgi"
	groupArray = ["SystemDevice", "Type", "Active", "Active.MACAddress", "Active.Active", "Active.IPAddress",
	              "Active.SubnetMask", "Active.Broadcast", "Active.IPV6Address", "Active.PrefixLengthV6"]
	file = open(g_File, "w")
	for group_T in groupArray:
		payload = {"action":"list", "group":"Network.Interface.I0."+group_T}
		response = requests.get(g_URL, params=payload)
		the_page = response.text
		file.write("[URL]: " + response.url + "\n")
		file.write("[Ret]: " + check_error(the_page) + "\n")
		file.write(the_page + "\n")
	file.close()

def p_update_BootProto():
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "BootProto")
	global g_URL
	global g_USER
	global g_PWD
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.Interface.I0.Link.BootProto":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.BootProto":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.BootProto":"dhcp"}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)

def p_update_IPAddress():
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "IPAddress")
	global g_URL
	global g_USER
	global g_PWD
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.Interface.I0.Manual.IPAddress":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	global g_CAM_IP
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.IPAddress":g_CAM_IP}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)

def p_update_SubnetMask():
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "SubnetMask")
	global g_URL
	global g_USER
	global g_PWD
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.Interface.I0.Manual.SubnetMask":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.SubnetMask":"255.255.0.0"}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)

def p_update_DefaultRouter():
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "DefaultRouter")
	global g_URL
	global g_USER
	global g_PWD
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.Interface.I0.Manual.DefaultRouter":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	global g_CAM_IP
	IP_array = g_CAM_IP.split(".")
	Source = IP_array[0] + "." + IP_array[1] + "." + IP_array[2] + ".254"
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.Interface.I0.Manual.DefaultRouter":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)

def p_list_IPandDNS():
	groupArray = ["Network.Resolver", "Network.Resolver.NameServer1", "Network.Resolver.NameServerList"]
	for group_T in groupArray:
		payload = {"action":"list", "group":group_T}
		response = requests.get(g_URL, params=payload)
		the_page = response.text
		set_Report(g_File, response.url, the_page)

def p_update_DNSServer():
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "DNSServer_1")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.DNSServer1":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "DNSServer_2")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.DNSServer2":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)

def p_update_PPPOE():
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "PPPoE_Enable")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.PPPoE.Enabled":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	Source_U = cfg.cfg_GetKey(g_iniFile, "Network", "PPPoE_USER")
	Source_P = cfg.cfg_GetKey(g_iniFile, "Network", "PPPoE_PWD")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.PPPoE.UserName":Source_U, "Network.PPPoE.Password":Source_P}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)

def p_update_DDNS():
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "DDNS_Enable")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.DNSUpdate.Enabled":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "DDNS_Vendor")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.DNSUpdate.Vendor":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "DDNS_Name")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.DNSUpdate.DNSName":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "DDNS_PWD")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.DNSUpdate.Password":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)

def p_update_HttpPort():
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "HTTP_Port")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "System.HTTPPort":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "Live_Port")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "System.LiveViewPort":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)

def p_update_RTSP():
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "RTSP_SName")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.RTSP.StreamName1":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "RTSP_Port")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.RTSP.Port":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "RTSP_VPort")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.RTP.VideoPort":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "RTSP_APort")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.RTP.AudioPort":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "RTSP_PSize")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.RTP.R0.PacketSize":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)

def p_update_RTP():
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "RTP_McastEn")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.RTP.R0.AlwaysMulticast":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "RTP_MVPort1")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.RTP.R0.VideoPort":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "RTP_MVPort2")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.RTP.R0.VideoPort2":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "RTP_MAPort")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.RTP.R0.AudioPort":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "RTP_MGVAdress")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.RTP.R0.VideoAddress":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "RTP_MGAAdress")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.RTP.R0.AudioAddress":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)
	
	Source = cfg.cfg_GetKey(g_iniFile, "Network", "RTP_MTTL")
	payload = {"action":"update", "USER":g_USER, "PWD":g_PWD, "Network.RTP.R0.TTL":Source}
	response = requests.get(g_URL, params=payload)
	the_page = response.text
	set_Report(g_File, response.url, the_page)


