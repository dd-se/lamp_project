aws_region        = "eu-north-1"
ec2_instance_name = "group_chorba_lamf_stack"
ingress_ports = {
  "Allow SSH"  = { protocol = "tcp", port = 22 },
  "Allow HTTP" = { protocol = "tcp", port = 80 },
  "Allow SQL"  = { protocol = "tcp", port = 3306 },
  "Allow APP"  = { protocol = "tcp", port = 8000 },
}
ssh_public_key = "./ssh_key/dd_key.pub"
host_count     = 8
