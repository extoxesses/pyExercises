def pgm2png():
    dir_path = "D:/Archive/Datasets/orl_faces/"
    for dir in range(1, 41):
      for i in range(1, 11):
          path = dir_path + "s" + str(dir) + "/" + str(i) + ".pgm"
          image = pdb.gimp_file_load(path, path)
          drawable = pdb.gimp_image_active_drawable(image)
          file_name = str(i) + ".png"
          file_path = dir_path + "s" + str(dir) + "/" + file_name
          pdb.file_png_save(image, drawable, file_path, file_name, 0, 9, 1, 1, 1, 1, 1)
    pdb.gimp_quit(1)