from aws_cdk import (
    aws_lambda as lambda_,
    NestedStack, Duration,
)
from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration, CognitoUserPoolsAuthorizer


class LambdaStack(Construct):

    def create_lambda_api_gateway_integration(self, module_name: str, method: str, api_resource: Resource, environment_variables: dict = {"STAGE": "TEST"}, authorizer=None):
        function = lambda_.Function(
            self, module_name.title(),
            code=lambda_.Code.from_asset(f"../src/routes"),
            handler=f"{module_name}.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            layers=[self.lambda_layer, self.lib_layer],
            memory_size=512,
            environment=environment_variables,
            timeout=Duration.seconds(15),
        )

        api_resource.add_resource(module_name.replace("_", "-")).add_method(method, integration=LambdaIntegration(function), authorizer=authorizer)

        return function

    def __init__(self, scope: Construct, api_gateway_resource: Resource, environment_variables: dict, authorizer: CognitoUserPoolsAuthorizer) -> None:
        super().__init__(scope, "SimpleTemplate_Lambda")

        self.lambda_layer = lambda_.LayerVersion(self, "SimpleTemplate_Layer",
                                                 code=lambda_.Code.from_asset("./shared"),
                                                 compatible_runtimes=[lambda_.Runtime.PYTHON_3_9],
                                                 )
        
        self.lib_layer = lambda_.LayerVersion(self, "SimpleTemplate_LibLayer",
                                                 code=lambda_.Code.from_asset("./requirements"),
                                                 compatible_runtimes=[lambda_.Runtime.PYTHON_3_9],
                                                 )

        self.health_check = self.create_lambda_api_gateway_integration(
            module_name="health_check",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
        )

        self.get_all_users = self.create_lambda_api_gateway_integration(
            module_name="get_all_users",
            method="GET",
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )
