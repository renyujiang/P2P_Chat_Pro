# import ast
#
# import requests
#
# url = "http://127.0.0.1:10000/login"
# params = {"username": "test1", "password": "123456"}
# response = requests.get(url)
#
# if response.status_code == 200:
#     # 如果响应成功，则可以获取响应内容
#     content = response.content.decode('utf-8')
#     my_list = ast.literal_eval(content)
#     my_tuples = [tuple(x) for x in my_list]
#     print(my_tuples[0][0])
#     print(content)
# else:
#     # 如果响应失败，则可以获取失败原因
#     print("请求失败，状态码为：", response.status_code)


import requests

url = 'http://127.0.0.1:10000/upload'
filename = '/Users/renyujiang/Desktop/EC530/Assignments/P2P_Chat_Pro/central_server_test.py'
username = 'test2'

with open(filename, 'rb') as f:
    files = {'file': f}
    data = {'username': username}
    response = requests.post(url, files=files, data=data)

if response.ok:
    print('File uploaded successfully')
else:
    print('Error uploading file')