from galaxy.queue_worker import (
    reload_data_managers,
    reload_toolbox,
)
from galaxy.tools.toolbox.watcher import (
    get_tool_conf_watcher,
    get_tool_data_dir_watcher
)


class ConfigWatchers(object):
    """Contains ToolConfWatcher, ToolWatcher and ToolDataWatcher objects."""

    def __init__(self, app):
        self.app = app
        self.tool_config_watcher = get_tool_conf_watcher(reload_callback=lambda: reload_toolbox(self.app), tool_cache=self.app.tool_cache)
        self.data_manager_config_watcher = get_tool_conf_watcher(reload_callback=lambda: reload_data_managers(self.app), tool_cache=self.app.tool_cache)
        self.tool_data_watcher = get_tool_data_dir_watcher(self.app.tool_data_tables, config=self.app.config)
        self.start()

    def start(self):
        [self.tool_config_watcher.watch_file(config) for config in self.tool_config_paths]
        [self.data_manager_config_watcher.watch_file(config) for config in self.data_manager_configs]
        [self.tool_data_watcher.watch_directory(tool_data_path) for tool_data_path in self.tool_data_paths]

    @property
    def data_manager_configs(self):
        data_manager_configs = []
        data_manager_configs.append(self.app.config.data_manager_config_file)
        if self.app.config.shed_data_manager_config_file:
            data_manager_configs.append(self.app.config.shed_data_manager_config_file)
        return data_manager_configs

    @property
    def tool_data_paths(self):
        tool_data_paths = []
        tool_data_paths.append(self.app.config.tool_data_path)
        if self.app.config.shed_tool_data_path:
            tool_data_paths.append(self.app.config.shed_tool_data_path)
        return tool_data_paths

    @property
    def tool_config_paths(self):
        tool_config_paths = self.app.config.tool_configs
        if self.app.config.migrated_tools_config not in tool_config_paths:
            tool_config_paths.append( self.app.config.migrated_tools_config )
        return tool_config_paths
