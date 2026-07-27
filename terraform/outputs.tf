output "s3_website_url" {
  description = "URL for the S3 static website hosting"
  value       = aws_s3_bucket_website_configuration.frontend.website_endpoint
}

output "api_gateway_endpoint" {
  description = "Public URL endpoint for the API Gateway"
  value       = aws_apigatewayv2_api.http_api.api_endpoint
}

output "vpc_id" {
  description = "Custom VPC ID"
  value       = aws_vpc.main.id
}