{{- define "mychart.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{- define "mychart.labels" -}}
managed-by: helm
chart: {{ .Chart.Name }}
release: {{ .Release.Name }}
date: {{ now | htmlDate }}
{{- end -}}


{{/* Expects a port to be passed as the context. */}}
{{- define "mychart.validators.portRange" -}}
{{- $sanitizedPort := int . -}}
{{- if or (lt $sanitizedPort 1) (gt $sanitizedPort 65535) -}}
{{- fail "Error: Ports must always be between 1 and 65535" -}}
{{- end -}}
{{- end -}}