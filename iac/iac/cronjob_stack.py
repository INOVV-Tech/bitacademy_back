from constructs import Construct
from aws_cdk import (
    Duration,
    aws_lambda as lambda_,
    aws_events,
    aws_events_targets
)

from .dynamo_stack import DynamoStack

class CronjobStack(Construct):
    def __init__(self, scope: Construct, environment_variables: dict, \
        dynamo_stack: DynamoStack) -> None:
        super().__init__(scope, 'BitAcademy_Cronjobs')
        
        self.cronjob_lambda_layer = lambda_.LayerVersion(self, 'BitAcademy_Cronjob_Layer',
            code=lambda_.Code.from_asset('./lambda_layer_out_temp'),
            compatible_runtimes=[ lambda_.Runtime.PYTHON_3_11 ]
        )

        self.update_home_coins = lambda_.Function(
            self, 'UpdateHomeCoins',
            code=lambda_.Code.from_asset(f'../src/cronjobs/update_home_coins'),
            handler='update_home_coins.lambda_handler',
            runtime=lambda_.Runtime.PYTHON_3_11,
            layers=[ self.cronjob_lambda_layer ],
            memory_size=512,
            environment=environment_variables,
            timeout=Duration.seconds(30)
        )

        self.update_signals = lambda_.Function(
            self, 'UpdateSignals',
            code=lambda_.Code.from_asset(f'../src/cronjobs/update_signals'),
            handler='update_signals.lambda_handler',
            runtime=lambda_.Runtime.PYTHON_3_11,
            layers=[ self.cronjob_lambda_layer ],
            memory_size=512,
            environment=environment_variables,
            timeout=Duration.seconds(360)
        )

        dynamo_stack.dynamo_table.grant_read_write_data(self.update_home_coins)
        dynamo_stack.dynamo_table.grant_read_write_data(self.update_signals)

        update_home_coins_rule = aws_events.Rule(
            self, 'UpdateHomeCoinsRule',
            schedule=aws_events.Schedule.rate(Duration.minutes(3))
        )

        update_home_coins_rule.add_target(aws_events_targets.LambdaFunction(self.update_home_coins))

        update_signals_rule = aws_events.Rule(
            self, 'UpdateSignalsRule',
            schedule=aws_events.Schedule.rate(Duration.minutes(30))
        )

        update_signals_rule.add_target(aws_events_targets.LambdaFunction(self.update_signals))
