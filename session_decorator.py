import contextlib

@contextlib.contextmanager
def transactional_session(session_cls, nested=False, **kwargs):
    """Context manager which provides transaction management for the nested
       block. A transaction is started when the block is entered, and then either
       committed if the block exits without incident, or rolled back if an error
       is raised.
       
       Nested (SAVEPOINT) transactions are enabled by default, unless nested=False is
       passed, meaning that this context manager can be nested within another and the
       transactions treated as independent units-of-work from the perspective of the nested
       blocks. If the error is handled further up the chain, the outer transactions will
       still be committed, while the inner ones will be rolled-back independently."""
    session = session_cls(**kwargs)
    try:
        yield session
    except:
        # Roll back if the nested block raised an error
        session.rollback()
        raise
    else:
        # Commit if it didn't (so flow ran off the end of the try block)
        session.commit()
    session.close()
