{{- define "mychart.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{- define "mychart.labels" -}}
managed-by: helm
chart: {{ .Chart.Name }}
release: {{ .Release.Name }}
date: {{ now | htmlDate }}
{{- end -}}