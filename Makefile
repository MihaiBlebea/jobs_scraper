venv-create:
	python3 -m venv virtualenv

venv-activate:
	source virtualenv/bin/activate

venv-lock:
	pip3 freeze > requirements.txt

venv-install-all:
	pip3 install -r requirements.txt

venv-install:
	./virtualenv/bin/pip3 install $(package)

api:
	./virtualenv/bin/python3 ./src/api.py

docker-build:
	docker build -t jobs:v1.0 .

docker-run:
	docker run -d -v $(PWD)/store.db:/app/store.db --name jobs -p 8080:5000 jobs:v1.0

docker: docker-build docker-run

docker-stop:
	docker stop jobs && docker rm jobs

ansible-deploy:
	ansible-playbook -i $$HOME/.ansible/inventory ./ansible/deploy.yaml

ansible-remove:
	ansible-playbook -i $$HOME/.ansible/inventory ./ansible/remove.yaml

git:
	git add . && git commit -m "$(msg)" && git push origin master

git-deploy: git ansible-deploy