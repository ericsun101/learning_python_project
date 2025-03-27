current_section = None
current_config = {}

file_path = 'example'
try:
    with open(file_path,'r') as f:
        for line in f:
            line = line.strip()
            #if not line检查处理后的行是否为空。line.startswith('#')检查是否以 #开头。跳过当前循环，处理下一行。
            if not line or line.startswith('#'):
                continue
            if line.startswith('[') and line.endswith(']'):
                print(line)
                if current_section and current_section.startswith('monitor://') and "sourcetype" in current_config:
                    path = current_section[len('monitor://'):]
                    monitor_configs.append((path, current_config["sourcetype"]))
except FileNotFoundError:
    print(f"未找到文件:{file_path}")



# #!/usr/bin/env python3
# # 提供正则表达式操作，用于复杂的字符串搜索和替换。
# import re
# # 用于处理配置文件，可以读取、写入和修改类似INI格式的配置文件。
# import configparser
# # 用于文件路径模式匹配，可以查找符合特定模式的文件路径。
# import glob
# # 提供面向对象的文件系统路径操作，使文件和目录操作更简单直观。
# from pathlib import Path
# # 提供Python解释器相关的变量和函数，常用于获取命令行参数等系统相关操作。
# import sys
#
#
# def parse_inputs_conf(file_path):
#     """Parse splunk inputs.conf file, extract monitor configurations and sourcetypes"""
#     monitor_configs = []
#     # Custom parsing to handle duplicate sections
#     current_section = None
#     current_config = {}
#
#     try:
#         with open(file_path, 'r') as f:
#             #逐行读取
#             for line in f:
#                 #删除所有的前导和尾随空白字符（包括空格、制表符、换行符等）
#                 line = line.strip()
#
#                 # Skip empty lines and comments
#                 if not line or line.startswith('#'):
#                     continue
#
#                 # Check for section headers
#                 if line.startswith('[') and line.endswith(']'):
#                     # Save previous section if it was a monitor section
#                     if current_section and current_section.startswith('monitor://') and "sourcetype" in current_config:
#                         path = current_section[len('monitor://'):]
#                         monitor_configs.append((path, current_config["sourcetype"]))
#                     # Start new section
#                     current_section = line[1:-1]  # Remove [ and ]
#                     current_config = {}
#                     continue
#
#                 # Parse key=value pairs
#                 if '=' in line:
#                     key, value = line.split('=', 1)
#                     current_config[key.strip()] = value.strip()
#
#             # Don't forget to process the last section
#             if current_section and current_section.startswith('monitor://') and "sourcetype" in current_config:
#                 path = current_section[len('monitor://'):]
#                 sourcetype = current_config["sourcetype"]
#                 monitor_configs.append((path, sourcetype))
#     except Exception as e:
#         print(f"Error parsing {file_path}: {str(e)}")
#
#     return monitor_configs
#
#
# def generate_vrl_condition(path, sourcetype):
#     """Generate VRL condition statement for given path and sourcetype"""
#     # If path already starts with a slash
#     if path.startswith('/'):
#         formatted_path = path
#     else:
#         formatted_path = f'/{path}'
#
#     # Handle wildcards in path
#     if '*' in formatted_path:
#         # Convert path to regex pattern, ensuring no double slashes at the beginning
#         regex_path = formatted_path.replace('//', '/').replace('*', '.*').replace('.', '\.')
#         # Remove unnecessary escaping for '.' if it's not at the start of the regex path
#         if not regex_path.startswith('\.'):
#             regex_path = regex_path.replace('\.', '.', 1)
#         return f'''event.source =~ /^{regex_path}$/'''
#     else:
#         # For exact path, use only equality (no trailing slash check)
#         return f'''event.source == "{formatted_path}"'''
#
#
# def generate_vrl_script(monitor_configs):
#     vrl_script = ""
#     for i, (path, sourcetype) in enumerate(monitor_configs):
#         condition = generate_vrl_condition(path, sourcetype)
#         if i == 0:
#             vrl_script += f"if ({condition}) {{\n"
#         else:
#             vrl_script += f" else if ({condition}) {{\n"
#         vrl_script += f" event.datatype = \"{sourcetype}\"\n"
#     # Add default case
#     vrl_script += " } else {\n"
#     vrl_script += " event.datatype = \"unknown\"\n"
#     vrl_script += " }\n"
#     return vrl_script
#
#
# def main():
#     # Get input file path from command line argument or prompt if not provided
#     if len(sys.argv) > 1:
#         inputs_conf_path = sys.argv[1]
#     else:
#         inputs_conf_path = input("Enter the path to inputs.conf file: ")
#
#     # Parse inputs.conf
#     monitor_configs = parse_inputs_conf(inputs_conf_path)
#
#     if not monitor_configs:
#         print("No monitor configurations or sourcetype information found")
#         return
#
#     # Generate VRL script
#     vrl_script = generate_vrl_script(monitor_configs)
#
#     # Output VRL script to terminal
#     print("Generated VRL script:")
#     print("-" * 50)
#     print(vrl_script)
#
#
# if __name__ == "__main__":
#     main()