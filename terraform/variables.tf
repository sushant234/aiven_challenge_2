variable "aiven_api_token" {
  description = "Aiven API Token"
  type        = string
}

variable "aiven_project_name" {
  description = "Aiven project name"
  type        = string
}

variable "aiven_cloud_name" {
  description = "Cloud name"
  type        = string
}

variable "kafka_version" {
  description = "Kafka version"
  type        = string
  default     = "2.8.0"
}

variable "postgresql_version" {
  description = "PostgreSQL version"
  type        = string
  default     = "13"
}
