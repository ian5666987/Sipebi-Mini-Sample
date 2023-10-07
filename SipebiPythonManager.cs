using System;
using System.Collections.Generic;
using System.Configuration;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using IronPython.Hosting;
using IronPython.Runtime;
using IronPython.Runtime.Types;
using Microsoft.Scripting.Hosting;
using SipebiMini.Core;

namespace SipebiMini {
	//IronPython example is taken from:
	//https://www.dotnetlovers.com/article/216/executing-python-script-from-c-sharp
	public class SipebiPythonManager {
		//Various constants
		public const string PY_DIR_NAME = "py";
		public const string CORE_DIR_NAME = "core";
		public const string LIBS_DIR_NAME = "libs";
		public const string DATA_DIR_NAME = "data";
		public const string DIAG_DIR_NAME = "diag";
		public const string DOCS_DIR_NAME = "docs";
		public const string PY_DIAG_SCRIPT_KEY = "PyDiagnosticsScripts";
		public const string PY_VAL_SCRIPT_KEY = "PyValidationScripts";
		public const string PY_DIAG_EXAMPLE_KEY = "PyDiagnosticsExampleScript";
		public const string PY_VAL_EXAMPLE_KEY = "PyValidationExampleScript";

		//Python Engine, diagnostics scripts, and validation scripts
		private static ScriptEngine pyEngine;
		private static List<string> pyDiagScriptNameClasses = new List<string>();
		private static List<string> pyValScriptNameClasses = new List<string>();

		//Example-related properties and constants (Python)
		private static SipebiPythonScript diagPyExampleScript = new SipebiPythonScript();

		//Directories and files
		private static string baseDir;
		private static string coreDir;
		private static string dataDir;
		private static string diagDir;
		private static string docsDir;
		private static string libsDir;
		private static string diagCoreDir;
		private static string diagDataDir;
		private static string diagLibsDir;
		private static string diagExampleFilePath;
		private static string diagExampleClassName;
		private static string diagErrorClassFilePath;

		//Diagnostics scripts-related properties
		private static Dictionary<string, SipebiPythonScript> pyDiagScripts = new Dictionary<string, SipebiPythonScript>();
		private static Dictionary<string, object> pyDiagSharedResources = new Dictionary<string, object>();
		private static Dictionary<string, object> pyDiagFileResources = new Dictionary<string, object>();
		private static Dictionary<string, object> pyValSharedResources = new Dictionary<string, object>();
		private static Dictionary<string, object> pyValFileResources = new Dictionary<string, object>();

		//Validation scripts-related properties
		private static Dictionary<string, SipebiPythonScript> pyValScripts = new Dictionary<string, SipebiPythonScript>();

		public static void Initialize() {
			try {
				//Python Engine initialization
				if (pyEngine != null) return;
				pyEngine = Python.CreateEngine();

				//All necessary directories
				baseDir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, PY_DIR_NAME);
				coreDir = Path.Combine(baseDir, CORE_DIR_NAME);
				dataDir = Path.Combine(baseDir, DATA_DIR_NAME);
				diagDir = Path.Combine(baseDir, DIAG_DIR_NAME);
				docsDir = Path.Combine(baseDir, DOCS_DIR_NAME);
				libsDir = Path.Combine(baseDir, LIBS_DIR_NAME);
				diagCoreDir = Path.Combine(diagDir, CORE_DIR_NAME);
				diagDataDir = Path.Combine(diagDir, DATA_DIR_NAME);
				diagLibsDir = Path.Combine(diagDir, LIBS_DIR_NAME);

				//Get all search paths
				List<string> searchPaths = new List<string>() {
					baseDir, coreDir, docsDir, libsDir,
					diagDir, diagCoreDir, diagLibsDir,
					//NOTE: data directiories are intentionally excluded from the search paths 
					//      dataDir, diagDataDir
				};
				foreach (string dir in searchPaths)
					Directory.CreateDirectory(dir);
				List<string> subLibsDirs = Directory.GetDirectories(libsDir, "*", SearchOption.AllDirectories).ToList();
				List<string> subDiagLibsDirs = Directory.GetDirectories(diagLibsDir, "*", SearchOption.AllDirectories).ToList();
				if (subLibsDirs != null && subLibsDirs.Count > 0)
					foreach (string dir in subLibsDirs)
						if (!searchPaths.Contains(dir))
							searchPaths.Add(dir);
				if (subDiagLibsDirs != null && subDiagLibsDirs.Count > 0)
					foreach (string dir in subDiagLibsDirs)
						if (!searchPaths.Contains(dir))
							searchPaths.Add(dir);
				pyEngine.SetSearchPaths(searchPaths);

				//Get all Python files used for diagnostics and for validation
				if (ConfigurationManager.AppSettings.AllKeys.Contains(PY_DIAG_SCRIPT_KEY))
					pyDiagScriptNameClasses = ConfigurationManager
						.AppSettings[PY_DIAG_SCRIPT_KEY]
						.Split(new string[] { "," }, StringSplitOptions.RemoveEmptyEntries)
						.Select(x => x.Trim()).ToList();
				if (ConfigurationManager.AppSettings.AllKeys.Contains(PY_VAL_SCRIPT_KEY))
					pyValScriptNameClasses = ConfigurationManager
						.AppSettings[PY_VAL_SCRIPT_KEY]
						.Split(new string[] { "," }, StringSplitOptions.RemoveEmptyEntries)
						.Select(x => x.Trim()).ToList();

				//Get all files under data and save their contents as shared resources
				string[] fileResourcePaths = Directory.GetFiles(dataDir, "*.*", SearchOption.TopDirectoryOnly)
					.Where(x => !x.ToLower().EndsWith(".md")).ToArray(); //.md files are excluded
				foreach (string fileResourcePath in fileResourcePaths) {
					string text = File.ReadAllText(fileResourcePath, Encoding.UTF8);
					string fileName = Path.GetFileName(fileResourcePath);
					string fileResourceName = Path.Combine(DATA_DIR_NAME, fileName);
					//Validation file resources are available only for validation scripts, not for diagnostics scripts
					if (!pyValFileResources.ContainsKey(fileResourceName))
						pyValFileResources.Add(fileResourceName, text);
				}
				string[] diagFileResourcePaths = Directory.GetFiles(diagDataDir, "*.*", SearchOption.TopDirectoryOnly)
					.Where(x => !x.ToLower().EndsWith(".md")).ToArray(); //.md files are excluded
				foreach (string dataFileResourcePath in diagFileResourcePaths) {
					string text = File.ReadAllText(dataFileResourcePath, Encoding.UTF8);
					string fileName = Path.GetFileName(dataFileResourcePath);
					string fileResourceName = Path.Combine(DIAG_DIR_NAME, DATA_DIR_NAME, fileName);
					//Diagnostics file resources are available for both diagnostics scripts and validation scripts
					if (!pyDiagFileResources.ContainsKey(fileResourceName))
						pyDiagFileResources.Add(fileResourceName, text);
					if (!pyValFileResources.ContainsKey(fileResourceName))
						pyValFileResources.Add(fileResourceName, text);
				}

				//Initialize diagnostics example script
				initDiagExampleScript();
			} catch (Exception ex){
				throw new Exception($"[{nameof(SipebiPythonManager)}] initialization failed! Ex: {ex}");
			}
		}

