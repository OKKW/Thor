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


