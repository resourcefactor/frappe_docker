import os, frappe, compileall, re, json

from frappe.migrate import migrate
from frappe.utils import get_sites
from check_connection import get_config

def save_config(config):
    with open('common_site_config.json', 'w') as f:
        return json.dump(config, f, indent=1, sort_keys=True)

def set_maintenance_mode(enable=True):
    conf = get_config()

    if enable:
        conf.update({ "maintenance_mode": 1, "pause_scheduler": 1 })
        save_config(conf)

    if not enable:
        conf.update({ "maintenance_mode": 0, "pause_scheduler": 0 })
        save_config(conf)

def migrate_sites(maintenance_mode=False):
    installed_sites = ":".join(get_sites())
    sites = os.environ.get("SITES", installed_sites).split(":")
    if not maintenance_mode:
        maintenance_mode = True if os.environ.get("MAINTENANCE_MODE") else False

    if maintenance_mode:
        set_maintenance_mode(True)

    for site in sites:
        print('Migrating', site)
        frappe.init(site=site)
        frappe.connect()
        try:
            migrate()
        finally:
            frappe.destroy()

    if maintenance_mode:
        set_maintenance_mode(False)

def main():
    migrate_sites()
    exit(0)

if __name__ == "__main__":
    main()
