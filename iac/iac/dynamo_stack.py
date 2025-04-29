import os
from constructs import Construct
from aws_cdk import (
    CfnOutput,
    aws_dynamodb,
    RemovalPolicy,
)

class DynamoStack(Construct):
    def __init__(self, scope: Construct) -> None:
        super().__init__(scope, 'BitAcademy_Dynamo')

        github_ref_name = os.environ.get('GITHUB_REF_NAME', 'dev')

        removal_policy = RemovalPolicy.RETAIN if 'prod' in github_ref_name else RemovalPolicy.DESTROY

        self.dynamo_table = aws_dynamodb.Table(
            self, 'BitAcademy_Table',
            partition_key=aws_dynamodb.Attribute(
                name='PK',
                type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name='SK',
                type=aws_dynamodb.AttributeType.STRING
            ),
            point_in_time_recovery=True,
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=removal_policy
        )

        # self.dynamo_table.add_global_secondary_index(
        #     index_name='GetAllEntities',
        #     partition_key=aws_dynamodb.Attribute(
        #         name='GSI#ENTITY_GETALL#PK',
        #         type=aws_dynamodb.AttributeType.STRING
        #     ),
        #     sort_key=aws_dynamodb.Attribute(
        #         name='GSI#ENTITY_GETALL#SK',
        #         type=aws_dynamodb.AttributeType.NUMBER
        #     )
        # )

        CfnOutput(self, 'BitAcademyTableName',
                  value=self.dynamo_table.table_name,
                  export_name=f'BitAcademy{github_ref_name}TableName')

        CfnOutput(self, 'DynamoBitAcademyRemovalPolicy',
                  value=removal_policy.value,
                  export_name=f'BitAcademy{github_ref_name}DynamoRemovalPolicy')
