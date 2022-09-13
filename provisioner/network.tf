resource "aws_vpc" "server_vpc" {
  cidr_block           = "10.123.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    Name = "production"
  }
}

# create a subnet and create relation with the vpc
resource "aws_subnet" "server_subnet" {
  vpc_id                  = aws_vpc.server_vpc.id
  cidr_block              = "10.123.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = var.aws_region == "eu-west-1" ? "eu-west-1a" : "eu-north-1a"
  tags = {
    Name = "gc-public"
  }
}

# create a gateway and map it to created vpc
resource "aws_internet_gateway" "server_gateway" {
  vpc_id = aws_vpc.server_vpc.id

  tags = {
    Name = "gc-gateway"
  }
}


# create a routing table
resource "aws_route_table" "server_route" {
  vpc_id = aws_vpc.server_vpc.id

  tags = {
    Name = "gc_public_rt"
  }
}

# create a default route, if destionation not in subnet send it through the gateway
resource "aws_route" "default_route" {
  route_table_id         = aws_route_table.server_route.id        # apply this to the table
  destination_cidr_block = "0.0.0.0/0"                            # 0.0.0.0 0.0.0.0 via gateway
  gateway_id             = aws_internet_gateway.server_gateway.id # mapping to gw
}


# associate the subnet with this route table
resource "aws_route_table_association" "server_table_assoc" {
  route_table_id = aws_route_table.server_route.id
  subnet_id      = aws_subnet.server_subnet.id

}

resource "aws_security_group" "allow_default" {
  name        = "gc_sg"
  description = "ingress ports"
  vpc_id      = aws_vpc.server_vpc.id
  dynamic "ingress" {

    for_each = var.ingress_ports
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = ingress.value.protocol
      cidr_blocks = contains(var.public_ports, ingress.value.port) ? ["0.0.0.0/0"] : [aws_subnet.server_subnet.cidr_block]
      description = ingress.key

    }

  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "gc_allow_rules"
  }
}
