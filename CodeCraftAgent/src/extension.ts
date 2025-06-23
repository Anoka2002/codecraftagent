// src/extension.ts

import * as vscode from 'vscode';
import axios from 'axios';

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('codecraftagent.generateCode', async () => {
        const prompt = await vscode.window.showInputBox({ prompt: 'پرامپت خود را وارد کنید' });
        if (!prompt) { return; }
        const language = await vscode.window.showInputBox({ prompt: 'زبان (مثال: python, auto)' });
        const format = await vscode.window.showQuickPick(['true', 'false'], { placeHolder: 'فرمت‌دهی؟' });

        try {
            const response = await axios.post('http://localhost:8000/generate_code', {
                prompt,
                language: language || 'auto',
                format: format === 'true'
            }, { timeout: 30000 });
            const editor = vscode.window.activeTextEditor;
            if (editor) {
                editor.edit(editBuilder => {
                    editBuilder.insert(editor.selection.active, response.data.generated_code);
                });
            } else {
                vscode.workspace.openTextDocument({ content: response.data.generated_code, language: response.data.language }).then(doc => {
                    vscode.window.showTextDocument(doc);
                });
            }
        } catch (error) {
            let errorMessage = 'خطا در تولید کد. سرور بک‌اند را بررسی کنید.';
            if (axios.isAxiosError(error)) {
                if (error.code === 'ECONNABORTED') {
                    errorMessage = 'خطای شبکه: لطفاً اتصال اینترنت یا VPN خود را بررسی کنید.';
                } else {
                    errorMessage = `خطای API: ${error.response?.data?.detail || error.message}`;
                }
            }
            vscode.window.showErrorMessage(errorMessage);
        }
    });
    context.subscriptions.push(disposable);
}

export function deactivate() {}
