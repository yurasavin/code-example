up:
	@docker-compose up -d

generate_data:
	@docker-compose exec app python manage.py migrate
	@docker-compose exec app python manage.py generate_random_data
