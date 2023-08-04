download:
	curl -OL https://raw.githubusercontent.com/FoundationDB/fdb-kubernetes-operator/main/config/crd/bases/apps.foundationdb.org_foundationdbclusters.yaml
	curl -OL https://raw.githubusercontent.com/FoundationDB/fdb-kubernetes-operator/main/config/crd/bases/apps.foundationdb.org_foundationdbbackups.yaml
	curl -OL https://raw.githubusercontent.com/FoundationDB/fdb-kubernetes-operator/main/config/crd/bases/apps.foundationdb.org_foundationdbrestores.yaml
	curl -OL https://raw.githubusercontent.com/foundationdb/fdb-kubernetes-operator/main/config/samples/deployment.yaml
helm: 
	helm template fdb-kubernetes-operator \
	#--repo https://foundationdb.github.io/fdb-kubernetes-operator/ \
		--values values.yaml \
		--create-namespace \
		--namespace archive \
		--include-crds=true \
                fdb-kubernetes-operator > fdb-kubernetes-operator.yaml
