import requests


with open('test_cases.txt', 'r') as f:
    data = f.read()
test_cases = data.split('\n')
test_cases = [each.split(',') for each in test_cases]

path = 'http://localhost:8000/fetch'
res = []
for case in test_cases:
    response = requests.post(path, json={'email': case[0], 'password': case[1]})
    res.append(response.text == case[2])
if all(res):
    print('All tests passed!')
