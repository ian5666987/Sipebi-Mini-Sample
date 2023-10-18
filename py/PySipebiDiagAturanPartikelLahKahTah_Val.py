# All validation class must be derived from PySipebiMiniValidationBase
from PySipebiMiniValidationBase import PySipebiMiniValidationBase
from diag.PySipebiDiagAturanPartikelLahKahTah import PySipebiDiagAturanPartikelLahKahTah
from diag.core.PySipebiStructs import PySipebiTextDivision
from PySipebiCommonValidationRunner import PySipebiCommonValidationRunner

class PySipebiDiagAturanPartikelLahKahTah_Val(PySipebiMiniValidationBase):
    # Additional properties which are not in the base class
    isInputFileAvailable = False  # Just an example
    commonMistakeFound = False  # Just an example
    specialMistakeFound = False  # Just an example

    # Values of base class properties requiring different default values
    diagScriptFileName = 'PySipebiDiagAturanPartikelLahKahTah.py'
    sipebiErrorCodes = ['[KE01]']

    # Shared resources and output-related properties
    hasSharedResources = True
    # file resources that are taken from py\data\ folder
    fileResourceNames = \
        ['PySipebiDiagAturanPartikelLahKahTah_common_check.txt',
        'PySipebiDiagAturanPartikelLahKahTah_test.txt']
    # the output file name of this validation script
    outputFilename = 'PySipebiDiagAturanPartikelLahKahTah_result.txt'

    # Supposing there is no override needed in the setup, init_changing_vars, and write_output_content methods
    # We will only need to override execute method as shown below
    def execute_with_shared_resources(self, shared_resources):
        # Some initialization here
        # re-initialize all the variables (to clear the results from the previous call)
        self.init_changing_vars()

        self.isInputFileAvailable = True
        self.commonMistakeFound = False
        self.specialMistakeFound = False

        # Wrap the whole mechanism except for write_output_content in a single try-except block
        try:
            if not self.isInputFileAvailable:
                self.failReason = 'the input file is not found'
                return  # Return immediately as nothing else can be done if there is no input file

            # Here, parse the common_guide text
            self.parse_common_check_python(shared_resources)

            # Run the diagnostics script here
            diag_script = PySipebiDiagAturanPartikelLahKahTah()
            # TODO read test input file here and execute the diagnostics script using the test input file [PySipebiDiagExample_test.txt]
            test_file = shared_resources.get('PySipebiDiagAturanPartikelLahKahTah_test.txt')

            sipebi_text_division = PySipebiTextDivision(test_file)
            shared_resources['sipebi_text_division'] = sipebi_text_division

            diag_script.execute_with_shared_resources(test_file, shared_resources)

            # TODO put clearer example here if needed
            counter = 0
            for diag in diag_script.diagList:
                if diag.ErrorCode in self.sipebiErrorCodes:
                    # compare with self.commonCheckDiagnosticsErrors
                    # self.commonCheckDiagnosticsErrors is a list of PySipebiDiagnosticsError
                    # code
                    checkDiag = self.commonCheckDiagnosticsErrors[counter]
                    if diag.ElementNo == checkDiag.ElementNo and diag.ParagraphNo == checkDiag.ParagraphNo and diag.OriginalElement == checkDiag.OriginalElement:
                        if diag.CorrectedElement != checkDiag.CorrectedElement:
                            self.commonMistakes.append(f"P{diag.ParagraphNo} E{diag.ElementNo} | Expected '{checkDiag.CorrectedElement}' but got '{diag.CorrectedElement}'")
                            
                    counter += 1

            for i in range(counter, len(self.commonCheckDiagnosticsErrors)):
                self.commonMistakes.append(f"P{self.commonCheckDiagnosticsErrors[i].ParagraphNo} E{self.commonCheckDiagnosticsErrors[i].ElementNo} | Expected '{self.commonCheckDiagnosticsErrors[i].OriginalElement} => {self.commonCheckDiagnosticsErrors[i].CorrectedElement}' but not detected")

                # Check the conditions to consider that the validation result is 'pass' or 'fail'
            self.isPassed = len(self.commonMistakes) == 0 and len(self.specialMistakes) == 0

            # If we reach this point, the validation has been executed successfully
            # Mark the execution as completed successfully, emptied out all mistakes for the next call
            self.isCompleted = True

        except Exception as e:  # catch essentially all exceptions, NOT the best practice but is sufficient for an example
            self.isCompleted = False
            self.failReason = 'Exception: ' + str(e.args)

        self.write_output_content_python()

if __name__ == "__main__":
    validation_runner = PySipebiCommonValidationRunner(PySipebiDiagAturanPartikelLahKahTah_Val)
    validation_runner.setup_and_run_validation()