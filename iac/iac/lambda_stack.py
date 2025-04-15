from aws_cdk import (
    aws_lambda as lambda_,
    Duration
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration, CognitoUserPoolsAuthorizer

class LambdaStack(Construct):
    functions_that_need_cognito_permissions = []
    functions_that_need_dynamo_permissions = []

    def create_lambda_api_gateway_integration(self, module_name: str, method: str, api_resource: Resource,
        environment_variables: dict = { 'STAGE': 'TEST' }, authorizer=None):
        function = lambda_.Function(
            self, module_name.title(),
            code=lambda_.Code.from_asset(f'../src/routes/{module_name}'),
            handler=f'{module_name}.lambda_handler',
            runtime=lambda_.Runtime.PYTHON_3_11,
            layers=[ self.lambda_layer ],
            memory_size=512,
            environment=environment_variables,
            timeout=Duration.seconds(15)
        )

        api_resource.add_resource(module_name.replace('_', '-')).add_method(method, 
            integration=LambdaIntegration(function), authorizer=authorizer)
        
        return function

    def __init__(self, scope: Construct, api_gateway_resource: Resource, environment_variables: dict,
                 authorizer: CognitoUserPoolsAuthorizer) -> None:
        super().__init__(scope, "SAExpress_Lambda")

        self.lambda_layer = lambda_.LayerVersion(self, "SAExpress_Layer",
                                                 code=lambda_.Code.from_asset("./lambda_layer_out_temp"),
                                                 compatible_runtimes=[lambda_.Runtime.PYTHON_3_11]
                                                 )
        
        ### FUNCTIONS ###

        ### PERMISSIONS ###

        self.functions_that_need_cognito_permissions = []
        self.functions_that_need_dynamo_permissions = []