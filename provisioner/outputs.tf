output "public_ip" {
  value = aws_instance.server_node[*].public_ip
}

output "private_ip" {
  value = aws_instance.server_node[*].private_ip
}

