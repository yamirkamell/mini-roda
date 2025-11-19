#!/bin/bash

# Script para instalar Traefik en Minikube o k3d

set -e

echo "Instalando Traefik Ingress Controller..."

# Detectar el tipo de cluster
if kubectl get nodes | grep -q "k3d"; then
    echo "Cluster k3d detectado - Traefik ya está instalado"
    exit 0
elif kubectl get nodes | grep -q "minikube"; then
    echo "Cluster Minikube detectado - Instalando Traefik con Helm..."
    
    # Verificar si Helm está instalado
    if ! command -v helm &> /dev/null; then
        echo "Helm no está instalado. Instalando Helm..."
        curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
    fi
    
    # Agregar repo de Traefik
    helm repo add traefik https://traefik.github.io/charts
    helm repo update
    
    # Instalar Traefik
    helm install traefik traefik/traefik \
        --namespace traefik \
        --create-namespace \
        --set ingressClass.enabled=true \
        --set ingressClass.isDefaultClass=true
    
    echo "Traefik instalado exitosamente"
    echo "Esperando a que Traefik esté listo..."
    kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=traefik -n traefik --timeout=300s
else
    echo "Tipo de cluster no reconocido. Instalando Traefik con Helm..."
    
    if ! command -v helm &> /dev/null; then
        echo "Helm no está instalado. Por favor instálalo primero."
        exit 1
    fi
    
    helm repo add traefik https://traefik.github.io/charts
    helm repo update
    
    helm install traefik traefik/traefik \
        --namespace traefik \
        --create-namespace \
        --set ingressClass.enabled=true \
        --set ingressClass.isDefaultClass=true
    
    echo "Traefik instalado exitosamente"
fi

echo "Verificando instalación..."
kubectl get pods -n traefik


