import re

class Parser:
    def analyze_c_string(self, input_string):
        # Regular expressions for matching patterns
        assignment_pattern = r'^[a-zA-Z_]\w*\s*=\s*.+;$'
        declaration_pattern = r'^[a-zA-Z_]\w*\s+[a-zA-Z_]\w*;$'
        function_call_pattern = r'^[a-zA-Z_]\w*\s*\(.*\);$'

        tuple = [input_string]

        # Check if the input matches any of the patterns
        if re.match(assignment_pattern, input_string):
            tuple.append("Accepted: Simple Assignment")
        elif re.match(declaration_pattern, input_string):
            tuple.append("Accepted: Declaration")
        elif re.match(function_call_pattern, input_string):
            tuple.append("Accepted: Function Call")
        else:
            tuple.append("Not Accepted")

        return tuple

    