# Kubernetes Manifests Reference

Complete guide to generating Kubernetes manifests.

## Basic Resources

### Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ project_name }}
  labels:
    app: {{ project_name }}
    version: {{ version }}
spec:
  replicas: {{ replicas | default: 3 }}
  selector:
    matchLabels:
      app: {{ project_name }}
  template:
    metadata:
      labels:
        app: {{ project_name }}
        version: {{ version }}
    spec:
      containers:
        - name: {{ project_name }}
          image: {{ image }}:{{ tag }}
          ports:
            - containerPort: {{ port | default: 8080 }}
              name: http
          env:
            - name: LOG_LEVEL
              value: "{{ log_level | default: 'info' }}"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: {{ project_name }}-secrets
                  key: database-url
          resources:
            requests:
              memory: "{{ memory_request | default: '128Mi' }}"
              cpu: "{{ cpu_request | default: '100m' }}"
            limits:
              memory: "{{ memory_limit | default: '256Mi' }}"
              cpu: "{{ cpu_limit | default: '200m' }}"
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 10
            periodSeconds: 5
          readinessProbe:
            httpGet:
              path: /ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 3
```

### Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ project_name }}
  labels:
    app: {{ project_name }}
spec:
  type: {{ service_type | default: 'ClusterIP' }}
  selector:
    app: {{ project_name }}
  ports:
    - name: http
      port: 80
      targetPort: http
      protocol: TCP
```

### Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ project_name }}
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
    - hosts:
        - {{ domain }}
      secretName: {{ project_name }}-tls
  rules:
    - host: {{ domain }}
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: {{ project_name }}
                port:
                  number: 80
```

## ConfigMaps and Secrets

### ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ project_name }}-config
data:
  config.yaml: |
    server:
      port: {{ port }}
      host: 0.0.0.0
    logging:
      level: {{ log_level }}
      format: json
```

### Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ project_name }}-secrets
type: Opaque
stringData:
  database-url: "{{ database_url }}"
  api-key: "{{ api_key }}"
```

### External Secrets (ESO)
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: {{ project_name }}-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    kind: ClusterSecretStore
    name: aws-secrets-manager
  target:
    name: {{ project_name }}-secrets
  data:
    - secretKey: database-url
      remoteRef:
        key: {{ project_name }}/{{ environment }}
        property: DATABASE_URL
```

## Advanced Resources

### HorizontalPodAutoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ project_name }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ project_name }}
  minReplicas: {{ min_replicas | default: 2 }}
  maxReplicas: {{ max_replicas | default: 10 }}
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

### PodDisruptionBudget
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: {{ project_name }}
spec:
  minAvailable: {{ min_available | default: 1 }}
  selector:
    matchLabels:
      app: {{ project_name }}
```

### NetworkPolicy
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: {{ project_name }}
spec:
  podSelector:
    matchLabels:
      app: {{ project_name }}
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
          port: 8080
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: database
      ports:
        - protocol: TCP
          port: 5432
```

## Kustomize

### kustomization.yaml
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: {{ namespace }}

commonLabels:
  app.kubernetes.io/name: {{ project_name }}
  app.kubernetes.io/part-of: {{ project_name }}

resources:
  - deployment.yaml
  - service.yaml
  - ingress.yaml
  - configmap.yaml

configMapGenerator:
  - name: {{ project_name }}-config
    files:
      - config.yaml

secretGenerator:
  - name: {{ project_name }}-secrets
    envs:
      - secrets.env

images:
  - name: {{ project_name }}
    newName: {{ registry }}/{{ project_name }}
    newTag: {{ tag }}
```

### Overlay Structure
```
kubernetes/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   └── patches/
    ├── staging/
    └── prod/
```

## Helm Templates

### Chart.yaml
```yaml
apiVersion: v2
name: {{ project_name }}
description: A Helm chart for {{ project_name }}
type: application
version: {{ chart_version | default: '1.0.0' }}
appVersion: {{ app_version | default: '1.0.0' }}
```

### values.yaml
```yaml
replicaCount: 3

image:
  repository: {{ registry }}/{{ project_name }}
  tag: "latest"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: {{ domain }}
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi
```
