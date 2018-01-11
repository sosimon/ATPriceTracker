# ATPriceTracker

## Create Kubernetes cluster

```
gcloud beta container clusters create atpricetracker \
  --region us-central1 \
  --node-locations us-central1-a,us-central1-c,us-central1-f \
  --num-nodes 1 \
  --machine-type f1-micro
```

## Deploy kube-lego

```
kubectl create -f gcp/lego/00-namespace.yml
kubectl create -f gcp/lego/configmap.yml
kubectl create -f gcp/lgeo/deployment.yml
```
