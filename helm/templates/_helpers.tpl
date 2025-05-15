{{/* vim: set filetype=mustache: */}}
{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "zyte-test-websites.name" -}}
{{- default .Release.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "zyte-test-websites.labels" -}}
{{- include "zyte-test-websites.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service | quote }}
helm.sh/chart: "{{ .Chart.Name }}-{{ .Chart.Version }}"
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "zyte-test-websites.selectorLabels" }}
app.kubernetes.io/name: {{ include "zyte-test-websites.name" . }}
app.kubernetes.io/instance: {{ .Release.Name | quote }}
{{- end }}

{{/*
Create the hostname used in the ingress.
*/}}
{{- define "zyte-test-websites.hostname" -}}
    {{ .Values.websiteName }}-test-website.{{ .Values.domain }}
{{- end -}}
