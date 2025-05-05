import os
from constructs import Construct
from aws_cdk import (
    Duration,
    aws_iam,
    aws_lambda as lambda_,
    aws_apigatewayv2 as apigwv2
)

from .dynamo_stack import DynamoStack

class CommunityStack(Construct):
    def __init__(self, scope: Construct, environment_variables: dict, \
        dynamo_stack: DynamoStack) -> None:
        super().__init__(scope, 'BitAcademy_Community')

        region = os.environ.get('AWS_REGION')
        github_ref_name = os.environ.get('GITHUB_REF_NAME', 'dev')

        self.comm_lambda_layer = lambda_.LayerVersion(self, 'BitAcademy_Community_Layer',
            code=lambda_.Code.from_asset('./lambda_layer_out_temp'),
            compatible_runtimes=[ lambda_.Runtime.PYTHON_3_11 ]
        )

        self.comm_connect_fn = lambda_.Function(
            self, 'Connect',
            code=lambda_.Code.from_asset(f'../src/community/connect'),
            handler='connect.lambda_handler',
            runtime=lambda_.Runtime.PYTHON_3_11,
            layers=[ self.comm_lambda_layer ],
            memory_size=512,
            environment=environment_variables,
            timeout=Duration.seconds(15)
        )

        self.comm_disconnect_fn = lambda_.Function(
            self, 'Disconnect',
            code=lambda_.Code.from_asset(f'../src/community/disconnect'),
            handler='disconnect.lambda_handler',
            runtime=lambda_.Runtime.PYTHON_3_11,
            layers=[ self.comm_lambda_layer ],
            memory_size=512,
            environment=environment_variables,
            timeout=Duration.seconds(15)
        )

        dynamo_stack.dynamo_table.grant_read_write_data(self.comm_connect_fn)
        dynamo_stack.dynamo_table.grant_read_write_data(self.comm_disconnect_fn)

        self.comm_api = apigwv2.CfnApi(self, 'CommunityWebSocketApi',
            name='CommunityWebSocketApi',
            protocol_type='WEBSOCKET',
            route_selection_expression='$request.body.action'
        )

        self.comm_stage = apigwv2.CfnStage(self, 'CommunityWebSocketStage',
            api_id=self.comm_api.ref,
            stage_name=github_ref_name,
            auto_deploy=True
        )

        def add_ws_route(route_key: str, fn: lambda_.Function):
            integration = apigwv2.CfnIntegration(self, f'{route_key}Integration',
                api_id=self.comm_api.ref,
                integration_type='AWS_PROXY',
                integration_uri=f'arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/{fn.function_arn}/invocations'
            )

            apigwv2.CfnRoute(self, f'{route_key}Route',
                api_id=self.comm_api.ref,
                route_key=route_key,
                target=f'integrations/{integration.ref}'
            )
            
            fn.grant_invoke(aws_iam.ServicePrincipal('apigateway.amazonaws.com'))

        add_ws_route('$connect', self.comm_connect_fn)
        add_ws_route('$disconnect', self.comm_disconnect_fn)