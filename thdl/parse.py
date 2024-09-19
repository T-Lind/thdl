import re
from typing import List, Dict

class HDLtoPythonConverter:
    def __init__(self, hdl_code: str):
        self.hdl_code = hdl_code
        self.parsed_parts = []
        self.inputs = []
        self.outputs = []
        self.internal_vars = set()

    def extract_chip_name(self):
        # Extract the chip name from the HDL code
        match = re.search(r'CHIP\s+(\w+)\s*{', self.hdl_code)
        if match:
            return match.group(1)
        return None

    def extract_inputs_outputs(self):
        # Extract the inputs (IN) and outputs (OUT) from the HDL code
        in_match = re.search(r'IN\s+([\w,\s\[\]]+);', self.hdl_code)
        out_match = re.search(r'OUT\s+([\w,\s\[\]]+);', self.hdl_code)

        self.inputs = self.parse_io_list(in_match.group(1)) if in_match else []
        self.outputs = self.parse_io_list(out_match.group(1)) if out_match else []

    def parse_io_list(self, io_str: str) -> List[Dict[str, str]]:
        # Parse inputs or outputs of the form 'a[16], b[16], carry_in' into a list of dictionaries
        io_list = []
        for io in io_str.split(","):
            io = io.strip()
            match = re.match(r'(\w+)(\[(\d+)\])?', io)
            if match:
                name, _, width = match.groups()
                io_list.append({
                    'name': name,
                    'width': width if width else '1'
                })
        return io_list

    def extract_parts(self):
        # Extract each part (component) from the HDL code (e.g., Add4 instances)
        parts = re.findall(r'(\w+)\((.*?)\);', self.hdl_code)
        for part in parts:
            part_name, connections = part
            connections_dict = self.parse_connections(connections)
            self.parsed_parts.append((part_name, connections_dict))
            # Extract internal variables (like carry1, carry2)
            for key, value in connections_dict.items():
                if key.startswith('carry_out') and value not in [out['name'] for out in self.outputs]:
                    self.internal_vars.add(value)


    def parse_connections(self, connections_str):
        # Parse connections in the form a=a[0..3], b=b[0..3], ...
        connections = {}
        for conn in connections_str.split(","):
            conn = conn.strip()
            if "=" in conn:
                var_name, var_value = conn.split("=")
                connections[var_name.strip()] = var_value.strip()
        return connections

    def generate_python_code(self):
        # Generate Python code based on the parsed HDL
        chip_name = self.extract_chip_name()
        self.extract_inputs_outputs()
        self.extract_parts()

        imports = [
            "from thdl.adders import Add4",
            "from thdl.basic_components import HalfAdder, FullAdder",
            "from thdl.val import Val, ValList",
            "from thdl.chip import Chip, Chip_SO"
        ]
        python_code = "\n".join(imports)

        # Start the Python class definition
        python_code += f"\n\nclass {chip_name}(Chip):\n"
        python_code += "    def __init__(self):\n"

        # Define the components inside __init__
        for i, (part_name, _) in enumerate(self.parsed_parts):
            python_code += f"        self.{part_name.lower()}_{i+1} = {part_name}()\n"

        # Define internal variables (like carry1, carry2) in __init__
        for var in self.internal_vars:
            python_code += f"        self.{var} = None\n"

        for inp in self.inputs:
            python_code += f"        self.{inp['name']} = None\n"

        python_code += "        super().__init__()\n\n"


        # Define the call method
        python_code += "    def __call__(self, " + self.generate_inputs_signature() + "):\n"

        # Add the logic for each part
        for i, (part_name, connections) in enumerate(self.parsed_parts):
            args = self.generate_part_call_arguments(connections)
            python_code += f"        self.{part_name.lower()}_{i+1} = self.{part_name.lower()}_{i+1}({args})\n"

        return python_code

    def generate_part_call_arguments(self, connections):
        # Generate arguments for each part call
        args = []
        for conn_name, conn_value in connections.items():
            if '[' in conn_value:  # Array/slice handling
                array_range = self.extract_range(conn_value)
                args.append(f"{conn_name}=self.{conn_value.split('[')[0]}{array_range}")
            else:
                args.append(f"{conn_name}=self.{conn_value}")
        return ", ".join(args)

    def generate_inputs_signature(self):
        # Generate the input signature for the Python method (handles multiple inputs)
        return ", ".join([f"{inp['name']}: ValList" if inp['width'] != '1' else f"{inp['name']}: Val" for inp in self.inputs])

    def generate_part_call_arguments(self, connections):
        # Generate arguments for each part call
        args = []
        for conn_name, conn_value in connections.items():
            if '[' in conn_value:  # Array/slice handling
                array_range = self.extract_range(conn_value)
                args.append(f"{conn_name}=self.{conn_value.split('[')[0]}{array_range}")
            else:
                args.append(f"{conn_name}=self.{conn_value}")
        return ", ".join(args)

    def generate_output_logic(self, output_name):
        # Placeholder for output logic (if complex sum, etc., needed)
        return output_name

    def extract_range(self, value):
        # Extract the range a[0..3] -> a[0:4] for Python slicing
        match = re.search(r'\[(\d+)\.\.(\d+)\]', value)
        if match:
            start, end = match.groups()
            return f"[{start}:{int(end)}]"
        return ""

with open('../test/add16.chip', 'r') as f:
    hdl_code = f.read()

# Convert the HDL to Python
converter = HDLtoPythonConverter(hdl_code)
python_code = converter.generate_python_code()

# save generated code to python file
with open('../test/add16.generated.py', 'w') as f:
    f.write(python_code)