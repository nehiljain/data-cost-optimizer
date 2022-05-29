from dagster import job, op, io_manager
from local_csv_io import LocalCSVIOManager
from resources.dco_snowflake_connection import snowflake_resource
from dotenv import load_dotenv

load_dotenv()


@io_manager
def local_csv_iom(_):
    # todo: move to iomanager class
    return LocalCSVIOManager()


@op(required_resource_keys={"snowflake"})
def get_query_history(context):
    query = """
    select *
    from snowflake.account_usage.query_history
    where month(start_time) >= month(current_date) - 1
    """
    result = context.resources.snowflake.execute_query(query, fetch_results=True)
    context.log.info(result.dtypes)
    # figure out a way to do chunking in case its a very large data source
    return result


@job(resource_defs={"snowflake": snowflake_resource, "io_manager": local_csv_iom})
def download_query_history_job():
    get_query_history()


if __name__ == "__main__":
    download_query_history_job.execute_in_process(
        run_config={
            "resources": {
                "snowflake": {
                    "config": {
                        "account": {"env": "SNOWFLAKE_ACCOUNT"},
                        "user": {"env": "SNOWFLAKE_USER"},
                        "password": {"env": "SNOWFLAKE_PASSWORD"},
                        "warehouse": {"env": "SNOWFLAKE_WAREHOUSE"},
                    }
                }
            }
        }
    )
