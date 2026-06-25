"""Blog lifecycle automation for {{DOMAIN}}.

Clean architecture layers (dependency rule points inward):

    interface  ->  application  ->  domain
        \\             |
         \\            v
          ----->  (ports implemented by) infrastructure

- domain:         entities + pure business rules (no I/O, no framework)
- application:    use cases + ports (abstract interfaces it needs)
- infrastructure: concrete adapters that implement the ports (FS, YAML, subprocess)
- interface:      delivery (CLI + presenter)

Runtime state lives in <repo>/workspace (see blog.infrastructure.paths.Workspace).
"""

__version__ = "2.0.0"
