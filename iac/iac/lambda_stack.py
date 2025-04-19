from constructs import Construct
from aws_cdk.aws_apigateway import Resource, LambdaIntegration, CognitoUserPoolsAuthorizer
from aws_cdk import (
    Duration,
    aws_lambda as lambda_
)

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
        super().__init__(scope, 'BitAcademy_Lambda')

        self.lambda_layer = lambda_.LayerVersion(self, 'BitAcademy_Layer',
            code=lambda_.Code.from_asset('./lambda_layer_out_temp'),
            compatible_runtimes=[ lambda_.Runtime.PYTHON_3_11 ]
        )
        
        ### FUNCTIONS ###

        ### FREE RESOURCE ###

        self.create_free_resource = self.create_lambda_api_gateway_integration(
            module_name='create_free_resource',
            method='POST',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_all_free_resources = self.create_lambda_api_gateway_integration(
            module_name='get_all_free_resources',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_one_free_resource = self.create_lambda_api_gateway_integration(
            module_name='get_one_free_resource',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.update_free_resource = self.create_lambda_api_gateway_integration(
            module_name='update_free_resource',
            method='PUT',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.delete_free_resource = self.create_lambda_api_gateway_integration(
            module_name='delete_free_resource',
            method='POST',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        ### BIT CLASS ###

        self.create_bit_class = self.create_lambda_api_gateway_integration(
            module_name='create_bit_class',
            method='POST',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_all_bit_classes = self.create_lambda_api_gateway_integration(
            module_name='get_all_bit_classes',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_one_bit_class = self.create_lambda_api_gateway_integration(
            module_name='get_one_bit_class',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.update_bit_class = self.create_lambda_api_gateway_integration(
            module_name='update_bit_class',
            method='PUT',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.delete_bit_class = self.create_lambda_api_gateway_integration(
            module_name='delete_bit_class',
            method='POST',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        ### HOME COINS ###

        self.get_home_coins = self.create_lambda_api_gateway_integration(
            module_name='get_home_coins',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
        )

        ### PERMISSIONS ###

        self.functions_that_need_cognito_permissions = [
            self.create_free_resource,
            self.get_all_free_resources,
            self.get_one_free_resource,
            self.update_free_resource,
            self.delete_free_resource,

            self.create_bit_class,
            self.get_all_bit_classes,
            self.get_one_bit_class,
            self.update_bit_class,
            self.delete_bit_class
        ]

        self.functions_that_need_dynamo_permissions = [
            self.create_free_resource,
            self.get_all_free_resources,
            self.get_one_free_resource,
            self.update_free_resource,
            self.delete_free_resource,

            self.create_bit_class,
            self.get_all_bit_classes,
            self.get_one_bit_class,
            self.update_bit_class,
            self.delete_bit_class,

            self.get_home_coins
        ]