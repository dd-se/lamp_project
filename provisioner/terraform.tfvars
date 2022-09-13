aws_region     = "eu-north-1"
ssh_public_key = "./ssh_key/dd_key.pub"
ingress_ports = {
  "Allow SSH"   = { protocol = "tcp", port = 22 },
  "Allow HTTP"  = { protocol = "tcp", port = 80 },
  "Allow HTTPS" = { protocol = "tcp", port = 443 },
  "Allow SQL"   = { protocol = "tcp", port = 3306 },
  "Allow APP"   = { protocol = "tcp", port = 8000 },
}
public_ports       = [443, 80, 22]
backend_host_count = 2
