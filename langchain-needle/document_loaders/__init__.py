"""
**Document Loaders** are classes to load Documents.

**Document Loaders** are usually used to load a lot of Documents in a single run.

**Class hierarchy:**

.. code-block::

    BaseLoader --> <name>Loader  # Examples: TextLoader, UnstructuredFileLoader

**Main helpers:**

.. code-block::

    Document, <name>TextSplitter
"""

from langchain_community.document_loaders.needle import NeedleLoader

__all__ = [
    "NeedleLoader",
]