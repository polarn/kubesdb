
IMAGE="polarn/kubesdb"
VERSION=$(shell git describe --tags | sed 's/^v//')

.ALWAYS:

version versions: modules/VERSION.py

modules/VERSION.py: .ALWAYS
	@echo "Creating version $(VERSION)"
	@echo "Version = \"$(VERSION)\"" > modules/VERSION.py

docker: version
	@echo "Building docker image $(IMAGE):$(VERSION)"
	@docker build --tag polarn/kubesdb:$(VERSION) .

push: docker
	@echo "Pushing docker image $(IMAGE):$(VERSION)"
	@docker push polarn/kubesdb:$(VERSION)
