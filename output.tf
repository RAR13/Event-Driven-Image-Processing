output "source_bucket" {
  value = aws_s3_bucket.source_bucket.bucket
}

output "destination_bucket" {
  value = aws_s3_bucket.destination_bucket.bucket
}

output "lambda_function" {
  value = aws_lambda_function.image_processor.function_name
}