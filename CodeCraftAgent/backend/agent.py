# backend/agent.py

import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import aiohttp
from dotenv import load_dotenv
from formatters import format_code

# تنظیم لاگینگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# بارگذاری متغیرهای محیطی
load_dotenv()

# تنظیمات API مدل زبانی
API_URL = os.getenv("MODEL_API_URL")
API_KEY = os.getenv("MODEL_API_KEY")

if not API_URL or not API_KEY:
    raise ValueError("MODEL_API_URL و MODEL_API_KEY باید در متغیرهای محیطی تنظیم شوند.")

# تعریف مدل داده برای درخواست کاربر
class CodeRequest(BaseModel):
    prompt: str
    language: str | None = None
    max_tokens: int = 1000
    format: bool = True

# تعریف مدل داده برای پاسخ
class CodeResponse(BaseModel):
    generated_code: str
    language: str

# ایجاد اپلیکیشن FastAPI
app = FastAPI(title="CodeCraftAgent Backend")

# منطق انتخاب خودکار زبان برنامه‌نویسی
def select_language(prompt: str) -> str:
    """
    انتخاب خودکار زبان برنامه‌نویسی بر اساس پرامپت.
    این یک پیاده‌سازی ساده است؛ می‌توان با تحلیل پیشرفته‌تر جایگزین کرد.
    
    Args:
        prompt (str): توضیحات کاربر
        
    Returns:
        str: زبان انتخاب‌شده
    """
    prompt_lower = prompt.lower()
    if any(keyword in prompt_lower for keyword in ["web", "frontend", "browser"]):
        return "javascript"
    elif any(keyword in prompt_lower for keyword in ["performance", "system"]):
        return "rust"
    elif any(keyword in prompt_lower for keyword in ["concurrent", "network"]):
        return "go"
    else:
        return "python"  # پیش‌فرض برای داده‌محوری یا اسکریپت‌نویسی

@app.post("/generate_code", response_model=CodeResponse)
async def generate_code(request: CodeRequest):
    """
    تولید کد بر اساس درخواست کاربر.
    
    Args:
        request (CodeRequest): شامل پرامپت، زبان، حداکثر توکن‌ها و وضعیت فرمت
    
    Returns:
        CodeResponse: کد تولیدشده و زبان
    """
    try:
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="پرامپت نمی‌تواند خالی باشد.")

        # انتخاب زبان اگر مشخص نشده باشد
        language = request.language or select_language(request.prompt)
        logger.info(f"پردازش پرامپت: {request.prompt}، زبان: {language}")

        # آماده‌سازی درخواست برای API مدل زبانی
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": f"Write a {language} code for: {request.prompt}",
            "max_tokens": request.max_tokens
        }

        # ارسال درخواست به API مدل زبانی
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, json=payload, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                generated_code = data.get("choices", [{}])[0].get("text", "").strip()
                if not generated_code:
                    raise HTTPException(status_code=500, detail="پاسخ API خالی است.")

        # مدیریت درخواست‌های خودارجاعی
        if "like yourself" in request.prompt.lower() or "code generator" in request.prompt.lower():
            generated_code = (
                f"# Simplified {language} code for a code-generating agent\n"
                f"{generated_code}\n"
                "# Note: This is a secure, simplified version to avoid recursion risks."
            )

        # فرمت‌دهی کد اگر درخواست شده و پشتیبانی شود
        if request.format:
            try:
                generated_code = format_code(generated_code, language)
            except Exception as e:
                logger.warning(f"خطا در فرمت‌دهی کد: {e}")

        logger.info(f"کد با موفقیت تولید شد برای زبان: {language}")
        return CodeResponse(generated_code=generated_code, language=language)

    except aiohttp.ClientError as e:
        logger.error(f"خطا در ارتباط با API مدل زبانی: {e}")
        raise HTTPException(status_code=500, detail=f"خطا در ارتباط با API: {str(e)}")
    except Exception as e:
        logger.error(f"خطای عمومی: {e}")
        raise HTTPException(status_code=500, detail=f"خطای عمومی: {str(e)}")

# اجرای سرور برای تست محلی
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
