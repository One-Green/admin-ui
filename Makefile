build-latest: export TAG=docker.io/shanisma/k8s-one-green-admin-ui:latest
build-latest:
	docker build -t ${TAG} .
	docker push ${TAG}
