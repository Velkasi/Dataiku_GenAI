# ☸️ Kubernetes Deployment avec Helm

Guide de déploiement Kubernetes avec Helm Chart pour le chatbot Dataiku.

## 📋 Prérequis

- Cluster Kubernetes opérationnel
- `kubectl` configuré et connecté au cluster
- `helm` installé (v3+)
- Image Docker buildée et pushée dans un registry

## 🚀 Quick Start

### 1. Créer le Secret avec les credentials

```bash
# Créez un secret Kubernetes avec vos credentials
kubectl create secret generic dataiku-chatbot-secrets \
  --from-literal=ANTHROPIC_API_KEY='sk-ant-api03-...' \
  --from-literal=DSS_URL='https://dss.example.com' \
  --from-literal=DSS_API_KEY='dkuaps-...' \
  --from-literal=DSS_PROJECT_KEY='TEST_WORKFLOW' \
  --from-literal=DSS_SSL_VERIFY='true'
```

### 2. Installer le Helm Chart

```bash
# Depuis le répertoire chatbot/
helm install dataiku-chatbot ./helm/dataiku-chatbot

# Avec valeurs custom
helm install dataiku-chatbot ./helm/dataiku-chatbot \
  --values my-values.yaml

# Avec overrides inline
helm install dataiku-chatbot ./helm/dataiku-chatbot \
  --set image.tag=v1.0.0 \
  --set ingress.enabled=true
```

### 3. Vérifier le déploiement

```bash
# Status du release
helm status dataiku-chatbot

# Pods
kubectl get pods -l app.kubernetes.io/name=dataiku-chatbot

# Services
kubectl get svc -l app.kubernetes.io/name=dataiku-chatbot

# Logs
kubectl logs -f -l app.kubernetes.io/name=dataiku-chatbot
```

## 🏗️ Build et Push de l'image

Avant de déployer sur K8s, il faut push l'image dans un registry.

### Avec Docker Hub

```bash
# Tag l'image
docker tag dataiku-chatbot:latest youruser/dataiku-chatbot:v1.0.0

# Login
docker login

# Push
docker push youruser/dataiku-chatbot:v1.0.0

# Update values.yaml
# image:
#   repository: youruser/dataiku-chatbot
#   tag: v1.0.0
```

### Avec un registry privé

```bash
# Tag
docker tag dataiku-chatbot:latest registry.company.com/dataiku-chatbot:v1.0.0

# Login
docker login registry.company.com

# Push
docker push registry.company.com/dataiku-chatbot:v1.0.0

# Créer imagePullSecret
kubectl create secret docker-registry regcred \
  --docker-server=registry.company.com \
  --docker-username=user \
  --docker-password=pass \
  --docker-email=email@company.com

# Update values.yaml
# imagePullSecrets:
#   - name: regcred
```

## ⚙️ Configuration

### Fichier values.yaml personnalisé

Créez `my-values.yaml` :

```yaml
# Image
image:
  repository: yourregistry/dataiku-chatbot
  tag: "v1.0.0"
  pullPolicy: IfNotPresent

# Resources
resources:
  requests:
    cpu: 500m
    memory: 512Mi
  limits:
    cpu: 2000m
    memory: 2Gi

# Replicas
replicaCount: 2

# Ingress
ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: dataiku-chatbot.company.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: dataiku-chatbot-tls
      hosts:
        - dataiku-chatbot.company.com

# Autoscaling
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 5
  targetCPUUtilizationPercentage: 70

# Node selector (optionnel)
nodeSelector:
  workload: data-engineering

# Affinity (optionnel)
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchExpressions:
          - key: app.kubernetes.io/name
            operator: In
            values:
            - dataiku-chatbot
        topologyKey: kubernetes.io/hostname
```

### Installation avec valeurs custom

```bash
helm install dataiku-chatbot ./helm/dataiku-chatbot \
  --values my-values.yaml \
  --namespace data-engineering \
  --create-namespace
```

## 🔄 Mises à jour

### Upgrade du release

```bash
# Après modification du code ou des values
helm upgrade dataiku-chatbot ./helm/dataiku-chatbot \
  --values my-values.yaml

# Avec nouvelle image
helm upgrade dataiku-chatbot ./helm/dataiku-chatbot \
  --set image.tag=v1.1.0

# Forcer le re-deploy
helm upgrade dataiku-chatbot ./helm/dataiku-chatbot \
  --force \
  --recreate-pods
```

### Rollback

```bash
# Voir l'historique
helm history dataiku-chatbot

# Rollback à la version précédente
helm rollback dataiku-chatbot

# Rollback à une revision spécifique
helm rollback dataiku-chatbot 2
```

## 🌐 Exposition (Ingress)

### Avec NGINX Ingress Controller

```yaml
# values.yaml
ingress:
  enabled: true
  className: nginx
  annotations:
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "300"
  hosts:
    - host: chatbot.company.com
      paths:
        - path: /
          pathType: Prefix
```

