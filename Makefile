build:
	docker build -t ikea-crawler:latest --cache-from ikea-crawler:latest --load . --platform=linux/amd64

run:
	@if [ $(shell docker ps -a -q -f name=ikea_crawler_container) ]; then docker rm -f ikea_crawler_container; fi

	docker run --name ikea_crawler_container --platform=linux/amd64 ikea-crawler:latest

	mkdir -p ./reports/$(PROJECT) ./logs
	docker cp ikea_crawler_container:/ikea_crawler/logs/. ./logs
	docker rm ikea_crawler_container