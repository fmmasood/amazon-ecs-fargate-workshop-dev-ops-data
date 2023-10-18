# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. SPDX-License-Identifier: MIT-0

from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_logs as logs,
    aws_ecs_patterns as ecs_patterns,
    App, Stack, Duration, CfnOutput, RemovalPolicy

)

class FargateWorkshopOpsNodeBackend(Stack):

    def __init__(self, scope: Stack, id: str, cluster: ecs.ICluster, vpc, private_subnets, sec_group, desired_service_count, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.cluster = cluster
        self.vpc = vpc
        self.private_subnets = private_subnets
        self.sec_group = sec_group

        self.service_discovery = cluster.default_cloud_map_namespace
        self.desired_service_count = desired_service_count

        self.task_definition = ecs.FargateTaskDefinition(
            self, "BackendNodeServiceTaskDef",
            cpu=256,
            memory_limit_mib=512,
        )

        self.task_definition.add_container(
            "BackendNodeServiceContainer",
            image=ecs.ContainerImage.from_registry("brentley/ecsdemo-nodejs"),
            logging=ecs.LogDrivers.firelens(
                options={
                    "Name": "cloudwatch",
                    "log_key": "log",
                    "region": "ap-southeast-2",
                    "delivery_stream": "my-stream",
                    "log_group_name": "firelens-fluent-bit",
                    "auto_create_group": "true",
                    "log_stream_prefix": "from-fluent-bit"}
            )
        )

        sgs= []
        self.fargate_service = ecs.FargateService(
            self, "BackendNodeFargateService",
            service_name="Fargate-Backend-NodeJS",
            task_definition=self.task_definition,
            cluster=self.cluster,
            max_healthy_percent=100,
            min_healthy_percent=0,
            vpc_subnets={
                "subnet_type" : ec2.SubnetType.PRIVATE_WITH_EGRESS
            },
            desired_count=self.desired_service_count,
            security_groups=sgs.append(self.sec_group),
            cloud_map_options={
                "name": "ecsdemo-nodejs"
            },
        )
