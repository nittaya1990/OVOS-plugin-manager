from ovos_plugin_manager.utils import load_plugin, find_plugins, PluginTypes
from ovos_utils.configuration import read_mycroft_config
from ovos_utils.log import LOG
from ovos_plugin_manager.templates.keywords import KeywordExtractor


def find_keyword_extract_plugins():
    return find_plugins(PluginTypes.KEYWORD_EXTRACTION)


def load_keyword_extract_plugin(module_name):
    """Wrapper function for loading keyword_extract plugin.

    Arguments:
        module_name (str): keyword_extract module name from config
    Returns:
        class: KeywordExtractor plugin class
    """
    return load_plugin(module_name, PluginTypes.KEYWORD_EXTRACTION)


class OVOSKeywordExtractorFactory:
    """ reads mycroft.conf and returns the globally configured plugin """
    MAPPINGS = {
        # default split at sentence boundaries
        # usually helpful in other plugins and included in base class
        "dummy": "ovos-keyword-plugin-dummy"
    }

    @staticmethod
    def get_class(config=None):
        """Factory method to get a KeywordExtractor engine class based on configuration.

        The configuration file ``mycroft.conf`` contains a ``keyword_extract`` section with
        the name of a KeywordExtractor module to be read by this method.

        "keyword_extract": {
            "module": <engine_name>
        }
        """
        config = config or get_keyword_extract_config()
        keyword_extract_module = config.get("module", "ovos-keyword-plugin-dummy")
        if keyword_extract_module in OVOSKeywordExtractorFactory.MAPPINGS:
            keyword_extract_module = OVOSKeywordExtractorFactory.MAPPINGS[keyword_extract_module]
        return load_keyword_extract_plugin(keyword_extract_module)

    @staticmethod
    def create(config=None):
        """Factory method to create a KeywordExtractor engine based on configuration.

        The configuration file ``mycroft.conf`` contains a ``keyword_extract`` section with
        the name of a KeywordExtractor module to be read by this method.

        "keyword_extract": {
            "module": <engine_name>
        }
        """
        config = config or get_keyword_extract_config()
        plugin = config.get("module") or "ovos-keyword-plugin-dummy"
        plugin_config = config.get(plugin) or {}
        try:
            clazz = OVOSKeywordExtractorFactory.get_class(config)
            return clazz(plugin_config)
        except Exception:
            LOG.error(f'Keyword extraction plugin {plugin} could not be loaded!')
            return KeywordExtractor()


def get_keyword_extract_config(config=None):
    config = config or read_mycroft_config()
    lang = config.get("lang")
    if "intentBox" in config and "keyword_extract" not in config:
        config = config["intentBox"] or {}
        lang = config.get("lang") or lang
    if "keyword_extract" in config:
        config = config["keyword_extract"]
        lang = config.get("lang") or lang
    config["lang"] = lang or "en-us"
    keyword_extract_module = config.get('module') or 'ovos-keyword-plugin-dummy'
    keyword_extract_config = config.get(keyword_extract_module, {})
    keyword_extract_config["module"] = keyword_extract_module
    return keyword_extract_config

