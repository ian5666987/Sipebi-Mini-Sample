class PySipebiCommonValidationRunner:
    def __init__(self, validation_class):
        self.validation_class = validation_class
        self.shared_resources = {}

    def input_into_shared_resources(self, file_resource_name):
        abs_filename = ''
        if "diag" in file_resource_name:
            file_resource_name = file_resource_name[file_resource_name.find('diag') + 5:]
            abs_filename = f'py\\diag\\data\\{file_resource_name}'       
            file_resource_name = f'diag\\data\\{file_resource_name}'
        else:
            abs_filename = f'py\\data\\{file_resource_name}'
        self.shared_resources[file_resource_name] = self.read_file(abs_filename)

    def read_file(self, filename):
        with open(filename, 'r', newline="\r\n") as f:
            return f.read()
        
    def setup_and_run_validation(self):
        # Instantiate and execute the validation class
        test = self.validation_class()
        for filename in test.fileResourceNames:
            self.input_into_shared_resources(filename)

        test.execute_with_shared_resources(self.shared_resources)