from .data import (DataReader)
from .data import (SnapDataReader)
from .data import (StockListing)
from .data import (EtfListing)
from .chart import (plot)

import importlib.metadata

try:
    __version__ = importlib.metadata.version("finance-datareader")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

__all__ = [
    '__version__', 
    'DataReader', 
    'SnapDataReader', 
    'StockListing', 
    'EtfListing', 
    'chart'
]
