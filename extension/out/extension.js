"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
const cp = __importStar(require("child_process"));
const vscode = __importStar(require("vscode"));
const node_1 = require("vscode-languageclient/node");
let client;
async function activate(context) {
    const serverPath = path.join(context.extensionPath, "server.py");
    const pythonExe = await ensureVenv(context);
    const serverOptions = {
        command: pythonExe,
        args: [serverPath]
    };
    const clientOptions = {
        documentSelector: [{ scheme: "file", language: "vizz" }]
    };
    client = new node_1.LanguageClient("vizzLanguageServer", "Vizz Language Server", serverOptions, clientOptions);
    client.start();
}
exports.activate = activate;
function deactivate() {
    if (!client) {
        return undefined;
    }
    return client.stop();
}
exports.deactivate = deactivate;
function exec(cmd, cwd) {
    return new Promise((resolve, reject) => {
        cp.exec(cmd, { cwd }, (err) => {
            if (err)
                reject(err);
            else
                resolve();
        });
    });
}
async function ensureVenv(context) {
    const venvDir = path.join(context.extensionPath, 'venv');
    if (!fs.existsSync(venvDir)) {
        vscode.window.showInformationMessage('Creating Python venv for Vizz...');
        await exec(`python -m venv venv`, context.extensionPath);
    }
    const pythonExe = process.platform === 'win32'
        ? path.join(venvDir, 'Scripts', 'python.exe')
        : path.join(venvDir, 'bin', 'python');
    vscode.window.showInformationMessage('Installing Python dependencies...');
    await exec(`"${pythonExe}" -m pip install --upgrade pip textX pygls`, venvDir);
    return pythonExe;
}
