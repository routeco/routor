import importlib
import logging
import pkgutil
from types import ModuleType
from typing import Dict

logger = logging.getLogger()


def discover_and_load_plugins() -> Dict[str, ModuleType]:
    """
    Discover and load routor plugins.
    """
    logger.debug("Loading plugins")

    plugins: Dict[str, ModuleType] = {}
    for _, name, _ in pkgutil.iter_modules():
        if not name.startswith('routor_'):
            continue

        module = importlib.import_module(name)
        plugins[name] = module
        logger.info("Loaded %s", name)

    return plugins


discovered_plugins = discover_and_load_plugins()