### Avec Traefik

```yaml
ingress:
  enabled: true
  className: traefik
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: websecure
  hosts:
    - host: chatbot.company.com
      paths:
        - path: /
          pathType: Prefix
```

### Avec cert-manager (HTTPS)

```yaml
ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: chatbot.company.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: chatbot-tls
      hosts:
        - chatbot.company.com
```

## 📊 Monitoring

### Logs

```bash
# Logs d'un pod
kubectl logs -f <pod-name>

# Logs de tous les pods du deployment
kubectl logs -f -l app.kubernetes.io/name=dataiku-chatbot

# Logs des 100 dernières lignes
kubectl logs --tail=100 -l app.kubernetes.io/name=dataiku-chatbot
```

### Métriques

```bash
# Utilisation des ressources
kubectl top pods -l app.kubernetes.io/name=dataiku-chatbot

# Describe le deployment
kubectl describe deployment dataiku-chatbot

# Events
kubectl get events --sort-by='.lastTimestamp'
```

### Healthchecks

```bash
# Vérifier les probes
kubectl describe pod <pod-name> | grep -A 5 "Liveness\|Readiness"

# Logs des healthchecks
kubectl logs <pod-name> | grep health
```

## 🔍 Debug

### Pod ne démarre pas

```bash
# Describe le pod
kubectl describe pod <pod-name>

# Logs
kubectl logs <pod-name>

# Events
kubectl get events --field-selector involvedObject.name=<pod-name>

# Shell dans le pod (si démarré)
kubectl exec -it <pod-name> -- /bin/bash
```

### ImagePullBackOff

```bash
# Vérifier le secret
kubectl get secret regcred -o yaml

# Vérifier que l'image existe
docker pull yourregistry/dataiku-chatbot:v1.0.0

# Recréer le secret
kubectl delete secret regcred
kubectl create secret docker-registry regcred ...
```

### CrashLoopBackOff

```bash
# Logs du container qui crash
kubectl logs <pod-name> --previous

# Vérifier les secrets
kubectl get secret dataiku-chatbot-secrets -o yaml

# Vérifier les variables d'env
kubectl exec <pod-name> -- env | grep -i dss
```

## 📦 Persistence (optionnel)

Si vous voulez persister les logs :

```yaml
# values.yaml
persistence:
  enabled: true
  storageClass: "standard"  # ou votre storage class
  size: 5Gi
  mountPath: /app/logs
```

Créer un PVC :

```bash
kubectl get pvc
kubectl describe pvc dataiku-chatbot
```

## 🔒 Sécurité

### Network Policies

Créez `networkpolicy.yaml` :

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: dataiku-chatbot-netpol
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: dataiku-chatbot
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8501
  egress:
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443  # Anthropic API
    - protocol: TCP
      port: 80   # Dataiku DSS (ajustez)
```

### Pod Security

Le chart utilise déjà des bonnes pratiques :
- runAsNonRoot: true
- readOnlyRootFilesystem: false (Streamlit a besoin d'écrire)
- No privileged containers

## 🚀 Autoscaling (HPA)

```yaml
# values.yaml
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80
```

Vérifier l'HPA :

```bash
kubectl get hpa
kubectl describe hpa dataiku-chatbot
```

## 🧪 Test du déploiement

```bash
# Port-forward pour tester localement
kubectl port-forward svc/dataiku-chatbot 8501:8501

# Ouvrir http://localhost:8501

# Test depuis un pod
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- \
  curl http://dataiku-chatbot:8501/_stcore/health
```

## 🗑️ Désinstallation

```bash
# Supprimer le release
helm uninstall dataiku-chatbot

# Supprimer le namespace (si créé)
kubectl delete namespace data-engineering

# Supprimer les secrets
kubectl delete secret dataiku-chatbot-secrets
kubectl delete secret regcred
```

## 📚 Commandes utiles

```bash
# Lister les releases Helm
helm list

# Voir les valeurs utilisées
helm get values dataiku-chatbot

# Voir tous les manifests générés
helm get manifest dataiku-chatbot

# Template local (dry-run)
helm template dataiku-chatbot ./helm/dataiku-chatbot

# Lint le chart
helm lint ./helm/dataiku-chatbot

# Package le chart
helm package ./helm/dataiku-chatbot
```

## 📋 Checklist Production

- [ ] Image buildée et pushée dans registry
- [ ] Secret Kubernetes créé avec credentials
- [ ] Ingress configuré avec HTTPS
- [ ] Resources limits/requests définis
- [ ] Autoscaling activé (HPA)
- [ ] Monitoring configuré (Prometheus/Grafana)
- [ ] Logs centralisés (ELK/Loki)
- [ ] Network policies en place
- [ ] Backup strategy définie
- [ ] Documentation mise à jour

---

**Prêt pour la production sur Kubernetes ! 🎉**
