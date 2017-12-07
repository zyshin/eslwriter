# -*- coding:utf-8 -*-
import os, django
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'eslwebsite.settings_debug'
django.setup()
reload(sys)
sys.setdefaultencoding('utf-8')

from eslwriter.utils import *
from eslwriter.lemmatizer import lemmatize
from common.utils import mongo_get_object
from common.models import UserProfile, Field
from eslwriter.views import _get_cids, group_query, sentence_query, dep_query


def generate_group_query(cases):
    file_object = open('group_query.txt', 'w')
    file_object.truncate()  # clear file

    for case in cases:
        print case
        case = case.strip()
        qtt, qdd = parse_query_str(case)
        qmii = []
        ll = [t if is_cn(t) else lemmatize(t) for t in qtt]
        llll = [expanded_token(l) for l in ll]
        iiii = [tt2ii(tt) for tt in llll]
        for ll in llll:
            if type(ll) is list and len(ll) >= 1:
                qmii.append(tt2ii([ll[0]])[0])
        ref_wwii = tt2ii([t.strip('?') for t in qtt])

        profile = {'field': settings.DEFAULT_FID, 'pub_corpora': settings.DEFAULT_CIDS}
        profile.update(mongo_get_object(UserProfile, pk=None) or {})
        profile['field'] = mongo_get_object(Field, pk=profile['field'])['name']
        pri_cids, pub_cids = _get_cids(profile)
        pub_gr = group_query(iiii, qdd, pub_cids, ref_wwii, qmii)
        generate_sentence_query(pub_gr)
        file_object.write(str(iiii) + '$' + str(qdd) + '$' + str(pub_cids) + '$'
                          + str(ref_wwii) + '$' + str(qmii) + '$' + str(pub_gr) + '\n')

    file_object.close()


def generate_sentence_query(gr):
    file_object = open('sentence_query.txt', 'w')

    if gr:
        gr = eval(gr[0]['qs'])
        ii = gr['ii']
        dd = gr['dd']
        ref = gr['ref']
        cids = gr['cids']
        sr = sentence_query(ii, dd, cids, ref)
        file_object.write(str(ii) + '$' + str(dd) + '$' + str(ref) + '$' + str(cids) + '$' + str(sr) + '\n')

    file_object.close()
    

def generate_dep_query(cases):
    file_object = open('dep_query.txt', 'w')
    file_object.truncate()

    for case in cases:
        print case
        case = case.strip()
        qtt, _ = parse_query_str(case)
        qlen = len(qtt)

        profile = mongo_get_object(UserProfile, pk=None)
        pri_cids, pub_cids = _get_cids(profile)
        cids = pub_cids + pri_cids

        if (qlen == 1 or qlen == 2) and cids:
            tt = [t.strip('?') for t in qtt[:2]]
            tt = [translate(t)[0] if is_cn(t) else t for t in tt]
            tt = [lemmatize(t) for t in tt]
            llii = tt2ii(tt, ignore=False)

            l1 = llii[0]
            if qlen == 1:
                qtt.append('*')
                l2 = 0
            else:
                l2 = llii[1]
            gr = dep_query(l1, l2, cids)
            file_object.write(str(l1) + '$' + str(l2) + '$' + str(cids) + '$' + str(gr) + '\n')

    file_object.close()


