# Surveon SDK, AutoTest Plan.
# Dreizehn.Wei
# v0.0.1: 2017/01/10

import os, sys, time, webbrowser
import pyping, requests
import cfg
import param_General
import param_Network

# Record Start: Date & Time
# ===========================================================================
nowDate = time.strftime("%Y-%m-%d")
nowTime = time.strftime("%H:%M:%S")
setDateTime = nowDate + " " + nowTime
cfg.cfg_SetKey("../setting.ini", "AutoTest_Date", "S_Time", setDateTime)

# main()
# ===========================================================================
CAM_IP = raw_input("Please input the IP address: ")
CAM_IP_R = pyping.ping(str(CAM_IP))
if CAM_IP_R.ret_code == 0:
	pingstatus = "Network Active"
else:
	pingstatus = "Network Error"
print("IP address: " + CAM_IP + " - " + pingstatus)
print("==========================================")
time.sleep(1)

if CAM_IP_R.ret_code == 0:
	print("Start AutoTest Plan...")
	print("==========================================")
	print("1. param_General..."),
	param_General.get_param_list(CAM_IP)
	param_General.p_update_Lang()
	param_General.p_list_Brand()
	param_General.p_update_Basic_HName()
	print("30%.."),
	param_General.p_update_Basic_CName()
	param_General.p_list_AccessLogin()
	param_General.p_list_UserAccount()
	param_General.p_update_UserAccount()
	param_General.p_list_Date()
	print("60%.."),
	param_General.p_update_Date()
	param_General.p_update_TimeZone()
	param_General.p_update_NTPSource()
	param_General.p_update_NTPServer()
	print("100%.. OK")
	print("2. param_Network..."),
	param_Network.p_list_NetInterface(CAM_IP)
	param_Network.p_update_BootProto()
	param_Network.p_update_IPAddress()
	param_Network.p_update_SubnetMask()
	print("30%.."),
	param_Network.p_update_DefaultRouter()
	param_Network.p_list_IPandDNS()
	param_Network.p_update_DNSServer()
	param_Network.p_update_PPPOE()
	param_Network.p_update_DDNS()
	param_Network.p_update_HttpPort()
	print("60%.."),
	param_Network.p_update_RTSP()
	param_Network.p_update_RTP()
	print("100%.. OK")
	print("==========================================")

# Record End: Date & Time
# ===========================================================================
nowDate = time.strftime("%Y-%m-%d")
nowTime = time.strftime("%H:%M:%S")
setDateTime = nowDate + " " + nowTime
cfg.cfg_SetKey("../setting.ini", "AutoTest_Date", "E_Time", setDateTime)
print("AutoTest is done... " + setDateTime)
time.sleep(3)