		//Method to initialize diagnostics example script
		private static void initDiagExampleScript() {
			if (ConfigurationManager.AppSettings.AllKeys.Contains(PY_DIAG_EXAMPLE_KEY)) {
				string diagExampleFileName = ConfigurationManager.AppSettings[PY_DIAG_EXAMPLE_KEY].Trim();
				diagExampleFilePath = Path.Combine(diagDir, diagExampleFileName);
				diagExampleClassName = diagExampleFileName.Substring(0, diagExampleFileName.Length - ".py".Length).Trim();
				diagPyExampleScript.Initialize(pyEngine, diagExampleFilePath, diagExampleFileName, diagExampleClassName);
			}
		}

		//Method to run a single diagnostics script
		private static List<SipebiDiagnosticsError> runDiagnosticsScript(string text, string scriptFileName, 
			string scriptClassName) {
			List<SipebiDiagnosticsError> errors = new List<SipebiDiagnosticsError>();
			string scriptPath = Path.Combine(diagDir, scriptFileName);

			//If script is not found, return immediately
			if (!File.Exists(scriptPath)) return errors;

			//Get the script, prepare all necessary properties associated with the script
			SipebiPythonScript pyScript = null;
			if (!pyDiagScripts.ContainsKey(scriptFileName)) {
				pyScript = new SipebiPythonScript();
				pyScript.Initialize(pyEngine, scriptPath, scriptFileName, scriptClassName);
				pyDiagScripts.Add(scriptFileName, pyScript);
			} else 
				pyScript = pyDiagScripts[scriptFileName];

			//Execute the script
			pyScript.ExecuteDiagnostics(text, pyDiagSharedResources, pyDiagFileResources);

			//Get the diagnostics results of the script
			PythonList diagList = pyScript.PyInstance.diagList;
			foreach (dynamic diagItem in diagList) {
				SipebiDiagnosticsError error = new SipebiDiagnosticsError();
				error.CorrectedCharPosition = diagItem.CorrectedCharPosition;
				error.CorrectedElement = diagItem.CorrectedElement;
				error.ElementNo = diagItem.ElementNo;
				error.ErrorCode = diagItem.ErrorCode;
				error.IsAmbiguous = diagItem.IsAmbiguous;
				error.OriginalElement = diagItem.OriginalElement;
				error.OriginalParagraphOffset = diagItem.OriginalParagraphOffset;
				error.ParagraphNo = diagItem.ParagraphNo;
				error.PositionOffset = diagItem.PositionOffset;
				errors.Add(error);
			}

			//Return the diagnostics errors
			return errors;
		}

