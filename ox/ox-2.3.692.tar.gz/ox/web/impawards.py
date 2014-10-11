# vi:si:et:sw=4:sts=4:ts=4
# encoding: utf-8
from __future__ import print_function
import re

from ox.cache import read_url
from ox.html import strip_tags
from ox.text import find_re


def get_data(id):
    '''
    >>> get_data('1991/silence_of_the_lambs')['imdbId']
    u'0102926'

    >>> get_data('1991/silence_of_the_lambs')['posters'][0]
    u'http://www.impawards.com/1991/posters/silence_of_the_lambs_ver1.jpg'

    >>> get_data('1991/silence_of_the_lambs')['url']
    u'http://www.impawards.com/1991/silence_of_the_lambs_ver1.html'
    '''
    data = {
        'url': get_url(id)
    }
    html = read_url(data['url'], unicode=True)
    data['imdbId'] = find_re(html, 'imdb.com/title/tt(\d{7})')
    if not data['imdbId']:
        data['imdbId'] = _id_map.get(id, '')
    data['title'] = strip_tags(find_re(html, '<p class="name white">(.*?) \(<a href="alpha1.html">'))
    data['year'] = find_re(html, '\(<a href="alpha1.html">(.*?)</a>\)')
    data['posters'] = []
    poster = find_re(html, '<img src="(posters.*?)"')
    if poster:
        poster = 'http://www.impawards.com/%s/%s' % (data['year'], poster)
        data['posters'].append(poster)
    results = re.compile('<a href = (%s.*?html)' % id[5:], re.DOTALL).findall(html)
    for result in results:
        result = result.replace('_xlg.html', '.html')
        url = 'http://www.impawards.com/%s/%s' % (data['year'], result)
        html = read_url(url, unicode=True)
        result = find_re(html, '<a href = (\w*?_xlg.html)')
        if result:
            url = 'http://www.impawards.com/%s/%s' % (data['year'], result)
            html = read_url(url, unicode=True)
            poster = 'http://www.impawards.com/%s/%s' % (data['year'], find_re(html, '<img SRC="(.*?)"'))
        else:
            poster = 'http://www.impawards.com/%s/%s' % (data['year'], find_re(html, '<img src="(posters.*?)"'))
        data['posters'].append(poster)

    return data

def get_id(url):
    split = url.split('/')
    year = split[3]
    split = split[4][:-5].split('_')
    if split[-1] == 'xlg':
        split.pop()
    if find_re(split[-1], 'ver\d+$'):
        split.pop()
    id = '%s/%s' % (year, '_'.join(split))
    return id

def get_ids(page=None):
    ids = []
    if page:
        html = read_url('http://www.impawards.com/archives/page%s.html' % page, timeout = -1, unicode=True)
        results = re.compile('<a href = \.\./(.*?)>', re.DOTALL).findall(html)
        for result in results:
            url = 'http://impawards.com/%s' % result
            ids.append(get_id(url))
        return set(ids)
    #get all
    html = read_url('http://www.impawards.com/archives/latest.html', timeout = 60*60, unicode=True)
    pages = int(find_re(html, '<a href= page(.*?).html>')) + 1
    for page in range(pages, 0, -1):
        for id in get_ids(page):
            if not id in ids:
                ids.append(id)
    return ids

def get_url(id):
    url = u"http://www.impawards.com/%s.html" % id
    html = read_url(url, unicode=True)
    if find_re(html, "No Movie Posters on This Page"):
        url = u"http://www.impawards.com/%s_ver1.html" % id
    return url

