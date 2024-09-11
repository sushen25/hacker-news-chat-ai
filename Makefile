.PHONY: dev-up
dev-up:
	cd myhackernews && flask run --port 8000

.PHONY: vue-up
vue-up:
	cd frontend && npm run serve

