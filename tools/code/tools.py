import io
import contextlib
from typing import Dict, Any
import traceback

from core.logger import logger

# List of allowed modules that can be imported
ALLOWED_MODULES = {
    'math', 'random', 'datetime', 'json', 're', 'collections',
    'itertools', 'functools', 'operator', 'string', 'array', 'bisect',
    'heapq', 'statistics', 'base64', 'hashlib', 'hmac', 'secrets'
}

class CodeExecutionError(Exception):
    """Custom exception for code execution errors"""
    pass

def _create_restricted_globals() -> Dict[str, Any]:
    """Create a restricted globals dictionary with safe builtins"""
    safe_builtins = {
        '__builtins__': {
            name: getattr(__builtins__, name) 
            for name in [
                'abs', 'all', 'any', 'bool', 'callable', 'chr', 'dict', 'divmod', 
                'enumerate', 'filter', 'float', 'frozenset', 'int', 'isinstance', 
                'issubclass', 'iter', 'len', 'list', 'map', 'max', 'min', 'next', 
                'object', 'ord', 'pow', 'print', 'range', 'repr', 'reversed', 
                'round', 'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'zip'
            ]
        },
        'math': __import__('math'),
        'random': __import__('random'),
        'datetime': __import__('datetime'),
        'json': __import__('json'),
        're': __import__('re'),
        'collections': __import__('collections'),
        'itertools': __import__('itertools'),
        'functools': __import__('functools'),
        'operator': __import__('operator'),
        'string': __import__('string'),
        'array': __import__('array'),
        'bisect': __import__('bisect'),
        'heapq': __import__('heapq'),
        'statistics': __import__('statistics'),
        'base64': __import__('base64'),
        'hashlib': __import__('hashlib'),
        'hmac': __import__('hmac'),
        'secrets': __import__('secrets'),
    }
    return safe_builtins

def execute_python_code(
    code: str,
    max_output_length: int = 1000
) -> Dict[str, Any]:
    """
    Execute Python code in a restricted environment.
    
    Args:
        code: Python code to execute
        max_output_length: Maximum length of the output
        
    Returns:
        Dict containing the execution result, output, and any errors
    """
    if not code.strip():
        return {
            'success': False,
            'error': 'No code provided',
            'output': ''
        }
    
    # Create a restricted globals dictionary
    restricted_globals = _create_restricted_globals()
    
    # Create a string buffer to capture stdout and stderr
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    
    # Redirect stdout and stderr
    with contextlib.redirect_stdout(stdout_buffer), \
         contextlib.redirect_stderr(stderr_buffer):
        
        try:
            # Compile the code first to check for syntax errors
            try:
                compiled_code = compile(code, '<string>', 'exec')
            except SyntaxError as e:
                logger.error(f"Syntax error: {str(e)}")
                return {
                    'success': False,
                    'error': f'Syntax error: {str(e)}',
                    'output': '',
                    'traceback': str(e)
                }
            
            # Execute the code with a timeout
            try:
                # Create a local namespace for the code execution
                local_vars = {}
                
                # Execute the code
                exec(compiled_code, restricted_globals, local_vars)
                
                # Get the result (if any)
                result = local_vars.get('result', None)
                
                # Get the output
                output = stdout_buffer.getvalue()
                
                # Truncate output if too long
                if len(output) > max_output_length:
                    output = output[:max_output_length] + '\n... (output truncated)'
                
                # Check for errors in stderr
                error_output = stderr_buffer.getvalue()
                if error_output:
                    logger.error(f"Error during execution: {error_output}")
                    return {
                        'success': False,
                        'error': 'Error during execution',
                        'output': output,
                        'stderr': error_output[:max_output_length]
                    }
                
                return {
                    'success': True,
                    'result': str(result) if result is not None else None,
                    'output': output,
                    'type': type(result).__name__ if result is not None else None
                }
                
            except Exception as e:
                tb = traceback.format_exc()
                logger.error(f"Execution error: {str(e)}")
                return {
                    'success': False,
                    'error': f'Execution error: {str(e)}',
                    'output': stdout_buffer.getvalue(),
                    'traceback': tb
                }
                
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Unexpected error: {str(e)}")
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'output': stdout_buffer.getvalue(),
                'traceback': tb
            }
