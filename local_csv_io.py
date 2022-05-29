class LocalCSVIOManager(IOManager):
    def handle_output(self, context, obj):
        write_csv(os.get_env('WORKING_DIR'))

    def load_input(self, context):
        return read_csv(os.get_env('WORKING_DIR'))
