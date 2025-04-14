import os
from aws_cdk import (
    CfnOutput,
    aws_dynamodb,
    RemovalPolicy,
)
from constructs import Construct


class DynamoStack(Construct):

    def __init__(self, scope: Construct) -> None:
        super().__init__(scope, "SAExpress_Dynamo")

        github_ref_name = os.environ.get("GITHUB_REF_NAME", "dev")
        removal_policy = RemovalPolicy.RETAIN if 'prod' in github_ref_name else RemovalPolicy.DESTROY

        self.dynamo_table = aws_dynamodb.Table(
            self, "SAExpress_Table",
            partition_key=aws_dynamodb.Attribute(
                name="PK",
                type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name="SK",
                type=aws_dynamodb.AttributeType.STRING
            ),
            point_in_time_recovery=True,
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=removal_policy
        )

        self.dynamo_table.add_global_secondary_index(
            partition_key=aws_dynamodb.Attribute(
                name="GSI#ENTITY",
                type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name="created_at",
                type=aws_dynamodb.AttributeType.NUMBER
            ),
            index_name="AllEntitiesMetadata"
        )

        self.dynamo_table.add_global_secondary_index(
            partition_key=aws_dynamodb.Attribute(
                name="tx_id",
                type=aws_dynamodb.AttributeType.STRING
            ),
            index_name="TXById"
        )

        CfnOutput(self, 'DynamoTableName',
                  value=self.dynamo_table.table_name,
                  export_name=f"SAExpress{github_ref_name}TableName")

        CfnOutput(self, 'DynamoSAExpressRemovalPolicy',
                  value=removal_policy.value,
                  export_name=f"SAExpress{github_ref_name}DynamoRemovalPolicy")
