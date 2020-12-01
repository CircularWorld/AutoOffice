import zipfile, os
zipFile = zipfile.ZipFile(r'test.zip', 'w')
for file in os.listdir('itemss'):
    zipFile.write(('itemss/'+file).encode(), file, zipfile.ZIP_DEFLATED)
print(zipFile.filelist)
zipFile.close()