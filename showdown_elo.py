# Copyright (c) 2020 RoccoDev
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import obspython as obs
import urllib.request
import urllib.error
import json

# Configuration
username = ""
format = ""
interval = 5
source_name = ""
str_format = ""

# Script meta


def script_description():
    return "Display your Pokemon Showdown ELO in a text source\n\nInfo and help: https://github.com/RoccoDev/showdown-elo-obs"


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
            if source_id == "text_gdiplus" or source_id == "text_gdiplus_v2" or source_id == "text_ft2_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)

        obs.source_list_release(sources)

    obs.obs_properties_add_text(
        props, "format", "Format (OU, UU etc.)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(
        props, "str_format", "Text format (see website for details)", obs.OBS_TEXT_DEFAULT)
    return props


def update_text():
    global username
    global format
    global interval
    global source_name
    global str_format

    source = obs.obs_get_source_by_name(source_name)
    if source is not None and obs.obs_source_active(source):
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent', 'ShowdownELOOBS/1.0')]
            r = opener.open(
                "http://play.pokemonshowdown.com/%7e%7eshowdown/action.php?act=ladderget&user=" + urllib.parse.quote(username))
            data = json.loads(r.read().decode('utf-8')[1:])
            obj = [o for o in data if o['formatid'] == format]

            # Statistics
            elo = 1000 if len(obj) == 0 else obj[0]['elo']
            gxe = "?" if len(obj) == 0 else str(obj[0]['gxe']) + '%'
            wins = 0 if len(obj) == 0 else int(obj[0]['w'])
            losses = 0 if len(obj) == 0 else int(obj[0]['l'])
            ties = 0 if len(obj) == 0 else int(obj[0]['t'])
            games = wins + losses + ties
            user = username if len(obj) == 0 else obj[0]['username']

            text = str_format.format(
                user=user, elo=f'{float(elo):.2f}', gxe=gxe, w=wins, l=losses, t=ties, g=games, elo_int=int(float(elo)))

            settings = obs.obs_data_create()
            obs.obs_data_set_string(
                settings, "text", text.replace('\\n', '\n'))
            obs.obs_source_update(source, settings)
            obs.obs_data_release(settings)

        except urllib.error.URLError as err:
            obs.script_log(obs.LOG_WARNING,
                           "Error opening URL: " + err.reason)
            obs.remove_current_callback()

        obs.obs_source_release(source)
