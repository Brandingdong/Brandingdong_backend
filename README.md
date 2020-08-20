# Brandingdong_backend

Brandi clone coding project

## Technologies
- python >= 3.8.2
- django >= 3.0

## SetUp
```python
$ pyenv virtualenv <python V> <VE name>
$ cd <root directory>
$ pyenv local <VE name>
$ pip install -r requirements.txt
```


## static files 적용하는 법
```
aws iam 등록
$ aws configure

$ python manage.py collectstatic
```

## install docker on ec2
https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html

## copy local ENV to ec2
scp -i ~/.ssh/brandingdong.pem -r ~/PROJECTPATH/Brandingdong_backend/.env ec2-user@52.78.75.94:~/.env



