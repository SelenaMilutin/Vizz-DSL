import * as path from "path";
import * as vscode from "vscode";
import {
  LanguageClient,
  LanguageClientOptions,
  ServerOptions
} from "vscode-languageclient/node";

let client: LanguageClient;

export function activate(context: vscode.ExtensionContext) {
  const serverPath = path.join(
    context.extensionPath,
    "server.py"
  );

  const serverOptions: ServerOptions = {
    command: "D:\\Faks\\Master\\Jezici specificni za domen\\Projekat\\Vizz-DSL\\venv\\Scripts\\python.exe",
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
