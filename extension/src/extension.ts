import * as path from "path";
import * as fs from 'fs';
import * as cp from 'child_process';
import * as vscode from "vscode";
import {
  LanguageClient,
  LanguageClientOptions,
  ServerOptions
} from "vscode-languageclient/node";

let client: LanguageClient;

export async function activate(context: vscode.ExtensionContext) {
  const serverPath = path.join(context.extensionPath, "server.py");
  const pythonExe = await ensureVenv(context);

  const serverOptions: ServerOptions = {
    command: pythonExe,
    args: [serverPath]
  };

  const clientOptions: LanguageClientOptions = {
    documentSelector: [{ scheme: "file", language: "vizz" }]
  };

  client = new LanguageClient(
    "vizzLanguageServer",
    "Vizz Language Server",
    serverOptions,
    clientOptions
  );

  client.start();
}

export function deactivate(): Thenable<void> | undefined {
  if (!client) {
    return undefined;
  }
  return client.stop();
}

function exec(cmd: string, cwd?: string): Promise<void> {
  return new Promise((resolve, reject) => {
    cp.exec(cmd, { cwd }, (err) => {
      if (err) reject(err);
      else resolve();
    });
  });
}

async function ensureVenv(context: vscode.ExtensionContext) {
  const venvDir = path.join(context.extensionPath, 'venv');

  if (!fs.existsSync(venvDir)) {
    vscode.window.showInformationMessage('Creating Python venv for Vizz...');
    await exec(`python -m venv venv`, context.extensionPath);
  }

  const pythonExe = process.platform === 'win32'
    ? path.join(venvDir, 'Scripts', 'python.exe')
    : path.join(venvDir, 'bin', 'python');

  vscode.window.showInformationMessage('Installing Python dependencies...');
  await exec(
    `"${pythonExe}" -m pip install --upgrade pip textX pygls`,
    venvDir
  );

  return pythonExe;
}
