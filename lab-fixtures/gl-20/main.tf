terraform {
  required_version = ">= 1.12.0, < 1.17.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "bucket_suffix" {
  type        = string
  description = "Unique suffix; learner supplies. No real account ids in git."
}

resource "aws_s3_bucket" "lab" {
  bucket = "aws-tf-workbook-${var.bucket_suffix}"

  tags = {
    Workbook  = "aws-tf-lab"
    LabId     = "gl-20"
    CreatedAt = timestamp()
  }
}

resource "aws_s3_bucket_public_access_block" "lab" {
  bucket                  = aws_s3_bucket.lab.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "bucket_name" {
  value = aws_s3_bucket.lab.bucket
}