_id_map = {
    '1933/forty_second_street': '0024034',
    '1933/tarzan_the_fearless': '0024645',
    '1935/informer': '0026529',
    '1935/thirty_nine_steps': '0026529',
    '1935/top_hat': '0027125',
    '1938/charlie_chaplin_cavalcade': '0284687',
    '1943/falcon_and_the_co-eds': '035855',
    '1969/angel_angel_down_we_go': '0065602',
    '1970/crimson_altar': '0062833',
    '1975/man_who_would_be_king_ver1': '0073341',
    '1975/picnic_at_hanging_rock_ver1': '0073540',
    '1979/electric_horseman_ver1': '0079100',
    '1980/caligula_ver1': '0080491',
    '1980/hollywood_knights_ver1': '0080881',
    '1981/history_of_the_world_part_i': '0082517',
    '1981/sea_wolves': '0081470',
    '1983/krull_ver1': '0085811',
    '1985/warriors_of_the_wind': '0087544',
    '1989/friday_the_thirteenth_part_viii_ver1': '0097388',
    '1989/high_hopes': '0095302',
    '1989/millenium': '0097883',
    '1989/story_of_women': '0096336',
    '1990/edward_scissorhands_ver1': '0099487',
    '1991/freddys_dead_ver1': '0101917',
    '1993/robocop_three_ver1': '0107978',
    '1993/waynes_world_two_ver1': '0108525',
    '1994/above_the_rim_ver1': '0109035',
    '1994/helas_pour_moi': '0107175',
    '1994/house_of_the_spirits_ver1': '0107151',
    '1994/i_dont_want_to_talk_about_it': '0106678',
    '1994/in_custody': '0107199',
    '1994/ladybird_ladybird': '0110296',
    '1994/leon_the_pig_farmer': '0104710',
    '1994/love_after_love': '0103710',
    '1994/l_six_two_seven': '0104658',
    '1994/martin_lawrence_you_so_crazy_ver1': '0111804',
    '1994/savage_nights': '0105032',
    '1994/sex_drugs_and_democracy': '0111135',
    '1995/bye_bye_love': '0112606',
    '1995/cold_comfort_farm': '0112701',
    '1995/gumby_the_movie': '0113234',
    '1995/les_miserables': '0113828',
    '1995/mystery_of_rampo': '0110943',
    '1995/pharaohs_army': '0114122',
    '1995/pure_formality': '0110917',
    '1995/quick_and_the_dead_ver1': '0114214',
    '1995/reflections_in_the_dark': '0110956',
    '1995/safe_ver1': '0114323',
    '1995/search_and_destroy': '0114371',
    '1995/secret_of_roan_inish_ver1': '0111112',
    '1995/underneath': '0114788',
    '1996/ghost_in_the_shell': '0113568',
    '1996/hate': '0113247',
    '1996/horseman_on_the_roof': '0113362',
    '1996/kids_in_the_hall_brain_candy': '0116768',
    '1996/maybe_maybe_not': '0109255',
    '1996/prisoner_of_the_mountains': '0116754',
    '1997/fifth_element_ver1': '0119116',
    '1997/fools_rush_in_ver1': '0119141',
    '1997/gi_jane_ver1': '0119173',
    '1997/happy_together_ver1': '0118845',
    '1997/lilies': '0116882',
    '1997/mouth_to_mouth': '0112546',
    '1997/mr_nice_guy': '0117786',
    '1997/nenette_and_boni': '0117221',
    '1997/paperback_romance': '0110405',
    '1997/second_jungle_book': '0120087',
    '1997/single_girl': '0113057',
    '1997/super_speedway': '0120245',
    '1997/temptress_moon': '0116295',
    '1998/alarmist': '0119534',
    '1998/barneys_great_adventure_the_movie': '0120598', 
    '1998/bulworth_ver1': '0118798',
    '1998/celebration': '0154420',
    '1998/east_palace_west_palace': '0119007',
    '1998/hurricane_streets': '0119338',
    '1998/i_married_a_strange_person': '0119346', 
    '1998/inheritors': '0141824',
    '1998/killing_time': '0140312',
    '1998/live_flesh': '0118819',
    '1998/music_from_another_room': '0119734',
    '1998/post_coitum_ver1': '0119923',
    '1998/steam_the_turkish_bath': '0119248',
    '1998/velocity_of_gary': '0120878',
    '1999/after_life': '0165078',
    '1999/emperor_and_the_assassin': '0162866', 
    '1999/fantasia_two_thousand': '0120910',
    '1999/get_bruce': '0184510',
    '1999/god_said_ha': '0119207',
    '1999/jawbreaker': '0155776',
    '1999/jeanne_and_the_perfect_guy': '0123923',
    '1999/king_and_i': '0160429',
    '1999/lovers_of_the_arctic_circle': '0133363',
    '1999/plunkett_and_macleane': '0134033',
    '1999/pokemon_the_first_movie': '0190641', 
    '1999/school_of_flesh': '0157208', 
    '1999/splendor': '0127296',
    '1999/stranger_in_the_kingdom': '0126680',
    '1999/train_of_life': '0170705',
    '1999/twice_upon_a_yesterday': '0138590', 
    '1999/whiteboys': '0178988',
    '1999/wildfire': '0194544',
    '1999/windhorse': '0169388',
    '2000/claim': '0218378', 
    '2000/color_of_paradise': '0191043',
    '2000/criminal_lovers': '0205735',
    '2000/everlasting_piece': '0218182',
    '2000/girl_on_the_bridge_ver1': '0144201',
    '2000/godzilla_two_thousand': '0188640',
    '2000/goya_in_bordeaux': '0210717',
    '2000/mad_about_mambo': '0156757', 
    '2000/picking_up_the_pieces': '0192455',
    '2000/pokemon_the_movie_2000': '0257001',
    '2000/seven_days_to_live': '0221928',  
    '2000/south_of_heaven_west_of_hell': '0179473',
    '2000/suzhou_river': '0234837',
    '2000/time_for_drunken_horses': '0259072',
    '2000/venus_beauty_institute': '0174330',
    '2001/circle': '0368646', 
    '2001/devils_backbone': '0256009',
    '2001/kill_me_later': '0243595',
    '2001/king_is_dancing': '0244173',
    '2001/learning_curve': '0219126',
    '2001/marco_polo__return_to_xanadu_ver1': '0296074',
    '2001/me_you_them': '0244504', 
    '2001/our_lady_of_the_assassins': '0250809',
    '2001/pinero': '0261066',
    '2001/pokemon_three_the_movie_ver1': '0266860',
    '2001/scratch': '0143861', 
    '2001/vampire_hunter_d_bloodlust_ver1': '0216651',
    '2002/el_bosque_animado': '0310790',
    '2002/fifty_first_state': '0227984',
    '2002/les_destinees': '0216689',
    '2002/sons_room': '0208990',
    '2003/open_hearts': '0315543',
    '2003/tulse_luper_suitcases': '0307596',
    '2003/valentin': '0296915',
    '2004/if_only_ver1': '0332136',
    '2004/wondrous_oblivion': '0334725',
    '2005/wu_ji': '0417976',
    '2006/golden_door': '0465188',
    '2006/kin': '1091189',
    '2007/revenge_of_the_nerds': '0088000',
    '2008/bad_batch': '1605644',
    '2008/mercedes': '1368083',
    '2008/spirit': '0831887',
    '2009/dead_air': '0993841',
    '2009/edge_of_love': '0819714',
    '2009/fuel': '1072437',
    '2009/fuel': '1072437', 
    '2009/one_good_man': '1239357',
    '2009/st_trinians': '1210106',
    '2009/surveillance': '0409345',
    '2009/taken': '0936501',
    '2009/vaml': '1610453', 
    '2010/adopting_haiti': '1764164',
    '2010/afterlife': '0838247',
    '2010/agora': '1186830',
    '2010/athlete': '1356996',
    '2010/beneath_the_blue': '1222698',
    '2010/bitch_slap': '1212974',
    '2010/black_waters_of_echos_pond': '0960066',
    '2010/case_thirty_nine': '0795351',
    '2010/finite_and_infinite_games': '1772268',
    '2010/hole': '1085779',
    '2010/jolene': '0867334',
    '2010/lake_mungo': '0816556',
    '2010/last_day_of_summer': '1242544',
    '2010/leaves_of_grass': '1151359',
    '2010/life_of_lemon': '1466057',
    '2010/man_in_the_maze': '1721692', 
    '2010/mr_immortality_the_life_and_times_of_twista': '1711017', 
    '2010/paper_man': '0437405', 
    '2010/perfect_game': '0473102',
    '2010/red_baron': '0365675',
    '2010/satin': '0433397',
    '2010/shutter_island': '1130884',
    '2010/strange_powers': '1534075',
    '2010/suicidegirls_must_die': '1584733',
    '2010/veronika_decides_to_die': '1068678',
    '2010/witchblade': '0494292',
    '2010/youth_in_revolt': '0403702',
    '2011/beastly': '1152398', 
    '2011/burning_palms': '1283887',
    '2011/cabin_in_the_woods': '1259521', 
    '2011/conan': '0816462',
    '2011/courageous': '1630036',
    '2011/cruces_divided_two': '1698645',
    '2011/green_with_envy': '1204342',
    '2011/happythankyoumoreplease': '1481572',
    '2011/homework': '1645080',
    '2011/i_got_next': '1915570',
    '2011/lebanon_pa': '1290082',
    '2011/money_pet': '1965198',
    '2011/my_suicide': '0492896',
    '2011/priest': '0822847', 
    '2011/prowl': '1559033',
    '2011/red_sonja': '0800175',
    '2011/season_of_the_witch': '0479997',
    '2011/stay_cool': '1235807', 
    '2011/sympathy_for_delicious': '1270277',
    '2011/trust': '1529572',
    '2011/undefeated': '1961604',
    '2011/vanishing_on_seventh_street': '1452628',
    '2011/where_is_robert_fisher': '2042712',
    '2011/yellowbrickroad': '1398428',
    '2012/haywire': '1506999', 
    '2012/last_call_at_the_oasis': '2043900',
}

if __name__ == '__main__':
    ids = get_ids()
    print(sorted(ids), len(ids))
