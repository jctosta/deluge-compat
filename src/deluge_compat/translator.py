"""Deluge to Python code translator."""

import re
from typing import Dict, List, Any


class DelugeTranslator:
    """Translates Deluge script syntax to Python code."""
    
    def __init__(self):
        self.indent_level = 0
        self.in_invokeurl = False
    
    def translate(self, deluge_code: str) -> str:
        """Translate Deluge code to Python code."""
        # Reset state for each translation
        self.indent_level = 0
        self.in_invokeurl = False
        
        # Preprocess the code to handle } else { patterns
        preprocessed = self._preprocess_code(deluge_code)
        
        lines = preprocessed.split('\n')
        python_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            translated = self._translate_line(line)
            if translated:
                python_lines.append(translated)
        
        return '\n'.join(python_lines)
    
    def _preprocess_code(self, code: str) -> str:
        """Preprocess Deluge code to handle special patterns."""
        # First handle inline } else { patterns
        code = re.sub(r'}\s*else\s*{', '}\nelse {', code)
        
        lines = code.split('\n')
        processed_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Handle } else { pattern (now on separate lines)
            if line == '}' and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith('else'):
                    # Add the closing brace
                    processed_lines.append('}')
                    # Add the else statement
                    if next_line.endswith('{'):
                        processed_lines.append(next_line[:-1].strip() + ' {')  # else with {
                    else:
                        processed_lines.append(next_line)
                    i += 2  # Skip the next line since we processed it
                    continue
            
            processed_lines.append(lines[i])
            i += 1
        
        return '\n'.join(processed_lines)
    
    def _translate_line(self, line: str) -> str:
        """Translate a single line of Deluge code."""
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('//'):
            return ''
        
        # Handle multi-line comments
        if line.startswith('/*') or line.endswith('*/'):
            return ''
        
        # Handle closing braces first (decrease indent before processing)
        if line == '}':
            self.indent_level -= 1
            return ''
        
        # Handle control structures that end with opening brace
        if line.startswith('if(') or line.startswith('if '):
            result = self._translate_if(line)
            if line.rstrip().endswith('{'):
                self.indent_level += 1
            return result
        elif line.startswith('for each'):
            result = self._translate_for_each(line)
            if line.rstrip().endswith('{'):
                self.indent_level += 1
            return result
        elif line.startswith('while('):
            result = self._translate_while(line)
            if line.rstrip().endswith('{'):
                self.indent_level += 1
            return result
        elif line.startswith('else'):
            result = self._translate_else(line)
            if line.rstrip().endswith('{'):
                self.indent_level += 1
            return result
        
        # Handle standalone opening braces
        elif line == '{':
            self.indent_level += 1
            return ''
        
        # Handle invokeurl blocks
        elif line.startswith('invokeurl'):
            return self._translate_invokeurl_start(line)
        elif line == '];':
            return self._translate_invokeurl_end()
        elif self.in_invokeurl and ':' in line:
            return self._translate_invokeurl_param(line)
        
        # Handle function calls and statements
        elif line.startswith('info '):
            return self._translate_info(line)
        elif line.startswith('return'):
            return self._translate_return(line)
        
        # Handle variable declarations and assignments
        elif '=' in line and not any(op in line for op in ['==', '!=', '<=', '>=']):
            return self._translate_assignment(line)
        
        # Handle statements ending with semicolon
        elif line.endswith(';'):
            return self._translate_statement(line)
        
        return ''
    
    def _get_indent(self) -> str:
        """Get current indentation string."""
        return '    ' * self.indent_level
    
    def _translate_assignment(self, line: str) -> str:
        """Translate variable assignment."""
        line = line.rstrip(';')
        
        # Handle special constructors
        if 'Map()' in line:
            line = line.replace('Map()', 'Map()')
        elif 'List()' in line:
            line = line.replace('List()', 'List()')
        elif 'list()' in line:
            line = line.replace('list()', 'List()')
        elif 'Collection()' in line:
            line = line.replace('Collection()', 'Map()')
        
        # Handle string literals - wrap in deluge_string
        line = self._wrap_string_literals(line)
        
        # Handle method calls on strings
        line = self._translate_string_methods(line)
        
        return self._get_indent() + line
    
    def _translate_if(self, line: str) -> str:
        """Translate if statement."""
        # Handle both 'if(' and 'if ' syntax
        if line.startswith('if('):
            # Extract condition from if(condition) {
            paren_start = line.find('(')
            paren_end = line.rfind(')')
            if paren_start != -1 and paren_end != -1:
                condition = line[paren_start + 1:paren_end]
            else:
                condition = line[3:].rstrip('{').strip()
        else:
            # Handle 'if ' syntax
            condition = line[3:].rstrip('{').strip()
        
        # Translate condition
        condition = self._translate_condition(condition)
        
        return self._get_indent() + f'if {condition}:'
    
    def _translate_else(self, line: str) -> str:
        """Translate else statement."""
        line_clean = line.rstrip('{').strip()
        
        # else/elif should be at the same level as the corresponding if
        # So we need to temporarily decrease indent to match the if level
        temp_indent_level = max(0, self.indent_level - 1) if line.endswith('{') else self.indent_level
        indent_str = '    ' * temp_indent_level
        
        if line_clean == 'else':
            return indent_str + 'else:'
        elif line_clean.startswith('else if'):
            # else if case
            condition = line_clean[7:].strip()  # Remove 'else if'
            if condition.startswith('(') and condition.endswith(')'):
                condition = condition[1:-1]
            condition = self._translate_condition(condition)
            return indent_str + f'elif {condition}:'
        else:
            return indent_str + 'else:'
    
    def _translate_for_each(self, line: str) -> str:
        """Translate for each loop."""
        # Extract variable and iterable from 'for each var in iterable'
        line_clean = line.rstrip('{').strip()
        match = re.match(r'for each\s+(\w+)\s+in\s+(.+)', line_clean)
        if match:
            var_name = match.group(1)
            iterable = match.group(2).strip()
            return self._get_indent() + f'for {var_name} in {iterable}:'
        return self._get_indent() + line_clean + ':'
    
    def _translate_while(self, line: str) -> str:
        """Translate while loop."""
        condition = line[6:].rstrip('{').strip()
        if condition.startswith('(') and condition.endswith(')'):
            condition = condition[1:-1]
        condition = self._translate_condition(condition)
        return self._get_indent() + f'while {condition}:'
    
    def _translate_condition(self, condition: str) -> str:
        """Translate condition expressions."""
        # Handle method calls
        condition = self._translate_string_methods(condition)
        
        # Handle null checks
        condition = condition.replace('== NULL', 'is None')
        condition = condition.replace('!= NULL', 'is not None')
        condition = condition.replace('== null', 'is None')
        condition = condition.replace('!= null', 'is not None')
        
        # Handle boolean values
        condition = condition.replace(' true', ' True')
        condition = condition.replace(' false', ' False')
        
        return condition
    
    def _translate_invokeurl_start(self, line: str) -> str:
        """Start of invokeurl block."""
        # Extract variable assignment if present
        if '=' in line:
            var_name = line.split('=')[0].strip()
            self.in_invokeurl = True
            return self._get_indent() + f'{var_name} = _invokeurl({{'
        else:
            self.in_invokeurl = True
            return self._get_indent() + '_invokeurl({'
    
    def _translate_invokeurl_param(self, line: str) -> str:
        """Translate invokeurl parameter."""
        line = line.strip()
        if line.endswith(','):
            line = line[:-1]
        
        # Split on first ':'
        parts = line.split(':', 1)
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            
            # Wrap string values in quotes if not already quoted
            if not (value.startswith('"') and value.endswith('"')):
                if not value.startswith('(') and not value.isdigit():
                    # Check if it's a variable reference
                    if not any(c in value for c in ['.', '(', ')', '+', '-', '*', '/']):
                        value = f'"{value}"'
            
            return self._get_indent() + f'    "{key}": {value},'
        
        return self._get_indent() + f'    {line},'
    
    def _translate_invokeurl_end(self) -> str:
        """End of invokeurl block."""
        self.in_invokeurl = False
        return self._get_indent() + '})'
    
    def _translate_info(self, line: str) -> str:
        """Translate info statement."""
        content = line[5:].rstrip(';').strip()
        return self._get_indent() + f'info({content})'
    
    def _translate_return(self, line: str) -> str:
        """Translate return statement."""
        content = line[6:].rstrip(';').strip()
        content = self._wrap_string_literals(content)
        return self._get_indent() + f'return {content}'
    
    def _translate_statement(self, line: str) -> str:
        """Translate general statement."""
        line = line.rstrip(';')
        line = self._translate_string_methods(line)
        return self._get_indent() + line
    
    def _wrap_string_literals(self, text: str) -> str:
        """Wrap string literals with deluge_string() calls."""
        # Find string literals (content within quotes)
        def replace_string(match):
            quote_char = match.group(1)
            content = match.group(2)
            return f'deluge_string({quote_char}{content}{quote_char})'
        
        # Handle both single and double quoted strings
        text = re.sub(r'(["\'])([^"\']*)\1', replace_string, text)
        return text
    
    def _translate_string_methods(self, text: str) -> str:
        """Translate string method calls to use Deluge string methods."""
        # Common method translations
        method_map = {
            '.trim()': '.trim()',
            '.length()': '.length()',
            '.contains(': '.contains(',
            '.startsWith(': '.startsWith(',
            '.endsWith(': '.endsWith(',
            '.toLowerCase()': '.toLowerCase()',
            '.toUpperCase()': '.toUpperCase()',
            '.substring(': '.substring(',
            '.subString(': '.subString(',
            '.subText(': '.subText(',
            '.indexOf(': '.indexOf(',
            '.lastIndexOf(': '.lastIndexOf(',
            '.replaceAll(': '.replaceAll(',
            '.replaceFirst(': '.replaceFirst(',
            '.toList(': '.toList(',
            '.toMap()': '.toMap()',
            '.size()': '.size()',
            '.isEmpty()': '.isEmpty()',
            '.get(': '.get(',
            '.put(': '.put(',
            '.add(': '.add(',
            '.remove(': '.remove(',
            '.clear()': '.clear()',
        }
        
        for deluge_method, python_method in method_map.items():
            text = text.replace(deluge_method, python_method)
        
        return text


def _invokeurl(params: Dict[str, Any]) -> Any:
    """Execute an HTTP request based on invokeurl parameters."""
    from .functions import getUrl, postUrl
    
    url = params.get('url', '')
    request_type = params.get('type', 'GET').upper()
    headers = params.get('headers', {})
    parameters = params.get('parameters', {})
    
    if request_type == 'GET':
        return getUrl(url, headers=headers)
    elif request_type == 'POST':
        return postUrl(url, body=parameters, headers=headers)
    else:
        # For other HTTP methods, use requests directly
        try:
            import requests
            method = request_type.lower()
            if hasattr(requests, method):
                response = getattr(requests, method)(url, json=parameters, headers=headers)
                return response.text
            else:
                return "Unsupported HTTP method"
        except ImportError:
            return "Requests module not available"