terraform {
  required_providers {
    aiven = {
      source = "aiven/aiven"
      version = "~> 2.0"
    }
  }
}


provider "aiven" {
  api_token = var.aiven_api_token
}

resource "aiven_kafka" "user_data_kafka" {
  project      = var.aiven_project_name
  cloud_name   = var.aiven_cloud_name
  service_name = "user-data-kafka"
  plan         = "business-4"
}


resource "aiven_pg" "user_data_postgresql" {
  project      = var.aiven_project_name
  cloud_name   = var.aiven_cloud_name
  service_name = "user-data-postgresql"
  plan         = "business-4"
}


resource "aiven_opensearch" "user_data_opensearch" {
  project      = var.aiven_project_name
  cloud_name   = var.aiven_cloud_name
  service_name = "user-data-opensearch"
  plan         = "business-4"
}
