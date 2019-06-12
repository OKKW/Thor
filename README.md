# DogClassifier
Me and a friend built a dog classification app for iOS and Android. 
This code is a sample of my contribution. 

I also build an API using an improved model which uses FastAPI and Gunicorn.




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


