
import { loadPyodide, type PyodideInterface } from 'pyodide'

// The pyodide instance is loaded once and stored in a promise to avoid re-loading.
let pyodidePromise: Promise<PyodideInterface> | null = null

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

`

function objectToSvgString(obj: any): string {
  if (!obj || typeof obj !== 'object') {
    return '';
  }

  const tagName = obj.tag;
  if (!tagName) {
    return '';
  }

  let propsString = '';
  if (obj.props) {
    for (const key in obj.props) {
      // Convert camelCase to kebab-case for SVG attributes
      const svgKey = key.replace(/([a-z0-9]|(?=[A-Z]))([A-Z])/g, '$1-$2').toLowerCase();
      propsString += ` ${svgKey}="${obj.props[key]}"`;
    }
  }

  let childrenString = '';
  if (obj.children) {
    for (const child of obj.children) {
      if (typeof child === 'string') {
        childrenString += child;
      } else if (typeof child === 'object') {
        childrenString += objectToSvgString(child);
      }
    }
  }

  return `<${tagName}${propsString}>${childrenString}</${tagName}>`;
}

class PythonRunner {
  private async getPyodide(): Promise<PyodideInterface> {
    if (pyodidePromise) {
      return pyodidePromise
    }

    pyodidePromise = (async () => {
      console.log('Loading Pyodide...')
      const pyodide = await loadPyodide({
        indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.28.2/full/',
      })
      console.log('Pyodide loaded.')
      return pyodide
    })()

    return pyodidePromise
  }

  public async runChallenge(
    userCode: string,
    testCases: Array<[any, any]>,
    functionName: string,
    successMessage: string,
    captureSvg: boolean = false
  ): Promise<{ output: string; success: boolean; error: string | null; svgOutput?: string }> {
    try {
      const pyodide = await this.getPyodide()
      let output = ''
      let svgOutput: string | undefined

      pyodide.setStdout({ batched: (str) => (output += str + '\n') })
      pyodide.setStderr({ batched: (str) => (output += str + '\n') })

      if (captureSvg) {
        // Install micropip and pyodide-turtlegraphics
        await pyodide.loadPackage('micropip')
        await pyodide.runPythonAsync(`
          import micropip
          micropip.install('/turtle-0.0.1-py3-none-any.whl')
        `)
        // Force re-import and setup of turtle for a clean state
        await pyodide.runPythonAsync(`
          import sys
          if 'turtle' in sys.modules:
              del sys.modules['turtle']
          import turtle
          turtle.setup()
        `)
      }

      const testCasesJson = JSON.stringify(testCases)

      // Combine user code and test code
      const fullCode = `
${userCode}

${GENERIC_PYTHON_TEST_RUNNER}
run_tests('${functionName}', '${testCasesJson}')
`

      await pyodide.runPythonAsync(fullCode)

      if (captureSvg) {
        // Get the SVG output
        const turtleSvgObject = pyodide.globals.get('turtle').svg()
        console.log('Raw SVG object from Pyodide:', turtleSvgObject)
        svgOutput = objectToSvgString(turtleSvgObject)
      }

      const success = output.includes(successMessage)

      return { output, success, error: null, svgOutput }
    } catch (e: any) {
      console.error('Error running python challenge', e)
      // The output might still be useful for debugging
      const finalOutput = (e.output || '') + `
--- ERROR ---
${e.message}`
      return { output: finalOutput, success: false, error: e.message }
    }
  }
}

// Export a singleton instance of the runner
export const pythonRunner = new PythonRunner()
