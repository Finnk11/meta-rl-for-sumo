import os
import tempfile


class Configuration:
    def __init__(self, net_file='', route_file='', duration=3600):

        content = f"""
            <configuration>
                <input>
                    <net-file value="{net_file}"/>"
                    <route-files value="{route_file}"/>
                </input>
                <time>
                    <begin value="0"/>
                    <end value="{duration}"/>
                </time>
            </configuration>
            """

        content = content.split('\n')[1:]
        bracket_index = content[0].index('<')
        content = [line[bracket_index:] for line in content]
        content = os.linesep.join(content)

        if os.name == 'nt':
            self._sumo_config = tempfile.NamedTemporaryFile(suffix='.sumocfg', delete=False)
        else:
            self._sumo_config = tempfile.NamedTemporaryFile(suffix='.sumocfg')

        self._sumo_config.write(content)
        self._sumo_config.close()

    def __del__(self):
        if os.name == 'nt':
            os.unlink(self._sumo_config.name)
