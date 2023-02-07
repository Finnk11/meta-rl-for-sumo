import os
import tempfile


class SumoConfiguration:
    def __init__(self, net_file_path: str, route_file_path: str, duration: int = 3600):

        content = f"""
            <configuration>
                <input>
                    <net-file value="{net_file_path}"/>
                    <route-files value="{route_file_path}"/>
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
        content = '\n'.join(content)

        if os.name == 'nt':
            self.sumo_config_file = tempfile.NamedTemporaryFile(suffix='.sumocfg', delete=False)
        else:
            self.sumo_config_file = tempfile.NamedTemporaryFile(suffix='.sumocfg')

        self.sumo_config_file.write(content.encode('utf-8'))
        self.sumo_config_file.close()

        print(self.sumo_config_file.name)

    def _abs_(self):
        self.sumo_config_file.close()
        if os.name == 'nt':
            os.unlink(self.sumo_config_file.name)
