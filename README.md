# airbnb-analytics
My pet project to analyze airbnb listings.

<br>
<h6>Run RabbitMQ</h6>
rabbitmq-server
<br>
<br>
<h6>Run Celery Worker</h6>
celery -A air_analytics worker -l info
<br>
<br>
<h6>Run Celery Beat Scheduler</h6>
celery -A air_analytics beat -l info -S django

