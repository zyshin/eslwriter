# -*- coding:utf-8 -*-
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'eslwebsite.settings_debug'
from django.conf import settings
django.setup()

from eslwriter.utils import *
from eslwriter.lemmatizer import lemmatize
from common.utils import mongo_get_object
from common.models import UserProfile, Field
from eslwriter.views import _get_cids, group_query


def generate_group_query():
    cases = {'humble', 'quality have','paper', 'ds', 'dev', 'collection', 'program',
             'improve quality', 'interface', 'graphical interface', 'improve', 'power transfer',
             'interactable', 'refer to', 'test', 'present a new method', 'present a method ', 'present',
             'present a method', 'search paper', 'present method', 'quality data', 'ID', 'quality',
             'qualify', ' collection', 'compensating', 'avoid speaking', 'grounded theory', 'the need',
             'lower memory demand', 'paper test', 'presents method', 'expend effort', 'expand', 'situation',
             'high quality', 'recommend', '使用', 'autonomous', 'quality of', 'telepresence', 'problem',
             'make evaluation', 'pretend', 'interfaces', 'graphical user interface', 'alchol', 'performance',
             '?????????', 'need', '大雨', 'novel', 'purport', 'heavy rain', 'dedicate to', 'carry on',
             '需求', 'for full', 'avoid', 'attached', 'esoda', '获取 information', 'break', 'guide',
             'software', 'make effort', '减少 the demand of', 'efficient', '变革', 'method', 'convolutional',
             'demand', 'reduce demand of', 'wait', 'waltz', 'screw', 'pursue', 'choose', 'conduct',
             'decuple', 'progress', 'jitters', 'urgent', 'appraise', 'algorithm', 'skillful', 'able',
             'ecology', 'productive', 'lithe', 'valuable', 'skilled', 'interaction', 'application',
             'best quality', 'quality (修饰)', 'ensure quality', 'profitable', 'da', 'date', 'data',
             'unintentional touch', 'once', 'bezel', 'border', 'quality (主谓)', 'calling', 'challenge',
             'helpful', 'reduce error', 'quality (介词)*', 'build up relationship', 'eyes-free selection',
             'advancement', 'preference', 'calculate', 'differ', 'pressure', 'after rain',
             'include complexity', 'complexities', 'advantage', 'ipsum', 'ui', '歌曲', 'active',
             'standard quality', '实验设计', '排除', 'eliminate irrelevant ', 'diagonal ', 'lie in', 'perform',
             'lack discriminability', 'discriminability', '更详细的数据',
             '??\xa1\xe4\xa8\xa8\xa1\xa5|????????\xa1\xe3???', 'position', 'launch', 'accelerometer',
             ' Online Communities ', 'impactful', 'field', '提问者', 'classified search', 'high-tech zone',
             '公司入驻', '数据show', 'papers', 'the of love', '\xe5\x87\x8f\xe5\xb0\x91 the demand of',
             'in a first user study', 'instability', 'default to doing', '数据读写', '数据', '相互干扰', '干扰',
             '整体性能显著降低', '自适应地', '线性地', '具体来说', '反馈', '波动剧烈', '快速设备', 'granuality', '间隔小', '顺序性',
             '占用资源', '造成很大影响', 'ubility', 'most n.', 'posture', 'subjective', 'automatic evaluation',
             'lower demand', 'user interface', 'forms + n', 'forms ', 'result in', 'apt', 'expression',
             'spetaqular', 'Spectacular'}

    file_object = open('cases.txt', 'w')
    file_object.truncate()

    for case in cases:
        case = case.strip()
        qtt, qdd = parse_query_str(case)
        ll = [t if is_cn(t) else lemmatize(t) for t in qtt]
        llll = [expanded_token(l) for l in ll]
        iiii = [tt2ii(tt) for tt in llll]
        ref_wwii = tt2ii([t.strip('?') for t in qtt])

        profile = {'field': settings.DEFAULT_FID, 'pub_corpora': settings.DEFAULT_CIDS}
        profile.update(mongo_get_object(UserProfile, pk=None) or {})
        profile['field'] = mongo_get_object(Field, pk=profile['field'])['name']
        pub_cids = _get_cids(profile)
        pub_gr = group_query(iiii, qdd, pub_cids, ref_wwii)
        file_object.write(str(iiii) + '$' + str(qdd) + '$' + str(pub_cids[1]) + '$' + str(ref_wwii) + '$' + str(pub_gr) + '\n')

    file_object.close()

generate_group_query()