# DogClassifier
Me and a friend built a dog classification app for iOS and Android. 
This code is a sample of the API used in the app.
<br>
You will also find a basic model building Jupyter notebook in this repo.
<br>
I also built a faster API using an improved model which uses FastAPI and Gunicorn, to be uploaded.

<br>
<br>



Flask App 
unicorn 
post image

build image
```
docker build -t dogflask:latest .
```
start container
```
docker run -d -p 6000:8000 dogflask
```

```
curl -X POST -F image=@tiger.jpg 'https://localhost:6000/predict'
```


