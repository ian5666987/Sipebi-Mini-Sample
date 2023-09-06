# The base class for all validation scripts
class PySipebiMiniValidationBase:
    # Validation script execution-related properties
    scriptName = ''  # the name of the Python diagnostics script (DS) associated with this validation base (i.e. PySipebiMiniPerbaikanKataHubung.py)
    sipebiErrorCodes = []  # the list of Sipebi error codes (i.e. [KH01, KH02, Sipebi Error 1]) associated with this validation base. Note that Sipebi error code may or may not be the same as EYD error code
    isReady = False # flag to indicate if this validation script is ready to be run (in case it needs a special preparation)
    isCompleted = False  # flag to indicate if a validation script is executed completely and successfully. Do not set this flag as true if the validation script is executed but not successfully
    failReason = ''  # string to explain the result for the failing the validation script execution (that is, isCompleted = False), if any

    # Diagnostics result-related properties
    isPassed = False  # flag to indicate if the DS functions fully as expected
    commonMistakes = []  # list of common mistakes after the execution of the DS, if any (the DS does NOT functions fully as expected)
    specialMistakes = []  # list of special mistakes after the execution of the DS, if any (the DS does NOT functions fully as expected)

    # Functions/Methods
    # The base function for validation script setup (by default there is nothing prepared for the validation to be ready)
    def setup(self):
        self.isReady = True

    # The base function to execute the validation script
    def execute(self):
        pass

    # The base function to re-initialize "changing" variables for the preparation of the next call
    def init_changing_vars(self):
        self.isCompleted = False
        self.isPassed = False
        self.failReason = ''
        self.commonMistakes = []
        self.specialMistakes = []

