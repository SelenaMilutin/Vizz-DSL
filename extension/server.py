from pygls.lsp.server import LanguageServer
from lsprotocol import types
from pygls.workspace import TextDocument
from textx import metamodel_from_file
from textx.exceptions import TextXSyntaxError
import os

server = LanguageServer("vizz-lsp", "0.1.0")
vizz_mm = metamodel_from_file(os.path.normpath(os.path.join(os.path.dirname(__file__), "vizz.tx")))

def validate(document: TextDocument):
    diagnostics = []
    lines = document.lines
    text = document.source

    try:
        vizz_mm.model_from_str(text)
    except TextXSyntaxError as e:
        line_idx = e.line - 1
        col_idx = e.col - 1

        line = lines[line_idx]

        end_idx = col_idx
        while end_idx < len(line) and not line[end_idx].isspace():
            end_idx += 1

        diagnostics.append(
            types.Diagnostic(
                range=types.Range(
                    start=types.Position(line=line_idx, character=col_idx),
                    end=types.Position(line=line_idx, character=end_idx),
                ),
                message=f"TextX syntax error: {e}",
                severity=types.DiagnosticSeverity.Error,
            )
        )

    return diagnostics

@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: LanguageServer, params: types.DidOpenTextDocumentParams):
    doc = ls.workspace.get_text_document(params.text_document.uri)
    diagnostics = validate(doc)

    ls.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(
            uri=doc.uri,
            version=doc.version,
            diagnostics=diagnostics,
        )
    )

@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: LanguageServer, params: types.DidChangeTextDocumentParams):
    doc = ls.workspace.get_text_document(params.text_document.uri)
    diagnostics = validate(doc)

    ls.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(
            uri=doc.uri,
            version=doc.version,
            diagnostics=diagnostics,
        )
    )

if __name__ == "__main__":
    server.start_io()
