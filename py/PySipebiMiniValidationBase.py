from diag.core.PySipebiDiagnosticsError import PySipebiDiagnosticsError

# The base class for all validation scripts
class PySipebiMiniValidationBase:
    # Validation script execution-related properties
    diagScriptFileName = ''  # the name of the Python diagnostics script (DS) associated with this validation script (i.e. PySipebiPerbaikanKataHubung.py)
    sipebiErrorCodes = []  # the list of Sipebi error codes (i.e. [KH01, KH02, Sipebi Error 1]) associated with this validation base. Note that Sipebi error code may or may not be the same as EYD error code
    isReady = False  # flag to indicate if this validation script is ready to be run (in case it needs a special preparation)
    isCompleted = False  # flag to indicate if a validation script is executed completely and successfully. Do not set this flag as true if the validation script is executed but not successfully
    failReason = ''  # string to explain the result for the failing the validation script execution (that is, isCompleted = False), if any
    outputContent = ''  # MUST BE FILLED PROPERLY: the string result of the validation
    outputFilename = ''  # MUST BE DEFINED PROPERLY: the string to indicate the intended output file name of this validation script

    # Diagnostics script result-related properties
    commonCheckErrorCodes = []  # the list of error codes provided by common check file, this may or may not be identical to sipebiErrorCodes
    commonCheckDiagnosticsErrors = []  # the list of diagnostics errors in the common check file, if any
    isPassed = False  # flag to indicate if the DS functions fully as expected
    commonMistakes = []  # list of common mistakes after the execution of the DS, if any (the DS does NOT functions fully as expected)
    specialMistakes = []  # list of special mistakes after the execution of the DS, if any (the DS does NOT functions fully as expected)

    # Shared resources related properties
    # hasSharedResources: indicating that this validation has file resources
    hasSharedResources = False
    fileResourceNames = []  # file resources that are taken from py\data\ folder
    diagFileResourceNames = []  # file resources that are taken from py\diag\data\ folder instead of from data folder

    # Functions/Methods
    # The base function for validation script setup (by default there is nothing prepared for the validation to be ready)
    def setup(self):
        self.isReady = True

    # The base function to execute the validation script
    def execute(self):
        pass

    # The base function to execute the validation script with shared resources
    def execute_with_shared_resources(self, shared_resources):
        pass

    # The base function to re-initialize "changing" variables for the preparation of the next call
    def init_changing_vars(self):
        self.isCompleted = False
        self.isPassed = False
        self.failReason = ''
        self.commonMistakes = []
        self.specialMistakes = []

    # Function to indicate if this script has to be executed using execute_with_shared_resources
    # override this function when needed
    def require_shared_resources(self):
        return False

    # The base function to get base diagnostics name from the given diagnostics script file name
    # Example: PyDiagExampleClass.py -> PyDiagExampleClass
    def get_diag_base_name(self):
        if len(self.diagScriptFileName) <= len('.py'):
            return ''
        return self.diagScriptFileName[0:len(self.diagScriptFileName)-len('.py')]

    # The base function to obtain the full name used as the key for the validation-exclusive file resource in the shared_resources
    def get_file_resource_key(self, file_resource_name):
        return "data\\" + file_resource_name

    # The base function to obtain the full name used as the key for the diagnostics file resource in the shared_resources
    def get_dfile_resource_key(self, file_resource_name):
        return "diag\\data\\" + file_resource_name

    # The base function to read the content of the file resources which have been registered in the fileResourceNames
    #   This function requires shared_resources as an input
    #   Thus, this function can only be called properly inside the function execute_with_shared_resources
    # Note: the encoding used for all file resources are 'UTF-8'
    def read_file(self, file_name, shared_resources):
        file_resource_key = self.get_file_resource_key(file_name)
        if file_resource_key in shared_resources.keys():
            return shared_resources[file_resource_key]
        return ''

    # Exactly the same function as read_file, except that this is used to read the file from py\diag\data folder
    #   instead of from py\data folder
    def read_dfile(self, file_name, shared_resources):
        file_resource_key = self.get_dfile_resource_key(file_name)
        if file_resource_key in shared_resources.keys():
            return shared_resources[file_resource_key]
        return ''

    # The base function to write the validation result to the outputContent
    def write_output_content(self):
        # Prepare to write the results to the output file
        self.outputContent = 'complete\r\n' if self.isCompleted else 'fail\r\n'
        if not self.isCompleted:
            self.outputContent += self.failReason + '\r\n'
        self.outputContent += 'pass\r\n' if self.isPassed else 'fail\r\n'
        cm_no = len(self.commonMistakes)
        self.outputContent += str(cm_no)
        for i in range(0, cm_no):
            self.outputContent += self.commonMistakes[i] + '\r\n'
        sm_no = len(self.specialMistakes)
        self.outputContent += str(sm_no)
        for i in range(0, sm_no):
            self.outputContent += self.specialMistakes[i] + '\r\n'

        # Getting the supposed output file name from the script name
        # PyDiagExampleClass.py -> PyDiagExampleClass + _result.txt
        self.outputFilename = self.get_diag_base_name() + '_result.txt'

    """ Content example:
        <line 1> KH01, KH02, Sipebi Error 1
        <line 2> 3
        <line 3> KH01|01|02|burungburung|burung-burung|False 
        <line 4> KH01|01|13|berhari hari|berhari-hari|False 
        <line 5> KH01|02|08|Kurukuru,|kuru-kuru,|True
        
        Content explanation:
        <line 1> KH01, KH02, Sipebi Error 1  -> the associated Sipebi error code tested
        <line 2> 3                           -> the expected no of PySipebiDiagnosticsError 
        <line 3>-<line 5>                    -> the list of PySipebiDiagnosticsErrors, in sequence
          Format of each PySipebiDiagnosticsError item in <line 3>-<line 5>: 
            <ErrorCode>|<ParagraphNo>|<ElementNo>|<OriginalElement>|<CorrectedElement>|<IsAmbiguous>
    """
    # The base method to parse common check file associated with this validation
    def parse_common_check(self, shared_resources):
        common_check_filename = self.get_diag_base_name() + '_common_check.txt'
        try:
            # Read common check file, get its content
            common_check_file = self.read_file(common_check_filename, shared_resources)
            common_check_lines = common_check_file.splitlines()

            # Splitting error codes (i.e. "KH01, KH02, Sipebi Error 1")
            self.commonCheckErrorCodes = [x.strip() for x in common_check_lines[0].split(',')]

            # Get the number of expected number of diagnostics errors/common mistakes
            common_check_no = int(common_check_lines[1].strip())
            self.commonCheckDiagnosticsErrors.clear()

            # List all the expected diagnostics errors
            for i in range(common_check_no):
                de_info_lines = [x for x in common_check_lines[i + 2].split('|')]  # Note: we must NOT use x.strip() here because whitespace could be part of the diagnosed and/or corrected text
                new_de = PySipebiDiagnosticsError()
                new_de.ErrorCode = '[' + de_info_lines[0] + ']'
                new_de.ParagraphNo = int(de_info_lines[1])
                new_de.ElementNo = int(de_info_lines[2])
                new_de.OriginalElement = int(de_info_lines[3])
                new_de.CorrectedElement = int(de_info_lines[4])
                new_de.IsAmbiguous = de_info_lines[5].lower() == 'true'
                self.commonCheckDiagnosticsErrors.append(new_de)

            # Return true if everything is OK
            return True
        except:
            # Return false if there is any problem with the common check file parsing
            return False
        
    def parse_common_check_python(self, shared_resources):
        common_check_filename = self.get_diag_base_name() + '_common_check.txt'
        try:
            # Read common check file, get its content
            common_check_file = shared_resources.get(common_check_filename)
            common_check_lines = common_check_file.splitlines()

            # Splitting error codes (i.e. "KH01, KH02, Sipebi Error 1")
            self.commonCheckErrorCodes = [x.strip() for x in common_check_lines[0].split(',')]

            # Get the number of expected number of diagnostics errors/common mistakes
            common_check_no = int(common_check_lines[1].strip())
            self.commonCheckDiagnosticsErrors.clear()

            # List all the expected diagnostics errors
            for i in range(common_check_no):
                de_info_lines = [x for x in common_check_lines[i + 2].split('|')]  # Note: we must NOT use x.strip() here because whitespace could be part of the diagnosed and/or corrected text
                new_de = PySipebiDiagnosticsError()
                new_de.ErrorCode = '[' + de_info_lines[0] + ']'
                new_de.ParagraphNo = int(de_info_lines[1])
                new_de.ElementNo = int(de_info_lines[2])
                new_de.OriginalElement = de_info_lines[3]
                new_de.CorrectedElement = de_info_lines[4]
                new_de.IsAmbiguous = de_info_lines[5].lower() == 'true'
                self.commonCheckDiagnosticsErrors.append(new_de)

            # Return true if everything is OK
            return True
        except:
            # Return false if there is any problem with the common check file parsing
            return False
        
    def write_output_content_python(self):
        # Prepare to write the results to the output file
        self.outputContent = 'complete\r\n' if self.isCompleted else 'fail\r\n'
        if not self.isCompleted:
            self.outputContent += self.failReason + '\r\n'
        self.outputContent += 'pass\r\n' if self.isPassed else 'fail\r\n'
        cm_no = len(self.commonMistakes)
        self.outputContent += str(cm_no) + ' common mistakes found\r\n'
        for i in range(0, cm_no):
            self.outputContent += self.commonMistakes[i] + '\r\n'
        sm_no = len(self.specialMistakes)
        self.outputContent += str(sm_no) + ' special mistakes found\r\n'
        for i in range(0, sm_no):
            self.outputContent += self.specialMistakes[i] + '\r\n'

        # Getting the supposed output file name from the script name
        # PyDiagExampleClass.py -> PyDiagExampleClass + _result.txt
        self.outputFilename = self.get_diag_base_name() + '_result.txt'
        root = 'py\\data\\results\\'

        root_and_filename = root + self.outputFilename

        # Write the output content to the output file
        with open(root_and_filename, 'w') as f:
            f.write(self.outputContent)