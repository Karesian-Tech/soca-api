create_local_db:
	docker exec -it postgres_db createdb -U postgres -W soca_db_local

drop_local_db:
	docker exec -it postgres_db dropdb -U postgres -W soca_db_local
