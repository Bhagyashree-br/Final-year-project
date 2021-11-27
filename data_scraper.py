"""This script queries the Real-time air-quality data API made available on data.gov.in 

To use this script, go to data.gov.in, sign up and generate an API key.
Once you have an API key replace the placeholder <API KEY> in the data_url with your API key and run"""
import requests 
import time
import os.path
import datetime
import winsound

def make_sound(seconds):
    for i in range(seconds):
        winsound.Beep(2000,500)
        time.sleep(0.5)

data_url = "https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69?api-key=<API KEY>&format=csv&offset=0&limit=2000"
  
while(True):
    try:
        currentDT = datetime.datetime.now()
        r = requests.get(data_url)
        data = str(r.content).split(",")
        filename = data[16].replace(":",",").strip('\"')
        if((currentDT - datetime.timedelta(hours = 1, minutes = 30)).strftime("%p") == "PM"):
            filename = filename[:11]+str(int(filename[11:13])+12)+filename[13:]
        middlename=""
        index=0
        while(os.path.isfile(filename+middlename+".csv")):
            index+=1
            middlename="("+str(index)+")"
        filename = filename+middlename+".csv"

        print("Collected data at ",currentDT.strftime("%H:%M:%S"),".")
        with open(filename, 'wb') as f: 
            f.write(r.content)

        if len(r.content) < 60000:
            print("Received Bad Data... Data Stored in ",filename,"... Trying Again")
            next_time = currentDT + datetime.timedelta(minutes = 5)
            print("Waiting till ",next_time.strftime("%H:%M:%S")," to collect again.")
            time.sleep(300)
        else:
            next_time = currentDT + datetime.timedelta(minutes = 30)
            print("Waiting till ",next_time.strftime("%H:%M:%S")," to collect again.")
            time.sleep(1800)

    except Exception as e:
        print(e)
        make_sound(45)

"""Script used to check if the 2 files downloaded in an hour by 
the scraper are same or not. You can delete the second fie if 
they are the same"""
import datetime
import os
time = datetime.datetime.strptime("01-04-2019 10,00,00", "%d-%m-%Y %H,%M,%S")
end = datetime.datetime.now() #datetime.datetime.strptime("28-03-2019 11,00,00", "%d-%m-%Y %H,%M,%S") 
while time < end:
    time_str = time.strftime("%d-%m-%Y %H,%M,%S")
    err = os.system("FC \""+time_str+"(1).csv\" \""+time_str+".csv\" > lol.txt")
    if err!=0:
        print(time_str," NOT SAFE TO DELETE",err)
    time += datetime.timedelta(hours=1)
