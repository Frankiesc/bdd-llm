from functions.get_file_content import get_file_content

def print_test(working_directory: str, file_path: str):
    result = get_file_content("calculator", "lorem.txt")
    print(f"{file_path} length: {len(result)}")
    print(f"{file_path} truncated: {'truncated' in result}")

print_test("calculator", "lorem.txt")
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))
