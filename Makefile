.PHONY: kind-cluster
kind-cluster:
	ctlptl create cluster kind --name kind-melvil --registry=ctlptl-registry

.PHONY: delete-kind-cluster
delete-kind-cluster:
	ctlptl delete cluster kind-melvil --ignore-not-found

clean-tilt: delete-kind-cluster kind-cluster
	tilt up
