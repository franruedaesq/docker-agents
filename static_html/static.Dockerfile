# declare what image to use
# FROM is the instruction to use the python image
# FROM image:tag

FROM python:latest

WORKDIR /app


# copy local folder to the container_folder
# RUN mkdir -p /static_folder
# COPY ./static_html /static_folder
COPY ./src .

# RUN echo "Hello World" > index.html


# docker build -f DockerFile -t pyapp . 
# docker run -it pyapp
# every time we make a change we need to rebuild the imange, with docker build and run

# if we want to push to docker hub we need to use our username
# docker build -f DockerFile -t franchy008/pyapp:latest . 
# docker push franchy008/pyapp:latest

# if we want to pull from docker hub we need to use our username
# docker pull franchy008/pyapp:latest
# docker run -it franchy008/pyapp:latest

# if we want to run a container from an image we need to use the image name
# docker run -it pyapp

# if we want to deploy we need to have this image in some kind of deployment process
# but we need a function that could run, like a lambda function or we application
# python has a build in web server, we can use it to run our application
# to run de webserver in python
# python -m http.server 8000 
# for the docker container to run this we need to use CMD
CMD ["python", "-m", "http.server", "8000"]
# the server will run inside the container
# if we want to open the port in our web browser we need to use the -p flag
# docker run -it -p 3000:8000 pyapp
# what this is doing is mapping the port 3000 in our machine to the port 8000 in the container


