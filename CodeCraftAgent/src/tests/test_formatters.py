# backend/tests/test_formatters.py

from backend.formatters import format_code

def test_format_python_code():
    raw_code = "def hello():print('Hello')"
    formatted = format_code(raw_code, "python")
    assert formatted == "def hello():\n    print('Hello')\n"

def test_format_javascript_code():
    raw_code = "function hello(){console.log('Hello')}"
    formatted = format_code(raw_code, "javascript")
    assert formatted == "function hello() {\n  console.log('Hello');\n}\n"

def test_format_unsupported_language():
    raw_code = "fn main() { println!('Hello'); }"
    formatted = format_code(raw_code, "rust")
    assert formatted == raw_code  # فرمت‌کننده‌ای برای Rust وجود ندارد
