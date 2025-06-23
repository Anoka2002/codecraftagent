# CodeCraftAgent

**CodeCraftAgent** ابزاری پیشرفته برای تولید کدهای باکیفیت، بهینه، و قابل اجرا برای انواع ایجنت‌های نرم‌افزاری (مانند چت‌بات‌ها، اسکریپرهای وب، پردازشگرهای داده، اسکریپت‌های خودکارسازی، دستیارهای هوش مصنوعی، یا ایجنت‌های خودتکراری) است. این پروژه شامل یک بک‌اند مبتنی بر FastAPI و یک افزونه VS Code است که با API مدل‌های زبانی (مانند Grok یا OpenAI) ادغام می‌شود.

## ویژگی‌ها
- تولید کد برای هر نوع ایجنت با پشتیبانی از زبان‌های متعدد (پایتون، جاوااسکریپت، Go، جاوا، Rust و غیره).
- انتخاب خودکار زبان برنامه‌نویسی بر اساس پرامپت کاربر.
- فرمت‌دهی خودکار کد (پشتیبانی از Black برای پایتون، Prettier برای جاوااسکریپت/تایپ‌اسکریپت، gofmt برای Go، google-java-format برای جاوا).
- افزونه VS Code برای تعامل آسان با API.
- تست‌های واحد برای بک‌اند (با Pytest) و افزونه (با Mocha).
- مستندات جامع و تنظیمات آماده برای توسعه‌دهندگان.

## ساختار پروژه

```
CodeCraftAgent/
├── backend/
│   ├── agent.py          # منطق اصلی API
│   ├── formatters.py     # فرمت‌دهی کد
│   ├── requirements.txt  # وابستگی‌های پایتون
│   ├── tests/            # تست‌های بک‌اند
│   │   ├── __init__.py
│   │   ├── test_agent.py
│   │   └── test_formatters.py
│   └── .venv/            # محیط مجازی
├── src/
│   ├── extension.ts      # افزونه VS Code
│   └── test/
│       └── extension.test.ts  # تست‌های افزونه
├── resources/
│   └── icon.svg          # آیکون افزونه
├── README.md             # مستندات
├── package.json          # تنظیمات افزونه VS Code
├── tsconfig.json         # تنظیمات TypeScript
├── .gitignore            # فایل‌های نادیده‌گرفته‌شده
└── .vscode/
    └── settings.json     # تنظیمات VS Code
```

## پیش‌نیازها
- **Python 3.8+** (برای بک‌اند)
- **Node.js 16+** و **npm 8+** (برای افزونه VS Code)
- **VS Code 1.80.0+** (برای توسعه و استفاده از افزونه)
- دسترسی به API مدل زبانی با URL و کلید معتبر
- افزونه‌های VS Code:
  - Python (`ms-python.python`)
  - Prettier (`esbenp.prettier-vscode`)
  - Mocha Test Explorer (`hbenl.vscode-mocha-test-explorer`, اختیاری برای تست)