def main():
    cases = {"extend * to", "for *", "length of 调和restriction", "*impact", "value is not the max", "开始programe"
             "extend *", "phasese", "Ma et al.s", "use？", "KDB’s performance", "nanopore", "howbeit",
             "a large number of", "is used for", "real bit", "communication link", "* (主谓) and * (主谓)", "open program",
             "bubble  cursor (修饰)", "analysis for source code", "dimensional", "supress", " supressed", "ordinarily",
             "data-structures", "approach to", "map to ", "value is not necessarily", "is not maximum", "开始progra",
             "* extend (介词) to", "a unimform", "* negative (modifies) impact", "UAV Relay Cvarianceommunication System",
             "deteriate", "(修饰) *impact ", "* (修饰) 还多", "bayesian", "e'a", "* (修饰) according", "wha", "the two",
             "equal", "tremendous", "emerg", "segment (介词) ", "is used", "be used (介词)", "re'qu", "high-accurate",
             "Ranging ability", "transceivers", "Rrake", "mai", "existing in", "constraints of", "thus (修饰) ",
             "communication among", "communication between", "in the channel", "multiple access method", "is needed to",
             "hot", "suppose ", "itrational", "jointed", " nodejoint", "connected by link", "muchfragmentation",
             "the reason", "RSA ", "RSA", "would", "essentially", "cdma", "update * (介词)", "computer system design",
             "In computer systems design", "interpretability (修饰) ", "substitute (主谓) ", "lenet", "if", "imidazolium ",
             " the average value", "trans", "transpo", "demonstrate", "fracture strength", "pressURing", "shown in",
             "sensitive", "effects ", "attain", "unique (介词) ", "gain insight (介词)", "significant  impact (介词) ",
             "amount of", "indicate", "will increase with", "convexness ", "do not", "changing rate", "accu",
             "Multidimensional", "crosslink", "Another one", "Another one is", "OFDM", "significance", "As  a",
             "around", "resuilting", "从原因推理结果", "aqueous", " miss operation ", "requirement", "aggregat",
             " as developping of  ", "bor", "born", "* (修饰) formation", "lie'yi'chu", "列yi'chu", "improt",
             "security area", "dimensional？", "landmark", "There", "Therefore", "different from", "performance",
             "different (修饰) *", "convexity", "si'n", "poin", "with many features", "nstruction-per-cycle",
             "instruction-per-cycle", "operations", "？operations", "infographic", "infographics", "low-overhead",
             " intuitionistic", "co.Ltd", "which", "on the other", "security tools", "respectively. ", "call chain",
             " We define", "red-", "red-black", "red-black ", "overwhelm", "increase to", "customarily", "usually",
             "卷积神经", "（卷积）", "**（卷积）", "(卷积)", "紧密结合", "依次采用", "逐步", "and its application in", "and its application",
             "effort is made", "complete control system", "tested under cases", "to cope with", "some effort",
             "numerically", "influ", "types attack", "it can be seen that", "phenomenon", "lithium", "mass data",
             "data size", "prediction", "exponential regression", "respectively", "workflows", "far away from",
             "hence ", "hence", "video ", "forgery", "avoid forgery", "avoidforgery", "avoiding forgery", "avoiding ",
             "authority", "intraframe", "after simplifying the deriavation", "， neither", "which quaulity ",
             "https://www.google.com/search?client=safari&rls=en&q=prevent+security&ie=UTF-8&oe=UTF-8", "apparently",
             "classify", "Firstly,", "Firstly, ", "Firstly", "secondly", "fatal issue", "严重的wen'ti", "fa't", "fatal",
             "cryptosystem", "unlike", "monopulse", "impact", "mathematically", "随NaOH浓度的提高，NOR的解吸率先增大后减小",
             "volume ", "24", "important", "submicroparticles", "timnetrade-off", "because", "beca", "bea",
             "give  challenge", "however   so", "Eq.", "using the", "using ", "here", "monotonically", "chitosans",
             "pretrain", "between", "proble", "acknowledge of", "therefore,", "is not necessarily maximum",
             "the appropriate value is", "I发", "stacked line Y-axis", "开始program", "Gini index、", "our aim *",
             "effect is *", "impact *", "*pressure", "* * (修饰) impact", "* 调整 (主谓) extend ", "each phasese",
             "* (modify) impact", "vaiation space", "yodel？", "xixixixixixii", "amongvarious decomposition",
             "doesn’t affect ", "due to  therie", "corpoa?", "reach accknowledge", "?", "conclude ? (介词) *",
             "specular?", "mostly?", "attain ? (动宾)", "become? (动宾) ", "corpora?", "spectecular", "extend (??) to *",
             "curiosity?", "effect? (动宾) *", "lower? (动宾) *", "conditioned (???����?) on", "essentially?", "ulterior?",
             "It is reasonable?", "exercise?", "open?  program", "build? model?", "* (modifies) impact", "a set? of",
             "* (v+n) approach", "the set? of", "conduct? (动宾) study?"}

    generate_group_query(cases)
    generate_dep_query(cases)

main()
