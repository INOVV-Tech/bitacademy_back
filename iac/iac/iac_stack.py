import os
from aws_cdk import (
    Stack,
    aws_cognito,
    aws_iam
)
from constructs import Construct
from .dynamo_stack import DynamoStack
from .lambda_stack import LambdaStack
from .community_stack import CommunityStack
from aws_cdk.aws_apigateway import RestApi, Cors, CognitoUserPoolsAuthorizer

class IacStack(Stack):
    lambda_stack: LambdaStack
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.user_pool_arn = os.environ.get('USER_POOL_ARN')
        self.user_pool_id = os.environ.get('USER_POOL_ID')
        self.app_client_id = os.environ.get('APP_CLIENT_ID')
        self.github_ref_name = os.environ.get('GITHUB_REF_NAME')
        
        self.dynamo_stack = DynamoStack(self)

        self.cognito_auth = CognitoUserPoolsAuthorizer(self, f'bitacademy_cognito_auth_{self.github_ref_name}',
            cognito_user_pools=[
                aws_cognito.UserPool.from_user_pool_arn(
                    self, f'bitacademy_cognito_auth_userpool_{self.github_ref_name}',
                    self.user_pool_arn
                )
            ]
        )
 
        self.rest_api = RestApi(self, 
            f'BitAcademy_RestApi_{self.github_ref_name}',
            rest_api_name=f'BitAcademy_RestApi_{self.github_ref_name}',
            description='This is the BitAcademy RestApi',
            default_cors_preflight_options={
                'allow_origins': Cors.ALL_ORIGINS,
                'allow_methods': [ 'GET', 'POST', 'PUT', 'DELETE', 'OPTIONS' ],
                'allow_headers': [ '*' ]
            }
        )

        ENVIRONMENT_VARIABLES = {
            'STAGE': self.github_ref_name.upper(),
            'REGION': self.region,
            'USER_POOL_ID': self.user_pool_id,
            'USER_POOL_ARN': self.user_pool_arn,
            'APP_CLIENT_ID': self.app_client_id,
            'DYNAMO_TABLE_NAME': self.dynamo_stack.dynamo_table.table_name,
            'BUCKET_NAME': os.environ.get('BUCKET_NAME', ''),
            'CMC_API_KEY': os.environ.get('CMC_API_KEY', '')
        }
        
        api_gateway_resource = self.rest_api.root.add_resource('mss-bitacademy', 
            default_cors_preflight_options={
                'allow_origins': Cors.ALL_ORIGINS,
                'allow_methods': [ 'GET', 'POST', 'PUT', 'DELETE', 'OPTIONS' ],
                'allow_headers': Cors.DEFAULT_HEADERS
            }
        )

        self.lambda_stack = LambdaStack(self, api_gateway_resource=api_gateway_resource,
            environment_variables=ENVIRONMENT_VARIABLES, authorizer=self.cognito_auth)
          
        cognito_admin_policy = aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            actions=[
                'cognito-idp:*',
            ],
            resources=[
                self.user_pool_arn
            ]
        )
        
        for f in self.lambda_stack.functions_that_need_cognito_permissions:
            f.add_to_role_policy(cognito_admin_policy)
        
        for f in self.lambda_stack.functions_that_need_dynamo_permissions:
            self.dynamo_stack.dynamo_table.grant_read_write_data(f)

        ### WEBSOCKET ###

        self.community_stack = CommunityStack(self, \
            environment_variables=ENVIRONMENT_VARIABLES, dynamo_stack=self.dynamo_stack)
