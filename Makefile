.PHONY: up
up: ## up services for development
	@sudo docker compose up

.PHONY: stop
stop: ## stop services for development
	@sudo docker compose stop

.PHONY: restart
restart: ## Reload services (restart without rebuild)
  @sudo docker compose restart

.PHONY: makemigrations
makemigrations: ## Run makemigrations
	@sudo docker compose exec web python manage.py makemigrations

.PHONY: migrate
migrate: ## Run migrate
	@sudo docker compose exec web python manage.py migrate

.PHONY: create-test-data
create-test-data: ## create test data in DB
	@sudo docker compose exec web python manage.py load_mock_data

.PHONY: shell
shell: ## Open Django shell
	@sudo docker compose exec web python manage.py shell

.PHONY: exec
exec: ## Enter web container bash
	@sudo docker compose exec web bash

.PHONY: createsuperuser
createsuperuser: ## Create superuser
	@sudo docker compose exec web python manage.py createsuperuser

.PHONY: help
help: ## help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
