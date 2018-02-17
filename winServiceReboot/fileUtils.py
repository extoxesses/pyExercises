import os
import shutil

def copy(src_path, dst_path, rewrite = False) :
  if (rewrite or not os.path.exists(dst_path)) :
    shutil.copy(src_path, dst_path)
  else :
    root, file_name = os.path.split(src_path);
    raise Exception("[ERROR] File " + file_name + " could not be copied to " + root + " directory!");