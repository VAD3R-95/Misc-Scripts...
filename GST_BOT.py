import requests
import pandas as pd
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from time import sleep

url = "https://findgst.in/"
client = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37",
           "referer": "https://findgst.in/",
           "origin": "https://findgst.in"
          }

df = pd.read_excel (r'file.xlsx') # GST file data


print("----------- Data Imported -----------")
print("\n")
print('Code$Name$GSTIN$Remarks$Trade_Name$Legal_Name$Registered_On$Similarity_Per')

for i in df.index:
   code  = str(df['Customer'][i])
   gstin = str(df['GSTIN'][i])
   name  = str(df['Name'][i])
   if len(gstin.strip()) == 15:
       #print(gstin)
       #sleep(5)
       first_req = client.get(url,headers=headers,verify=True)
       if first_req.status_code != 200:
          print('Code: '+str(first_req.status_code)+" !! Website Down !!")
          break
       soup = BeautifulSoup(first_req.text,'html.parser')
   
       csrf_middleware_token = str( soup.find("input",{"name":"csrfmiddlewaretoken"}) ['value'] )
       #print(csrf_middleware_token)

       payload = {"gstnum":gstin,
                  "csrfmiddlewaretoken":csrf_middleware_token
                 }

       second_req = client.post(url,headers=headers,data=payload,verify=True)
       soup2 = BeautifulSoup(second_req.text,'html.parser')

       table = soup2.find('table')
       #print(table)
        
       if table != None:
           table_rows = table.find_all('tr')
           for tr in table_rows:
               td = tr.find_all('td')
               row = [tr.text for tr in td if tr]
               if len(row) > 0:
                  if row[0] == 'Trade Name':
                     trade_name = row[1]
                  elif row[0] == 'Legal Name':
                     legal_name = row[1]
                  elif row[0] =='Registered on':
                     registered_on = row[1]
                     
           similarity_1 = SequenceMatcher(None, name.upper(), trade_name.upper()).ratio() 
           similarity_2 = SequenceMatcher(None, name.upper(), legal_name.upper()).ratio() 
           similarity   = max(similarity_1,similarity_2) * 100             
           
           remarks = 'Valid GST'
       else:
          trade_name=''
          legal_name=''
          registered_on=''
          remarks = 'Invalid GST'
   else:
       remarks = 'Invalid GST Length <> 15'
       
   print(code+'$'+name+'$'+gstin+'$'+remarks+'$'+trade_name+'$'+legal_name+'$'+registered_on[0:10]+'$'+str(similarity))
        
print("\n")
print("-------------- Completed ----------------")

#df2 = pd.DataFrame(list_gst, columns=["Particulars", "Details",])
#print(df2)

#df.to_excel("GST.xlsx")

#print("-------------- File Created: GST.xlsx ----------------")







    
'''VAD3R'''
