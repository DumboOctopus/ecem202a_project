from PIL import Image
import os
from os import path
import io
import time
import requests
import csv

session = requests.Session()
server_addr = 'http://192.168.1.19:8080/test'


def ask_server(my_stream):
  t0 = time.time()
  my_stream.seek(0)

  pil_image = Image.open(my_stream)

  # resize
  resized = pil_image.resize((128, 128))

  buf = io.BytesIO()
  resized.save(buf, format="JPEG")
  buf.seek(0)
  t2 = time.time()

  # request
  files = {"media": ('file.jpg', buf, 'image/jpg')}
  #print(requests.Request('POST', 'http://example.com', files=files).prepare().body)
  response = session.post(server_addr, files=files)#, headers=headers)
  t1 = time.time()

  try:
      data = response.json()
      # print(data)
      total_time = t1-t0
      proc_time = t2 - t0
      # print('time total:', t1 - t0)
      # print('time proc: ', t2 - t0)

      # do not include computing image size as part of computation
      # since robot doesn't actually do that normally
      size = buf.getbuffer().nbytes
      buf.close()

      return data['obstacles'], {
          "total_time": total_time, 
          "proc_time": proc_time, 
          "request_time": data["request_time"],
          "model_time": data["model_time"],
          "accuracy": data["accuracy"],
          "size": size
      }
  except requests.exceptions.RequestException:
      print(response.text)

  return False, {}


if __name__ == '__main__':
    folder_of_images = 'origin_dataset'
    files = os.listdir(folder_of_images)

    first_image = files[0]
    first_time = True

    with open(f'timing-{folder_of_images}_128.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for image in [first_image] + files:

            # putting it into memory to make testing set up exactly the same
            # as robot code
            buf = None
            with open(path.join(folder_of_images, image), 'rb') as fh:
                buf = io.BytesIO(fh.read())

            for _ in range(5):
                _, timing_info = ask_server(buf)
                # the session re uses connection
                # so first result is going to take longer
                if not first_time:
                    csv_writer.writerow([
                        image,
                        timing_info['total_time'],
                        timing_info['proc_time'],
                        timing_info['request_time'],
                        timing_info['model_time'],
                        timing_info['accuracy'],
                        timing_info['size']
                    ])
                    print(image, timing_info)

            buf.close()

            first_time = False
