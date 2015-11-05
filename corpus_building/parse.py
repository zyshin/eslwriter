import os, subprocess, datetime
from django.conf import settings

from common.utils import *


def parse_files(cid, pids, prop_file='3.5.1_paper.properties'):
    r = {'type': 'parse', 'corpus': cid}
    if not cid or not pids:
        return r
    
    props = os.path.join(settings.STANFORD_CORENLP, prop_file)
    corpus_dir = corpus_path(cid)
    time = str(datetime.datetime.now()).replace(':', '-')
    input_file = os.path.join(corpus_dir, '%s build.input' % time)
    with open(input_file, 'w') as fout:
        fout.write('\n'.join([refined_path(pid) for pid in pids]))

    try:
        log = subprocess.check_output([settings.JAVA, '-cp', settings.STANFORD_CORENLP_CP, '-Xmx4g', 'edu.stanford.nlp.pipeline.StanfordCoreNLP', '-props', props, '-filelist', input_file, '-outputDirectory', settings.PARSED_DIR], stderr=subprocess.STDOUT)
        success = True
        #compatible for old version
        # for pid in pids:
        #     with open(os.path.join(settings.PARSED_DIR, str(pid)+'.conll'), 'r') as fin, open(os.path.join(settings.PARSED_DIR, str(pid)+'.txt'), 'w') as fout:
        #         fout.write(convert_parsed(fin.read()))
    except subprocess.CalledProcessError as e:
        log = e.output
        success = False
    
    r.update({'success': success, 'input_file': input_file, 'log': log})
    return r
