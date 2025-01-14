from ovos_plugin_manager.utils import find_plugins, PluginTypes
from ovos_utils.messagebus import get_mycroft_bus
from ovos_utils.log import LOG


def find_skill_plugins():
    return find_plugins(PluginTypes.SKILL)


def load_skill_plugins(*args, **kwargs):
    """Load installed skill plugins.

    Returns:
        List of skills
    """
    plugin_skills = []
    plugins = find_skill_plugins()
    for skill_id, plug in plugins.items():
        skill = plug(*args, **kwargs)
        plugin_skills.append(skill)
    return plugin_skills
