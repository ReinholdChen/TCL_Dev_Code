# -*- encoding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
#import matplotlib.pyplot as plt
import json
import csv
import os
import zipfile
import datetime
import xlrd
import io  
import sys 
#from sendEmail import SendEmail

# COOKIES_PATH = "./Cookies.json"
# REPORT_PATH = '../Report'
# CURRENT_DATE = datetime.datetime.today().strftime("%Y-%m-%d")
# DAILY_REPORT_PATH = '/'.join([REPORT_PATH, CURRENT_DATE])
# ZIPFILE_PATH = '../Report/{}_Report.zip'.format(DAILY_REPORT_PATH)
# if not os.path.exists(DAILY_REPORT_PATH):
# 		os.mkdir(DAILY_REPORT_PATH)
# ANALYSIS_PATH = '/'.join([DAILY_REPORT_PATH, 'Analysis.xls'])
"""
New = N
More Info = M
Failed = F
Ready to release = R
Invalid 
Ready to test = T
Assigned = A
Ready to Deploy = D
SCCB review = S
Closed = C

"""

def parse_data():

	with open(COOKIES_PATH) as cookie:
		Cookies = json.load(cookie)
	return Cookies

def get_id(url, header):

	response = requests.get(url, headers=header)
	html = response.text
	soup = BeautifulSoup(html, 'lxml')
	issue_id = soup.findAll('td',{'class': 'column-id'})
	return issue_id

def get_status(url, header):

	status = []
	response = requests.get(url, headers=header)
	html = response.text
	soup = BeautifulSoup(html, 'lxml')
	issue_status = soup.findAll('td', {'class': 'column-status'})
	for each in issue_status:
		p = each.find('span').string
		status.append(p)
	return status

def get_severity(url, header):

	severity = []
	response = requests.get(url, headers=header)
	html = response.text
	soup = BeautifulSoup(html, 'lxml')
	issue_severity = soup.findAll('td', {'class': 'column-severity'})
	for each in issue_severity:
		severity.append(each.string)
	return severity

def get_date(url, header):
	submit_date = []
	due_date = []
	last_modified_date = []
	response = requests.get(url, headers=header)
	html = response.text
	soup = BeautifulSoup(html, 'lxml')
	issue_submit_date = soup.findAll('td',{'class': 'column-date-submitted'})
	issue_due_date = soup.findAll('td', {'class': 'column-due-date'})
	issue_last_modified_date = soup.findAll('td', {'class': 'column-last-modified'})

	for each in issue_submit_date:
		submit_date.append(each.string)
	for each in issue_due_date:
		due_date.append(each.string)
	for each in issue_last_modified_date:
		last_modified_date.append(each.string)
	return submit_date, due_date, last_modified_date

