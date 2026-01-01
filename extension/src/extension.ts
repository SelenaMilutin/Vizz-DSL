import * as path from "path";
import * as vscode from "vscode";
import {
  LanguageClient,
  LanguageClientOptions,
  ServerOptions
} from "vscode-languageclient/node";

let client: LanguageClient;

export function activate(context: vscode.ExtensionContext) {
  const serverPath = path.join(context.extensionPath, "server.py");
  const pythonExePath = path.join(context.extensionPath, "..", "venv", "Scripts", "python.exe");

  const serverOptions: ServerOptions = {
    command: pythonExePath,
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
