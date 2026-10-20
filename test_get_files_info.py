from functions.get_files_info import get_files_info

def print_test(working_directory: str, directory: str = "."):
    print(f"Result for '{directory}' directory:")
    print(get_files_info(working_directory, directory))

print_test("calculator", ".")

print_test("calculator", "pkg")

print_test("calculator", "/bin")

print_test("calculator", "../")
