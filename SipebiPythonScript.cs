using System;
using System.Collections.Generic;
using System.Configuration;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using IronPython;
using IronPython.Hosting;
using IronPython.Runtime;
using Microsoft.Scripting.Hosting;
using SipebiMini.Core;

namespace SipebiMini {
	//IronPython example is taken from:
	//https://www.dotnetlovers.com/article/216/executing-python-script-from-c-sharp
	public class SipebiPythonScript {
		//All properties of a script
		private ScriptEngine pyEngine;
		private string pyScript;
		private ScriptSource pySource;
		private ScriptScope pyScope;
		private dynamic pyClass;
		public dynamic PyInstance;

		public bool IsReady { get; private set; } = false;

		public void Initialize(ScriptEngine pyEngine, string scriptPath, string scriptFileName, string scriptClassName) {
			if (pyEngine == null || string.IsNullOrWhiteSpace(scriptPath) || !File.Exists(scriptPath) ||
				string.IsNullOrWhiteSpace(scriptFileName) || string.IsNullOrWhiteSpace(scriptClassName))
				return;
			//Get the script, prepare all necessary properties associated with the script
			pyScript = getFormattedScript(scriptPath);
			if (string.IsNullOrWhiteSpace(pyScript)) return;
			this.pyEngine = pyEngine;
			pySource = this.pyEngine.CreateScriptSourceFromString(pyScript);
			pyScope = this.pyEngine.CreateScope();
			pySource.Execute(pyScope);
			pyClass = pyScope.GetVariable(scriptClassName);
			PyInstance = this.pyEngine.Operations.CreateInstance(pyClass);
			PyInstance.setup(); //Setup the script
			IsReady = PyInstance.isReady;
		}

		//Method to reformat original Python script into script that is executable using this SipebiPythonScript
		private static string reformatScript(string originalPyScript) {
			if (string.IsNullOrWhiteSpace(originalPyScript)) return originalPyScript;
			string[] lines = originalPyScript.Split(new string[] { "\r\n", "\n" }, StringSplitOptions.None);
			StringBuilder sb = new StringBuilder();
			foreach (string line in lines) {
				if (!line.Trim().StartsWith("from ")) {
					sb.AppendLine(line);
					continue;
				}
				//i.e. from diag.PyDiagExampleClass import PyDiagExampleClass
				string[] lineParts = line.Split(new string[] { " " }, StringSplitOptions.RemoveEmptyEntries);
				List<string> reformattedParts = new List<string>();
				foreach (string linePart in lineParts) {
					if (!linePart.Contains('.')) {
						reformattedParts.Add(linePart);
						continue;
					}
					//i.e. diag.PyDiagExampleClass
					string[] subParts = linePart.Split(new string[] { "." }, StringSplitOptions.RemoveEmptyEntries);
					reformattedParts.Add(subParts[subParts.Length - 1]); //Just add the last subpart (i.e. PyDiagExampleClass)
				}
				sb.AppendLine(string.Join(" ", reformattedParts));
			}
			return sb.ToString();
		}

		//Method to get (re-)formatted script, ready to be used by this SipebiPythonScript, from a file path
		private static string getFormattedScript(string scriptPath) {
			string script = File.ReadAllText(scriptPath);
			script = reformatScript(script);
			return script;
		}
	}
}
