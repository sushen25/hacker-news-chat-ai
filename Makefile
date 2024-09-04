.PHONY: dev-up
dev-up:
	cd myhackernews && serverless wsgi serve -p 8000

.PHONY: vue-up
vue-up:
	cd frontend && npm run serve