def plot_SubmitDate_DI(status, severity, submit_date, project):

	ss_submit = list(zip(status, severity,submit_date))
	unique_submit_date = set(submit_date)


	count_Open_S = dict(zip(unique_submit_date,[0 for _ in range(len(unique_submit_date))]))
	count_Open_A = dict(zip(unique_submit_date,[0 for _ in range(len(unique_submit_date))]))
	count_Open_B = dict(zip(unique_submit_date,[0 for _ in range(len(unique_submit_date))]))
	count_Open_C = dict(zip(unique_submit_date,[0 for _ in range(len(unique_submit_date))]))
	count_Open_D = dict(zip(unique_submit_date,[0 for _ in range(len(unique_submit_date))]))


	count_Closed_S = dict(zip(unique_submit_date,[0 for _ in range(len(unique_submit_date))]))
	count_Closed_A = dict(zip(unique_submit_date,[0 for _ in range(len(unique_submit_date))]))
	count_Closed_B = dict(zip(unique_submit_date,[0 for _ in range(len(unique_submit_date))]))
	count_Closed_C = dict(zip(unique_submit_date,[0 for _ in range(len(unique_submit_date))]))
	count_Closed_D = dict(zip(unique_submit_date,[0 for _ in range(len(unique_submit_date))]))

	count_MoreInfo_S = dict(zip(unique_submit_date,[0 for _ in range(len(unique_submit_date))]))
	count_MoreInfo_A = dict(zip(unique_submit_date,[0 for _ in range(len(unique_submit_date))]))
	count_MoreInfo_B = dict(zip(unique_submit_date,[0 for _ in range(len(unique_submit_date))]))
	count_MoreInfo_C = dict(zip(unique_submit_date,[0 for _ in range(len(unique_submit_date))]))
	count_MoreInfo_D = dict(zip(unique_submit_date,[0 for _ in range(len(unique_submit_date))]))

	for i in ss_submit:
		if (i[0] == "N" or i[0] == "M" or i[0] == "F" or i[0] == "R" or i[0] == "T" or i[0] == "A" or i[0] == "S") and i[1] == "S":
			count_Open_S[i[2]] += 1
		if (i[0] == "N" or i[0] == "M" or i[0] == "F" or i[0] == "R" or i[0] == "T" or i[0] == "A" or i[0] == "S") and i[1] == "A":
			count_Open_A[i[2]] += 1
		if (i[0] == "N" or i[0] == "M" or i[0] == "F" or i[0] == "R" or i[0] == "T" or i[0] == "A" or i[0] == "S") and i[1] == "B":
			count_Open_B[i[2]] += 1
		if (i[0] == "N" or i[0] == "M" or i[0] == "F" or i[0] == "R" or i[0] == "T" or i[0] == "A" or i[0] == "S") and i[1] == "C":
			count_Open_C[i[2]] += 1
		if (i[0] == "N" or i[0] == "M" or i[0] == "F" or i[0] == "R" or i[0] == "T" or i[0] == "A" or i[0] == "S") and i[1] == "D":
			count_Open_D[i[2]] += 1


		if i[0] == "C" and i[1] == "S":
			count_Closed_S[i[2]] += 1
		if i[0] == "C" and i[1] == "A":
			count_Closed_A[i[2]] += 1
		if i[0] == "C" and i[1] == "B":
			count_Closed_B[i[2]] += 1
		if i[0] == "C" and i[1] == "C":
			count_Closed_C[i[2]] += 1
		if i[0] == "C" and i[1] == "D":
			count_Closed_D[i[2]] += 1

		if i[0] == "M" and i[1] == "S":
			count_MoreInfo_S[i[2]] += 1
		if i[0] == "M" and i[1] == "A":
			count_MoreInfo_A[i[2]] += 1
		if i[0] == "M" and i[1] == "B":
			count_MoreInfo_B[i[2]] += 1
		if i[0] == "M" and i[1] == "C":
			count_MoreInfo_C[i[2]] += 1
		if i[0] == "M" and i[1] == "D":
			count_MoreInfo_D[i[2]] += 1

	sorted_submit_date = sorted(unique_submit_date)

	y_open_S, y_open_A, y_open_B, y_open_C, y_open_D, open_di = [],[],[],[],[],[]
	y_closed_S, y_closed_A, y_closed_B, y_closed_C, y_closed_D, closed_di = [],[],[],[],[],[]
	y_MoreInfo_S, y_MoreInfo_A, y_MoreInfo_B, y_MoreInfo_C, y_MoreInfo_D, MoreInfo_di = [],[],[],[],[],[]
	y_open_total = []

	date = []
	for i in range(len(sorted_submit_date)):
		if count_Open_S[sorted_submit_date[i]] != 0 or count_Open_A[sorted_submit_date[i]] != 0 or count_Open_B[sorted_submit_date[i]] != 0 or count_Open_C[sorted_submit_date[i]] != 0 or count_Open_D[sorted_submit_date[i]] != 0:
			date.append(sorted_submit_date[i])

	for i in range(len(date)):
	    y_open_S.append(count_Open_S[date[i]])
	    y_open_A.append(count_Open_A[date[i]])
	    y_open_B.append(count_Open_B[date[i]])
	    y_open_C.append(count_Open_C[date[i]])
	    y_open_D.append(count_Open_D[date[i]])
	    open_di.append(y_open_S[i]*10 + y_open_A[i]*3 + y_open_B[i]*1 + y_open_C[i]*0.5)
	    y_open_total.append(y_open_S[i] + y_open_A[i] + y_open_B[i] + y_open_C[i] + y_open_D[i])

	    y_closed_S.append(count_Closed_S[date[i]])
	    y_closed_A.append(count_Closed_A[date[i]])
	    y_closed_B.append(count_Closed_B[date[i]])
	    y_closed_C.append(count_Closed_C[date[i]])
	    y_closed_D.append(count_Closed_D[date[i]])
	    closed_di.append(y_closed_S[i]*10 + y_closed_A[i]*3 + y_closed_B[i]*1 + y_closed_C[i]*0.5)

	    y_MoreInfo_S.append(count_MoreInfo_S[date[i]])
	    y_MoreInfo_A.append(count_MoreInfo_A[date[i]])
	    y_MoreInfo_B.append(count_MoreInfo_B[date[i]])
	    y_MoreInfo_C.append(count_MoreInfo_C[date[i]])
	    y_MoreInfo_D.append(count_MoreInfo_D[date[i]])
	    MoreInfo_di.append(y_MoreInfo_S[i]*10 + y_MoreInfo_A[i]*3 + y_MoreInfo_B[i]*1 + y_MoreInfo_C[i]*0.5) 



	plt.figure(figsize=(80,50))
	plt.subplots_adjust(left = 0.05, right = 0.98, bottom = 0.15, top = 0.96)
	plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
	plt.title('BUG趋势图 << 项目 -- {} >>'.format(project), fontsize = 90, fontweight = "black")
	plt.xlabel("Bug提交日期", fontweight = "black", fontsize = 90)
	plt.ylabel("数量级", fontweight = "black", fontsize = 90)
	plt.xticks(rotation = 60, fontsize = 60)
	plt.yticks(fontsize = 75)
	plt.plot(date,open_di, color = 'green', label='DI', linewidth = 20, marker = '*', markerfacecolor = 'cyan', markersize = 35)
	plt.plot(date, y_open_total, color = "red", label="Open Total", linewidth = 20, marker = '*', markerfacecolor = 'cyan', markersize = 35)
	plt.plot(date, y_open_S, color = "blue", label="Open S", linewidth = 20, marker = 'o', markerfacecolor = 'cyan', markersize = 30)
	plt.plot(date, y_open_A, color = "orange", label="Open A", linewidth = 20, marker = 'o', markerfacecolor = 'cyan', markersize = 30)
	plt.plot(date,y_open_B, color = 'violet', label='Open B', linewidth = 20, marker = 'o', markerfacecolor = 'cyan', markersize = 30)
	plt.plot(date,y_open_C, color = 'deepskyblue',label='Open C', linewidth = 20, marker = 'o', markerfacecolor = 'cyan', markersize = 30)
	
	plt.legend(fontsize = 80)
	for i,j in zip(date, open_di):
		if j != 0:
	    		plt.text(i, j+0.03, '%.0f'%j, ha = 'center', va = 'bottom', fontsize = 70, fontweight = "black", rotation = -30)

	for i,j in zip(date, y_open_B):
		if j != 0:
	    		plt.text(i, j+0.03, '%.0f'%j, ha = 'center', va = 'bottom', fontsize = 70, fontweight = "black", rotation = -30)

	for i,j in zip(date, y_open_C):
		if j != 0:
	    		plt.text(i, j+0.03, '%.0f'%j, ha = 'center', va = 'bottom', fontsize = 70, fontweight = "black", rotation = -30)

	for i,j in zip(date, y_open_S):
		if j != 0:
	    		plt.text(i, j+0.03, '%.0f'%j, ha = 'center', va = 'bottom', fontsize = 70, fontweight = "black", rotation = -30)

	for i,j in zip(date, y_open_A):
		if j != 0:
	    		plt.text(i, j+0.03, '%.0f'%j, ha = 'center', va = 'bottom', fontsize = 70, fontweight = "black", rotation = -30)

	for i,j in zip(date, y_open_total):
		if j != 0:
	    		plt.text(i, j+0.03, '%.0f'%j, ha = 'center', va = 'bottom', fontsize = 70, fontweight = "black", rotation = -30)
	# plt.tight_layout()
	
	plt.savefig(REPORT_PATH + '/{}/{}__BUG趋势图.png'.format(CURRENT_DATE, project))
	plt.close()


