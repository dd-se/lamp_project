aws_region     = "eu-north-1"
ssh_public_key = "./ssh_key/dd_key.pub"
ingress_ports = {
  "Allow SSH"  = { protocol = "tcp", port = 22 },
  "Allow HTTP" = { protocol = "tcp", port = 80 },
  "Allow SQL"  = { protocol = "tcp", port = 3306 },
  "Allow APP"  = { protocol = "tcp", port = 8000 },
}
backend_host_count = 2
