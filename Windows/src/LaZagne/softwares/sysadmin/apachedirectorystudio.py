import os
from config.write_output import print_output, print_debug
from config.constant import *
from config.header import Header
from config.moduleInfo import ModuleInfo
import xml.etree.ElementTree as ET

class ApacheDirectoryStudio(ModuleInfo):

    def __init__(self):
        options = {'command': '-t', 'action': 'store_true', 'dest': 'apachedirectorystudio', 'help': 'Apache Directory Studio'}
        ModuleInfo.__init__(self, 'apachedirectorystudio', 'sysadmin', options)
        # Interesting XML attributes in ADS connection configuration
        self.attr_to_extract = ["host", "port", "bindPrincipal", "bindPassword"]


    def extract_connections_credentials(self):
        """
        Extract all connection's credentials.

        :return: List of dict in which one dict contains all information for a connection.
        """
        repos_creds = []
        connection_file_location = os.environ.get("USERPROFILE") + "\\.ApacheDirectoryStudio\\.metadata\\.plugins\\org.apache.directory.studio.connection.core\\connections.xml"
        if os.path.isfile(connection_file_location):
            try:
                connections = ET.parse(connection_file_location).getroot()
                connection_nodes = connections.findall(".//connection")
                for connection_node in connection_nodes:
                    creds = {}
                    for connection_attr_name in connection_node.attrib:
                        if connection_attr_name in self.attr_to_extract:
                            creds[connection_attr_name] = connection_node.attrib[connection_attr_name].strip()
                    if len(creds) > 0:
                        repos_creds.append(creds)
            except Exception as e:
                print_debug("ERROR", "Cannot retrieve connections credentials '%s'" % e)
                pass

        return repos_creds


    def run(self):
        """
        Main function
        """
        # Print title
        title = "ApacheDirectoryStudio"
        Header().title_info(title)

        # Extract all available connections credentials
        repos_creds = self.extract_connections_credentials()

        # Parse and process the list of connections credentials
        pwd_found = []
        for creds in repos_creds:
            values = {}
            values["Host"] = creds["host"]
            values["Port"] = creds["port"]
            values["BindPrincipal"] = creds["bindPrincipal"]
            values["BindPassword"] = creds["bindPassword"]
            pwd_found.append(values)

        # Print the results
        print_output(title, pwd_found)
