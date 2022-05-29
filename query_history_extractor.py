from dagster import job, op
from dagster_snowflake import snowflake_resource
from dotenv import load_dotenv

load_dotenv()

@op(required_resource_keys={'snowflake'})
def get_query_history(context):
    query = """
    select *
    from snowflake.account_usage.query_history
    where month(start_time) >= month(current_date) - 1
    """
    return context.resources.snowflake.execute_query(query)

@job(resource_defs={'snowflake': snowflake_resource})
def my_snowflake_job():
    get_query_history()

my_snowflake_job.execute_in_process(
    run_config={
        'resources': {
            'snowflake': {
                'config': {
                    'account': {'env': 'SNOWFLAKE_ACCOUNT'},
                    'user': {'env': 'SNOWFLAKE_USER'},
                    'password': {'env': 'SNOWFLAKE_PASSWORD'},
                    'warehouse': {'env': 'SNOWFLAKE_WAREHOUSE'},
                }
            }
        }
    }
)
