# Copyright (c) 2020 RoccoDev
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import obspython as obs
import urllib3.request
import json

# Configuration
username = ""
format = ""
interval = 5
source_name = ""
str_format = ""

source_active = False

http = urllib3.PoolManager()

# Script meta


def script_description():
    return "Display your Pokemon Showdown ELO in a text source\n\nInfo and help: https://github.com/RoccoDev/showdown-elo-obs"


def script_load(settings):
    sh = obs.obs_get_signal_handler()
    obs.signal_handler_connect(sh, "source_activate", src_active)
    obs.signal_handler_connect(sh, "source_deactivate", src_inactive)


def script_update(settings):
    global username
    global format
    global interval
    global source_name
    global str_format

    username = obs.obs_data_get_string(settings, "username")
    format = obs.obs_data_get_string(settings, "format")
    interval = obs.obs_data_get_int(settings, "interval")
    source_name = obs.obs_data_get_string(settings, "source")
    str_format = obs.obs_data_get_string(settings, "str_format")

    obs.timer_remove(update_text)

    if username != "" and source_name != "":
        obs.timer_add(update_text, interval * 1000)


def script_defaults(settings):
    obs.obs_data_set_default_int(settings, "interval", 5)
    obs.obs_data_set_default_string(settings, "format", "gen8ou")
    obs.obs_data_set_default_string(settings, "username", "Zarel")
    obs.obs_data_set_default_string(settings, "str_format", "{user}: {elo}")


def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_text(
        props, "username", "Showdown Username", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_int(
        props, "interval", "Update interval (seconds)", 5, 3600, 1)

    p = obs.obs_properties_add_list(
        props, "source", "Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_id(source)
            if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)

        obs.source_list_release(sources)

    obs.obs_properties_add_text(
        props, "format", "Format (OU, UU etc.)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(
        props, "str_format", "Text format (see website for details)", obs.OBS_TEXT_DEFAULT)
    return props


def activate(cd, activating):
    global source_active

    src = obs.calldata_source(cd, "source")
    if src is not None:
        name = obs.obs_source_get_name(src)
        if name == source_name:
            source_active = activating


def src_active(cd):
    activate(cd, True)


def src_inactive(cd):
    activate(cd, False)


def update_text():
    global username
    global format
    global interval
    global source_name
    global str_format

    source = obs.obs_get_source_by_name(source_name)
    if source is not None and source_active:
        try:
            r = http.request("GET",
                             "http://play.pokemonshowdown.com/%7e%7eshowdown/action.php?act=ladderget&user=" + username,
                             headers={
                                 'User-Agent': 'ShowdownELOOBS/1.0'
                             })
            data = json.loads(r.data.decode('utf-8')[1:])
            obj = [o for o in data if o['formatid'] == format]

            # Statistics
            elo = 1000 if len(obj) == 0 else obj[0]['elo']
            gxe = "?" if len(obj) == 0 else str(obj[0]['gxe']) + '%'
            wins = 0 if len(obj) == 0 else obj[0]['w']
            losses = 0 if len(obj) == 0 else obj[0]['l']
            ties = 0 if len(obj) == 0 else obj[0]['t']
            games = wins + losses + ties
            user = username if len(obj) == 0 else obj[0]['username']

            text = str_format.format(
                user=user, elo=f'{float(elo):.2f}', gxe=gxe, w=wins, l=losses, t=ties, g=games, elo_int=int(float(elo)))

            settings = obs.obs_data_create()
            obs.obs_data_set_string(
                settings, "text", text.replace('\\n', '\n'))
            obs.obs_source_update(source, settings)
            obs.obs_data_release(settings)

        except urllib3.exceptions.HTTPError as err:
            obs.script_log(obs.LOG_WARNING,
                           "Error opening URL: " + err)
            obs.remove_current_callback()

        obs.obs_source_release(source)
