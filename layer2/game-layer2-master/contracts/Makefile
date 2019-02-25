TAG ?= latest

.PHONY: default deploy-factory deploy-registry output-contracts build-docker

default:
	@echo "Please provide a valid target."
	@exit 2

deploy:
	npx truffle migrate --network ganache
	npx truffle exec --network ganache ./scripts/deploy_registry.js
	cp -r ./build/contracts ./conf

build-docker:
	docker build -t mixyanbin/rocket-contracts:$(TAG) .