- ابزارهای اختیاری:
  - `vsce` برای انتشار افزونه (`npm install -g vsce`)
  - **فرمت‌کننده‌های کد**:
    - **Prettier**: `npm install -g prettier`
    - **gofmt**: نصب Go از [golang.org](https://golang.org/)
    - **google-java-format**: دانلود JAR از [GitHub](https://github.com/google/google-java-format) و نصب Java

## نصب و راه‌اندازی

### 1. راه‌اندازی بک‌اند
1. به دایرکتوری بک‌اند بروید:
   ```bash
   cd backend
   ```
2. محیط مجازی ایجاد کنید:
   ```bash
   python -m venv .venv
   ```
3. محیط مجازی را فعال کنید:
   - لینوکس/مک:
     ```bash
     source .venv/bin/activate
     ```
   - ویندوز:
     ```bash
     .venv\Scripts\activate
     ```
4. وابستگی‌ها را نصب کنید:
   ```bash
   pip install -r requirements.txt
   ```
5. فایل `.env` را در دایرکتوری `backend` ایجاد کنید و متغیرهای محیطی را تنظیم کنید:
   ```env
   MODEL_API_URL=<your-api-url>
   MODEL_API_KEY=<your-api-key>
   ```
6. سرور را اجرا کنید:
   ```bash
   python agent.py
   ```

### 2. راه‌اندازی افزونه VS Code
1. به دایرکتوری افزونه بروید:
   ```bash
   cd src
   ```
2. وابستگی‌ها را نصب کنید:
   ```bash
   npm install
   ```
3. کد را فرمت کنید (اختیاری):
   ```bash
   npm run format
   ```
4. کد TypeScript را کامپایل کنید:
   ```bash
   npm run compile
   ```
5. افزونه را در VS Code تست کنید:
   - VS Code را باز کنید.
   - دایرکتوری پروژه را با `File > Open Folder` باز کنید.
   - کلید `F5` را فشار دهید تا افزونه در حالت دیباگ اجرا شود.
6. برای اجرای تست‌های افزونه:
   ```bash
   npm run test
   ```

### 3. تنظیمات VS Code
- فایل `.vscode/settings.json` به طور خودکار Python (با Black و Flake8)، TypeScript/JavaScript (با Prettier)، و تست‌ها (با Mocha) را تنظیم می‌کند.
- افزونه‌های Python و Prettier را نصب کنید:
  ```bash
  code --install-extension ms-python.python
  code --install-extension esbenp.prettier-vscode
  ```

## استفاده

### استفاده از API بک‌اند
- **Endpoint**: `POST /generate_code`
- **پارامترها**:
  - `prompt` (رشته، الزامی): توضیحات ایجنت.
  - `language` (رشته، اختیاری): زبان برنامه‌نویسی (مثل `python`, `javascript`; اگر مشخص نشود، خودکار انتخاب می‌شود).
  - `max_tokens` (عدد، اختیاری): حداکثر توکن‌ها (پیش‌فرض: 1000).
  - `format` (بولین، اختیاری): فرمت‌دهی کد (پیش‌فرض: true).

#### نمونه درخواست:
```bash
curl -X POST http://localhost:8000/generate_code \
  -H "Content-Type: application/json" \
  -d '{"prompt": "یک چت‌بات پایتون بساز", "language": "python", "format": true}'
```

#### نمونه پاسخ:
```json
{
  "generated_code": "def chatbot(message):\n    if message.lower() == 'hello':\n        return 'Hi!'\n    return 'Unknown command.'\n",
  "language": "python"
}
```

### استفاده از افزونه VS Code
1. افزونه را در VS Code فعال کنید.
2. دستور `CodeCraftAgent: Generate Code` را اجرا کنید:
   - کلیدهای `Ctrl+Shift+P` را فشار دهید.
   - عبارت `Generate Code` را تایپ کنید و Enter بزنید.
3. پرامپت، زبان (یا `auto` برای انتخاب خودکار)، و گزینه فرمت‌دهی را وارد کنید.
4. کد تولیدشده در فایل جدیدی باز می‌شود.

## توسعه‌دهندگان

### افزودن فرمت‌کننده جدید
1. در `backend/formatters.py`، تابع فرمت‌دهی برای زبان جدید اضافه کنید.
2. ابزار CLI مربوطه را نصب کنید (مثلاً `npm install -g prettier` برای جاوااسکریپت).
3. تست کنید که فرمت‌دهی از طریق API و افزونه کار می‌کند.

### تست بک‌اند
1. تست‌های واحد را در `backend/tests/` با Pytest اجرا کنید:
   ```bash
   pytest
   ```

### توسعه افزونه
- برای افزودن قابلیت‌های جدید، `src/extension.ts` را ویرایش کنید.
- تست‌های جدید را در `src/test/extension.test.ts` اضافه کنید.
- کد را با Prettier فرمت کنید:
   ```bash
   npm run format
   ```

### انتشار افزونه
1. افزونه را با `vsce` بسته‌بندی کنید:
   ```bash
   vsce package
   ```
2. فایل `.vsix` را در VS Code Marketplace آپلود کنید یا به صورت دستی نصب کنید:
   ```bash
   code --install-extension codecraftagent-0.1.0.vsix
   ```
3. **توجه**: قبل از انتشار، `publisher` در `package.json` را با حساب واقعی جایگزین کنید.

## عیب‌یابی

- **سرور بک‌اند اجرا نمی‌شود**:
  - بررسی کنید که پورت 8000 آزاد باشد.
  - اطمینان حاصل کنید که `.env` درست تنظیم شده است.
- **افزونه کار نمی‌کند**:
  - مطمئن شوید بک‌اند روی `http://localhost:8000` اجرا می‌شود.
  - وابستگی‌های npm را دوباره نصب کنید: `cd src && npm install`.
- **خطای فرمت‌دهی**:
  - بررسی کنید که ابزارهای فرمت‌دهی (Black، Prettier و غیره) نصب شده‌اند.
- **تست‌ها اجرا نمی‌شوند**:
  - مطمئن شوید Mocha و ts-node نصب شده‌اند.
  - برای بک‌اند، Pytest را بررسی کنید.

## لایسنس
MIT License

---
**آخرین به‌روزرسانی**: ژوئن 2025  
**تماس**: برای سؤالات، یک issue در مخزن GitHub ایجاد کنید.
```

---

#### آیا تغییراتی برای اجرا نیاز است؟

بله، برای اجرای کامل پروژه **CodeCraftAgent**، باید تغییراتی اعمال شود یا ابزارهای اضافی نصب شوند. این تغییرات مربوط به نصب ابزارهای فرمت‌دهی کد هستند که در فایل `requirements.txt` یا `package.json` به‌صورت پیش‌فرض گنجانده نشده‌اند. در زیر جزئیات این موارد آورده شده است:

1. **نصب ابزارهای فرمت‌دهی کد**:
   - **Prettier**: برای فرمت‌دهی کدهای جاوااسکریپت و تایپ‌اسکریپت.
     ```bash
     npm install -g prettier
     ```
   - **gofmt**: برای فرمت‌دهی کدهای Go. این ابزار با نصب Go در دسترس قرار می‌گیرد:
     - Go را از [golang.org](https://golang.org/) نصب کنید.
   - **google-java-format**: برای فرمت‌دهی کدهای جاوا.
     - فایل JAR را از [GitHub](https://github.com/google/google-java-format) دانلود کنید.
     - Java (JDK) را نصب کنید تا این ابزار اجرا شود.

2. **چرا این تغییرات لازم است؟**:
   - این ابزارها به‌صورت جداگانه نصب می‌شوند، زیرا بخشی از وابستگی‌های استاندارد پایتون (در `requirements.txt`) یا Node.js (در `package.json`) نیستند.
   - بدون نصب این فرمت‌کننده‌ها، قابلیت فرمت‌دهی خودکار کد برای زبان‌های جاوااسکریپت، Go، و جاوا کار نخواهد کرد، هرچند بک‌اند و افزونه همچنان برای زبان‌هایی مثل پایتون (با Black که در `requirements.txt` است) قابل اجرا هستند.

3. **اقدام پیشنهادی**:
   - اگر قصد استفاده از همه زبان‌های پشتیبانی‌شده را دارید، ابزارهای فوق را نصب کنید.
   - اگر فقط از پایتون استفاده می‌کنید، نصب Black (که در `requirements.txt` گنجانده شده) کافی است و نیازی به نصب ابزارهای اضافی نیست.

با انجام این تغییرات و نصب ابزارهای مورد نیاز، پروژه به‌طور کامل و بدون مشکل اجرا خواهد شد.
