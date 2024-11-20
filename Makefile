.PHONY: flask-up
flask-up:
	cd myhackernews && flask run --port 8000

.PHONY: vue-up
vue-up:
	cd frontend && npm run serve

.PHONY: database-up
database-up:
	cd myhackernews && cd db && docker-compose up

.PHONY: dev-up
dev-up:
	tmux new-session -d -s myhackernews
	
	tmux split-window -h
	tmux select-pane -t 0

	tmux send-keys -t myhackernews 'make flask-up' C-m
	
	tmux select-pane -t 1
	tmux send-keys -t myhackernews 'make vue-up' C-m

	tmux split-window -v
	tmux select-pane -t 2
	tmux send-keys -t myhackernews 'cd myhackernews && cd db' C-m
	tmux send-keys -t myhackernews 'docker-compose up' C-m

	tmux attach-session -t myhackernews

.PHONY: dev-attach
dev-attach:
	tmux attach-session -t myhackernews

.PHONY: dev-down
dev-down:
	tmux kill-session -t myhackernews
	cd myhackernews && cd db && docker-compose down