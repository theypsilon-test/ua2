# Copyright (c) 2022 José Manuel Barroso Galindo <theypsilon@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# You can download the latest version of this tool from:
# https://github.com/theypsilon-test/ua2
from update_all.ui_engine import run_ui_engine

_settings_screen_model = {
    "formatters": {
        "yesno": {
            "false": "no",
            "true": "yes",
        },
        "enabled": {
            "false": "Disabled.",
            "true": "Enabled. ",
        },
        "do_enable": {
            "false": "Enable",
            "true": "Disable",
        },
        "encc_forks": {
            "false": "MiSTer-devel",
            "true": "MiSTer-DB9",
        },
        "encc_forks_description": {
            "false": "Official Cores from MiSTer-devel",
            "true": "DB9 / SNAC8 forks with ENCC",
        },
        "download_beta_cores": {
            "false": "jtcores",
            "true": "jtpremium",
        },
        "bool_flag_presence_text": {
            "0": "Ignore them entirely",
            "1": "Place them only on its {0} folder",
            "2": "Place them everywhere",
        }
    },
    "variables": {
        "update_all_version": {"default": "2.0"},
        "main_updater": {"default": "true", "values": ["false", "true"]},
        "encc_forks": {"default": "false", "values": ["false", "true"]},
        "jotego_updater": {"default": "true", "values": ["false", "true"]},
        "download_beta_cores": {"default": "false", "values": ["false", "true"]},
        "unofficial_updater": {"default": "false", "values": ["false", "true"]},
        "llapi_updater": {"default": "false", "values": ["false", "true"]},
        "bios_getter": {"default": "false", "values": ["false", "true"]},
        "arcade_roms_db_downloader": {"default": "false", "values": ["false", "true"]},
        "names_txt_updater": {"default": "true", "values": ["false", "true"]},
        "arcade_organizer": {"default": "true", "values": ["false", "true"]},
    },
    "base_types": {
        "dialog_sub_menu": {
            "type": "menu",
            "hotkeys": [
                {
                    "keys": [27],
                    "action": [{
                        "type": "navigate",
                        "target": "back"
                    }]
                },
            ],
            "actions": [
                {
                    "title": "Select",
                    "type": "symbol",
                    "symbol": "ok"
                },
                {
                    "title": "Back",
                    "type": "fixed",
                    "fixed": [{
                        "type": "navigate",
                        "target": "back"
                    }]
                }
            ],
            "entries": [
                {
                    "title": "BACK",
                    "description": "",
                    "actions": {"ok": [{"type": "navigate", "target": "back"}]}
                },
            ]
        },
    },
    "items": {
        "main_menu": {
            "type": "menu",
            "header": "Update All {update_all_version} Settings",
            "hotkeys": [
                {
                    "keys": [27],
                    "action": [
                        {"type": "calculate_needs_save"},
                        {
                            "type": "condition",
                            "variable": "needs_save",
                            "true": [{
                                "type": "confirm",
                                "header": "INI file/s were not saved",
                                "text": ["Do you really want to abort Update All without saving your changes?"],
                                "actions": [
                                    {"title": "Yes", "type": "fixed", "fixed": [{"type": "navigate", "target": "abort"}]},
                                    {"title": "No", "type": "fixed", "fixed": [{"type": "navigate", "target": "back"}]}
                                ],
                            }],
                            "false": [{"type": "message", "text": ["Pressed ESC/Abort", "Closing Update All..."], "effects": [{"type": "navigate", "target": "abort"}]}]
                        }
                    ]
                },
            ],
            "actions": [
                {
                    "title": "Select",
                    "type": "symbol",
                    "symbol": "ok"
                },
                {
                    "title": "Toggle",
                    "type": "symbol",
                    "symbol": "toggle"
                },
                {
                    "title": "Abort",
                    "type": "fixed",
                    "fixed": [
                        {"type": "calculate_needs_save"},
                        {
                            "type": "condition",
                            "variable": "needs_save",
                            "true": [{
                                "type": "confirm",
                                "header": "INI file/s were not saved",
                                "text": ["Do you really want to abort Update All without saving your changes?"],
                                "actions": [
                                    {"title": "Yes", "type": "fixed", "fixed": [{"type": "navigate", "target": "abort"}]},
                                    {"title": "No", "type": "fixed", "fixed": [{"type": "navigate", "target": "back"}]}
                                ],
                            }],
                            "false": [{"type": "message", "text": ["Pressed ESC/Abort", "Closing Update All..."], "effects": [{"type": "navigate", "target": "abort"}]}]
                        }
                    ]
                }
            ],
            "entries": [
                {
                    "title": "1 Main Distribution",
                    "description": "{main_updater:enabled} Main MiSTer cores from {encc_forks}",
                    "actions": {
                        "ok": [{"type": "navigate", "target": "main_distribution_menu"}],
                        "toggle": [{"type": "rotate_variable", "target": "main_updater"}],
                    }
                },
                {
                    "title": "2 JTCORES for MiSTer",
                    "description": "{jotego_updater:enabled} Cores made by Jotego ({download_beta_cores})",
                    "actions": {
                        "ok": [{"type": "navigate", "target": "jtcores_menu"}],
                        "toggle": [{"type": "rotate_variable", "target": "jotego_updater"}],
                    }
                },
                {
                    "title": "3 theypsilon Unofficial",
                    "description": "{unofficial_updater:enabled} Some unofficial cores",
                    "actions": {
                        "ok": [{"type": "navigate", "target": "theypsilon_unofficial_menu"}],
                        "toggle": [{"type": "rotate_variable", "target": "unofficial_updater"}],
                    }
                },
                {
                    "title": "4 LLAPI Folder",
                    "description": "{llapi_updater:enabled} Forks adapted to LLAPI",
                    "actions": {
                        "ok": [{"type": "navigate", "target": "llapi_folder_menu"}],
                        "toggle": [{"type": "rotate_variable", "target": "llapi_updater"}],
                    }
                },
                {
                    "title": "5 BIOS Database",
                    "description": "{bios_getter:enabled} BIOS files for your systems",
                    "actions": {
                        "ok": [{"type": "navigate", "target": "bios_database_menu"}],
                        "toggle": [{"type": "rotate_variable", "target": "bios_getter"}],
                    }
                },
                {
                    "title": "6 Arcade ROMs Database",
                    "description": "{arcade_roms_db_downloader:enabled} ROMs for Arcades Cores",
                    "actions": {
                        "ok": [{"type": "navigate", "target": "arcade_roms_database_menu"}],
                        "toggle": [{"type": "rotate_variable", "target": "arcade_roms_db_downloader"}],
                    }
                },
                {
                    "title": "7 Names TXT",
                    "description": "{names_txt_updater:enabled} Better core names in the menus",
                    "actions": {
                        "ok": [{"type": "navigate", "target": "names_txt_menu"}],
                        "toggle": [{"type": "rotate_variable", "target": "names_txt_updater"}],
                    }
                },
                {
                    "title": "8 Arcade Organizer",
                    "description": "{arcade_organizer:enabled} Creates folder for easy navigation",
                    "actions": {
                        "ok": [{"type": "navigate", "target": "arcade_organizer_menu"}],
                        "toggle": [{"type": "rotate_variable", "target": "arcade_organizer"}],
                    }
                },
                {
                    "title": "9 Misc",
                    "description": "",
                    "actions": {
                        "ok": [{"type": "navigate", "target": "misc_menu"}],
                        "toggle": [],
                    }
                },
                {
                    "title": "0 Patrons Menu",
                    "description": "Last updated: 2022.06.24",
                    "actions": {
                        "ok": [
                            {"type": "calculate_patrons"},
                            {
                                "type": "condition",
                                "variable": "can_access_patron_menu",
                                "true": [{"type": "navigate", "target": "patrons_menu"}],
                                "false": [{
                                    "type": "message",
                                    "header": "Patreon Key not found!",
                                    "text": [
                                        "This menu contains exclusive content for patrons only.",
                                        "",
                                        "Get your 'Patreon Key' at \Zu\Z4patreon.com/theypsilon\Z7\Zn and put it on the \Zb/Scripts\Zn folder to unlock early access and experimental options.",
                                        "",
                                        "Thank you so much for your support!",
                                    ],
                                    "effects": [{
                                        "type": "message",
                                        "header": "Support MiSTer",
                                        "text": [
                                            "Consider supporting Alexey Melnikov 'Sorgelig' for his invaluable work as the main maintainer of the MiSTer Project: \Zu\Z4patreon.com/FPGAMiSTer\Z7\Zn",
                                            "",
                                            "Other key contributors:",
                                            "  ·Ace \Zu\Z4ko-fi.com/ace9921\Z7\Zn - Arcade cores",
                                            "  ·Artemio \Zu\Z4patreon.com/aurbina\Z7\Zn Pinobatch \Zu\Z4patreon.com/pineight\Z7\Zn - Testing tools",
                                            "  ·Atrac17 \Zu\Z4patreon.com/atrac17\Z7\Zn - MRAs & Modelines",
                                            "  ·Blackwine \Zu\Z4patreon.com/blackwine\Z7\Zn - Arcade cores",
                                            "  ·FPGAZumSpass \Zu\Z4patreon.com/FPGAZumSpass\Z7\Zn - Console & Computer cores",
                                            "  ·d0pefish \Zu\Z4ko-fi.com/d0pefish\Z7\Zn - mt32pi author",
                                            "  ·Jotego \Zu\Z4patreon.com/topapate\Z7\Zn - Arcade & Console cores",
                                            "  ·MiSTer-X \Zu\Z4patreon.com/MrX_8B\Z7\Zn - Arcade cores",
                                            "  ·Nullobject \Zu\Z4patreon.com/nullobject\Z7\Zn - Arcade cores",
                                            "  ·Srg320 \Zu\Z4patreon.com/srg320\Z7\Zn - Console cores",
                                            "  ·Theypsilon \Zu\Z4patreon.com/theypsilon\Z7\Zn - Downloader, Update All & Other Tools",
                                            "",
                                            "Your favorite open-source projects require your support to keep evolving!"
                                        ]
                                    }],
                                }]
                            }
                        ],
                        "toggle": [],
                    }
                },
                {
                    "title": "SAVE",
                    "description": "Writes all changes to the INI file/s",
                    "actions": {
                        "ok": [
                            {"type": "calculate_needs_save"},
                            {
                                "type": "condition",
                                "variable": "needs_save",
                                "true": [{
                                    "type": "confirm",
                                    "header": "Are you sure?",
                                    "text": [
                                        "Following files may be overwritten with your changes:",
                                        "  - downloader.ini",
                                        "  - update_all.ini",
                                        "  - update_arcade-organizer.ini",
                                    ],
                                    "preselected_action": "No",
                                    "actions": [
                                        {
                                            "title": "Yes",
                                            "type": "fixed",
                                            "fixed": [{"type": "save"}, {"type": "navigate", "target": "back"}]
                                        },
                                        {
                                            "title": "No",
                                            "type": "fixed",
                                            "fixed": [{"type": "navigate", "target": "back"}]
                                        }
                                    ],
                                }],
                                "false": [{"type": "message", "text": ["No changes to save"]}]
                            }
                        ],
                        "toggle": [],
                    }
                },
                {
                    "title": "EXIT and RUN UPDATE ALL",
                    "description": "",
                    "actions": {
                        "ok": [
                            {"type": "calculate_needs_save"},
                            {
                                "type": "condition",
                                "variable": "needs_save",
                                "true": [{
                                    "type": "confirm",
                                    "header": "INI file/s were not saved",
                                    "text": [
                                        "Do you really want to run Update All without saving your changes?",
                                        "(current changes will apply only for this run)",
                                    ],
                                    "actions": [
                                        {
                                            "title": "Yes",
                                            "type": "fixed",
                                            "fixed": [{"type": "navigate", "target": "exit_and_run"}]
                                        },
                                        {
                                            "title": "No",
                                            "type": "fixed",
                                            "fixed": [{"type": "navigate", "target": "back"}]
                                        }
                                    ],
                                }],
                                "false": [{"type": "navigate", "target": "exit_and_run"}]
                            },
                            {"type": "navigate", "target": "exit_and_run"}
                        ],
                        "toggle": [],
                    }
                }
            ]
        },
        "main_distribution_menu": {
            "type": "dialog_sub_menu",
            "header": "Main Distribution Settings",
            "entries": [
                {
                    "title": "1 {main_updater:do_enable}",
                    "description": "Activated: {main_updater}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "main_updater"}]}
                },
                {
                    "title": "2 Cores versions",
                    "description": "{encc_forks:encc_forks_description}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "encc_forks"}]}
                },
            ]
        },
        "jtcores_menu": {
            "type": "dialog_sub_menu",
            "header": "JTCORES Settings",
            "entries": [
                {
                    "title": "1 {jotego_updater:do_enable}",
                    "description": "Activated: {jotego_updater}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "jotego_updater"}]}
                },
                {
                    "title": "2 Install Premium Cores",
                    "description": "{download_beta_cores:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "download_beta_cores"}]}
                },
            ]
        },
        "theypsilon_unofficial_menu": {
            "type": "dialog_sub_menu",
            "header": "theypsilon Unofficial Distribution Settings",
            "entries": [
                {
                    "title": "1 {unofficial_updater:do_enable}",
                    "description": "Activated: {unofficial_updater}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "unofficial_updater"}]}
                },
            ]
        },
        "llapi_folder_menu": {
            "type": "dialog_sub_menu",
            "header": "LLAPI Folder Settings",
            "entries": [
                {
                    "title": "1 {llapi_updater:do_enable}",
                    "description": "Activated: {llapi_updater}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "llapi_updater"}]}
                },
            ]
        },
        "bios_database_menu": {
            "type": "dialog_sub_menu",
            "header": "BIOS Database Settings",
            "entries": [
                {
                    "title": "1 {bios_getter:do_enable}",
                    "description": "Activated: {bios_getter}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "bios_getter"}]}
                },
            ]
        },
        "arcade_roms_database_menu": {
            "type": "dialog_sub_menu",
            "header": "Arcade ROMs Database Settings",
            "entries": [
                {
                    "title": "1 {arcade_roms_db_downloader:do_enable}",
                    "description": "Activated: {arcade_roms_db_downloader}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_roms_db_downloader"}]}
                },
            ]
        },
        "names_txt_menu": {
            "type": "dialog_sub_menu",
            "header": "Names TXT Settings",
            "variables": {
                "names_region": {"default": "US", "values": ["US", "EU", "JP"]},
                "names_char_code": {"default": "CHAR18", "values": ["CHAR18", "CHAR28"]},
                "names_sort_code": {"default": "Common", "values": ["Common", "Manufacturer"]},
            },
            "entries": [
                {
                    "title": "1 {names_txt_updater:do_enable}",
                    "description": "Activated: {names_txt_updater}",
                    "actions": {"ok": [
                        {"type": "calculate_file_exists", "target": "names.txt"},
                        {
                            "type": "condition",
                            "variable": "file_exists",
                            "true": [{
                                "type": "message",
                                "text": ["WARNING! Your current names.txt file will be overwritten after updating"],
                                "alert_level": "black",
                                "effects": [{"type": "rotate_variable", "target": "names_txt_updater"}],
                            }],
                            "false": [{"type": "rotate_variable", "target": "names_txt_updater"}]
                        }
                    ]}
                },
                {
                    "title": "2 Region",
                    "description": "{names_region}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "names_region"}]}
                },
                {
                    "title": "3 Char Code",
                    "description": "{names_char_code}",
                    "actions": {"ok": [
                        {"type": "rotate_variable", "target": "names_char_code"},
                        {"type": "calculate_names_char_code_warning"},
                        {
                            "type": "condition",
                            "variable": "names_char_code_warning",
                            "true": [{
                                "type": "message",
                                "text": ["It's recommended to set rbf_hide_datecode=1 on MiSTer.ini when using CHAR28"],
                            }],
                            "false": []
                        }
                    ]}
                },
                {
                    "title": "4 Sort Code",
                    "description": "{names_sort_code}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "names_sort_code"}]}
                },
                {
                    "title": "5 Remove \"names.txt\"",
                    "description": "Back to standard core names based on RBF files",
                    "actions": {"ok": [
                        {"type": "calculate_file_exists", "target": "names.txt"},
                        {
                            "type": "condition",
                            "variable": "file_exists",
                            "true": [{
                                "type": "confirm",
                                "header": "Are you sure?",
                                "text": ["If you have done changes to names.txt, they will be lost"],
                                "preselected_action": "No",
                                "actions": [
                                    {"title": "Yes", "type": "fixed", "fixed": [
                                        {"type": "remove_file", "target": "names.txt"},
                                        {"type": "message", "text": ["names.txt Removed"]}
                                    ]},
                                    {"title": "No", "type": "fixed", "fixed": [
                                        {"type": "message", "text": ["Operaton Canceled"]}
                                    ]}
                                ],
                            }],
                            "false": [{"type": "message", "text": ["names.txt doesn't exist"]}]
                        }
                    ]}
                },
            ]
        },
        "misc_menu": {
            "type": "dialog_sub_menu",
            "header": "Misc | Other Settings",
            "variables": {
                "arcade_offset_downloader": {"default": "false", "values": ["false", "true"]},
                "tty2oled_files_downloader": {"default": "false", "values": ["false", "true"]},
                "i2c2oled_files_downloader": {"default": "false", "values": ["false", "true"]},
                "mistersam_files_downloader": {"default": "false", "values": ["false", "true"]},

                "autoreboot": {"default": "true", "values": ["false", "true"]},
                "wait_time_for_reading": {"default": "2", "values": ["2", "0", "30"]},
                "countdown_time": {"default": "15", "values": ["15", "4", "60"]},
            },
            "entries": [
                {
                    "title": "1 Arcade Offset folder",
                    "description": "{arcade_offset_downloader:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_offset_downloader"}]}
                },
                {
                    "title": "2 tty2oled files",
                    "description": "{tty2oled_files_downloader:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "tty2oled_files_downloader"}]}
                },
                {
                    "title": "3 i2c2oled files",
                    "description": "{i2c2oled_files_downloader:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "i2c2oled_files_downloader"}]}
                },
                {
                    "title": "4 MiSTer SAM files",
                    "description": "{mistersam_files_downloader:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "mistersam_files_downloader"}]}
                },
                {
                    "title": "5 Autoreboot (if needed)",
                    "description": "{autoreboot:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "autoreboot"}]}
                },
                {
                    "title": "6 Pause (between updaters)",
                    "description": "{wait_time_for_reading}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "wait_time_for_reading"}]}
                },
                {
                    "title": "7 Countdown Timer",
                    "description": "{countdown_time}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "countdown_time"}]}
                },
            ]
        },
        "patrons_menu": {
            "type": "menu",
            "header": "Patrons Menu",
            "hotkeys": [
                {
                    "keys": [27],
                    "action": [{
                        "type": "condition",
                        "variable": "spinner_needs_reboot",
                        "true": [{
                            "type": "message",
                            "header": "The Firmware has been changed",
                            "text": ["Please reboot NOW to execute it!"]
                        }],
                        "false": [{"type": "navigate", "target": "back"}]
                    }]
                },
            ],
            "actions": [
                {
                    "title": "Select",
                    "type": "symbol",
                    "symbol": "ok"
                },
                {
                    "title": "Back",
                    "type": "fixed",
                    "fixed": [{
                        "type": "condition",
                        "variable": "spinner_needs_reboot",
                        "true": [{
                            "type": "message",
                            "header": "The Firmware has been changed",
                            "text": ["Please reboot NOW to execute it!"]
                        }],
                        "false": [{"type": "navigate", "target": "back"}]
                    }]
                }
            ],
            "variables": {
                "test_unstable_spinner_option": {"default": "Test Unstable Spinner Firmware", "values": ["Test Unstable Spinner Firmware", "Revert Unstable Spinner Firmware"]},
                "test_unstable_spinner_desc": {"default": "For the Taito EGRET II Mini", "values": ["For the Taito EGRET II Mini", "Restore the original MiSTer binary"]},
            },
            "entries": [
                {
                    "title": "1 Play Bad Apple Database",
                    "description": "",
                    "actions": {"ok": [{"type": "play_bad_apple"}]}
                },
                {
                    "title": "2 {test_unstable_spinner_option}",
                    "description": "{test_unstable_spinner_desc}",
                    "actions": {"ok": [
                        {"type": "test_unstable_spinner"}
                    ]}
                },
                {
                    "title": "BACK",
                    "description": "",
                    "actions": {"ok": [
                        {
                            "type": "condition",
                            "variable": "spinner_needs_reboot",
                            "true": [{
                                "type": "message",
                                "header": "The Firmware has been changed",
                                "text": ["Please reboot NOW to execute it!"]
                            }],
                            "false": [{"type": "navigate", "target": "back"}]
                        },
                    ]}
                },
            ]
        },
        "arcade_organizer_menu": {
            "type": "dialog_sub_menu",
            "header": "Arcade Organizer 2.0 Settings",
            "variables": {
                "arcade_organizer_orgdir": {"real_name": "orgdir", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_mad_db_description": {"real_name": "mad_db_description", "file": "Scripts/update_arcade-organizer.ini", "default": "https://raw.githubusercontent.com/misteraddons/MiSTer_Arcade_MAD/db/mad_db.json.zip", "values": ["https://raw.githubusercontent.com/misteraddons/MiSTer_Arcade_MAD/db/mad_db.json.zip", "https://raw.githubusercontent.com/theypsilon/MAD_Database_MiSTer/db/mad_db.json.zip"]},
                "arcade_organizer_topdir": {"real_name": "topdir", "file": "Scripts/update_arcade-organizer.ini", "default": "", "values": ["", "platform", "core", "year"]},
                "arcade_organizer_skipalts": {"real_name": "skipalts", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_prepend_year": {"real_name": "prepend_year", "file": "Scripts/update_arcade-organizer.ini]", "default": "false", "values": ["false", "true"]},
                "arcade_organizer_verbose": {"real_name": "verbose", "file": "Scripts/update_arcade-organizer.ini", "default": "false", "values": ["false", "true"]},
            },
            "entries": [
                {
                    "title": "1 {arcade_organizer:do_enable}",
                    "description": "Activated: {arcade_organizer}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer"}]}
                },
                {
                    "title": "2 Organized Folders",
                    "description": "{arcade_organizer_orgdir}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_orgdir"}]}
                },
                {
                    "title": "3 Selected Database",
                    "description": "{arcade_organizer_mad_db_description}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_mad_db_description"}]}
                },
                {
                    "title": "4 Top additional folders",
                    "description": "{arcade_organizer_topdir}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_topdir"}]}
                },
                {
                    "title": "5 Skip MRA-Alternatives",
                    "description": "{arcade_organizer_skipalts:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_skipalts"}]}
                },
                {
                    "title": "6 Chronological sort below",
                    "description": "{arcade_organizer_prepend_year:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_prepend_year"}]}
                },
                {
                    "title": "7 Verbose script output",
                    "description": "{arcade_organizer_verbose:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_verbose"}]}
                },
                {
                    "title": "8 Alphabetic",
                    "description": "Options for 0-9 and A-Z folders",
                    "actions": {"ok": [{"type": "navigate", "target": "arcade_organizer_alphabetic_menu"}]}
                },
                {
                    "title": "9 Region",
                    "description": "Options for Regions (World, Japan, USA...)",
                    "actions": {"ok": [{"type": "navigate", "target": "arcade_organizer_region_menu"}]}
                },
                {
                    "title": "0 Collections",
                    "description": "Options for Platform, Core, Category, Year...",
                    "actions": {"ok": [{"type": "navigate", "target": "arcade_organizer_collections_menu"}]}
                },
                {
                    "title": "A Video & Input",
                    "description": "Options for Rotation, Resolution, Inputs...",
                    "actions": {"ok": [{"type": "navigate", "target": "arcade_organizer_video_input_menu"}]}
                },
                {
                    "title": "S Extra Software",
                    "description": "Options for Homebrew, Bootleg, Hacks...",
                    "actions": {"ok": [{"type": "navigate", "target": "arcade_organizer_extra_software_menu"}]}
                },
                {
                    "title": "D Advanced Submenu",
                    "description": "Advanced Options",
                    "actions": {"ok": [{"type": "navigate", "target": "arcade_organizer_advanced_menu"}]}
                },
            ]
        },
        "arcade_organizer_alphabetic_menu": {
            "type": "dialog_sub_menu",
            "header": "Arcade Organizer 2.0 Alphabetic Options",
            "variables": {
                "arcade_organizer_az_dir": {"real_name": "az_dir", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
            },
            "entries": [
                {
                    "title": "1 Alphabetic folders",
                    "description": "Activated: {arcade_organizer_az_dir:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_az_dir"}]}
                },
            ]
        },
        "arcade_organizer_region_menu": {
            "type": "dialog_sub_menu",
            "header": "Arcade Organizer 2.0 Region Options",
            "variables": {
                "arcade_organizer_region_dir": {"real_name": "region_dir", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_region_main_description": {"real_name": "region_main_description", "file": "Scripts/update_arcade-organizer.ini", "default": "DEV PREFERRED", "values": ["DEV PREFERRED", "Japan", "World", "USA", "Asia", "Europe", "Hispanic", "Spain", "Argentina", "Italy", "Brazil", "France", "Germany"]},
                "arcade_organizer_region_others": {"real_name": "region_others", "file": "Scripts/update_arcade-organizer.ini", "default": "1", "values": ["1", "0", "2"]},
            },
            "entries": [
                {
                    "title": "1 Region folders",
                    "description": "{arcade_organizer_region_dir:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_region_dir"}]}
                },
                {
                    "title": "2 Main region",
                    "description": "{arcade_organizer_region_main_description}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_region_main_description"}]}
                },
                {
                    "title": "3 MRAs with other regions",
                    "description": "{arcade_organizer_region_others:bool_flag_presence_text=Region}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_region_others"}]}
                },
            ]
        },
        "arcade_organizer_collections_menu": {
            "type": "dialog_sub_menu",
            "header": "Arcade Organizer 2.0 Collections Options",
            "variables": {
                "arcade_organizer_platform_dir": {"real_name": "platform_dir", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_core_dir": {"real_name": "core_dir", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_category_dir": {"real_name": "category_dir", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_manufacturer_dir": {"real_name": "manufacturer_dir", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_series_dir": {"real_name": "series_dir", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_best_of_dir": {"real_name": "best_of_dir", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
            },
            "entries": [
                {
                    "title": "1 Platform folders",
                    "description": "{arcade_organizer_platform_dir:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_platform_dir"}]}
                },
                {
                    "title": "2 MiSTer Core folders",
                    "description": "{arcade_organizer_core_dir:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_core_dir"}]}
                },
                {
                    "title": "3 Year options",
                    "description": "",
                    "actions": {"ok": [{"type": "navigate", "target": "arcade_organizer_year_options_menu"}]}
                },
                {
                    "title": "4 Category folders",
                    "description": "{arcade_organizer_category_dir:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_category_dir"}]}
                },
                {
                    "title": "5 Manufacturer folders",
                    "description": "{arcade_organizer_manufacturer_dir:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_manufacturer_dir"}]}
                },
                {
                    "title": "6 Series folders",
                    "description": "{arcade_organizer_series_dir:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_series_dir"}]}
                },
                {
                    "title": "7 Best-of folders",
                    "description": "{arcade_organizer_best_of_dir:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_best_of_dir"}]}
                },
            ]
        },
        "arcade_organizer_year_options_menu": {
            "type": "dialog_sub_menu",
            "header": "Arcade Organizer 2.0 Year Options",
            "variables": {
                "arcade_organizer_year_dir": {"real_name": "year_dir", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_decades_dir": {"real_name": "decades_dir", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
            },
            "entries": [
                {
                    "title": "1 Year folders",
                    "description": "{arcade_organizer_year_dir:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_year_dir"}]}
                },
                {
                    "title": "2 Decade folders",
                    "description": "{arcade_organizer_decades_dir:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_decades_dir"}]}
                },
            ]
        },
        "arcade_organizer_video_input_menu": {
            "type": "dialog_sub_menu",
            "header": "Arcade Organizer 2.0 Video & Inputs Options",
            "variables": {
                "arcade_organizer_move_inputs": {"real_name": "move_inputs", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_num_buttons": {"real_name": "num_buttons", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_special_controls": {"real_name": "special_controls", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_num_controllers": {"real_name": "num_controllers", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_cocktail_dir": {"real_name": "cocktail_dir", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_num_monitors": {"real_name": "num_monitors", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
            },
            "entries": [
                {
                    "title": "1 Resolution options",
                    "description": "",
                    "actions": {"ok": [{"type": "navigate", "target": "arcade_organizer_resolution_menu"}]}
                },
                {
                    "title": "2 Rotation options",
                    "description": "",
                    "actions": {"ok": [{"type": "navigate", "target": "arcade_organizer_rotation_menu"}]}
                },
                {
                    "title": "3 Move Inputs folders",
                    "description": "{arcade_organizer_move_inputs:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_move_inputs"}]}
                },
                {
                    "title": "4 Num Buttons folders",
                    "description": "{arcade_organizer_num_buttons:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_num_buttons"}]}
                },
                {
                    "title": "5 Special Inputs folders",
                    "description": "{arcade_organizer_special_controls:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_special_controls"}]}
                },
                {
                    "title": "6 Num Controllers folders",
                    "description": "{arcade_organizer_num_controllers:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_num_controllers"}]}
                },
                {
                    "title": "7 Cockail folders",
                    "description": "{arcade_organizer_cocktail_dir:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_cocktail_dir"}]}
                },
                {
                    "title": "8 Num Monitors folders",
                    "description": "{arcade_organizer_num_monitors:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_num_monitors"}]}
                },
            ]
        },
        "arcade_organizer_resolution_menu": {
            "type": "dialog_sub_menu",
            "header": "Arcade Organizer 2.0 Resolution Options",
            "variables": {
                "arcade_organizer_resolution_dir": {"real_name": "resolution_dir", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_resolution_15khz": {"real_name": "resolution_15khz", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_resolution_24khz": {"real_name": "resolution_24khz", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_resolution_31khz": {"real_name": "resolution_31khz", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
            },
            "entries": [
                {
                    "title": "1 Resolution folders",
                    "description": "{arcade_organizer_resolution_dir:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_resolution_dir"}]}
                },
                {
                    "title": "2 15 kHz Scan Rate",
                    "description": "{arcade_organizer_resolution_15khz:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_resolution_15khz"}]}
                },
                {
                    "title": "3 24 kHz Scan Rate",
                    "description": "{arcade_organizer_resolution_24khz:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_resolution_24khz"}]}
                },
                {
                    "title": "4 31 kHz Scan Rate",
                    "description": "{arcade_organizer_resolution_31khz:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_resolution_31khz"}]}
                },
            ]
        },
        "arcade_organizer_rotation_menu": {
            "type": "dialog_sub_menu",
            "header": "Arcade Organizer 2.0 Rotation Options",
            "variables": {
                "arcade_organizer_rotation_dir": {"real_name": "rotation_dir", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_rotation_0": {"real_name": "rotation_0", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_rotation_90": {"real_name": "rotation_90", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_rotation_270": {"real_name": "rotation_270", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_rotation_180": {"real_name": "rotation_180", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
                "arcade_organizer_flip": {"real_name": "flip", "file": "Scripts/update_arcade-organizer.ini", "default": "true", "values": ["false", "true"]},
            },
            "entries": [
                {
                    "title": "1 Rotation folders",
                    "description": "{arcade_organizer_rotation_dir:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_rotation_dir"}]}
                },
                {
                    "title": "2 Horizontal",
                    "description": "{arcade_organizer_rotation_0:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_rotation_0"}]}
                },
                {
                    "title": "3 Vertical Clockwise",
                    "description": "{arcade_organizer_rotation_90:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_rotation_90"}]}
                },
                {
                    "title": "4 Vertical Counter-Clockwise",
                    "description": "{arcade_organizer_rotation_270:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_rotation_270"}]}
                },
                {
                    "title": "5 Horizontal (reversed)",
                    "description": "{arcade_organizer_rotation_180:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_rotation_180"}]}
                },
                {
                    "title": "6 Cores with Flip in opposite Rotations",
                    "description": "{arcade_organizer_flip:yesno}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_flip"}]}
                },
            ]
        },
        "arcade_organizer_extra_software_menu": {
            "type": "dialog_sub_menu",
            "header": "Arcade Organizer 2.0 Extra Software Options",
            "variables": {
                "arcade_organizer_homebrew": {"real_name": "homebrew", "file": "Scripts/update_arcade-organizer.ini", "default": "1", "values": ["1", "0", "2"]},
                "arcade_organizer_bootleg": {"real_name": "bootleg", "file": "Scripts/update_arcade-organizer.ini", "default": "1", "values": ["1", "0", "2"]},
                "arcade_organizer_enhancements": {"real_name": "enhancements", "file": "Scripts/update_arcade-organizer.ini", "default": "1", "values": ["1", "0", "2"]},
                "arcade_organizer_translations": {"real_name": "translations", "file": "Scripts/update_arcade-organizer.ini", "default": "1", "values": ["1", "0", "2"]},
            },
            "entries": [
                {
                    "title": "1 Homebrew",
                    "description": "{arcade_organizer_homebrew:bool_flag_presence_text=Homebrew}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_homebrew"}]}
                },
                {
                    "title": "2 Bootleg",
                    "description": "{arcade_organizer_bootleg:bool_flag_presence_text=Bootleg}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_bootleg"}]}
                },
                {
                    "title": "3 Enhancements",
                    "description": "{arcade_organizer_enhancements:bool_flag_presence_text=Enhancements}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_enhancements"}]}
                },
                {
                    "title": "4 Translations",
                    "description": "{arcade_organizer_translations:bool_flag_presence_text=Translations}",
                    "actions": {"ok": [{"type": "rotate_variable", "target": "arcade_organizer_translations"}]}
                },
            ]
        },
        "arcade_organizer_advanced_menu": {
            "type": "dialog_sub_menu",
            "header": "Arcade Organizer 2.0 Advanced Options",
            "entries": [
                {
                    "title": "1 Clean Folders",
                    "description": "Deletes the Arcade Organizer folders",
                    "actions": {"ok": [
                        {"type": "calculate_arcade_organizer_folders"},
                        {
                            "type": "condition",
                            "variable": "has_arcade_organizer_folders",
                            "true": [
                                {
                                    "type": "confirm",
                                    "header": "ARE YOU SURE?",
                                    "text": [
                                        "WARNING! You will lose ALL the data contained in the folders:",
                                        "{arcade_organizer_folders_list}"
                                    ],
                                    "alert_level": "black",
                                    "preselected_action": "No",
                                    "actions": [
                                        {"title": "Yes", "type": "fixed", "fixed": [
                                            {"type": "clean_arcade_organizer_folders"},
                                            {"type": "message", "text": ["Organized folder Cleared"]}
                                        ]},
                                        {"title": "No", "type": "fixed", "fixed": [{"type": "message", "text": ["Operaton Canceled"]}]}
                                    ],
                                }
                            ],
                            "false": [{"type": "message", "text": ["Operaton Canceled"]}]
                        },
                    ]}
                },
            ]
        },
    }
}


