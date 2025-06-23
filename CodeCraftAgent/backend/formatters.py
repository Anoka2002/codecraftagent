# backend/formatters.py

import subprocess
import logging
from typing import Optional

# تنظیم لاگینگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def format_python_code(code: str) -> str:
    """
    فرمت کردن کد پایتون با استفاده از Black.

    Args:
        code (str): کد خام پایتون.

    Returns:
        str: کد فرمت‌شده یا کد اصلی در صورت بروز خطا.
    """
    try:
        # فرض می‌شود Black در محیط مجازی نصب شده است
        result = subprocess.run(
            ["black", "-"],
            input=code.encode(),
            capture_output=True,
            check=True,
        )
        formatted_code = result.stdout.decode().strip()
        logger.info("کد پایتون با موفقیت با Black فرمت شد.")
        return formatted_code
    except subprocess.CalledProcessError as e:
        logger.error(f"خطا در فرمت کردن کد پایتون با Black: {e}")
        return code
    except FileNotFoundError:
        logger.error("Black نصب نشده یا در PATH یافت نشد.")
        return code

def format_javascript_code(code: str) -> str:
    """
    فرمت کردن کد JavaScript/TypeScript با استفاده از Prettier.

    Args:
        code (str): کد خام JavaScript/TypeScript.

    Returns:
        str: کد فرمت‌شده یا کد اصلی در صورت بروز خطا.
    """
    try:
        # فرض می‌شود Prettier به‌صورت سراسری یا در پروژه نصب شده است
        result = subprocess.run(
            ["prettier", "--stdin-filepath", "file.js"],
            input=code.encode(),
            capture_output=True,
            check=True,
        )
        formatted_code = result.stdout.decode().strip()
        logger.info("کد JavaScript/TypeScript با موفقیت با Prettier فرمت شد.")
        return formatted_code
    except subprocess.CalledProcessError as e:
        logger.error(f"خطا در فرمت کردن کد JavaScript/TypeScript با Prettier: {e}")
        return code
    except FileNotFoundError:
        logger.error("Prettier نصب نشده یا در PATH یافت نشد.")
        return code

def format_go_code(code: str) -> str:
    """
    فرمت کردن کد Go با استفاده از gofmt.

    Args:
        code (str): کد خام Go.

    Returns:
        str: کد فرمت‌شده یا کد اصلی در صورت بروز خطا.
    """
    try:
        # فرض می‌شود gofmt در PATH موجود است
        result = subprocess.run(
            ["gofmt"],
            input=code.encode(),
            capture_output=True,
            check=True,
        )
        formatted_code = result.stdout.decode().strip()
        logger.info("کد Go با موفقیت با gofmt فرمت شد.")
        return formatted_code
    except subprocess.CalledProcessError as e:
        logger.error(f"خطا در فرمت کردن کد Go با gofmt: {e}")
        return code
    except FileNotFoundError:
        logger.error("gofmt نصب نشده یا در PATH یافت نشد.")
        return code

def format_java_code(code: str) -> str:
    """
    فرمت کردن کد Java با استفاده از google-java-format.
    """
    try:
        result = subprocess.run(
        ["java", "-jar", "backend/google-java-format-1.15.0-all-deps.jar", "-"],
        input=code.encode(),
        capture_output=True,
        check=True,
        )
        formatted_code = result.stdout.decode().strip()
        logger.info("کد Java با موفقیت با google-java-format فرمت شد.")
        return formatted_code
    except subprocess.CalledProcessError as e:
        logger.error(f"خطا در فرمت کردن کد Java با google-java-format: {e}")
        return code
    except FileNotFoundError:
        logger.error("فایل google-java-format.jar یافت نشد یا Java نصب نشده است.")
        return code


def format_code(code: str, language: str) -> str:
    """
    فرمت کردن کد بر اساس زبان برنامه‌نویسی.

    Args:
        code (str): کد خام.
        language (str): زبان برنامه‌نویسی (مثلاً 'python'، 'javascript'، 'go'، 'java').

    Returns:
        str: کد فرمت‌شده یا کد اصلی در صورت عدم وجود فرمت‌کننده.
    """
    language = language.lower()
    if language == "python":
        return format_python_code(code)
    elif language in ["javascript", "typescript"]:
        return format_javascript_code(code)
    elif language == "go":
        return format_go_code(code)
    elif language == "java":
        return format_java_code(code)
    else:
        logger.warning(f"فرمت‌کننده‌ای برای زبان {language} پیاده‌سازی نشده است.")
        return code
