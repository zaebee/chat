
import { loadPyodide, type PyodideInterface } from 'pyodide'

// The pyodide instance is loaded once and stored in a promise to avoid re-loading.
let pyodidePromise: Promise<PyodideInterface> | null = null

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
    testCode: string,
    successMessage: string
  ): Promise<{ output: string; success: boolean; error: string | null }> {
    try {
      const pyodide = await this.getPyodide()
      let output = ''
      pyodide.setStdout({ batched: (str) => (output += str + '\n') })
      pyodide.setStderr({ batched: (str) => (output += str + '\n') })

      // Combine user code and test code
      const fullCode = `${userCode}\n\n${testCode}`

      await pyodide.runPythonAsync(fullCode)

      const success = output.includes(successMessage)

      return { output, success, error: null }
    } catch (e: any) {
      console.error('Error running python challenge', e)
      // The output might still be useful for debugging
      const finalOutput = (e.output || '') + `\n--- ERROR ---\n${e.message}`
      return { output: finalOutput, success: false, error: e.message }
    }
  }
}

// Export a singleton instance of the runner
export const pythonRunner = new PythonRunner()
