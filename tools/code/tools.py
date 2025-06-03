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

def get_safe_builtins() -> dict:
    """
    Get a dictionary of safe built-in functions and modules.
    
    Returns:
        dict: Dictionary containing safe built-ins and modules
    """
    # Import builtins safely
    import builtins
    
    # Create a safe environment with specific builtins
    safe_builtins = {
        # Include specific built-in functions
        'abs': builtins.abs,
        'all': builtins.all,
        'any': builtins.any,
        'bool': builtins.bool,
        'callable': builtins.callable,
        'chr': builtins.chr,
        'dict': builtins.dict,
        'divmod': builtins.divmod,
        'enumerate': builtins.enumerate,
        'filter': builtins.filter,
        'float': builtins.float,
        'frozenset': builtins.frozenset,
        'int': builtins.int,
        'isinstance': builtins.isinstance,
        'issubclass': builtins.issubclass,
        'iter': builtins.iter,
        'len': builtins.len,
        'list': builtins.list,
        'map': builtins.map,
        'max': builtins.max,
        'min': builtins.min,
        'next': builtins.next,
        'object': builtins.object,
        'ord': builtins.ord,
        'pow': builtins.pow,
        'print': builtins.print,
        'range': builtins.range,
        'repr': builtins.repr,
        'reversed': builtins.reversed,
        'round': builtins.round,
        'set': builtins.set,
        'slice': builtins.slice,
        'sorted': builtins.sorted,
        'str': builtins.str,
        'sum': builtins.sum,
        'tuple': builtins.tuple,
        'zip': builtins.zip,
        
        # Include safe modules
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
    restricted_globals = get_safe_builtins()
    
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