def zip_file(from_dir, to_zip):

	report_zipfile = zipfile.ZipFile(to_zip, 'w', zipfile.ZIP_DEFLATED)
	for file_name in os.listdir(from_dir):
		file_path = from_dir + '/' + file_name
		report_zipfile.write(file_path)
	report_zipfile.close()



def main():
	# url = "http://mantis.tclking.com:8090/view_all_bug_page.php"
	# CookiesList = parse_data()
	# for i in range(len(CookiesList)):
	# 		response = requests.get(url,headers=CookiesList[i]["cookie"])
	# 		html = response.text
	# 		status = get_status(url, CookiesList[i]["cookie"])
	# 		severity = get_severity(url, CookiesList[i]["cookie"])
	# 		submit_date, due_date, last_modified_date = get_date(url, CookiesList[i]["cookie"])
	# 		plot_SubmitDate_DI(status, severity, submit_date, project=CookiesList[i]["Project"])
	
	# zip_file(REPORT_PATH, ZIPFILE_PATH)


	# From = 'deyan.chen@tcl.com'
	# To = [	'deyan.chen@tcl.com'
	# 		# "林丰<feng5.lin@tcl.com>",
 #   #          "吕天榆<tianyu.lv@tcl.com>",
 #   #          "林华坚<huajian.lin@tcl.com>",
 #   #          "陈玉洪<yuhong3.chen@tcl.com>",
 #   #          "李祖豪<zuhao.li@tcl.com>"
 #          ]
	# message_text_html = open("./email_config.html", encoding="utf-8").read()
	# send_email = SendEmail(From, To, message_text_html)
	# send_email.send_result_using_email()

	# url = "http://mantis.tclking.com:8090/view_all_bug_page.php"
	# response = requests.get(url, verify=False)
	# print(response)
	# html = response.text
	# print(html)
	# soup = BeautifulSoup(html, 'html.parser')
	# #改变标准输出的默认编码 
	# #utf-8中文乱码
	# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
	# print(soup)

	# url = "http://mantis.tclking.com:8090/view_all_bug_page.php"
	# response = requests.get(url, verify=False)
	# html = response.text
	# soup = BeautifulSoup(html, 'html.parser')
	# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
	# print(soup)
	# issue_id = soup.findAll('td',{'class': 'column-id'})
	# print(issue_id)
	# a = "{\"a\":1,\"b\":2,\"c\":3}"
	# b = a.findAll('[a-z]')
	# print(b)

	import random
	import numpy as np
	 
	a = random.randint(10,20)
	res = np.random.randn(5)
	ret = random.random()
	print("正整数:"+str(a))
	print("5个随机小数:"+str(res))
	print("0-1随机小数:"+str(ret))

if __name__ == "__main__":
	main()

    
    
