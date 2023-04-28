# Get Food
This API get_food takes a datetime that you want a meal and returns you all open restaurants

# Running through Docker

I have dockerized this program for simplicity and used Postman to send the request.
Clone the repo, make sure docker is running, and navigate the terminal of your choice to the repo.

To create the image for the docker container:

`docker build -t get-food .`

And to run the program:
`docker run -p 80:80 get-food`

Then send a GET request using your preferred API test client like Postman or Insomnia like this:
`http://localhost:80/get_food/?meal_time=2023-08-29 07:30:00`

Feel free to change the datetime, just make sure it is in that format
