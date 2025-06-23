
import * as assert from 'assert';
import * as sinon from 'sinon';
import * as vscode from 'vscode';
import { activate } from '../extension';
import axios from 'axios';

// تعریف سوئیت تست
suite('CodeCraftAgent Extension Test Suite', () => {
  let sandbox: sinon.SinonSandbox;

  // قبل از هر تست، سندباکس جدید ایجاد می‌شود
  setup(() => {
    sandbox = sinon.createSandbox();
  });

  // بعد از هر تست، سندباکس بازنشانی می‌شود
  teardown(() => {
    sandbox.restore();
  });

  test('افزونه باید فعال شود', async () => {
    const context: vscode.ExtensionContext = {
      subscriptions: [],
      workspaceState: {
        get: sandbox.stub(),
        update: sandbox.stub(),
      },
      globalState: {
        get: sandbox.stub(),
        update: sandbox.stub(),
      },
      extensionPath: '',
      asAbsolutePath: sandbox.stub(),
      storagePath: '',
      globalStoragePath: '',
      logPath: '',
    } as any;

    // فعال‌سازی افزونه
    await activate(context);

    // بررسی ثبت دستور
    assert.strictEqual(context.subscriptions.length, 1, 'دستور generateCode باید ثبت شود.');
  });

  test('دستور generateCode باید با پرامپت معتبر کد تولید کند', async () => {
    // جعل ورودی‌های کاربر
    const showInputBoxStub = sandbox.stub(vscode.window, 'showInputBox').resolves('یک چت‌بات پایتون بساز');
    const showQuickPickStub = sandbox.stub(vscode.window, 'showQuickPick');
    showQuickPickStub.onCall(0).resolves('python'); // انتخاب زبان
    showQuickPickStub.onCall(1).resolves('yes'); // فرمت‌دهی

    // جعل پاسخ API
    const axiosPostStub = sandbox.stub(axios, 'post').resolves({
      data: {
        generated_code: 'def chatbot(message):\n    return "Hello!"\n',
        language: 'python',
      },
    } as any);

    // جعل عملیات فایل
    const writeFileStub = sandbox.stub(vscode.workspace.fs, 'writeFile').resolves();
    const openTextDocumentStub = sandbox.stub(vscode.workspace, 'openTextDocument').resolves({} as any);
    const showTextDocumentStub = sandbox.stub(vscode.window, 'showTextDocument').resolves();
    const showInformationMessageStub = sandbox.stub(vscode.window, 'showInformationMessage');

    // اجرای دستور
    await vscode.commands.executeCommand('codecraftagent.generateCode');

    // بررسی فراخوانی‌ها
    assert.strictEqual(showInputBoxStub.calledOnce, true, 'باید پرامپت درخواست شود.');
    assert.strictEqual(showQuickPickStub.callCount, 2, 'باید زبان و فرمت‌دهی درخواست شوند.');
    assert.strictEqual(axiosPostStub.calledOnce, true, 'باید درخواست API ارسال شود.');
    assert.strictEqual(writeFileStub.calledOnce, true, 'باید فایل نوشته شود.');
    assert.strictEqual(openTextDocumentStub.calledOnce, true, 'باید فایل باز شود.');
    assert.strictEqual(showTextDocumentStub.calledOnce, true, 'باید فایل نمایش داده شود.');
    assert.strictEqual(showInformationMessageStub.calledOnce, true, 'باید پیام موفقیت نمایش داده شود.');
  });

  test('دستور generateCode باید در صورت پرامپت خالی خطا نمایش دهد', async () => {
    // جعل ورودی خالی
    const showInputBoxStub = sandbox.stub(vscode.window, 'showInputBox').resolves(undefined);
    const showErrorMessageStub = sandbox.stub(vscode.window, 'showErrorMessage');

    // اجرای دستور
    await vscode.commands.executeCommand('codecraftagent.generateCode');

    // بررسی خطا
    assert.strictEqual(showInputBoxStub.calledOnce, true, 'باید پرامپت درخواست شود.');
    assert.strictEqual(showErrorMessageStub.calledOnce, true, 'باید پیام خطا نمایش داده شود.');
    assert.strictEqual(
      showErrorMessageStub.calledWith('پرامپت وارد نشده است.'),
      true,
      'پیام خطا باید درست باشد.'
    );
  });

test('دستور generateCode باید خطای API را مدیریت کند', async () => {
    // جعل ورودی‌های کاربر
    const showInputBoxStub = sandbox.stub(vscode.window, 'showInputBox').resolves('یک چت‌بات پایتون بساز');
    const showQuickPickStub = sandbox.stub(vscode.window, 'showQuickPick');
    showQuickPickStub.onCall(0).resolves('python');
    showQuickPickStub.onCall(1).resolves('yes');

    // جعل خطای API
    const axiosPostStub = sandbox.stub(axios, 'post').rejects({
      response: { data: { detail: 'خطا در سرور' } },
    });

    // جعل پیام خطا
    const showErrorMessageStub = sandbox.stub(vscode.window, 'showErrorMessage');

    // اجرای دستور
    await vscode.commands.executeCommand('codecraftagent.generateCode');

    // بررسی مدیریت خطا
    assert.strictEqual(axiosPostStub.calledOnce, true, 'باید درخواست API ارسال شود.');
    assert.strictEqual(showErrorMessageStub.calledOnce, true, 'باید پیام خطا نمایش داده شود.');
    assert.strictEqual(
      showErrorMessageStub.calledWith('خطا در تولید کد: خطا در سرور'),
      true,
      'پیام خطا باید درست باشد.'
    );
  });
});