		//Method to run a single validation script
		private static void runValidationScript(string scriptFileName, string scriptClassName) {
			string scriptPath = Path.Combine(baseDir, scriptFileName);

			//If script is not found, return immediately
			if (!File.Exists(scriptPath)) return;

			//Get the script, prepare all necessary properties associated with the script
			SipebiPythonScript pyScript = null;
			if (!pyValScripts.ContainsKey(scriptFileName)) {
				pyScript = new SipebiPythonScript();
				pyScript.Initialize(pyEngine, scriptPath, scriptFileName, scriptClassName, isValidation: true);
				pyValScripts.Add(scriptFileName, pyScript);
			} else
				pyScript = pyValScripts[scriptFileName];

			//Execute the script with the original text as an argument
			pyScript.ExecuteValidation(pyValSharedResources, pyValFileResources);
		}

		//Method to run all diagnostics scripts
		public static List<SipebiDiagnosticsError> RunDiagnostics(string text, SipebiMiniDiagnosticsReport report) {
			List<SipebiDiagnosticsError> errors = new List<SipebiDiagnosticsError>();
			if (pyEngine == null) return errors;
			string currentDiagnosticsScript = string.Empty;
			try {
				//Every time the diagnostics script sequence is re-executed, the shared resources must be cleared
				pyDiagSharedResources.Clear();

				foreach (var scriptNameClass in pyDiagScriptNameClasses) {
					List<SipebiDiagnosticsError> currentScriptErrors = new List<SipebiDiagnosticsError>();

					//Get the diagnostics script and name
					currentDiagnosticsScript = scriptNameClass;

					//script-name possible formats: (1) scriptName-scriptClass or (2) scriptName
					//TODO (1) may no longer be supported
					string scriptFileName = scriptNameClass;
					string scriptClassName = Path.GetFileNameWithoutExtension(scriptNameClass);
					if (scriptNameClass.Contains("-")) {
						List<string> scriptNameParts = scriptNameClass
							.Split('-').Where(x => !string.IsNullOrWhiteSpace(x))
							.Select(x => x.Trim()).ToList();
						//Script name parts must consist of exactly two parts
						if (scriptNameParts.Count == 2) {
							scriptFileName = scriptNameParts[0];
							scriptClassName = scriptNameParts[1];
						}
					}

					//Run the script
					currentScriptErrors = runDiagnosticsScript(text, scriptFileName, scriptClassName);

					//Add the current diagnostics result to the overall diagnostics result
					errors.AddRange(currentScriptErrors);
				}
			} catch (Exception ex) {
				throw new Exception($"Diagnostics script: [{currentDiagnosticsScript}] failed! Ex: {ex}");
			}
			return errors;
		}

		//Method to run all validation scripts
		public static void RunValidation() {
			if (pyEngine == null) return;
			string currentValidationScript = string.Empty;
			try {
				//Every time the validation script sequence is re-executed, the shared resources must be cleared
				pyValSharedResources.Clear();

				foreach (var scriptNameClass in pyValScriptNameClasses) {
					//Get the validation script and name
					currentValidationScript = scriptNameClass;

					//script-name possible formats: (1) scriptName-scriptClass or (2) scriptName
					//TODO (1) may no longer be supported
					string scriptFileName = scriptNameClass;
					string scriptClassName = Path.GetFileNameWithoutExtension(scriptNameClass);
					if (scriptNameClass.Contains("-")) {
						List<string> scriptNameParts = scriptNameClass
							.Split('-').Where(x => !string.IsNullOrWhiteSpace(x))
							.Select(x => x.Trim()).ToList();
						//Script name parts must consist of exactly two parts
						if (scriptNameParts.Count == 2) {
							scriptFileName = scriptNameParts[0];
							scriptClassName = scriptNameParts[1];
						}
					}

					//Run the script
					runValidationScript(scriptFileName, scriptClassName);
				}
			} catch (Exception ex) {
				throw new Exception($"Validation script: [{currentValidationScript}] failed! Ex: {ex}");
			}
		}

		#region Examples
		public static string RunDiagnosticsExample() {
			if (pyEngine == null) return "Test failed!";
			if (diagPyExampleScript == null || !diagPyExampleScript.IsReady ||
				  string.IsNullOrWhiteSpace(diagExampleFilePath) || !File.Exists(diagExampleFilePath))
				initDiagExampleScript();
			if (!diagPyExampleScript.IsReady)
				return "Diagnostics example script is not ready!";
			//Note we do NOT clear the shared resources used in the example to test if it is indeed
			//  NOT re-creating shared resources (supposedly simulating sequential, different, diagnostics scripts execution)
			diagPyExampleScript.ExecuteDiagnostics("initial text", pyDiagSharedResources);
			StringBuilder sb = new StringBuilder();
			sb.AppendLine($"varNo: {diagPyExampleScript.PyInstance.varNo.ToString()}");
			sb.AppendLine($"varStr: {diagPyExampleScript.PyInstance.varStr.ToString()}");
			PythonList diagList = diagPyExampleScript.PyInstance.diagList;
			sb.AppendLine($"diagList: \n-{string.Join("\n-", diagList.ToList().Select(x => ((dynamic)x).SimpleDisplay()))}");
			return sb.ToString();
		}
		#endregion Examples
	}
}
