#!/bin/bash

# Script para configurar k3d cluster con Traefik

set -e

CLUSTER_NAME="mini-roda"
KUBECONFIG_PATH="$HOME/.kube/config"

echo "Creando cluster k3d: $CLUSTER_NAME"

# Crear cluster k3d con Traefik habilitado (por defecto)
k3d cluster create $CLUSTER_NAME \
    --port "80:80@loadbalancer" \
    --port "443:443@loadbalancer" \
    --port "8080:8080@loadbalancer" \
    --k3s-arg "--disable=traefik@server:0" \
    --wait

echo "Cluster creado exitosamente"

# Instalar Traefik usando Helm
echo "Instalando Traefik..."
helm repo add traefik https://traefik.github.io/charts
helm repo update

helm install traefik traefik/traefik \
    --namespace traefik \
    --create-namespace \
    --set ingressClass.enabled=true \
    --set ingressClass.isDefaultClass=true \
    --set service.type=LoadBalancer

echo "Esperando a que Traefik esté listo..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=traefik -n traefik --timeout=300s

echo "Cluster k3d configurado exitosamente!"
echo "Para usar este cluster: export KUBECONFIG=$(k3d kubeconfig write $CLUSTER_NAME)"


