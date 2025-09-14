import pulumi
import pulumi_aws as aws
from pulumi import ResourceOptions
from knightstar_pulumi_utils import ks_ctx_from_config

ctx = ks_ctx_from_config()                  # uses foundation:ks.* (client, baseDomain)
region = aws.config.region or "us-west-2"
cfg = pulumi.Config()

# Either adopt an existing VPC or create one (controlled by config)
existing_vpc_id = cfg.get("network.existingVpcId")
vpc_cidr = cfg.get("network.cidr") or "10.0.0.0/16"

if existing_vpc_id:
    real = aws.ec2.get_vpc(id=existing_vpc_id)
    vpc = aws.ec2.Vpc(
        ctx.name("vpc"),
        cidr_block=real.cidr_block,
        enable_dns_support=True,
        enable_dns_hostnames=True,
        tags=ctx.tags({"Name": ctx.name("vpc")}),
        opts=ResourceOptions(import_=existing_vpc_id),
    )
else:
    vpc = aws.ec2.Vpc(
        ctx.name("vpc"),
        cidr_block=vpc_cidr,
        enable_dns_support=True,
        enable_dns_hostnames=True,
        tags=ctx.tags({"Name": ctx.name("vpc")}),
    )

# Private hosted zone: int.<env>.<base_domain>
phz = aws.route53.Zone(
    ctx.name("phz"),
    name=ctx.private_zone_name(),    # requires foundation:ks.baseDomain
    vpcs=[aws.route53.ZoneVpcArgs(vpc_id=vpc.id, vpc_region=region)],
    tags=ctx.tags({"Name": ctx.private_zone_name()}),
)

pulumi.export("vpcId", vpc.id)
pulumi.export("vpcCidr", vpc.cidr_block)
pulumi.export("privateZoneId", phz.zone_id)
pulumi.export("privateZoneName", phz.name)
