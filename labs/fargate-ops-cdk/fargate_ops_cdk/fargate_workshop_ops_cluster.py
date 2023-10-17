# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. SPDX-License-Identifier: MIT-0
from constructs import Construct

from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_cloudtrail as cloudtrail,
    Stack
    
)


class FargateWorkshopOpsCluster(Stack):

    def __init__(self, scope: Construct, id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.trail = cloudtrail.Trail(self, 'ECSWorkshopCloudTrail');

        self.cluster = ecs.Cluster(
                scope = self,
                id = 'OpsCluster',
                vpc = vpc,
                containerInsights = True
        )
        # Adding service discovery namespace to cluster
        self.cluster.add_default_cloud_map_namespace(
            name="service",
        )




