from abc import abstractmethod


from galaxy.util import bunch
from galaxy.util.dictifiable import Dictifiable
from galaxy.util.odict import odict
from .parser import ensure_tool_conf_item


panel_item_types = bunch.Bunch(
    TOOL="TOOL",
    WORKFLOW="WORKFLOW",
    SECTION="SECTION",
    LABEL="LABEL",
)


class HasPanelItems:
    """
    """

    @abstractmethod
    def panel_items(self):
        """ Return an ordered dictionary-like object describing tool panel
        items (such as workflows, tools, labels, and sections).
        """

    def panel_items_iter(self):
        """ Iterate through panel items each represented as a tuple of
        (panel_key, panel_type, panel_content).
        """
        for panel_key, panel_value in self.panel_items().items():
            if panel_value is None:
                continue
            panel_type = panel_item_types.SECTION
            if panel_key.startswith("tool_"):
                panel_type = panel_item_types.TOOL
            elif panel_key.startswith("label_"):
                panel_type = panel_item_types.LABEL
            elif panel_key.startswith("workflow_"):
                panel_type = panel_item_types.WORKFLOW
            yield (panel_key, panel_type, panel_value)


class ToolSection(Dictifiable, HasPanelItems):
    """
    A group of tools with similar type/purpose that will be displayed as a
    group in the user interface.
    """

    dict_collection_visible_keys = ['id', 'name', 'version']

    def __init__(self, item=None):
        """ Build a ToolSection from an ElementTree element or a dictionary.
        """
        if item is None:
            item = dict()
        self.name = item.get('name') or ''
        self.id = item.get('id') or ''
        self.version = item.get('version') or ''
        self.elems = ToolPanelElements()

    def copy(self):
        copy = ToolSection()
        copy.name = self.name
        copy.id = self.id
        copy.version = self.version
        copy.elems = self.elems.copy()
        return copy

    def to_dict(self, trans, link_details=False, tool_help=False, toolbox=None):
        """ Return a dict that includes section's attributes. """

        section_dict = super().to_dict()
        section_elts = []
        kwargs = dict(
            trans=trans,
            link_details=link_details,
            tool_help=tool_help
        )
        for elt in self.elems.values():
            if hasattr(elt, "tool_type") and toolbox:
                section_elts.append(toolbox.get_tool_to_dict(trans, elt, tool_help=tool_help))
            else:
                section_elts.append(elt.to_dict(**kwargs))
        section_dict['elems'] = section_elts

        return section_dict

    def panel_items(self):
        return self.elems


class ToolSectionLabel(Dictifiable):
    """
    A label for a set of tools that can be displayed above groups of tools
    and sections in the user interface
    """
    dict_collection_visible_keys = ['id', 'text', 'version']

    def __init__(self, item):
        """ Build a ToolSectionLabel from an ElementTree element or a
        dictionary.
        """
        item = ensure_tool_conf_item(item)
        self.text = item.get("text")
        self.id = item.get("id")
        self.version = item.get("version") or ''

    def to_dict(self, **kwds):
        return super().to_dict()


class ToolPanelElements(odict, HasPanelItems):
    """ Represents an ordered dictionary of tool entries - abstraction
    used both by tool panel itself (normal and integrated) and its sections.
    """

    def update_or_append(self, index, key, value):
        if key in self or index is None:
            self[key] = value
        else:
            self.insert(index, key, value)

    def get_label(self, label):
        for element in self.values():
            if isinstance(element, ToolSection) and element.name == label:
                return element

    def has_tool_with_id(self, tool_id):
        key = f'tool_{tool_id}'
        return key in self

    def replace_tool(self, previous_tool_id, new_tool_id, tool):
        previous_key = f'tool_{previous_tool_id}'
        new_key = f'tool_{new_tool_id}'
        index = self.keys().index(previous_key)
        del self[previous_key]
        self.insert(index, new_key, tool)

    def index_of_tool_id(self, tool_id):
        query_key = f'tool_{tool_id}'
        for index, target_key in enumerate(self.keys()):
            if query_key == target_key:
                return index
        return None

    def insert_tool(self, index, tool):
        key = f"tool_{tool.id}"
        self.insert(index, key, tool)

    def get_tool_with_id(self, tool_id):
        key = f"tool_{tool_id}"
        return self[key]

    def append_tool(self, tool):
        key = f"tool_{tool.id}"
        self[key] = tool

    def stub_tool(self, key):
        key = f"tool_{key}"
        self[key] = None

    def stub_workflow(self, key):
        key = f'workflow_{key}'
        self[key] = None

    def stub_label(self, key):
        key = f'label_{key}'
        self[key] = None

    def append_section(self, key, section_elems):
        self[key] = section_elems

    def panel_items(self):
        return self
