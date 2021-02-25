build-latest: export TAG=docker.io/shanisma/k8s-one-green-admin-ui:latest
build-latest:
	docker build -t ${TAG} .
	docker push ${TAG}

build-latest-arm: export TAG=docker.io/shanisma/k8s-one-green-admin-ui:arm-latest
build-latest-arm:
	sudo docker build -t ${TAG} . --build-arg  ARG_PYARROW_CMAKE_OPTIONS="-DARROW_ARMV8_ARCH=armv8-a"
	sudo docker push ${TAG}
