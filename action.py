#encoding=utf-8
import os
import argparse
import time
env=os.environ
Required_args=['DOCKER_USERNAME','DOCKER_PASSWORD','DOCKER_IMAGE_NAME']
for Required_arg in Required_args:
    if Required_arg not in env.keys():
        print("Require "+Required_arg)
        exit(1)

class getinfo:
    def __init__(self):
        self.DOCKER_USERNAME = env.get('DOCKER_USERNAME')
        self.DOCKER_PASSWORD = env.get('DOCKER_PASSWORD')
        self.DOCKER_IMAGE_NAME = env.get('DOCKER_IMAGE_NAME')
        self.DOCKER_IMAGE_TAG = env.get('DOCKER_IMAGE_TAG',time.strftime("%Y%m%d%H%M%S", time.localtime()))
        self.Push_latest = env.get('Push_latest',True)
        self.Only_Push_latest = env.get('Only_Push_latest',False)
        self.Dockerfile = env.get('Dockerfile','./Dockerfile')


info = getinfo()
#docker login
os.system('echo {DOCKER_PASSWORD} | docker login --username {DOCKER_USERNAME} --password-stdin'.format(DOCKER_USERNAME=info.DOCKER_USERNAME,DOCKER_PASSWORD=info.DOCKER_PASSWORD))

build_name = '{DOCKER_IMAGE_NAME}:{DOCKER_IMAGE_TAG}'.format(DOCKER_IMAGE_NAME=info.DOCKER_IMAGE_NAME,DOCKER_IMAGE_TAG=info.DOCKER_IMAGE_TAG)
latest_name = '{DOCKER_IMAGE_NAME}:latest'.format(DOCKER_IMAGE_NAME=info.DOCKER_IMAGE_NAME)
if(info.Only_Push_latest!=False or info.DOCKER_IMAGE_TAG=='latest'):
    build_name = '{DOCKER_IMAGE_NAME}:latest'.format(DOCKER_IMAGE_NAME=info.DOCKER_IMAGE_NAME)

os.system('docker build . --file {Dockerfile} --tag {build_name}'.format(Dockerfile=info.Dockerfile,build_name=build_name))
os.system('docker push {build_name}'.format(build_name=build_name))

if build_name!=latest_name:
    os.system('docker tag {build_name} {latest_name}'.format(build_name=build_name,latest_name=latest_name))
    os.system('docker push {latest_name}'.format(latest_name=latest_name))

print('docker build and push over')
