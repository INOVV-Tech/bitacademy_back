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

        ### FREE MATERIAL ###

        self.create_free_material = self.create_lambda_api_gateway_integration(
            module_name='create_free_material',
            method='POST',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_all_free_materials = self.create_lambda_api_gateway_integration(
            module_name='get_all_free_materials',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_one_free_material = self.create_lambda_api_gateway_integration(
            module_name='get_one_free_material',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.update_free_material = self.create_lambda_api_gateway_integration(
            module_name='update_free_material',
            method='PUT',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.delete_free_material = self.create_lambda_api_gateway_integration(
            module_name='delete_free_material',
            method='POST',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        ### COURSE ###

        self.create_course = self.create_lambda_api_gateway_integration(
            module_name='create_course',
            method='POST',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_all_courses = self.create_lambda_api_gateway_integration(
            module_name='get_all_courses',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_one_course = self.create_lambda_api_gateway_integration(
            module_name='get_one_course',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.update_course = self.create_lambda_api_gateway_integration(
            module_name='update_course',
            method='PUT',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.delete_course = self.create_lambda_api_gateway_integration(
            module_name='delete_course',
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
            authorizer=authorizer
        )

        ### NEWS ###

        self.create_news = self.create_lambda_api_gateway_integration(
            module_name='create_news',
            method='POST',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_all_news = self.create_lambda_api_gateway_integration(
            module_name='get_all_news',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_one_news = self.create_lambda_api_gateway_integration(
            module_name='get_one_news',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.update_news = self.create_lambda_api_gateway_integration(
            module_name='update_news',
            method='PUT',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.delete_news = self.create_lambda_api_gateway_integration(
            module_name='delete_news',
            method='POST',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        ### TOOL ###

        self.create_tool = self.create_lambda_api_gateway_integration(
            module_name='create_tool',
            method='POST',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_all_tools = self.create_lambda_api_gateway_integration(
            module_name='get_all_tools',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_one_tool = self.create_lambda_api_gateway_integration(
            module_name='get_one_tool',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.update_tool = self.create_lambda_api_gateway_integration(
            module_name='update_tool',
            method='PUT',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.delete_tool = self.create_lambda_api_gateway_integration(
            module_name='delete_tool',
            method='POST',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        ### TAG ###

        self.get_all_tags = self.create_lambda_api_gateway_integration(
            module_name='get_all_tags',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        ### SIGNAL ###

        self.create_signal = self.create_lambda_api_gateway_integration(
            module_name='create_signal',
            method='POST',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_all_signals = self.create_lambda_api_gateway_integration(
            module_name='get_all_signals',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_one_signal = self.create_lambda_api_gateway_integration(
            module_name='get_one_signal',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.update_signal = self.create_lambda_api_gateway_integration(
            module_name='update_signal',
            method='PUT',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.delete_signal = self.create_lambda_api_gateway_integration(
            module_name='delete_signal',
            method='POST',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        ### COMMUNITY ###

        self.create_community_channel = self.create_lambda_api_gateway_integration(
            module_name='create_community_channel',
            method='POST',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_all_community_channels = self.create_lambda_api_gateway_integration(
            module_name='get_all_community_channels',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_one_community_channel = self.create_lambda_api_gateway_integration(
            module_name='get_one_community_channel',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.update_community_channel = self.create_lambda_api_gateway_integration(
            module_name='update_community_channel',
            method='PUT',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.delete_community_channel = self.create_lambda_api_gateway_integration(
            module_name='delete_community_channel',
            method='POST',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.create_community_forum_topic = self.create_lambda_api_gateway_integration(
            module_name='create_community_forum_topic',
            method='POST',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_community_channel_forum_topics = self.create_lambda_api_gateway_integration(
            module_name='get_community_channel_forum_topics',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.delete_community_forum_topic = self.create_lambda_api_gateway_integration(
            module_name='delete_community_forum_topic',
            method='POST',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.get_community_channel_messages = self.create_lambda_api_gateway_integration(
            module_name='get_community_channel_messages',
            method='GET',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )
        
        self.update_community_message = self.create_lambda_api_gateway_integration(
            module_name='update_community_message',
            method='PUT',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        self.delete_community_message = self.create_lambda_api_gateway_integration(
            module_name='delete_community_message',
            method='POST',
            api_resource=api_gateway_resource,
            environment_variables=environment_variables,
            authorizer=authorizer
        )

        ### PERMISSIONS ###

        self.functions_that_need_cognito_permissions = [
            self.create_free_material,
            self.get_all_free_materials,
            self.get_one_free_material,
            self.update_free_material,
            self.delete_free_material,

            self.create_course,
            self.get_all_courses,
            self.get_one_course,
            self.update_course,
            self.delete_course,

            self.get_home_coins,

            self.create_news,
            self.get_all_news,
            self.get_one_news,
            self.update_news,
            self.delete_news,

            self.create_tool,
            self.get_all_tools,
            self.get_one_tool,
            self.update_tool,
            self.delete_tool,

            self.get_all_tags,

            self.create_signal,
            self.get_all_signals,
            self.get_one_signal,
            self.update_signal,
            self.delete_signal,

            self.create_community_channel,
            self.get_all_community_channels,
            self.get_one_community_channel,
            self.update_community_channel,
            self.delete_community_channel,
            self.create_community_forum_topic,
            self.get_community_channel_forum_topics,
            self.delete_community_forum_topic,            
            self.get_community_channel_messages,
            self.update_community_message,
            self.delete_community_message
        ]

        self.functions_that_need_dynamo_permissions = [
            self.create_free_material,
            self.get_all_free_materials,
            self.get_one_free_material,
            self.update_free_material,
            self.delete_free_material,

            self.create_course,
            self.get_all_courses,
            self.get_one_course,
            self.update_course,
            self.delete_course,

            self.get_home_coins,

            self.create_news,
            self.get_all_news,
            self.get_one_news,
            self.update_news,
            self.delete_news,

            self.create_tool,
            self.get_all_tools,
            self.get_one_tool,
            self.update_tool,
            self.delete_tool,

            self.get_all_tags,

            self.create_signal,
            self.get_all_signals,
            self.get_one_signal,
            self.update_signal,
            self.delete_signal,

            self.create_community_channel,
            self.get_all_community_channels,
            self.get_one_community_channel,
            self.update_community_channel,
            self.delete_community_channel,
            self.create_community_forum_topic,
            self.get_community_channel_forum_topics,
            self.delete_community_forum_topic,
            self.get_community_channel_messages,
            self.update_community_message,
            self.delete_community_message
        ]