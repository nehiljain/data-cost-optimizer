from dagster import IOManager
import os
import pandas as pd


class LocalCSVIOManager(IOManager):
    def handle_output(self, context, obj):
        # TODO:need to get name from context
        obj.to_csv(os.get_env("WORKING_DIR", "/tmp") + "/output.csv", header=True, index=False)

    def load_input(self, context):
        # TODO: need to get name from context like default io manager
        return pd.read_csv(os.get_env("WORKING_DIR", "/tmp") + "/output.csv")
