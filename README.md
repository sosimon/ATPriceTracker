# ATPriceTracker

## Create Kubernetes cluster

```
gcloud beta container clusters create atpricetracker \
  --region us-central1 \
  --node-locations us-central1-a,us-central1-c,us-central1-f \
  --num-nodes 1 \
  --machine-type f1-micro \
  --enable-autoscaling \
  --max-nodes 12 \
  --min-nodes 3
```

## Deploy kube-lego

```
kubectl create -f gcp/lego/00-namespace.yml
kubectl create -f gcp/lego/configmap.yml
kubectl create -f gcp/lgeo/deployment.yml
```

## Deploy app

```
kubectl apply -f gcp/k8s/deployment.yml
kubectl apply -f gcp/k8s/service.yml
kubectl apply -f gcp/k8s/ingress.yml
```

Notes:
* Remember to configure DNS to map domain name to load balancer IP
* May need to apply gcp/k8s/ingress.yml again to trigger kube-lego?


