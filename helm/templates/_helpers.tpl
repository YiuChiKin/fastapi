{{/*
Expand the name of the chart.
*/}}
{{- define "stock-api.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
Truncates at 63 chars because some Kubernetes name fields have that limit.
*/}}
{{- define "stock-api.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart label value: "<chart-name>-<chart-version>"
*/}}
{{- define "stock-api.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels applied to every resource.
*/}}
{{- define "stock-api.labels" -}}
helm.sh/chart: {{ include "stock-api.chart" . }}
{{ include "stock-api.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- with .Values.commonLabels }}
{{ toYaml . }}
{{- end }}
{{- end }}

{{/*
Selector labels used by Deployments and Services to match pods.
*/}}
{{- define "stock-api.selectorLabels" -}}
app.kubernetes.io/name: {{ include "stock-api.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Name of the Secret that holds the Finnhub API key.
*/}}
{{- define "stock-api.secretName" -}}
{{- include "stock-api.fullname" . }}-finnhub
{{- end }}
