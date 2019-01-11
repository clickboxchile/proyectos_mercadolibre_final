from flask import Flask, render_template, request
from werkzeug import secure_filename

import csv
import requests
import json
import time

datos = []

print("introduce el access_token de la pagina")

app = Flask(__name__)

url = 'https://api.mercadolibre.com/items?access_token='
headers = {'content-type': 'application/json'}
access_token = input()


@app.route('/')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file_btn():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))

      with open('data.csv', newline='') as File:
          reader = csv.reader(File)
          for row in reader:
              seller_custom_field =row[0]
              title = row[1]
              category_id = row[2]
              price = row[3]
              currency_id = row[4]
              available_quantity = row[5]
              buying_mode = row[6]
              listing_type_id = row[7]
              condition = row[8]
              description = row[9]
              video_id = row[10]
              warranty = row[11]

              source1 = row[12]
              source2 = row[13]
              source3 = row[14]
              source4 = row[15]
              source5 = row[16]
              source6 = row[17]
              costos = row[18]
              costos_nombre = row[19]

              data_product = {
                                "title": title,
                                "category_id":category_id,
                                "price":price,
                                "currency_id":currency_id,
                                "available_quantity":available_quantity,
                                "buying_mode":buying_mode,
                                "listing_type_id":listing_type_id,
                                "condition":condition,
                                "description": {"plain_text":description},
                                "video_id": video_id,
                                "warranty": warranty,
                                "pictures":[
                                {"source": source1},{"source":source2},{"source":source3},{"source":source4},{"source":source5},{"source":source6}
                                ],
                                "shipping": {
                            	"mode": "custom",
                            	"local_pick_up": "false",
                            	"free_shipping": "false",
                            	"methods": [],
                            	"costs": [
                                	{
                                    	"description": costos_nombre,
                                    	"cost": costos
                                	}
                            	]
                        	}
                                }
              r = requests.post(url + access_token, data=json.dumps(data_product),headers=headers)

              json_convert = json.loads(r.content)
              id_item = json_convert["id"]

              url_value = (f'https://api.mercadolibre.com/items/{id_item}?access_token={access_token}')

              data = {'seller_custom_field':str(seller_custom_field)}

              r = requests.put(url_value, data = json.dumps(data))

              print('numero de item :' +  str(row) + ' status code: ' + str(r.status_code))
              print(' ')
              print('--------------------------------------------------------------------------------------------------------------')

              x = [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19]]

              datos.insert(0, x)


              time.sleep(1)
      with open('data_out.csv', mode='w') as archivo:
          archivo = csv.writer(archivo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
          for linea in range(len(datos)):
              archivo.writerow(datos[linea])



      return 'file uploaded successfully'

if __name__ == '__main__':
   app.run(debug = True, host = '0.0.0.0')