class _SettingsScreenEffects:
    def __init__(self, ui):
        self._ui = ui
        self._test_toggle = False

    def resolve_custom_effect(self, effect):
        if effect['type'] == 'calculate_needs_save':
            self._test_toggle = not self._test_toggle
            self._ui.set_value('needs_save', 'true' if self._test_toggle else 'false')
        elif effect['type'] == 'calculate_patrons':
            self._test_toggle = not self._test_toggle
            self._ui.set_value('can_access_patron_menu', 'true' if self._test_toggle else 'false')
            self._ui.set_value('test_unstable_spinner_option', "Test Unstable Spinner Firmware" if self._test_toggle else "Revert Unstable Spinner Firmware")
            self._ui.set_value('test_unstable_spinner_desc', "For the Taito EGRET II Mini" if self._test_toggle else "Restore the original MiSTer binary")
            self._ui.set_value('spinner_needs_reboot', 'false')
        elif effect['type'] == 'test_unstable_spinner':
            self._ui.set_value('test_unstable_spinner_option', "Test Unstable Spinner Firmware" if self._ui.get_value('test_unstable_spinner_option') == "Revert Unstable Spinner Firmware" else "Revert Unstable Spinner Firmware")
            self._ui.set_value('test_unstable_spinner_desc', "For the Taito EGRET II Mini" if self._ui.get_value('test_unstable_spinner_desc') == "Restore the original MiSTer binary" else "Restore the original MiSTer binary")
            self._ui.set_value('spinner_needs_reboot', 'true')
            self._ui.refresh_screen()
        elif effect['type'] == 'play_bad_apple':
            raise NotImplementedError('Bad Apple is not implemented!')
        elif effect['type'] == 'save':
            raise NotImplementedError('Save is not implemented!')
        elif effect['type'] == 'calculate_file_exists':
            raise NotImplementedError(f'File exists "{effect["target"]}" is not implemented!')
        elif effect['type'] == 'remove_file':
            raise NotImplementedError(f'Remove File "{effect["target"]}" is not implemented!')
        elif effect['type'] == 'calculate_arcade_organizer_folders':
            self._ui.set_value('has_arcade_organizer_folders', 'true')
            self._ui.set_value('arcade_organizer_folders_list', '')
        elif effect['type'] == 'clean_arcade_organizer_folders':
            raise NotImplementedError('Clean Arcade Organizer Folders is not implemented!')
        elif effect['type'] == 'calculate_names_char_code_warning':
            raise NotImplementedError('Calculate Names Char Code Warning is not implemented!')
        else:
            raise NotImplementedError(f'Wrong effect type :"{effect["type"]}"')


class SettingsScreen:
    def load_main_menu(self):
        run_ui_engine('main_menu', _settings_screen_model, _SettingsScreenEffects)
