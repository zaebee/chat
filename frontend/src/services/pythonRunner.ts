import { loadPyodide, type PyodideInterface } from "pyodide";

// The pyodide instance is loaded once and stored in a promise to avoid re-loading.
let pyodidePromise: Promise<PyodideInterface> | null = null;

const GENERIC_PYTHON_TEST_RUNNER = `
import sys
import json

def run_tests(func_name, test_cases_json):
    test_cases = json.loads(test_cases_json)
    all_passed = True
    for i, test_case in enumerate(test_cases):
        args = test_case[0]
        expected = test_case[1]
        try:
            # Dynamically get the function to test
            func = globals()[func_name]
            
            # Handle single argument vs multiple arguments
            if isinstance(args, list) or isinstance(args, tuple):
                result = func(*args)
            else:
                result = func(args)

            assert result == expected, f"Test #{i+1} failed for input {args}: returned {result}, expected {expected}"
            print(f"Test #{i+1} passed!")
        except Exception as e:
            print(f"An error occurred during test #{i+1}: {e}", file=sys.stderr)
            all_passed = False
            break
    if all_passed:
        print("All tests passed!")

`;

interface SvgObject {
  tag: string;
  props?: Record<string, string>;
  children?: Array<string | SvgObject>;
}

function objectToSvgString(obj: unknown): string {
  if (typeof obj !== "object" || obj === null || !("tag" in obj) || typeof obj.tag !== "string") {
    return "";
  }

  const svgObj = obj as SvgObject; // Type assertion after checks

  let propsString = "";
  if (svgObj.props) {
    for (const key in svgObj.props) {
      // Convert camelCase to kebab-case for SVG attributes
      const svgKey = key.replace(/([a-z0-9]|(?=[A-Z]))([A-Z])/g, "$1-$2").toLowerCase();
      propsString += ` ${svgKey}="${svgObj.props[key]}"`;
    }
  }

  let childrenString = "";
  if (svgObj.children) {
    for (const child of svgObj.children) {
      if (typeof child === "string") {
        childrenString += child;
      } else if (typeof child === "object") {
        childrenString += objectToSvgString(child);
      }
    }
  }

  return `<${svgObj.tag}${propsString}>${childrenString}</${svgObj.tag}>`;
}

class PythonRunner {
  private async getPyodide(): Promise<PyodideInterface> {
    if (pyodidePromise) {
      return pyodidePromise;
    }

    pyodidePromise = (async () => {
      // Loading Pyodide...
      const pyodide = await loadPyodide({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.28.2/full/",
      });
      // Pyodide loaded successfully
      return pyodide;
    })();

    return pyodidePromise;
  }

  private onOutputHandler: ((text: string) => void) | null = null;
  private onInputRequestHandler: ((prompt: string) => Promise<string>) | null = null;

  public setIoHandlers(
    onOutput: (text: string) => void,
    onInputRequest: (prompt: string) => Promise<string>,
  ) {
    this.onOutputHandler = onOutput;
    this.onInputRequestHandler = onInputRequest;
  }

  public async runChallenge(
    userCode: string,
    testCases: Array<[unknown, unknown]>,
    functionName: string,
    successMessage: string,
    captureSvg: boolean = false,
  ): Promise<{ output: string; success: boolean; error: string | null; svgOutput?: string }> {
    try {
      const pyodide = await this.getPyodide();
      let output = "";
      let svgOutput: string | undefined;

      // Redirect stdout and stderr to our handler
      pyodide.setStdout({
        batched: (str: string) => {
          output += str + "\n";
          if (this.onOutputHandler) {
            this.onOutputHandler(str);
          }
        },
      });
      pyodide.setStderr({
        batched: (str: string) => {
          output += str + "\n";
          if (this.onOutputHandler) {
            this.onOutputHandler(str);
          }
        },
      });

      // Redirect stdin to our handler
      pyodide.setStdin({
        stdin: () => {
          if (this.onInputRequestHandler) {
            // For now, return a simple prompt - this will need improvement for full async support
            const result = prompt("Python input requested:") || "";
            return result;
          } else {
            console.warn("Input requested but no handler set.");
            return ""; // Return empty string if no handler
          }
        },
      });

      if (captureSvg) {
        // Install micropip and pyodide-turtlegraphics
        await pyodide.loadPackage("micropip");
        await pyodide.runPythonAsync(`
          import micropip
          micropip.install('/turtle-0.0.1-py3-none-any.whl')
        `);
        // Force re-import and setup of turtle for a clean state
        await pyodide.runPythonAsync(`
          import sys
          if 'turtle' in sys.modules:
              del sys.modules['turtle']
          import turtle
          turtle.setup()
        `);
      }

      const testCasesJson = JSON.stringify(testCases);

      // Combine user code and test code
      const fullCode = `
${userCode}

${GENERIC_PYTHON_TEST_RUNNER}
run_tests('${functionName}', '${testCasesJson}')
`;

      await pyodide.runPythonAsync(fullCode);

      if (captureSvg) {
        // Get the SVG output
        const turtleSvgObject = pyodide.globals.get("turtle").svg();
        // Raw SVG object received from Pyodide
        svgOutput = objectToSvgString(turtleSvgObject);
      }

      const success = output.includes(successMessage);

      return { output, success, error: null, svgOutput };
    } catch (error: unknown) {
      console.error("Error running python challenge", error);
      // The output might still be useful for debugging
      let errorMessage = "An unknown error occurred.";
      let errorOutput = "";

      if (error instanceof Error) {
        errorMessage = error.message;
      } else if (typeof error === "string") {
        errorMessage = error;
      }

      // Check if error has an 'output' property (e.g., from Pyodide)
      if (
        typeof error === "object" &&
        error !== null &&
        "output" in error &&
        typeof (error as { output?: string }).output === "string"
      ) {
        errorOutput = (error as { output: string }).output;
      }

      const finalOutput = errorOutput + `\n--- ERROR ---\n${errorMessage}`;
      return { output: finalOutput, success: false, error: errorMessage };
    }
  }

  public async runScript(userCode: string): Promise<{ output: string; error: string | null }> {
    try {
      const pyodide = await this.getPyodide();
      let output = "";

      pyodide.setStdout({
        batched: (str: string) => {
          output += str + "\n";
          if (this.onOutputHandler) {
            this.onOutputHandler(str);
          }
        },
      });
      pyodide.setStderr({
        batched: (str: string) => {
          output += str + "\n";
          if (this.onOutputHandler) {
            this.onOutputHandler(str);
          }
        },
      });

      await pyodide.runPythonAsync(userCode);

      // Quest Verification Logic
      const { useGameStore } = await import("@/stores/game");
      const gameStore = useGameStore();

      if (gameStore.genesisQuestPhase === 1 && output.trim() === "Fiat Lux") {
        gameStore.advanceGenesisQuest();
        output += "\n\n✨ A divine light fills the cosmos! The first ritual is complete. Quest phase advanced! ✨";
      }

      return { output, error: null };
    } catch (error: unknown) {
      console.error("Error running python script", error);
      let errorMessage = "An unknown error occurred.";
      if (error instanceof Error) {
        errorMessage = error.message;
      }
      return { output: errorMessage, error: errorMessage };
    }
  }
}

// Export a singleton instance of the runner
export const pythonRunner = new PythonRunner();
