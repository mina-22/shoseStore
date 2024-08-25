import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE_BYTES = 12 * 1024 * 1024  # 12MB

def accepted_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def accepted_file_size(file):
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0, os.SEEK_SET)
    return file_size <= MAX_FILE_SIZE_BYTES

def priceVaild(price):
    if int(price) <5 and int(price)>500:
        return False 
    else:
        return True
def PriceSaleValdi(Sale,Price):
    if int(Sale) >=int(Price) or int(Sale)<0:
        return False
    else:
        return True