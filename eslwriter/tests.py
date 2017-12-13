from django.test import TestCase
from eslwriter.views import group_query, sentence_query, dep_query
from eslwriter.utils import match_cost, parse_query_str, find_best_match, refine_ii_dd
from eslwriter.thesaurus import synonyms, antonyms
from eslwriter.lemmatizer import lemmatize


class eslTestCase(TestCase):
    def setUp(self):
        pass

    def test_views_group_query(self):
        for line in open("eslwriter/group_query.txt"):
            case_iiii, case_dd, case_cids, case_ref, case_qmii, case_expected_gr = line.split('$')
            case_iiii = eval(case_iiii)
            case_dd = eval(case_dd)
            case_cids = eval(case_cids)
            case_ref = eval(case_ref)
            case_qmii = eval(case_qmii)
            case_expected_gr = case_expected_gr[:-1]   # \n
            case_expected_gr = eval(case_expected_gr)
            case_gr = group_query(iiii=case_iiii, dd=case_dd, cids=case_cids, ref=case_ref, qmii=case_qmii)
            self.assertEqual(case_gr, case_expected_gr)

    def test_views_sentence_query(self):
        for line in open("eslwriter/sentence_query.txt"):
            case_ii, case_dd, case_ref, case_cids, case_expected_sr = line.split('$')
            case_ii = eval(case_ii)
            case_dd = eval(case_dd)
            # case_ref = eval(case_ref)
            case_cids = eval(case_cids)
            case_ref = eval(case_ref)
            case_expected_sr = case_expected_sr[:-1]
            case_expected_sr = eval(case_expected_sr)
            case_sr = sentence_query(ii=case_ii, dd=case_dd, cids=case_cids, ref=case_ref, start=0, count=100)
            self.assertEqual(case_sr, case_expected_sr)

    def test_views_dep_query(self):
        for line in open("eslwriter/dep_query.txt"):
            case_l1, case_l2, case_cids, case_expected_gr = line.split('$')
            case_l1 = eval(case_l1)
            case_l2 = eval(case_l2)
            case_cids = eval(case_cids)
            case_expected_gr = case_expected_gr[:-1]
            case_expected_gr = eval(case_expected_gr)
            case_gr = dep_query(l1=case_l1, l2=case_l2, cids=case_cids)
            self.assertEqual(case_gr, case_expected_gr)

    def test_utils_find_best_match(self):
        for line in open("eslwriter/find_best_match.txt"):
            case_r, case_ii, case_dd, case_ref, case_tt, case_expected_r1, case_expected_r2 = line.split('$')
            case_r = eval(case_r)
            case_ii = eval(case_ii)
            case_dd = eval(case_dd)
            case_ref = eval(case_ref)
            case_tt = eval(case_tt)
            case_expected_r1 = eval(case_expected_r1)
            case_expected_r2 = case_expected_r2[:-1]
            case_expected_r2 = eval(case_expected_r2)
            case_r1, case_r2 = find_best_match(case_r, case_ii, case_dd, case_ref, case_tt)
            self.assertEqual(case_r1, case_expected_r1)
            self.assertEqual(case_r2, case_expected_r2)

    def test_utils_match_cost(self):
        for line in open("eslwriter/match_cost.txt"):
            case_T, case_m, case_ref, case_tt, case_expected_cost = line.split('$')
            case_T = eval(case_T)
            case_m = eval(case_m)
            case_ref = eval(case_ref)
            case_tt = eval(case_tt)
            case_expected_cost = case_expected_cost[:-1]
            case_expected_cost = eval(case_expected_cost)
            case_cost = match_cost(case_T, case_m, case_ref, case_tt)
            self.assertEqual(case_cost, case_expected_cost)

    def test_utils_refine_ii_dd(self):
        for line in open("eslwriter/refine_ii_dd.txt"):
            case_ii, case_dd, case_expected_iiii, case_expected_qdd = line.split('$')
            case_ii = eval(case_ii)
            case_dd = eval(case_dd)
            case_expected_iiii = eval(case_expected_iiii)
            case_expected_qdd = case_expected_qdd[:-1]
            case_expected_qdd = eval(case_expected_qdd)
            case_iiii, case_qdd = refine_ii_dd(case_ii, case_dd)
            self.assertEqual(case_iiii, case_expected_iiii)
            self.assertEqual(case_qdd, case_expected_qdd)

    def test_utils_parse_query_str(self):
        case1_q = "open (v+n) door"
        case1_pqs = parse_query_str(q=case1_q)
        self.assertEqual(case1_pqs, (['open', 'door'], [(2, 0, 1)]))

    def test_thesaurus_synonyms(self):
        case1_word = "incomprehensible"
        case1_syn = synonyms(word=case1_word)
        case1_expected_res = ['incomprehensible', u'unfathomable', u'unintelligible', u'puzzling', u'opaque',
                               u'unimaginable', u'mystifying', u'baffling', u'inconceivable', u'impenetrable',
                               u'enigmatic', u'unclear', u'fathomless', u'incognizable', u'inscrutable', u'mysterious',
                               u'perplexing', u'sibylline', u'ungraspable', u'delphic', u'unknowable', u'cryptic',
                               u'greek', u'obscure']
        self.assertEqual(case1_syn, case1_expected_res)

        case2_word = "with"
        case2_syn = synonyms(word=case2_word)
        case2_expected_res = ['with', u'among', u'via', u'past', u'into', u'within', u'near', u'down', u'as', u'anti', u'at', u'in', u'beyond', u'before', u'considering', u'from', u'for', u'since', u'excepting', u'except', u'per', u'than', u'beside', u'to', u'behind', u'above', u'between', u'save', u'across', u'outside', u'versus', u'over', u'towards', u'around', u'opposite', u'concerning', u'after', u'upon', u'regarding', u'but', u'underneath', u'unlike', u'under', u'besides', u'despite', u'during', u'along', u'by', u'on', u'about', u'off', u'like', u'excluding', u'amid', u'inside', u'up', u'against', u'until', u'below', u'without', u'plus', u'aboard', u'of', u'following', u'through', u'beneath', u'toward', u'onto', u'round']
        self.assertEqual(case2_syn, case2_expected_res)

        case3_word = "save"
        case3_syn = synonyms(word=case3_word)
        case3_expected_res = ['save', u'shield', u'manage', u'maintain', u'recover', u'conserve', u'sustain', u'store', u'preserve', u'deliver', u'free', u'spare', u'salvage', u'keep', u'collect', u'amass', u'cache', u'spring', u'extricate', u'squirrel', u'ransom', u'safeguard', u'defend', u'treasure', u'scrimp', u'hoard', u'unchain', u'skimp', u'retrench', u'screen', u'redeem', u'hold', u'emancipate', u'gather', u'stash', u'stockpile', u'deposit', u'liberate', u'reserve', u'unshackle']
        self.assertEqual(case3_syn, case3_expected_res)

    def test_thesaurus_antonyms(self):
        case1_word = "inexplicable"
        case1_ant = antonyms(word=case1_word)
        case1_expected_res = [u'usual', u'fathomable', u'standard', u'regular', u'normal', u'understandable',
                              u'explainable', u'comprehensible', u'intelligible', u'explicable', u'comprehendible']
        self.assertEqual(case1_ant, case1_expected_res)

    def test_lemma_lemmatize(self):
        case1_s = "Our"
        self.assertEqual(lemmatize(case1_s), u'we')

        case2_s = "social media"
        self.assertEqual(lemmatize(case2_s), u'social')

        case3_s = "discuss"
        self.assertEqual(lemmatize(case3_s), u'discuss')

        case4_s = "assess?"
        self.assertEqual(lemmatize(case4_s), u'assess?')

        case5_s = "details"
        self.assertEqual(lemmatize(case5_s), u'detail')

        case6_s = "times"
        self.assertEqual(lemmatize(case6_s), u'time')

        case7_s = "ACM"
        self.assertEqual(lemmatize(case7_s), u'acm')
