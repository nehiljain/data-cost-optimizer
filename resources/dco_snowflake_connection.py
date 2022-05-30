from dagster_snowflake.resources import (
    define_snowflake_config,
    resource,
    sys,
    check,
    closing,
    SnowflakeConnection,
)
import pandas as pd


class DCOSnowflakeConnection(SnowflakeConnection):
    def execute_query(self, sql, parameters=None, fetch_results=False):
        check.str_param(sql, "sql")
        check.opt_dict_param(parameters, "parameters")
        check.bool_param(fetch_results, "fetch_results")

        with self.get_connection() as conn:
            with closing(conn.cursor()) as cursor:
                if sys.version_info[0] < 3:
                    sql = sql.encode("utf-8")

                self.log.info("Executing query: " + sql)
                cursor.execute(sql, parameters)  # pylint: disable=E1101
                cols = [item[0] for item in cursor.description]
                if fetch_results:
                    return pd.DataFrame(cursor.fetchall(), columns=cols)
        return super().execute_query(sql, parameters, fetch_results)


@resource(
    config_schema=define_snowflake_config(),
    description="This resource is for connecting to the Snowflake data warehouse",
)
def snowflake_resource(context):
    """A resource for connecting to the Snowflake data warehouse.
    A simple example of loading data into Snowflake and subsequently querying
    that data is shown below:
    Examples:
    .. code-block:: python
        from dagster import job, op
        from dagster_snowflake import snowflake_resource
        @op(required_resource_keys={'snowflake'})
        def get_one(context):
            context.resources.snowflake.execute_query('SELECT 1')
        @job(resource_defs={'snowflake': snowflake_resource})
        def my_snowflake_job():
            get_one()
        my_snowflake_job.execute_in_process(
            run_config={
                'resources': {
                    'snowflake': {
                        'config': {
                            'account': {'env': 'SNOWFLAKE_ACCOUNT'},
                            'user': {'env': 'SNOWFLAKE_USER'},
                            'password': {'env': 'SNOWFLAKE_PASSWORD'},
                            'database': {'env': 'SNOWFLAKE_DATABASE'},
                            'schema': {'env': 'SNOWFLAKE_SCHEMA'},
                            'warehouse': {'env': 'SNOWFLAKE_WAREHOUSE'},
                        }
                    }
                }
            }
        )
    """
    return DCOSnowflakeConnection(context.resource_config, context.log)
