import os
from typing import Dict, Set
from openpilot.selfdrive.manager.process import ManagerProcess, PythonProcess
from openpilot.selfdrive.configs.base import COMMON_SERVICES, DMONITORING_SERVICES, UI_SERVICES, BaseConfig, Processes
from openpilot.selfdrive.manager.process_config import MAPSD, MICD, SOUNDD, always_run


class PCConfig(BaseConfig):
  def get_services(self) -> Set[ManagerProcess]:
    services = COMMON_SERVICES | UI_SERVICES | DMONITORING_SERVICES
    if "MAPBOX_TOKEN" not in os.environ:
      services -= {MAPSD}

    services -= {MICD, SOUNDD}
    return services


METADRIVE_BRIDGE = PythonProcess("bridge", "tools.sim.run_bridge", always_run)

METADRIVE_SERVICES: Processes = {METADRIVE_BRIDGE}

class MetaDriveConfig(PCConfig):
  def __init__(self):
    super().__init__()

  def get_services(self) -> Set[ManagerProcess]:
    return (super().get_services() | METADRIVE_SERVICES) - DMONITORING_SERVICES

  def get_env(self) -> Dict[str, str]:
    return {
      "PASSIVE": "0",
      "NOBOARD": "1",
      "SIMULATION": "1",
      "SKIP_FW_QUERY": "1",
      "FINGERPRINT": "HONDA CIVIC 2016"
    }
