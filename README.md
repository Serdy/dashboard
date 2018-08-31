# Flask Dashboard

This is small dashboard on python flask framework.

## Install and Run

```
	sudo docker build -t dashboard .
	sudo docker run --name dashboard -it --rm \ 
	-e AWS_ACCESS_KEY_ID='your_key' \
    -e AWS_SECRET_ACCESS_KEY='your_secret' \
    -e AWS_DEFAULT_REGION=us-east-1 -e GITHUB_CLIENT_ID=github_id \
    -e GITHUB_CLIENT_SECRET='github_secret' -p 8080:8080 dash
```

