import os
import zipfile

path = r"F:\Database\Drive Data\weekly option\Nifty\2021"
#
# zips = os.listdir(path)
# for zip in zips:
#     with zipfile.ZipFile(os.path.join(path, zip), 'r') as zip_ref:
#         zip_ref.extractall(path)

#
# zips = os.listdir(path)
# for file in zips:
#     zi = os.listdir(os.path.join(path, file))[0]
#     with zipfile.ZipFile(os.path.join(os.path.join(path, file), zi), 'r') as zip_ref:
#         zip_ref.extractall(os.path.join(path, file))


# folders = os.listdir(path)
# for folder in folders:
#     inside = os.path.join(path, folder)
#     dir = os.listdir(inside)
#     for csv in dir:
#         if csv[-3:] == "csv":
#             os.rename(os.path.join(inside, csv), os.path.join(inside, csv[-11:]))

#
# """Rename folder"""
# folders = os.listdir(path)
# for folder in folders:
#     print(folder)
#     name = input('Enter Name : ')
#     os.rename(os.path.join(path, folder), os.path.join(path, name))
