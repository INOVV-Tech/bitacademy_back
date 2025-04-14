import os
from aws_cdk import (
    aws_lambda as lambda_,
    Stack,
    aws_cognito,
    Duration,
    aws_iam
)
from constructs import Construct
from .lambda_stack import LambdaStack
from aws_cdk.aws_apigateway import RestApi, Cors


class IacStack(Stack):
    lambda_stack: LambdaStack

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.github_ref_name = os.environ.get("GITHUB_REF_NAME")
 
        self.rest_api = RestApi(self, f"SimpleTemplate_RestApi_{self.github_ref_name}",
                                rest_api_name=f"SimpleTemplate_RestApi_{self.github_ref_name}",
                                description="This is the SimpleTemplate RestApi",
                                default_cors_preflight_options={
                                    "allow_origins": Cors.ALL_ORIGINS,
                                    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                                    "allow_headers": ["*"]
                                },
                                )

        ENVIRONMENT_VARIABLES = {
            "STAGE": self.github_ref_name.upper(),
        }

        api_gateway_resource = self.rest_api.root.add_resource("mss--SimpleTemplate", default_cors_preflight_options={
            "allow_origins": Cors.ALL_ORIGINS,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": Cors.DEFAULT_HEADERS
        }
        )

        self.lambda_stack = LambdaStack(self, api_gateway_resource=api_gateway_resource, environment_variables=ENVIRONMENT_VARIABLES, authorizer=None)