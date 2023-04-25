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

url = 'http://127.0.0.1:10000/login'
params = {'username': 'test1', 'password': '123456'}
response = requests.get(url, params=params)

if response.status_code == 200:
    print(response.content.decode('utf-8'))
else:
    print(f'Login failed: {response.status_code}')

