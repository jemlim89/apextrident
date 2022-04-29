import pandas as pd
import requests

# URL for datalog xml file
xml_url = 'http://therainforest.tplinkdns.com:4999/cgi-bin/datalog.xml'

# getting the last recorded datetime
dates_df = pd.read_xml(xml_url, xpath="/datalog/record")
latest_datetime = dates_df['date'].iloc[-1]

# getting values of alk, ca, mg, orp, pH, temp
values_df = pd.read_xml(xml_url, xpath="/datalog/record/probe")
type_to_extract = ['alk','ca','mg' ,'ORP', 'pH', 'Temp' ]
latest_values = values_df[values_df['type'].isin(type_to_extract)][-6:][['type','value']]
latest_values = latest_values.set_index('type')
latest_values = latest_values.to_dict()
results = latest_values['value']
result_str = str(results)[1:-1]
result_str=result_str.replace("'",'')

# combining into string
final_output = latest_datetime + '\n' + result_str

# sending to telegram channel
bot_token = '5341978335:AAFPQphqSaRiSR5T9-m8Xf3ZSDFyIdYA-Ss'
channel_id = '-672811249'
send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + channel_id + '&parse_mode=Markdown&text=' + 'APEX Tank Parameters \n' + final_output

    
r = requests.get(send_text)
r.json()
