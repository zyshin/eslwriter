import os, shutil, subprocess
from django.conf import settings
# from django.db import transaction
# from azure.storage import BlobService
from PyPDF2 import PdfFileReader
from common.utils import timeit


def combine_chunks(total_parts, total_size, source_folder, dest):
    """ Combine a chunked file into a whole file again. Goes through each part
    , in order, and appends that part's bytes to another destination file.

    Chunks are stored in media/chunks
    Uploads are saved in media/uploads
    """
    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
    with open(dest, 'wb+') as destination:
        for i in xrange(total_parts):
            part = os.path.join(source_folder, str(i))
            with open(part, 'rb') as source:
                destination.write(source.read())


def save_upload(f, path):
    """ Save an upload. Django will automatically "chunk" incoming files
    (even when previously chunked by fine-uploader) to prevent large files
    from taking up your server's memory. If Django has chunked the file, then
    write the chunks, otherwise, save as you would normally save a file in
    Python.

    Uploads are stored in media/uploads
    """
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, 'wb+') as destination:
        if hasattr(f, 'multiple_chunks') and f.multiple_chunks():
            for chunk in f.chunks():
                destination.write(chunk)
        else:
            destination.write(f.read())


def ispdf(f):
    try:
        inputFile = PdfFileReader(f)
        # pageNums = inputFile.getNumPages() # pdf page nums
        # if pageNums < 4:
        #     raise Exception
    except Exception as e:
        # PyPDF2.utils.PdfReadError
        # print repr(e)
        return False
    return True


@timeit
def extracted(pdfPath):
    try:
        r = subprocess.check_output([settings.PDFTOTEXT, '-enc', 'ASCII7', '-eol', 'unix', '-nopgbrk', '-q', pdfPath, '-']) # TODO: handle unicode
    except Exception as e:
        print '[Exception when pdftotext]', repr(e)
        r = ''
    return r


'''
@transaction.atomic
def update_word_count():
    print 'begin updating'
    count = 0
    for p in Paper.objects.all():
        path1 = os.path.join(settings.UPLOAD_DIR, p.qquuid, 'refined2.txt')
        path2 = os.path.join(settings.UPLOAD_DIR, p.qquuid, 'content.txt')
        if os.path.isfile(path1) or os.path.isfile(path2):
            if os.path.isfile(path1):
                with open(path1, 'r') as fin:
                    num_words = len(fin.read().split())
            elif os.path.isfile(path2):
                with open(path2, 'r') as fin:
                    num_words = len(fin.read().split())
            if p.num_words != num_words:
                p.num_words = num_words
                p.save()
                count += 1
        else:
            print 'invalid paper record:', p.qquuid
    print count, 'files updated'


def clean_uploads():
    print 'begin cleaning'
    count = 0
    for qquuid in os.listdir(settings.UPLOAD_DIR):
        if not Paper.objects.filter(qquuid=qquuid).count():
            print qquuid
            shutil.rmtree(os.path.join(settings.UPLOAD_DIR, qquuid))
            count += 1
    print count, 'items cleaned'
'''

def save_chunk_local(f, path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, 'wb+') as destination:
        if hasattr(f, 'multiple_chunks') and f.multiple_chunks():
            for chunk in f.chunks():
                destination.write(chunk)
        else:
            destination.write(f.read())

def save_pdf_file(bytes,name):
    if(not name.lower().endswith('.pdf')):
        name=name+'.pdf'
    if(not settings.IS_STORE_BY_AZURE):
        path=settings.PAPERS_DIR
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path,name), 'wb+') as destination:
            destination.write(bytes)

def save_extracted_file(content,name):
    if(not name.lower().endswith('.txt')):
        name=name+'.txt'
    if(not settings.IS_STORE_BY_AZURE):
        path=settings.EXTRACTED_DIR
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path,name),'w+') as destination:
            destination.write(content)

def save_refined_file(content,name):
    if(not name.lower().endswith('.txt')):
        name=name+'.txt'
    if(not settings.IS_STORE_BY_AZURE):
        path=settings.REFINED_DIR
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path,name),'w+') as destination:
            destination.write(content)
"""
save_type:
    1 origin file
    2 extracted file
    3 refined file
"""
def save_file(save_type, content, name):
    isAzure = settings.IS_STORE_BY_AZURE
    if save_type == 1:
        if not isAzure:
            path = settings.PAPERS_DIR
            if not os.path.exists(path):
                os.makedirs(path)
            shutil.copyfile(content, os.path.join(path, name))
        else:
            save_file_azure(1, settings.AZURE_PAPERS_CONTAINER, name, content)
    elif save_type == 2:
        if not isAzure:
            path = settings.EXTRACTED_DIR
            if not os.path.exists(path):
                os.makedirs(path)
            save_file_local('text', content, os.path.join(path, name))
        else:
            save_file_azure(3, settings.AZURE_EXTRACTED_CONTAINER, name, content)
    elif save_type == 3:
        if not isAzure:
            path=settings.REFINED_DIR
            if not os.path.exists(path):
                os.makedirs(path)
            save_file_local('text', content, os.path.join(path, name))
        else:
            save_file_azure(3, settings.AZURE_REFINED_CONTAINER, name, content)


"""
file_type:
    'text' text file
    'bytes' binary file
"""
def save_file_local(file_type, content, path):
    if file_type == 'text':
        mode = 'w+'
    elif file_type == 'bytes':
        mode = 'wb+'
    if mode:    
        with open(path, mode) as destination:
            destination.write(content)

"""
save_type:
    1 file path
    2 bytes array
    3 text
"""
def save_file_azure(save_type, container, blob_name, value):
    blob_service = BlobService(account_name=settings.AZURE_STORAGE_ACCOUNT_NAME, account_key=settings.AZURE_STORAGE_ACCOUNT_KEY,host_base=settings.AZURE_STORAGE_HOST_BASE)
    if save_type == 1:
        blob_service.put_block_blob_from_path(container, blob_name, value)
    elif save_type == 2:
        blob_service.put_block_blob_from_bytes(container, blob_name, value)
    elif save_type == 3:
        blob_service.put_block_blob_from_text(container, blob_name, value, 'ASCII')

def delete_file_azure(container,blob_name):
    blob_service = BlobService(account_name=settings.AZURE_STORAGE_ACCOUNT_NAME, account_key=settings.AZURE_STORAGE_ACCOUNT_KEY,host_base=settings.AZURE_STORAGE_HOST_BASE)
    blob_service.delete_blob(container,blob_name)
