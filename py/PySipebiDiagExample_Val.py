# All validation class must be derived from PySipebiMiniValidationBase
from PySipebiMiniValidationBase import PySipebiMiniValidationBase
# Below are references to the diagnostics classes associated with this validation, change accordingly
from diag.PySipebiDiagExample import PySipebiDiagExample
from diag.core.PySipebiDiagnosticsError import PySipebiDiagnosticsError

# An example of Sipebi Mini validation script
# All Sipebi Mini validation script must be derived from PySipebiMiniValidationBase
class PySipebiDiagExample_Val(PySipebiMiniValidationBase):
    # Additional properties which are not in the base class
    isInputFileAvailable = False  # Just an example
    commonMistakeFound = False  # Just an example
    specialMistakeFound = False  # Just an example

    # Values of base class properties requiring different default values
    diagScriptFileName = 'PySipebiDiagExample.py'
    sipebiErrorCodes = ['KH01', 'KH02', 'Sipebi Error 1']

    # Shared resources and output-related properties
    hasSharedResources = True
    # file resources that are taken from py\data\ folder
    fileResourceNames = \
        ['initial_file_resource_example.txt',
         'PySipebiPerbaikanKataHubung_common_check.txt',
         'PySipebiPerbaikanKataHubung_test.txt']
    # file resources that are taken from py\diag\data\ folder instead of from data folder
    diagFileResourceNames = ['initial_diag_file_resource_example.txt']
    # the output file name of this validation script
    outputFilename = 'PySipebiPerbaikanKataHubung_result.txt'

    # Supposing there is no override needed in the setup, init_changing_vars, and write_output_content methods
    # We will only need to override execute method as shown below
    def execute_with_shared_resources(self, shared_resources):
        # Some initialization here
        # re-initialize all the variables (to clear the results from the previous call)
        self.init_changing_vars()

        self.isInputFileAvailable = False
        self.commonMistakeFound = False
        self.specialMistakeFound = False

        # Wrap the whole mechanism except for write_output_content in a single try-except block
        try:
            # Some setup and checking here (i.e. the checking and getting of input files)
            # Input files: [PySipebiDiagExample_test.txt] + [PySipebiDiagExample_common_guide.txt] + other files needed for this validation
            # Supposing the input file cannot be found for some reason
            if not self.isInputFileAvailable:
                self.failReason = 'the input file is not found'
                return  # Return immediately as nothing else can be done if there is no input file

            # Here, parse the common_guide text
            self.parse_common_check(shared_resources)

            # Run the diagnostics script here
            diag_script = PySipebiDiagExample()
            # TODO read test input file here and execute the diagnostics script using the test input file [PySipebiDiagExample_test.txt]
            diag_script.execute('Replace this with validation test text (i.e. content of [PySipebiDiagExample_test.txt])')

            # Here, make use of diag_script.diagList to identify common mistake(s) and special mistake(s)
            # Compare them with the expected results self.commonCheckDiagnosticsErrors
            # TODO put clearer example here if needed

            # Suppose common mistake(s) is(are) found
            if self.commonMistakeFound:
                # Add the common mistake(s) to the list
                self.commonMistakes.add('diagnostics index [1] [berhari hari] is not generated by [' + self.diagScriptFileName + ']')
                self.commonMistakes.add('[IsAmbiguous] value for diagnostics index [2] [Kurukuru, -> kuru-kuru,] is [False]. Excpected: [True]')

            # Suppose special mistake(s) is(are) found
            if self.specialMistakeFound:
                # Add the special mistake(s) to the list
                self.specialMistakes.add('special comments for special mistakes here')

            # Check the conditions to consider that the validation result is 'pass' or 'fail'
            self.isPassed = len(self.commonMistakes) == 0 and len(self.specialMistakes) == 0

            # If we reach this point, the validation has been executed successfully
            # Mark the execution as completed successfully, emptied out all mistakes for the next call
            self.isCompleted = True

        except Exception as e:  # catch essentially all exceptions, NOT the best practice but is sufficient for an example
            self.isCompleted = False
            self.failReason = 'Exception: ' + str(e.args)

        # Write the validation result to a text file using default (base) method
        self.write_output_content()
