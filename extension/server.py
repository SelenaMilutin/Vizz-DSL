from pygls.lsp.server import LanguageServer
from lsprotocol import types
from pygls.workspace import TextDocument

server = LanguageServer("vizz-lsp", "0.1.0")


def validate_text_document(document: TextDocument):
    diagnostics = []

    for idx, line in enumerate(document.lines):
        if "plot" not in line:
            diagnostics.append(
                types.Diagnostic(
                    message="Vizz program mora da sadrži 'plot'",
                    severity=types.DiagnosticSeverity.Error,
                    range=types.Range(
                        start=types.Position(line=idx, character=0),
                        end=types.Position(line=idx, character=len(line) - 1),
                    )
                )
            )

    return diagnostics


@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: LanguageServer, params: types.DidOpenTextDocumentParams):
    print("desilo se (open)", flush=True)
    
    doc = ls.workspace.get_text_document(params.text_document.uri)
    diagnostics = validate_text_document(doc)

    ls.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(
            uri=doc.uri,
            version=doc.version,
            diagnostics=diagnostics,
        )
    )


@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls: LanguageServer, params: types.DidChangeTextDocumentParams):
    print("desilo se (change)", flush=True)
    
    doc = ls.workspace.get_text_document(params.text_document.uri)
    diagnostics = validate_text_document(doc)

    ls.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(
            uri=doc.uri,
            version=doc.version,
            diagnostics=diagnostics,
        )
    )


if __name__ == "__main__":
    server.start_io()
