# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. SPDX-License-Identifier: MIT-0

from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_logs as logs,
    aws_ecs_patterns as ecs_patterns,
    App, Stack, Duration, CfnOutput, RemovalPolicy

)

class FargateWorkshopOpsFailed(Stack):

    def __init__(self, scope: Stack, id: str, cluster: ecs.ICluster, vpc, private_subnets, sec_group, desired_service_count, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.cluster = cluster
        self.vpc = vpc
        self.private_subnets = private_subnets
        self.sec_group = sec_group

        self.service_discovery = cluster.default_cloud_map_namespace
        self.desired_service_count = desired_service_count

        self.task_definition = ecs.FargateTaskDefinition(
            self, "FailedServiceTaskDef",
            cpu=256,
            memory_limit_mib=512,
        )

        self.task_definition.add_container(
            "FailedServiceContainer",
            image=ecs.ContainerImage.from_registry("mbednarz/fargate_issue"),
            logging=ecs.AwsLogDriver(stream_prefix="ecsdemo-nodejs", log_retention=logs.RetentionDays.THREE_DAYS),
        )

        sgs = []

        self.fargate_service = ecs.FargateService(
            self, "FailedFargateService",
            service_name="Fargate-Backend-Failed",
            task_definition=self.task_definition,
            cluster=self.cluster,
            max_healthy_percent=100,
            min_healthy_percent=0,
            vpc_subnets={
                "subnet_type" : ec2.SubnetType.PRIVATE_WITH_EGRESS
            },
            desired_count=self.desired_service_count,
            security_groups=sgs.append(self.sec_group)
        )
