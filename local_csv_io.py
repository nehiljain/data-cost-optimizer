import time
from dagster import IOManager, io_manager
import os
import pandas as pd


class LocalCSVIOManager(IOManager):
    def handle_output(self, context, obj):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        file_name = f"{context.pipeline_name}__{context.step_key}_output__{timestr}.parquet"
        file_path = os.path.join(os.getenv("WORKING_DIR", "."), file_name)
        context.log.debug(f"Saving file to {file_path}")
        obj.to_parquet(file_path)

    def load_input(self, context):
        # TODO: need to get name from context like default io manager
        return pd.read_parquet(os.getenv("WORKING_DIR", "/tmp") + "/output.parquet")


@io_manager
def local_parquet_iom(_):
    return LocalCSVIOManager()
