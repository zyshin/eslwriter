from django.test import TestCase
from eslwriter.views import group_query, sentence_query, dep_query
from eslwriter.utils import match_cost, parse_query_str
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
        # Case 1: search '* (n+v) impact'
        case1_ii = [38, 700]
        case1_dd = [[1, 0, 1]]
        case1_cids = [u'acm_trans_comput_hum_interact_tochi_', u'user_model_user_adapt_interact_umuai_', u'int_j_hum_comput_stud_ijmms_', u'mobile_hci', u'ecscw', u'uist', u'chi', u'its', u'iui', u'hci', u'ubicomp', u'cscw']
        case1_ref = [0, 700]
        case1_start = 0
        case1_count = 100
        case1_sr = sentence_query(ii=case1_ii, dd=case1_dd, cids=case1_cids, ref=case1_ref, start=case1_start, count=case1_count)
        case1_expected_sr = [({'url': u'http://www.dblp.org/rec/bibtex/conf/uist/RetelnyRTLPRDVB14', 'source': u"UIST'14. D. Retelny et. al. Expert crowdsourcing with flash teams. "}, u'If a task finishes early, Foundry recalculates the starting <strong>times</strong> for all downstream tasks and emails all <strong>impacted</strong> workers with a new estimated start time for their next task.'), ({'url': u'http://www.dblp.org/rec/bibtex/conf/chi/HsiehC09', 'source': u"CHI'09. G. Hsieh et. al. mimir: a market-based real-time question and answer service. "}, u"Since it is possible that the <strong>time</strong> when a best answer is selected would <strong>impact</strong> the users' answering behavior, we selected the best answers in the two systems at the same time."), ({'url': u'http://www.dblp.org/rec/bibtex/conf/chi/BaumerST08', 'source': u"CHI'08. E. Baumer et. al. Exploring the role of the reader in the activity of blogging. "}, u'Non-chronous - While readers experience blog posts in temporal order, the exact <strong>times</strong> of the posts does not significantly <strong>impact</strong> the reading activity.'), ({'url': u'http://www.dblp.org/rec/bibtex/conf/cscw/JunuzovicD12', 'source': u"CSCW'12. S. Junuzovic et. al. Towards self-optimizing collaborative systems. "}, u'Think <strong>times</strong> can <strong>impact</strong> response times because when think times of commands are low, slower computers may fall behind the faster computers in processing the commands.'), ({'url': u'http://www.dblp.org/rec/bibtex/conf/cscw/JunuzovicD12', 'source': u"CSCW'12. S. Junuzovic et. al. Towards self-optimizing collaborative systems. "}, u'The additional processing <strong>time</strong> <strong>impacted</strong> the critical computer time when it was the source.'), ({'url': u'http://www.dblp.org/rec/bibtex/conf/cscw/JunuzovicD12', 'source': u"CSCW'12. S. Junuzovic et. al. Towards self-optimizing collaborative systems. "}, u'However, for the parallel policy, the processing <strong>time</strong> of any kind does not <strong>impact</strong> the critical computer time.')]
        self.assertEqual(case1_sr, case1_expected_sr)

    def test_views_dep_query(self):
        pass

    def test_utils_match_cost(self):
        # Case 1: search '* (n+v) impact'
        case1_t = [{u'i': 0, u'w': 3209236, u'l': 96, u'pt': 28}, {u'i': 1, u'w': 2, u'l': 2, u'pt': 4}, {u'i': 2, u'w': 11, u'l': 11, u'pt': 14}, {u'i': 3, u'w': 1, u'l': 1, u'pt': 11}, {u'i': 4, u'w': 407, u'l': 407, u'pt': 15}, {u'i': 5, u'w': 413, u'l': 413, u'pt': 20}, {u'i': 6, u'w': 2, u'l': 2, u'pt': 4}, {u'i': 7, u'w': 1, u'l': 1, u'pt': 11}, {u'i': 8, u'w': 459, u'l': 459, u'pt': 20}, {u'i': 9, u'w': 38, u'l': 38, u'pt': 20}, {u'i': 10, u'w': 5, u'l': 5, u'pt': 14}, {u'i': 11, u'w': 87, u'l': 87, u'pt': 11}, {u'i': 12, u'w': 845, u'l': 845, u'pt': 20}, {u'i': 13, u'w': 3116610, u'l': 46, u'pt': 40}, {u'i': 14, u'w': 23, u'l': 23, u'pt': 28}, {u'i': 15, u'w': 700, u'l': 700, u'pt': 35}, {u'i': 16, u'w': 1, u'l': 1, u'pt': 11}, {u'i': 17, u'w': 886, u'l': 886, u'pt': 15}, {u'i': 18, u'w': 532, u'l': 532, u'pt': 20}, {u'i': 19, u'w': 38, u'l': 38, u'pt': 20}, {u'i': 20, u'w': 3, u'l': 3, u'pt': 7}]
        case1_m = (9, 15)
        case1_ref = [0, 700]
        case1_tt = [0]
        case1_mc = match_cost(T=case1_t, m=case1_m, ref=case1_ref, tt=case1_tt)
        self.assertEqual(case1_mc, 17)

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
