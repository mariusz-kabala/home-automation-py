from miio.vaccum import Vacuum
import os

vacuum = Vacuum(ip=os.environ['VACUUM_HOST'], token=os.environ['VACUUM_TOKEN'])
# todo
