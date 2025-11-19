#!/bin/bash

# Script para configurar Minikube con Traefik

set -e

echo "Iniciando Minikube..."

# Iniciar Minikube
minikube start --driver=docker --memory=4096 --cpus=2

echo "Minikube iniciado"

# Habilitar ingress addon (opcional, si no usas Traefik)
# minikube addons enable ingress

# Instalar Traefik usando Helm
echo "Instalando Traefik..."
helm repo add traefik https://traefik.github.io/charts
helm repo update

helm install traefik traefik/traefik \
    --namespace traefik \
    --create-namespace \
    --set ingressClass.enabled=true \
    --set ingressClass.isDefaultClass=true

echo "Esperando a que Traefik esté listo..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=traefik -n traefik --timeout=300s

# Configurar tunnel para acceso local (opcional)
echo "Para acceder a los servicios, ejecuta en otra terminal:"
echo "minikube tunnel"

echo "Minikube configurado exitosamente!"


