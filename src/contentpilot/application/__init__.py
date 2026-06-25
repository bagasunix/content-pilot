"""Application layer — use cases and the ports they depend on.

Depends only on the domain layer. Knows nothing about the filesystem, YAML,
subprocess, or the CLI — those live behind the ports defined here and are
supplied by the infrastructure layer at wiring time.
"""
